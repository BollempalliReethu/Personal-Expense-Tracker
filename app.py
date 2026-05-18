import streamlit as st
import pandas as pd
from datetime import date

# Page Title
st.set_page_config(page_title="Personal Expense Tracker", layout="wide")

# Store transactions
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# ---------------- HOME PAGE ----------------
if menu == "Home":

    st.title("💰 Personal Expense Tracker")

    st.write("""
    This is a Streamlit-based web application used to track personal income and expenses.

    ### Features:
    - Add Income
    - Add Expenses
    - View Transaction History
    - Calculate Total Income
    - Calculate Total Expenses
    - Display Remaining Balance
    - Category-wise Expense Summary

    ### Purpose:
    To help users manage daily financial activities in an organized way.
    """)

# ---------------- ADD TRANSACTION ----------------
elif menu == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    if transaction_type == "Income":
        category = st.text_input("Income Source")
    else:
        category = st.selectbox(
            "Expense Category",
            ["Food", "Travel", "Shopping", "Bills",
             "Education", "Medical", "Others"]
        )

    amount = st.number_input("Amount", min_value=0.0)

    transaction_date = st.date_input("Date", value=date.today())

    description = st.text_area("Description")

    if st.button("Add Transaction"):

        transaction = {
            "Type": transaction_type,
            "Category/Source": category,
            "Amount": amount,
            "Date": str(transaction_date),
            "Description": description
        }

        st.session_state.transactions.append(transaction)

        st.success("Transaction Added Successfully!")

# ---------------- VIEW TRANSACTIONS ----------------
elif menu == "View Transactions":

    st.title("📋 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No transactions available.")

# ---------------- SUMMARY ----------------
elif menu == "Summary":

    st.title("📊 Financial Summary")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        # Total Income
        total_income = df[df["Type"] == "Income"]["Amount"].sum()

        # Total Expense
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

        # Balance
        balance = total_income - total_expense

        st.subheader("Summary Details")

        st.write(f"### Total Income: ₹ {total_income}")
        st.write(f"### Total Expenses: ₹ {total_expense}")
        st.write(f"### Remaining Balance: ₹ {balance}")

        # Category-wise Expense Summary
        st.subheader("Category-wise Expense Summary")

        expense_df = df[df["Type"] == "Expense"]

        if not expense_df.empty:

            category_summary = expense_df.groupby(
                "Category/Source"
            )["Amount"].sum()

            st.table(category_summary)

            st.bar_chart(category_summary)

        else:
            st.info("No expense data available.")

    else:
        st.warning("No transactions available.")