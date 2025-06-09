from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import sqlite3
import gradio as gr

# Load small model
model_name = "mrm8488/t5-small-finetuned-wikiSQL"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Load SQLite DB
DB_PATH = "classicmodels.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Initialize the database
with open("mysqlsampledatabase.sql", "r") as f:
    conn.executescript(f.read())
conn.commit()

# Function to handle user query
def chatbot(nl_query):
    try:
        input_text = f"translate English to SQL: {nl_query}"
        sql = pipe(input_text, max_length=128, do_sample=False)[0]["generated_text"]
        cursor.execute(sql)
        result = cursor.fetchall()
        return f"SQL: {sql}\n\nResults:\n{result if result else 'No data found.'}"
    except Exception as e:
        return f"Error: {str(e)}"

gr.Interface(fn=chatbot,
             inputs="text",
             outputs="text",
             title="Chat with SQL Database",
             description="Ask natural language questions and convert to SQL using T5-small model."
).launch()
