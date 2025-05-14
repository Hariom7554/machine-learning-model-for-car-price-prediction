import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import tkinter as tk
from tkinter import ttk

# Load dataset
df = pd.read_csv("car data.csv")

# Encode categorical features
car_encoder = LabelEncoder()
fuel_encoder = LabelEncoder()

df["Car_Name_Encoded"] = car_encoder.fit_transform(df["Car_Name"])
df["Fuel_Type_Encoded"] = fuel_encoder.fit_transform(df["Fuel_Type"])

# Prepare features and target
X = df[["Car_Name_Encoded", "Driven_kms", "Year", "Fuel_Type_Encoded"]]
y = df["Present_Price"]

# Train model
model = LinearRegression()
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(x_train, y_train)

# ----------- Build UI using Tkinter ---------------

def predict_price():
    try:
        car = car_name_var.get()
        kms = float(driven_kms_var.get())
        year = int(year_var.get())
        fuel = fuel_type_var.get()

        # Encode inputs
        car_encoded = car_encoder.transform([car])[0]
        fuel_encoded = fuel_encoder.transform([fuel])[0]

        input_data = [[car_encoded, kms, year, fuel_encoded]]
        prediction = model.predict(input_data)[0]
        result_label.config(text=f"Estimated Price: ₹ {prediction:.2f} lakhs")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Create main window
root = tk.Tk()
root.title("Car Price Estimator")
root.geometry("500x500")

# Variables for inputs
car_name_var = tk.StringVar()
fuel_type_var = tk.StringVar()
driven_kms_var = tk.StringVar()
year_var = tk.StringVar()

# Car name dropdown
ttk.Label(root, text="Select Car Name").grid(row=0, column=0, padx=20, pady=15, sticky='w')
ttk.Combobox(root, textvariable=car_name_var, values=list(car_encoder.classes_)).grid(row=0, column=1)

# Year of manufacture
ttk.Label(root, text="Year of Manufacture").grid(row=1, column=0, padx=10, pady=5, sticky='w')
ttk.Entry(root, textvariable=year_var).grid(row=1, column=1)

# Driven kilometers
ttk.Label(root, text="KMs Driven").grid(row=2, column=0, padx=10, pady=5, sticky='w')
ttk.Entry(root, textvariable=driven_kms_var).grid(row=2, column=1)

# Fuel type dropdown
ttk.Label(root, text="Fuel Type").grid(row=3, column=0, padx=10, pady=5, sticky='w')
ttk.Combobox(root, textvariable=fuel_type_var, values=list(fuel_encoder.classes_)).grid(row=3, column=1)

# Predict button
ttk.Button(root, text="Estimate Price", command=predict_price).grid(row=4, column=0, columnspan=2, pady=15)

# Result label
result_label = ttk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
