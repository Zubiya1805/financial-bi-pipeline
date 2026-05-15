import pandas as pd
import numpy as np
import os
import random
from faker import Faker
from datetime import datetime, date

regions = ['North', 'South', 'East', 'West']
segments = ['Consumer' , 'Corporate' , 'Small Business','Freelancer','Enterprise']
products = {
    'Office Supplies': ['Paper', 'Binders', 'Pens', 'Envelopes', 'Labels'],
    'Technology': ['Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Printer','Headphones', 'Camera', 'Speaker', 'Smartwatch', 'Router'],
    'Furniture': ['Chair', 'Desk', 'Bookcase', 'Filing Cabinet', 'Sofa'],
    'Clothing': ['Shirt', 'Pants', 'Jacket', 'Shoes', 'Hat']
}

fake = Faker()
def generate_transaction():
    region = random.choice(regions)
    segment =  random.choice(segments)
    product_category =  random.choice(list(products.keys()))
    product = random.choice(products[product_category]) 
    sales = np.random.uniform(500, 50000)
    quantity = np.random.randint(1,20)
    discount = np.random.random()
    if discount > 0.9 :
        discount = np.random.uniform(0.4, 0.6)
    else:
        discount = np.random.uniform(0.0, 0.35)
    
    profit = sales*(1-discount)*np.random.uniform(0.1, 0.3)
    transaction_id = fake.uuid4()
    transaction_date = date.today()
    return {
            'Transaction ID': transaction_id,
            'Region': region,
            'Segment' : segment,
            'Product Category': product_category,
            'Product': product,
            'Sales': round(sales, 2),
            'Quantity': quantity,
            'Discount': round(discount, 2),
            'Profit': round(profit, 2),
            'Transaction Date': transaction_date
        }

def generate_and_save_transactions(num_records):
    transactions = []
    for i in range(num_records):
        transaction = generate_transaction()
        transactions.append(transaction)
    df = pd.DataFrame(transactions)
    filename = f'transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    filepath = os.path.join('data', 'raw', filename)
    df.to_csv(filepath, index=False)
    print(f"File saved: {filepath}")
    
if __name__ == "__main__":
    generate_and_save_transactions(100)