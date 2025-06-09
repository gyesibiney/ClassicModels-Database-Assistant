import sqlite3
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os

# Load the tokenizer and model
model_id = "defog/sqlcoder"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Set up SQLite DB
DB_PATH = "classicmodels.db"
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    with open("mysqlsampledatabase.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
else:
    conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Function to convert NL to SQL using HF model
def generate_sql(nl_query):
    prompt = f"-- Given the classicmodels database\n-- Question: {nl_query}\nSELECT"
    output = generator(prompt, max_new_tokens=100, do_sample=False)[0]['generated_text']
    
    # Extract the SQL (from after 'SELECT')
    start = output.find("SELECT")
    sql = output[start:].strip().split(";")[0]
    return sql

# Chatbot function
def chatbot(nl_query):
    try:
        sql = generate_sql(nl_query)
        cursor.execute(sql)
        result = cursor.fetchall()
        return f"SQL: {sql}\n\nResult:\n{result if result else 'No data found.'}"
    except Exception as e:
        return f"Error: {e}"

# Gradio interface
gr.Interface(fn=chatbot,
             inputs="text",
             outputs="text",
             title="Chat with SQL Database (Hugging Face)",
             description="Ask a question about the classicmodels database (e.g. 'List customers in USA')"
             ).launch()
