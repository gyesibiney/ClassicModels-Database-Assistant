import sqlite3
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load CodeT5-small model
model_name = "Salesforce/codet5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Load the SQLite database with thread-safe option
conn = sqlite3.connect("classicmodels.db", check_same_thread=False)
cursor = conn.cursor()

def chatbot(nl_query):
    try:
        prompt = f"Convert this to SQL: {nl_query}"
        sql = pipe(prompt, max_length=100, do_sample=False)[0]["generated_text"]
        cursor.execute(sql)
        result = cursor.fetchall()
        return f"SQL: {sql}\n\nResult:\n{result if result else 'No data found.'}"
    except Exception as e:
        return f"Error: {str(e)}"

gr.Interface(fn=chatbot,
             inputs="text",
             outputs="text",
             title="Chat with SQL Database",
             description="Ask natural language questions. Example: 'List customers from France.'"
).launch()