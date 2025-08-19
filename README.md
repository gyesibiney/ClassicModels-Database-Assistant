🏭 Chat_DataBase_v1
Natural Language SQL Assistant for the ClassicModels Database


📌 Overview
This project provides a chat-based SQL assistant for the ClassicModels ERP-style database.
It uses Google Gemini (via langchain_google_genai) and LangChain’s SQL agent toolkit to translate natural language queries into SQL queries.
The assistant enables users to explore the ClassicModels database with simple English questions.

🚀 Features
🔍 Ask in plain English: "Show customers from France", "List products needing restock"

📊 Query supported tables:

productlines, products, offices

employees, customers, payments

orders, orderdetails

🛡️ Safe by design: Blocks data modification queries (INSERT, DELETE, DROP, etc.)

💵 Auto-formatting: Currency in USD ($1,000.00), dates as YYYY-MM-DD

🧩 Interactive Gradio UI: Easy-to-use input box with example queries

📂 Database Schema
Key relationships include:

customers → orders → orderdetails → products → productlines

employees → offices

customers → payments

⚙️ Tech Stack
LLM: Google Gemini 2.0 Flash

Frameworks:

LangChain

Gradio

Database: classicmodels.db (SQLite)

Deployment: Hugging Face Spaces

🔑 Setup
Clone the repository or open the Space.

Ensure the ClassicModels database file (classicmodels.db) is present in the working directory.

Set up Hugging Face secrets:

bash
GEMINI_API_KEY = "your_google_api_key"
Install dependencies:

bash
pip install -r requirements.txt
▶️ Usage
Run locally with:

bash
python app.py
Or open directly in Hugging Face Space:
👉 Chat_DataBase_v1

💡 Example Queries
"List all classic cars under $50"

"Show customers who haven't ordered in 6 months"

"Which office has the most employees?"

"Find orders with missing payments"



---
title: Chat DataBase V1
emoji: 🐠
colorFrom: pink
colorTo: pink
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
