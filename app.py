import google.generativeai as genai
from dotenv import load_dotenv
import os
import sqlite3
import re
import gradio as gr
import time
from functools import lru_cache


# Load Gemini API key
load_dotenv()
model = genai.GenerativeModel("gemini-2.0-flash-001")

# Database schema detection with caching
@lru_cache(maxsize=1)
def get_schema():
    conn = sqlite3.connect("classicmodels.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    schema = {}
    for table in cursor.fetchall():
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema[table_name] = [col[1] for col in cursor.fetchall()]
    conn.close()
    return schema

SCHEMA = get_schema()

# Database operations with timeout
def query_db(query, args=(), timeout=5):
    try:
        conn = sqlite3.connect("classicmodels.db", timeout=timeout)
        cursor = conn.cursor()
        cursor.execute(query, args)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        raise Exception(f"Database error: {str(e)}")

# Pre-defined quick queries
QUICK_QUERIES = {
    r'list (?:the )?offices': {
        'query': "SELECT officeCode, city, country, phone FROM offices",
        'format': lambda r: "\n".join([f"{row[0]}: {row[1]}, {row[2]} (Phone: {row[3]})" for row in r])
    },
    r'list (?:the )?products': {
        'query': "SELECT productName, productLine, buyPrice FROM products ORDER BY productName LIMIT 20",
        'format': lambda r: "First 20 products:\n" + "\n".join([f"- {row[0]} ({row[1]}) - ${row[2]:,.2f}" for row in r])
    },
    r'count (?:the )?(employees|customers|products|offices)': {
        'query': lambda m: f"SELECT COUNT(*) FROM {m.group(1)}",
        'format': lambda r, m: f"There are {r[0][0]} {m.group(1)} in the database"
    }
}

def handle_quick_query(prompt):
    prompt_lower = prompt.lower()
    for pattern, handler in QUICK_QUERIES.items():
        match = re.search(pattern, prompt_lower)
        if match:
            query = handler['query'](match) if callable(handler['query']) else handler['query']
            results = query_db(query)
            return handler['format'](results, match) if 'm' in handler['format'].__code__.co_varnames else handler['format'](results)
    return None

# Special question handlers (now properly defined)
def handle_special_query(prompt):
    prompt_lower = prompt.lower()
    
    # Top products by price
    if re.search(r'top \d+ (?:most )?expensive products', prompt_lower):
        limit = int(re.search(r'top (\d+)', prompt_lower).group(1))
        products = query_db(f"""
            SELECT productName, buyPrice 
            FROM products 
            ORDER BY buyPrice DESC 
            LIMIT {limit}
        """)
        if not products:
            return "No products found."
        response = [f"Top {limit} most expensive products:"]
        for i, (name, price) in enumerate(products, 1):
            response.append(f"{i}. {name} - ${price:,.2f}")
        return "\n".join(response)
    
    # Products out of stock
    if "out of stock" in prompt_lower:
        products = query_db("""
            SELECT productName, quantityInStock 
            FROM products 
            WHERE quantityInStock = 0
        """)
        if not products:
            return "All products are in stock."
        return "Out of stock products:\n" + "\n".join(f"- {row[0]}" for row in products)
    
    return None

def extract_sql(text):
    """Robust SQL extraction with validation"""
    match = re.search(
        r'(SELECT\s.+?;)',
        text,
        re.IGNORECASE | re.DOTALL
    )
    if not match:
        raise Exception("No valid SQL found in response")
    return match.group(1).strip()

def chatbot(prompt):
    start_time = time.time()
    
    # First try quick handlers
    if (response := handle_quick_query(prompt)):
        print(f"Quick query took {time.time()-start_time:.2f}s")
        return response
    
    # Then try special handlers
    if (response := handle_special_query(prompt)):
        print(f"Special query took {time.time()-start_time:.2f}s")
        return response
    
    # Finally use Gemini for complex queries
    try:
        response = model.generate_content(
            f"""Convert this query to efficient SQLite SQL using schema: {SCHEMA}.
            Return ONLY the SQL query, no explanations.
            Query: '{prompt}'""",
            generation_config={"temperature": 0.1}
        )
        
        sql_query = extract_sql(response.text)
        print("[DEBUG] Generated SQL:", sql_query)
        
        if not sql_query.strip().upper().startswith('SELECT'):
            raise Exception("Only SELECT queries are allowed")
        
        results = query_db(sql_query, timeout=10)
        
        if not results:
            return "No matching records found."
        
        # Format results
        if len(results[0]) == 1:  # Single column
            items = [str(row[0]) for row in results[:20]]
            response = "\n".join(f"- {item}" for item in items)
            if len(results) > 20:
                response += f"\n...showing 20 of {len(results)} total results"
            return response
        
        # Multi-column
        explanation = model.generate_content(
            f"Summarize these results in one sentence: {results[:5]}",
            generation_config={"temperature": 0.2}
        )
        print(f"Complex query took {time.time()-start_time:.2f}s")
        return explanation.text
        
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""# Database Expert Chatbot""")
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(label="Ask anything about the database", 
                                placeholder="e.g., List offices, Show top products...")
            submit_btn = gr.Button("Search", variant="primary")
        with gr.Column():
            output = gr.Textbox(label="Response", interactive=False)
    
    examples = gr.Examples(
        examples=[
            "List the offices",
            "Show top 5 most expensive products",
            "Which products are out of stock?",
            "Count customers from France"
        ],
        inputs=question
    )
    
    submit_btn.click(
        chatbot,
        inputs=question,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()