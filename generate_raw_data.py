import numpy as np
import pandas as pd

np.random.seed(42)
n = 1500

dates = pd.date_range("2024-01-01", "2024-12-31", periods=n)
categories = np.random.choice(
    ["Electrónica", "Mobiliario", "Accesorios", "Oficina"],
    size=n,
    p=[0.25, 0.25, 0.30, 0.20],
)
regions = np.random.choice(["Norte", "Sur", "Centro", "Este", "Oeste"], size=n)

sales = np.round(np.random.exponential(scale=160, size=n) + 25, 2)
discounts = np.random.choice(
    [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50], size=n
)

# Mayor tasa de retorno en mobiliario
ret_prob = np.where(categories == "Mobiliario", 0.28, 0.07)
returns = np.random.binomial(1, ret_prob)

# Beneficio dependiente del descuento
profit = np.round(sales * (np.random.uniform(0.18, 0.38, size=n) - (discounts * 1.4)), 2)

df_raw = pd.DataFrame(
    {
        "Order_ID": [f"ORD-{2000 + i}" for i in range(n)],
        "Order_Date": dates,
        "Customer_Name": [f"Cliente {i}" for i in range(n)],
        "Customer_Email": [f"user_{i}@empresa.com" for i in range(n)],
        "Region": regions,
        "Category": categories,
        "Sales": sales,
        "Discount": discounts,
        "Profit": profit,
        "Returned": returns,
    }
)

# Inyección deliberada de inconsistencias para limpieza
df_raw.loc[10:20, "Sales"] = np.nan
df_raw.loc[30:35, "Discount"] = np.nan
df_raw = pd.concat([df_raw, df_raw.iloc[0:5]], ignore_index=True)  # Duplicados

df_raw.to_csv("raw_sales_data.csv", index=False)
print("Dataset bruto generado: raw_sales_data.csv")