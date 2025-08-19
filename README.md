# 🏭 Chat_DataBase_v1
**Natural Language SQL Assistant for the ClassicModels Database**

---

## 🚀 Overview
**Chat_DataBase_v1** is an interactive chatbot that connects to the **ClassicModels** sample database and allows users to query it using **natural language**.  

It uses:  
- **LangChain** for LLM orchestration  
- **Google Gemini API** for natural language → SQL  
- **Gradio** for a clean and interactive UI  

---

## ✨ Features
- 💬 **Natural Language to SQL** – Ask business questions without writing SQL.  
- 🔗 **Relational Awareness** – Supports schema links:  
  - `customers → orders → orderdetails → products → productlines`  
  - `employees → offices`  
  - `customers → payments`  
- 💵 **Smart Formatting** –  
  - Currency shown in **USD** (`$1,000.00`)  
  - Dates in `YYYY-MM-DD` format  
- 🔒 **Read-Only Queries** – Prevents destructive queries (`INSERT`, `UPDATE`, `DELETE`).  
- 🎨 **Clean Gradio UI** with **ready-to-use examples**.  

---

## 📊 Example Queries
Here are some queries you can try:  

```text
- List all classic cars under $50
- Show customers who haven’t ordered in 6 months
- Which office has the most employees?
- Find orders with missing payments

📂 Project Structure
bash

📦 Chat_DataBase_v1
 ┣ 📜 app.py               # Main application logic
 ┣ 📜 classicmodels.db     # SQLite database (auto-detected)
 ┣ 📜 requirements.txt     # Dependencies
 ┗ 📜 README.md            # Project documentation
🔑 Setup on Hugging Face
Clone the repository or open directly in Hugging Face Spaces.

Add your Gemini API Key in the Space settings → Secrets:

bash

GEMINI_API_KEY = your_google_api_key
Run the Space – the app will automatically detect and load classicmodels.db.



🙌 Credits
Database: ClassicModels Sample DB

Frameworks: LangChain, Gradio

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
```

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference



LLM: Google Gemini

🌐 Live Demo
👉 Open Chat_DataBase_v1 on Hugging Face

