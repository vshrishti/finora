import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

def calculate_metrics(df):
    if df.empty:
        return 0, 0, 0, 0
    
    income_df = df[df['transaction_type'] == 'Income']
    expense_df = df[df['transaction_type'] == 'Expense']
    
    total_income = income_df['amount'].sum()
    total_expenses = expense_df['amount'].sum()
    savings = total_income - total_expenses
    
    savings_rate = 0
    if total_income > 0:
        savings_rate = (savings / total_income) * 100
        
    return total_income, total_expenses, savings, savings_rate

def get_income_vs_expense_chart(df):
    if df.empty:
        return None
        
    df['month'] = pd.to_datetime(df['transaction_date']).dt.to_period('M').astype(str)
    monthly_data = df.groupby(['month', 'transaction_type'])['amount'].sum().reset_index()
    
    if monthly_data.empty:
        return None
        
    fig = px.bar(
        monthly_data, 
        x='month', 
        y='amount', 
        color='transaction_type', 
        barmode='group',
        color_discrete_map={'Income': '#2e7d32', 'Expense': '#c62828'},
        labels={'amount': 'Amount (₹)', 'month': 'Month', 'transaction_type': 'Type'}
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='rgba(0,0,0,0)')
    return fig

def get_expense_category_chart(df):
    expense_df = df[df['transaction_type'] == 'Expense']
    if expense_df.empty:
        return None
        
    cat_data = expense_df.groupby('category')['amount'].sum().reset_index()
    
    fig = px.pie(
        cat_data, 
        names='category', 
        values='amount', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def get_daily_spending_trend(df):
    expense_df = df[df['transaction_type'] == 'Expense'].copy()
    if expense_df.empty:
        return None
        
    expense_df['date'] = pd.to_datetime(expense_df['transaction_date'])
    daily_data = expense_df.groupby('date')['amount'].sum().reset_index()
    
    fig = px.line(
        daily_data, 
        x='date', 
        y='amount',
        line_shape='spline',
        color_discrete_sequence=['#c62828']
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0), 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Date",
        yaxis_title="Amount (₹)"
    )
    return fig

def get_monthly_savings_trend(df):
    if df.empty:
        return None
        
    df['month'] = pd.to_datetime(df['transaction_date']).dt.to_period('M').astype(str)
    monthly_data = df.groupby(['month', 'transaction_type'])['amount'].sum().unstack(fill_value=0).reset_index()
    
    if 'Income' not in monthly_data.columns:
        monthly_data['Income'] = 0
    if 'Expense' not in monthly_data.columns:
        monthly_data['Expense'] = 0
        
    monthly_data['Savings'] = monthly_data['Income'] - monthly_data['Expense']
    
    fig = px.bar(
        monthly_data,
        x='month',
        y='Savings',
        color='Savings',
        color_continuous_scale=['#c62828', '#2e7d32'],
        color_continuous_midpoint=0,
        labels={'month': 'Month', 'Savings': 'Savings (₹)'}
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
    return fig

def get_top_spending_categories(df, top_n=5):
    expense_df = df[df['transaction_type'] == 'Expense']
    if expense_df.empty:
        return pd.DataFrame()
        
    cat_data = expense_df.groupby('category')['amount'].sum().reset_index()
    return cat_data.sort_values(by='amount', ascending=False).head(top_n)

def calculate_mom_expense_change(df):
    expense_df = df[df['transaction_type'] == 'Expense'].copy()
    if expense_df.empty:
        return None
        
    expense_df['month'] = pd.to_datetime(expense_df['transaction_date']).dt.to_period('M')
    monthly_expenses = expense_df.groupby('month')['amount'].sum()
    
    if len(monthly_expenses) < 2:
        return None
        
    current_month = monthly_expenses.index.max()
    prev_month = current_month - 1
    
    if prev_month not in monthly_expenses.index:
        return None
        
    current_val = monthly_expenses[current_month]
    prev_val = monthly_expenses[prev_month]
    
    if prev_val == 0:
        return None
        
    change_pct = ((current_val - prev_val) / prev_val) * 100
    return change_pct
