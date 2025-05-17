def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

fastapi_thread = Thread(target=run_fastapi, daemon=True)
fastapi_thread.start()


dash_app = Dash(__name__)
dash_app.title = "Smart Inventory Dashboard"

dash_app.layout = html.Div([
    html.H1("Smart Inventory Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.H2("Sales History"),
        dcc.Graph(id="sales-history-chart"),
    ]),

    html.Div([
        html.H2("Forecasted Demand"),
        dcc.Graph(id="forecast-chart"),
    ]),

    html.Div([
        html.H2("Inventory Summary"),
        dcc.Graph(id="inventory-summary"),
    ]),

    html.Div([
        html.H2("Alerts"),
        dcc.Graph(id="alerts-table"),
    ]),

    html.Div([
        html.H2("Category Demand"),
        dcc.Graph(id="category-demand-chart"),
    ]),
])

@dash_app.callback(
    Output("sales-history-chart", "figure"),
    Input("sales-history-chart", "id")
)
def update_sales_history(_):
    try:
        sales_data = pd.read_json("http://127.0.0.1:8000/sales_history")
        fig = px.line(
            sales_data, 
            x="sale_date", 
            y="quantity_sold", 
            color="products_id",
            title="Sales History (Time Series)"
        )
        return fig
    except Exception as e:
        return px.scatter(title=f"Error loading data: {str(e)}")



@dash_app.callback(
    Output("forecast-chart", "figure"),
    Input("forecast-chart", "id")
)
def update_forecast_chart(_):
    try:
        forecast_data = pd.read_json("http://127.0.0.1:8000/forecast_data")
        fig = px.line(
            forecast_data, 
            x="Date", 
            y="Predicted Demand",
            title="Forecasted Demand"
        )
        return fig
    except Exception as e:
        return px.scatter(title=f"Error loading data: {str(e)}")


@dash_app.callback(
    Output("inventory-summary", "figure"),
    Input("inventory-summary", "id")
)
def update_inventory_summary(_):
    try:
        inventory_data = pd.read_json("http://127.0.0.1:8000/inventory_summary")
        fig = px.bar(
            inventory_data, 
            x="products_id", 
            y="current_stock",
            title="Current Inventory Levels"
        )
        return fig
    except Exception as e:
        return px.scatter(title=f"Error loading data: {str(e)}")



@dash_app.callback(
    Output("alerts-table", "figure"),
    Input("alerts-table", "id")
)
def update_alerts(_):
    try:
        alerts_data = pd.read_json("http://127.0.0.1:8000/alerts")
        fig = px.bar(
            alerts_data, 
            x="products_id", 
            y="alert_message",
            title="Inventory Alerts"
        )
        return fig
    except Exception as e:
        return px.scatter(title=f"Error loading data: {str(e)}")


@dash_app.callback(
    Output("category-demand-chart", "figure"),
    Input("category-demand-chart", "id")
)
def update_category_demand(_):
    try:
        category_demand_data = pd.read_json("http://127.0.0.1:8000/category_demand")
        fig = px.bar(
            category_demand_data, 
            x="products_category", 
            y="total_quantity_sold",
            title="Category-Wise Product Demand"
        )
        return fig
    except Exception as e:
        return px.scatter(title=f"Error loading data: {str(e)}")
def open_dashboard():
    webbrowser.open("http://127.0.0.1:8050/")

if __name__ == "__main__":
    open_dashboard()
    dash_app.run_server(debug=True, port=8050)