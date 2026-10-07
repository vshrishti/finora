from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import database as db
import pandas as pd
from datetime import date
import uuid

app = FastAPI()

db.init_db()

class TransactionCreate(BaseModel):
    transaction_date: str
    transaction_type: str
    amount: float
    category: str
    description: Optional[str] = ""
    payment_method: Optional[str] = "Cash"

@app.get("/api/metrics")
def get_metrics():
    df = db.get_transactions()
    if df.empty:
        return {"total_income": 0, "total_expenses": 0, "savings": 0, "savings_rate": 0}
    
    income = df[df['transaction_type'] == 'Income']['amount'].sum()
    expense = df[df['transaction_type'] == 'Expense']['amount'].sum()
    savings = income - expense
    savings_rate = (savings / income * 100) if income > 0 else 0
    return {
        "total_income": round(income, 2),
        "total_expenses": round(expense, 2),
        "savings": round(savings, 2),
        "savings_rate": round(savings_rate, 2)
    }

@app.get("/api/transactions")
def list_transactions():
    df = db.get_transactions()
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.post("/api/transactions")
def add_transaction(tx: TransactionCreate):
    t_id = str(uuid.uuid4())
    db.add_transaction(
        t_id, tx.transaction_date, tx.transaction_type, 
        tx.amount, tx.category, tx.description, tx.payment_method
    )
    return {"status": "success", "id": t_id}

@app.get("/api/charts/category")
def chart_category():
    df = db.get_transactions()
    if df.empty:
        return {"labels": [], "values": []}
    expense_df = df[df['transaction_type'] == 'Expense']
    cat_data = expense_df.groupby('category')['amount'].sum().reset_index()
    return {
        "labels": cat_data['category'].tolist(),
        "values": cat_data['amount'].tolist()
    }

@app.get("/api/charts/trend")
def chart_trend():
    df = db.get_transactions()
    if df.empty:
        return {"labels": [], "values": []}
    expense_df = df[df['transaction_type'] == 'Expense'].copy()
    expense_df['date'] = pd.to_datetime(expense_df['transaction_date']).dt.strftime('%Y-%m-%d')
    daily = expense_df.groupby('date')['amount'].sum().reset_index()
    daily = daily.sort_values('date')
    return {
        "labels": daily['date'].tolist(),
        "values": daily['amount'].tolist()
    }

@app.post("/api/demo")
def load_demo():
    db.clear_all_data()
    db.load_sample_data()
    return {"status": "success"}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")
