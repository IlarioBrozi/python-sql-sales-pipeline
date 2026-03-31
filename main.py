import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# create database and connect sql
conn =sqlite3.connect("sales.db")
cursor=conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")

# create table
cursor.execute("""
CREATE TABLE sales (
    customer TEXT,
    category TEXT,
    amount REAL
)
""")

# insert data
data = [
    ("Mario", "A", 100),
    ("Anna", "B", 200),
    ("Mario", "A", 150),
    ("Anna", "B", None),
    ("Luca", "A", 120),
    ("Sara", "B", 300),
    ("Luca", "A", 120)
]

cursor.executemany("INSERT INTO sales VALUES (?,?,?)",data)
conn.commit()

#convert SQL table into pandas dataframe
query = "SELECT * FROM sales"
df = pd.read_sql(query, conn)

# remove duplicates
df = df.drop_duplicates()

# handle missing values
df["amount"] = df["amount"].fillna(0)

# discounted sales
df["discounted_sales"] = df["amount"]*0.9

# category label
def classify(x):
    if x < 150:
        return "low"
    if x <= 200:
        return "medium"
    else:
        return "high"
    
df["sales_category"] = df["amount"].apply(classify)

print(df)

#group by customer analysis
summary = df.groupby("customer")["discounted_sales"].sum().reset_index()

#export results in csv
summary.to_csv("sales_summary.csv", index=False)

print(summary)

#create visualization bar chart
summary.plot(
    x="customer",
    y="discounted_sales",
    kind="bar",
    title="Sales by Customer"
)

plt.xticks(rotation=45)  # tilt labels
plt.savefig("sales_by_customer.png")  # saves the file
plt.show()
