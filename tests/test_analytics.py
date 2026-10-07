import pytest
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import analytics as an

def test_calculate_metrics():
    # Test empty dataframe
    df_empty = pd.DataFrame()
    income, expense, savings, rate = an.calculate_metrics(df_empty)
    assert income == 0
    assert expense == 0
    assert savings == 0
    assert rate == 0

    # Test with data
    data = {
        'transaction_type': ['Income', 'Expense', 'Expense', 'Income'],
        'amount': [5000, 1000, 500, 2000]
    }
    df = pd.DataFrame(data)
    
    income, expense, savings, rate = an.calculate_metrics(df)
    assert income == 7000
    assert expense == 1500
    assert savings == 5500
    assert rate == (5500 / 7000) * 100

def test_calculate_mom_expense_change():
    data = {
        'transaction_date': ['2023-09-15', '2023-09-20', '2023-10-10'],
        'transaction_type': ['Expense', 'Expense', 'Expense'],
        'amount': [1000, 2000, 3600]
    }
    df = pd.DataFrame(data)
    
    mom = an.calculate_mom_expense_change(df)
    # Sep total = 3000
    # Oct total = 3600
    # Change = ((3600 - 3000) / 3000) * 100 = 20%
    assert mom == 20.0

def test_get_top_spending_categories():
    data = {
        'transaction_type': ['Expense', 'Expense', 'Income', 'Expense'],
        'category': ['Food', 'Travel', 'Salary', 'Food'],
        'amount': [1000, 5000, 10000, 2000]
    }
    df = pd.DataFrame(data)
    
    top_cat = an.get_top_spending_categories(df, top_n=1)
    assert len(top_cat) == 1
    assert top_cat.iloc[0]['category'] == 'Travel'
    assert top_cat.iloc[0]['amount'] == 5000
