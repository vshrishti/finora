import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join("data", "finance.db")

def get_connection():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            transaction_date DATE NOT NULL,
            transaction_type TEXT NOT NULL,
            amount INTEGER NOT NULL, -- Stored in paise
            category TEXT NOT NULL,
            description TEXT,
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id TEXT PRIMARY KEY,
            month TEXT NOT NULL, -- Format: YYYY-MM
            category TEXT NOT NULL,
            budget_amount INTEGER NOT NULL, -- Stored in paise
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(month, category)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_transaction(t_id, t_date, t_type, amount_rupees, category, description, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    amount_paise = int(round(amount_rupees * 100))
    cursor.execute('''
        INSERT INTO transactions (id, transaction_date, transaction_type, amount, category, description, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (t_id, t_date, t_type, amount_paise, category, description, payment_method))
    conn.commit()
    conn.close()

def edit_transaction(t_id, t_date, t_type, amount_rupees, category, description, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    amount_paise = int(round(amount_rupees * 100))
    cursor.execute('''
        UPDATE transactions
        SET transaction_date = ?, transaction_type = ?, amount = ?, category = ?, description = ?, payment_method = ?
        WHERE id = ?
    ''', (t_date, t_type, amount_paise, category, description, payment_method, t_id))
    conn.commit()
    conn.close()

def delete_transaction(t_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (t_id,))
    conn.commit()
    conn.close()

def get_transactions(start_date=None, end_date=None, t_type=None, category=None):
    conn = get_connection()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND transaction_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND transaction_date <= ?"
        params.append(end_date)
    if t_type and t_type != "All":
        query += " AND transaction_type = ?"
        params.append(t_type)
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
        
    query += " ORDER BY transaction_date DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    # Convert paise to rupees
    if not df.empty:
        df['amount'] = df['amount'] / 100.0
    return df

def set_budget(b_id, month, category, amount_rupees):
    conn = get_connection()
    cursor = conn.cursor()
    amount_paise = int(round(amount_rupees * 100))
    cursor.execute('''
        INSERT INTO budgets (id, month, category, budget_amount)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(month, category) DO UPDATE SET budget_amount = excluded.budget_amount
    ''', (b_id, month, category, amount_paise))
    conn.commit()
    conn.close()

def get_budgets(month=None):
    conn = get_connection()
    query = "SELECT * FROM budgets"
    params = []
    if month:
        query += " WHERE month = ?"
        params.append(month)
        
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    if not df.empty:
        df['budget_amount'] = df['budget_amount'] / 100.0
    return df

def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions')
    cursor.execute('DELETE FROM budgets')
    conn.commit()
    conn.close()

def load_sample_data():
    import uuid
    import random
    from datetime import timedelta
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists to avoid duplicates
    cursor.execute('SELECT COUNT(*) FROM transactions')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False
        
    income_categories = ['Salary', 'Freelance', 'Investments']
    expense_categories = ['Food', 'Travel', 'Shopping', 'Rent', 'Bills', 'Entertainment']
    
    today = datetime.now()
    
    transactions = []
    for i in range(90): # 90 days
        current_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Add income (salary once a month)
        if i % 30 == 0:
            transactions.append((str(uuid.uuid4()), current_date, 'Income', 50000 * 100, 'Salary', 'Monthly Salary', 'Bank Transfer'))
        
        # Add random expenses
        num_expenses = random.randint(1, 3)
        for _ in range(num_expenses):
            cat = random.choice(expense_categories)
            amt = random.randint(100, 2000) * 100
            transactions.append((str(uuid.uuid4()), current_date, 'Expense', amt, cat, f'Sample {cat}', 'Credit Card'))
            
    cursor.executemany('''
        INSERT INTO transactions (id, transaction_date, transaction_type, amount, category, description, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', transactions)
    
    # Sample budgets
    budgets = []
    current_month = today.strftime('%Y-%m')
    for cat in expense_categories:
        amt = random.randint(2000, 10000) * 100
        budgets.append((str(uuid.uuid4()), current_month, cat, amt))
        
    cursor.executemany('''
        INSERT INTO budgets (id, month, category, budget_amount)
        VALUES (?, ?, ?, ?)
    ''', budgets)
    
    conn.commit()
    conn.close()
    return True
