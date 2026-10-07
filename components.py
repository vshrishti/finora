import streamlit as st

def format_currency(amount):
    """Format number to Indian Rupees."""
    return f"₹{amount:,.2f}"

def render_metric_card(title, value, delta=None, delta_color="normal"):
    """Render a styled metric card using Streamlit metrics."""
    st.metric(label=title, value=format_currency(value) if isinstance(value, (int, float)) else value, delta=delta, delta_color=delta_color)

def apply_custom_css():
    """Inject custom CSS for premium look."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global Typography */
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Headers */
        h1, h2, h3, h4 {
            color: #1e293b !important;
            font-weight: 700 !important;
        }

        /* Metric Cards overriding */
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #f1f5f9;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #2e7d32;
        }

        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1.05rem !important;
            color: #64748b !important;
            font-weight: 500 !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        }
        
        /* Sidebar Nav text */
        .stRadio label {
            font-weight: 500;
            font-size: 1.1rem;
        }

        /* Dataframes */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            background-color: #2e7d32 !important;
            color: white !important;
            transition: all 0.2s !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        }
        
        .stButton>button:hover {
            background-color: #1b5e20 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            transform: translateY(-1px);
        }

        /* Input fields */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            padding: 0.5rem 1rem;
        }
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
            border-color: #2e7d32;
            box-shadow: 0 0 0 1px #2e7d32;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #334155 !important;
            background-color: #f8f9fa !important;
            border-radius: 8px !important;
        }
        
        /* Empty states & Info boxes */
        .stAlert {
            border-radius: 8px;
            border: none;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }
        
        </style>
    """, unsafe_allow_html=True)
