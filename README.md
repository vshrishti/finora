# Finora - Personal Finance & Expense Analytics

A complete personal finance management application that helps users track income, expenses, savings, budgets, and spending patterns through an interactive dashboard.

## Problem Statement

Managing personal finances manually can make it difficult to
track spending habits, monitor budgets, and understand savings
patterns. Finora provides a centralized dashboard to record
transactions, analyze expenses, and manage monthly budgets.


## Features

- **Dashboard:** Overview of finances including total income, expenses, savings, savings rate, and budget usage.
- **Analytics:** Visualizations of spending trends, income vs expenses, category breakdowns, and month-over-month comparisons.
- **Transactions Management:** Add, edit, delete, and view all transactions. Filter by date, type, category, and payment method.
- **Budgeting:** Set category-wise monthly budgets. Monitor budget consumption with visual progress bars and warnings for overspending.
- **Data Import/Export:** Export transactions to CSV or import transactions via CSV upload.
- **Sample Data:** Populate the database with realistic sample data for demonstration purposes (can be easily cleared).

## Technology Stack

- **Frontend:** Streamlit
- **Backend/Logic:** Python
- **Database:** SQLite3
- **Data Manipulation:** Pandas
- **Data Visualization:** Plotly

## Database Schema

### `transactions`
- `id` (TEXT, Primary Key)
- `transaction_date` (DATE)
- `transaction_type` (TEXT)
- `amount` (INTEGER, stored in paise for precision)
- `category` (TEXT)
- `description` (TEXT)
- `payment_method` (TEXT)
- `created_at` (TIMESTAMP)

### `budgets`
- `id` (TEXT, Primary Key)
- `month` (TEXT, format YYYY-MM)
- `category` (TEXT)
- `budget_amount` (INTEGER, stored in paise for precision)
- `created_at` (TIMESTAMP)

## Installation Instructions

1. Clone or download the repository.
2. Navigate to the project directory:
   ```bash
   cd finance-analytics
   ```
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application

Start the FastAPI server with the following command:

```bash
uvicorn app:app --reload
```

The application will open automatically in your default web browser (usually at `http://127.0.0.1:8000`).

## Testing Instructions

Automated tests are included to verify database operations and financial calculations.

Run the tests using `pytest`:

```bash
pytest tests/
```

## Sample Data Instructions

To see how the dashboard looks with populated data:
1. Run the application.
2. Navigate to the **Settings** page from the sidebar.
3. Click the **Load Sample Data** button.
4. Navigate back to the Dashboard or Analytics pages to view the populated charts and metrics.
5. To reset the data, go back to **Settings** and use the **Clear All Data** button.

## Future Improvements

- Add user authentication and support for multiple users.
- Connect directly to bank APIs for automatic transaction fetching.
- Add long-term financial goal tracking (e.g., saving for a car/house).
- Implement predictive analytics and ML models for expense forecasting.
- Add export functionality to PDF for monthly reports.
