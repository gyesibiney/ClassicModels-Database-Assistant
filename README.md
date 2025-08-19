🏭 Chat_DataBase_v1
Natural Language SQL Assistant for the ClassicModels Database


🚀 Overview
Chat_DataBase_v1 is an interactive chatbot that connects to the ClassicModels sample database and allows users to query it using natural language.
It leverages LangChain, Google Gemini API, and Gradio to provide a conversational interface for exploring customers, orders, products, employees, and more—without writing SQL manually.

✨ Features
💬 Natural Language to SQL: Ask business questions without SQL knowledge.

🔗 Relational Awareness: Predefined schema relationships:

customers → orders → orderdetails → products → productlines

employees → offices

customers → payments

💵 Smart Formatting:

Currency in USD ($1,000.00)

Dates in YYYY-MM-DD format

🔒 Read-Only Queries: Data modification (INSERT, UPDATE, DELETE) is blocked.

🎨 Clean UI: Powered by Gradio with ready-to-use examples.

🛠️ Tech Stack
LLM: Google Gemini 2.0 Flash

Frameworks: LangChain, Gradio

Database: SQLite (classicmodels.db)

Hosting: Hugging Face Spaces

📊 Example Queries
Try asking:

"List all classic cars under $50"

"Show customers who haven’t ordered in 6 months"

"Which office has the most employees?"

"Find orders with missing payments"

📂 Project Structure
bash
Copy
Edit
📦 Chat_DataBase_v1
 ┣ 📜 app.py               # Main application logic
 ┣ 📜 classicmodels.db     # SQLite database (auto-detected)
 ┣ 📜 requirements.txt     # Dependencies
 ┗ 📜 README.md            # Project documentation
🔑 Setup on Hugging Face
Clone the repository or open in Hugging Face Spaces.

Add your Gemini API Key in the Space settings → Secrets:

ini
Copy
Edit
GEMINI_API_KEY = your_google_api_key
Run the Space. The app will automatically detect and load classicmodels.db.

🙌 Credits
Database: ClassicModels Sample DB

Frameworks: LangChain, Gradio

LLM: Google Gemini

🌐 Live Demo
👉 Open Chat_DataBase_v1 on Hugging Face





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
