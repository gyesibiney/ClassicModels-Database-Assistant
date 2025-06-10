from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import sqlite3
import gradio as gr

# Load small text-to-SQL model with slow tokenizer
model_name = "mrm8488/t5-small-finetuned-wikiSQL"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Setup DB
conn = sqlite3.connect("classicmodels.db")
cursor = conn.cursor()

# Initialize DB from .sql file
with open("classicmodels.db", "r") as f:
    cursor.executescript(f.read())
conn.commit()

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
             title="Chat with SQL Database (T5-small)",
             description="Ask questions about your database in natural language"
).launch()
