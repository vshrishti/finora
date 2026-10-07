import pytest
import os
import sqlite3
import pandas as pd
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database as db

# Setup test database
TEST_DB = "test_finance.db"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Override db path for testing
    db.DB_PATH = TEST_DB
    db.init_db()
    
    yield
    
    # Teardown
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except:
            pass

def test_add_transaction():
    db.add_transaction("t1", "2023-10-01", "Expense", 500.50, "Food", "Lunch", "Cash")
    
    df = db.get_transactions()
    assert len(df) == 1
    assert df.iloc[0]['id'] == "t1"
    assert df.iloc[0]['amount'] == 500.50  # Should be returned in rupees
    
    # Verify in DB it's stored as paise
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM transactions WHERE id = 't1'")
    db_amount = cursor.fetchone()[0]
    conn.close()
    
    assert db_amount == 50050

def test_edit_transaction():
    db.add_transaction("t2", "2023-10-01", "Expense", 500.00, "Food", "Lunch", "Cash")
    db.edit_transaction("t2", "2023-10-02", "Income", 1000.00, "Salary", "October Salary", "Bank")
    
    df = db.get_transactions()
    assert len(df) == 1
    assert df.iloc[0]['amount'] == 1000.00
    assert df.iloc[0]['transaction_type'] == "Income"

def test_delete_transaction():
    db.add_transaction("t3", "2023-10-01", "Expense", 500.00, "Food", "Lunch", "Cash")
    db.delete_transaction("t3")
    
    df = db.get_transactions()
    assert len(df) == 0

def test_get_transactions_filter():
    db.add_transaction("t4", "2023-10-01", "Expense", 500.00, "Food", "Lunch", "Cash")
    db.add_transaction("t5", "2023-10-05", "Income", 1000.00, "Salary", "Oct", "Bank")
    
    # Filter by date
    df = db.get_transactions(start_date="2023-10-02", end_date="2023-10-10")
    assert len(df) == 1
    assert df.iloc[0]['id'] == "t5"
    
    # Filter by type
    df = db.get_transactions(t_type="Expense")
    assert len(df) == 1
    assert df.iloc[0]['id'] == "t4"

def test_budget_operations():
    db.set_budget("b1", "2023-10", "Food", 5000.00)
    
    df = db.get_budgets(month="2023-10")
    assert len(df) == 1
    assert df.iloc[0]['budget_amount'] == 5000.00
    assert df.iloc[0]['category'] == "Food"
    
    # Update budget
    db.set_budget("b2", "2023-10", "Food", 6000.00) # Same month and category should update
    df = db.get_budgets(month="2023-10")
    assert len(df) == 1
    assert df.iloc[0]['budget_amount'] == 6000.00
