import google.generativeai as genai
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from sqlalchemy import create_engine, MetaData
import gradio as gr
import os
import sqlite3
import shutil

# 1. Handle database file properly
DB_NAME = "classicmodels.db"

# Ensure we're working with the correct file
if not os.path.exists(DB_NAME):
    for file in os.listdir():
        if file.startswith("classicmodels") and file.endswith(".db"):
            shutil.copy(file, DB_NAME)
            print(f"Using database file: {file}")
            break

# Verify connection
try:
    conn = sqlite3.connect(DB_NAME)
    tables = conn.cursor().execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    print(f"Database connected. Tables: {[t[0] for t in tables]}")
except Exception as e:
    print(f"Database error: {str(e)}")
    raise


# 2. Configure SQLDatabase
db = SQLDatabase.from_uri(
    f"sqlite:///{DB_NAME}",
    include_tables=[
        'productlines', 'products', 'offices',
        'employees', 'customers', 'payments',
        'orders', 'orderdetails'
    ],
    sample_rows_in_table_info=1,
    view_support=False
)

# This will automatically get the secret from Hugging Face
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("No Gemini API key found. Please set GEMINI_API_KEY secret in Hugging Face.")

#genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini API key
#load_dotenv()
#model = genai.GenerativeModel("gemini-2.0-flash-001")

# 4. Initialize LLM with UPDATED model name
llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",  # Updated model name
    temperature=0.3,
    google_api_key=GEMINI_API_KEY,
    max_output_tokens=2048,
    top_k=40,
    top_p=0.95
)



# 4. Proper prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a ClassicModels database expert. Follow these rules:
1. Use these relationships:
   - customers → orders → orderdetails → products → productlines
   - employees → offices
   - customers → payments
2. Format currency as USD ($1,000.00)
3. Use dates as YYYY-MM-DD
4. Never modify data
5. Schema: {schema}"""),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

# 5. Create agent with error handling
agent = create_sql_agent(
    llm=llm_model,
    db=db,
    prompt=prompt,
    agent_type="openai-tools",
    verbose=False,
    max_iterations=10,
    handle_parsing_errors=True,
    return_intermediate_steps=False


# 6. Enhanced query processing
def process_query(question):
    try:
        # Block harmful queries
        blocked_terms = ["drop", "delete", "insert", "update", "alter", ";--"]
        if any(term in question.lower() for term in blocked_terms):
            raise ValueError("Data modification queries are disabled")
            
        # Get the database schema to include in the prompt
        schema = db.get_table_info()
        response = agent.invoke({
            "input": question,
            "schema": schema  # Add the schema to the input
        })
        result = response['output']
        
        # Clean common Gemini artifacts
        if "```sql" in result:
            result = result.split("```")[-2].replace("```sql", "").strip()
        return result
        
    except Exception as e:
        error_message = str(e)
        # Format the error output nicely
        return f""" **Error Processing Query**  
        
{error_message}  

 **Try rephrasing your question like:**  
- "Show customers from France"  
- "List products needing restock"  
- "Which employees report to Diane Murphy?"  
- "What are our top 5 selling products?"  

 **Tips:**  
• Use simple, clear questions  
• Focus on customers, products, orders, or employees  
• Avoid special characters or complex syntax"""    
    
    
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏭 ClassicModels Database Assistant
    *Natural language interface for the ClassicModels ERP system*
    """)
    
    with gr.Row():
        query = gr.Textbox(label="Ask about products, customers, or orders", 
                         placeholder="e.g., 'Show motorcycle products with low stock'")
        output = gr.Textbox(label="Results", lines=5)
    
    examples = gr.Examples(
        examples=[
            "List all classic cars under $50",
            "Show customers who haven't ordered in 6 months",
            "Which office has the most employees?",
            "Find orders with missing payments"
        ],
        inputs=query
    )
    
    # Add a submit button
    submit_btn = gr.Button("Submit", variant="primary")
    submit_btn.click(fn=process_query, inputs=query, outputs=output)
    
    # Keep the enter-key submission as well
    query.submit(fn=process_query, inputs=query, outputs=output)

demo.launch(debug=True)