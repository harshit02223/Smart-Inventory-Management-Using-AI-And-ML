from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
import pandas as pd
from fastapi.responses import JSONResponse

# Database Connection
DATABASE_URL = "mysql+pymysql://root:your_password@127.0.0.1/smart_inventory"
engine = create_engine(DATABASE_URL)

def fetch_data(query):
    """Fetch data from the database."""
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sales_history")
def get_sales_history():
    try:
        query = "SELECT * FROM sales_history"
        data = fetch_data(query)
        return JSONResponse(content=data.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/inventory_summary")
def get_inventory_summary():
    try:
        query = "SELECT * FROM inventory_level"
        data = fetch_data(query)
        return JSONResponse(content=data.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/forecast_data")
def get_forecast_data():
    try:
        query = "SELECT * FROM forecast_df"
        data = fetch_data(query)
        return JSONResponse(content=data.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/alerts")
def get_alerts():
    try:
        query = "SELECT * FROM alert"
        data = fetch_data(query)
        return JSONResponse(content=data.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/category_demand")
def get_category_demand():
    try:
        query = """
        SELECT p.products_category, SUM(s.quantity_sold) as total_quantity_sold
        FROM products p
        JOIN sales_history s ON p.products_id = s.products_id
        GROUP BY p.products_category
        """
        data = fetch_data(query)
        return JSONResponse(content=data.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000)
