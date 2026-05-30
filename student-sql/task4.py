import logging
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv('../.env')
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Начало ETL")

    try:
        logging.info("Читаем CSV")
        sales_df = pd.read_csv("sales.csv")
        customers_df = pd.read_csv("customers.csv")
        logging.info("Файлы прочитаны")
    except Exception as e:
        logging.error(f"Ошибка при чтении: {e}")
        return

    logging.info("Обработку данных")

    sales_df = sales_df.drop_duplicates()

    sales_df["quantity"] = sales_df["quantity"].fillna(0)
    sales_df["unit_price"] = sales_df["unit_price"].fillna(0)

    sales_df["total_price"] = sales_df["quantity"] * sales_df["unit_price"]

    sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])
    sales_df["sale_month"] = sales_df["order_date"].dt.strftime("%Y-%m")

    customers_df = customers_df.drop_duplicates()

    customers_df["registration_date"] = pd.to_datetime(customers_df["registration_date"])
    today = pd.to_datetime("today")
    customers_df["loyalty_days"] = (today - customers_df["registration_date"]).dt.days

    customers_df["is_email_valid"] = customers_df["email"].str.contains("@", na=False)

    sales_summary = (sales_df.groupby("category")["total_price"].sum().reset_index())
    sales_summary.columns = ["category", "total_revenue"]

    merged_df = pd.merge(sales_df, customers_df, on="customer_id", how="inner")
    region_avg_check = (merged_df.groupby("region")["total_price"].mean().reset_index())
    region_avg_check.columns = ["region", "average_check"]

    product_ranking = (sales_df.groupby("product_name")["quantity"].sum().reset_index())
    product_ranking = product_ranking.sort_values(by="quantity", ascending=False).head(5)
    product_ranking.columns = ["product_name", "total_quantity_sold"]

    logging.info("Обработка данных завершена")

    logging.info("Загрузка в БД PostgreSQL...")

    try:
        customers_df.to_sql("customers", con=engine, if_exists="replace", index=False)
        sales_df.to_sql("sales", con=engine, if_exists="replace", index=False)

        sales_summary.to_sql("sales_summary", con=engine, if_exists="replace", index=False)
        product_ranking.to_sql("product_ranking", con=engine, if_exists="replace", index=False)

        region_avg_check.to_sql("region_avg_check", con=engine, if_exists="replace", index=False)

        logging.info("Процесс завершен")

    except Exception as e:
        logging.error(f"Ошибка при загрузке в БД: {e}")


if __name__ == "__main__":
    main()
