import hashlib
import numpy as np
import pandas as pd

df = pd.read_csv("raw_sales_data.csv")

# 1. Ética y Privacidad: Anonimización de PII
# Se eliminan nombres y correos; se reemplaza Customer_Name con un identificador hash
df["customer_hash"] = df["Customer_Email"].apply(
    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:10]
)
df.drop(columns=["Customer_Name", "Customer_Email"], inplace=True)

# 2. Homologación y estandarización de columnas
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# 3. Tratamiento de duplicados y nulos
df.drop_duplicates(subset=["order_id"], keep="first", inplace=True)
df["sales"] = df["sales"].fillna(df["sales"].median())
df["discount"] = df["discount"].fillna(0.0)
df["returned"] = df["returned"].fillna(0).astype(int)

# 4. Homologación de texto
df["region"] = df["region"].str.title().str.strip()
df["category"] = df["category"].str.title().str.strip()

# 5. Métricas de negocio calculadas
df["net_revenue"] = np.where(
    df["returned"] == 1, 0, df["sales"] * (1 - df["discount"])
)
df["profit_margin"] = (df["profit"] / df["sales"]) * 100

# Guardar dataset limpio
df.to_csv("clean_sales_data.csv", index=False)
print("Dataset limpio generado con éxito: clean_sales_data.csv")