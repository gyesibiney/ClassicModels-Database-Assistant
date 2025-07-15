import sqlite3
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv
import os



def get_db_schema():
    conn = sqlite3.connect("classicsmodel.db")
    cursor = conn.cursor()
    
    # Fetch all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Fetch schema for each table
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema[table_name] = [col[1] for col in columns]  # Extract column names
    
    conn.close()
    return schema

schema = get_db_schema()
print("Database Schema:", schema)


# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDOp2eNePSknhlbg91ADtPrdmcUwvTGWIo"))
model = genai.GenerativeModel("gemini-pro")

# Database connection
def query_db(query, args=()):
    conn = sqlite3.connect("classicsmodel.db")
    cursor = conn.cursor()
    cursor.execute(query, args)
    results = cursor.fetchall()
    conn.close()
    return results

# Chatbot with schema context
def chatbot(prompt):
    schema = get_db_schema()  # From Step 1
    
    # Step 1: Generate SQL using schema
    response = model.generate_content(
        f"""Convert this user query into SQL for SQLite. Database schema: {schema}.
        Return ONLY the SQL query, nothing else. Query: '{prompt}'"""
    )
    sql_query = response.text.strip()
    print("Generated SQL:", sql_query)  # Debugging

    # Step 2: Execute SQL
    try:
        results = query_db(sql_query)
        
        # Step 3: Explain results
        if results:
            explanation = model.generate_content(
                f"Explain these database results in a conversational way: {results}"
            )
            return explanation.text
        else:
            return "No results found."
            
    except Exception as e:
        return f"Sorry, I couldn't process that. Error: {str(e)}"

    while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("Bot:", chatbot(user_input))