import streamlit as st
import psycopg2

# --- Connect to PostgreSQL ---
def get_connection():
    return psycopg2.connect(
        host="192.168.137.1",        # your laptop’s IPv4 address
        port="5432",                 # default PostgreSQL port
        database="image identifier", # your DB name
        user="postgres",             # your DB username
        password="Chinna@2005"       # your DB password
    )

# --- Example usage ---
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    st.sidebar.success(f"Connected to PostgreSQL: {db_version[0]} ✅")

except Exception as e:
    st.sidebar.error(f"Database connection failed: {e}")