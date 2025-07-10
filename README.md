# Text to SQL Assistant for AaiTech Industries

A Streamlit web app that converts natural language business questions into SQL queries, executes them on a MySQL database, and displays the results. Powered by Azure OpenAI and Azure Cognitive Search.
![Screenshot 2025-07-10 122800](https://github.com/user-attachments/assets/f6f6c346-fac5-454a-adc0-f6a3d876e06e)

## Features

- Ask business questions in plain English.
- Automatically generates SQL queries using Azure OpenAI.
- Executes queries on a MySQL database and displays results.
- Uses Azure Cognitive Search for schema-aware context (RAG).
- Modern, responsive UI with Streamlit.

## Project Structure

- `app.py` — Main Streamlit app.
- `text_to_sql.py` — Converts questions to SQL using Azure OpenAI and Azure Search.
- `database.py` — Handles MySQL connection and query execution.
- `create_and_upload_index.py` — Creates and uploads schema info to Azure Search.
- `data/` — Contains CSVs and schema SQL for the sample database.
- `.env` — Environment variables for API keys and DB credentials.
- `requirements.txt` — Python dependencies.

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd sql_assistant_by_aaitech
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure environment variables

- Copy `.env` and fill in your Azure OpenAI, Azure Search, and MySQL credentials.

### 4. Create and upload Azure Search index

```sh
python create_and_upload_index.py
```

### 5. Run the app

```sh
streamlit run app.py
```

## Usage

- Open the Streamlit app in your browser.
- Enter a business question (e.g., "Show total orders by country").
- View the generated SQL and query results.

## Requirements

- Python 3.8+
- MySQL server
- Azure OpenAI and Azure Cognitive Search accounts

## License

MIT License

---
