import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pickle

# Selected features and default values
features = [
    "HighBP", "HighChol", "CholCheck", "BMI", "HeartDiseaseorAttack",
    "HvyAlcoholConsump", "GenHlth", "DiffWalk", "Sex", "Age", "Income"
]
default_values = [0, 0, 1, 25, 0, 0, 3, 0, 1, 20, 4]

descriptions = {
    "HighBP": "0 = no high BP, 1 = high BP",
    "HighChol": "0 = no high cholesterol, 1 = high cholesterol",
    "CholCheck": "0 = no check in 5 years, 1 = yes check in 5 years",
    "BMI": "Body Mass Index",
    "HeartDiseaseorAttack": "Coronary heart disease or heart attack? 0 = no, 1 = yes",
    "HvyAlcoholConsump": "Heavy alcohol: Men ≥14/wk, Women ≥7/wk; 0 = no, 1 = yes",
    "GenHlth": "General health rating: 1=excellent, 5=poor",
    "DiffWalk": "Difficulty walking/climbing stairs? 0 = no, 1 = yes",
    "Sex": "0 = female, 1 = male",
    "Age": "Age category: 1=18-24, ..., 13=80+",
    "Income": "Income level (1-8; 1 = < $10k, 5 = < $35k, 8 = ≥ $75k)"
}

# Load model
try:
    with open("XGB_model.pkl", "rb") as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")

# GUI Setup
root = tk.Tk()
root.title("Diabetes Prediction")
root.geometry("875x575")
root.configure(bg="#f4f4f4")

LARGE_FONT = ("Arial", 16)
MEDIUM_FONT = ("Arial", 14)
SMALL_FONT = ("Arial", 12)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Create two frames for left and right sides
left_frame = ttk.Frame(main_frame, padding=10)
left_frame.grid(row=0, column=0, sticky="n")
right_frame = ttk.Frame(main_frame, padding=10)
right_frame.grid(row=0, column=1, sticky="n")

entries = {}

def clear_placeholder(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(foreground="black")

def restore_placeholder(event, entry, default_text):
    if not entry.get():
        entry.insert(0, default_text)
        entry.config(foreground="grey")

left_row = 0
right_row = 0

# Create input fields with descriptions on two sides
for i, (feature, default) in enumerate(zip(features, default_values)):
    if i % 2 == 0:
        frame = left_frame
        row_index = left_row
        left_row += 2
    else:
        frame = right_frame
        row_index = right_row
        right_row += 2

    ttk.Label(frame, text=f"{feature}:", font=MEDIUM_FONT).grid(row=row_index, column=0, sticky="e", padx=5, pady=4)
    entry = ttk.Entry(frame, width=10)
    entry.insert(0, str(default))
    entry.config(foreground="grey", font=MEDIUM_FONT)
    entry.bind("<FocusIn>", lambda event, e=entry, d=str(default): clear_placeholder(event, e, d))
    entry.bind("<FocusOut>", lambda event, e=entry, d=str(default): restore_placeholder(event, e, d))
    entry.grid(row=row_index, column=1, padx=5, pady=4)
    ttk.Label(frame, text=descriptions[feature], font=SMALL_FONT, foreground="gray", background="#f4f4f4")\
        .grid(row=row_index+1, column=0, columnspan=2, sticky="w", padx=5)
    entries[feature] = entry

def predict():
    if model is None:
        messagebox.showerror("Error", "Model not loaded. Ensure 'XGB_model.pkl' is in the directory.")
        return
    try:
        input_data = {feature: float(entries[feature].get().strip()) for feature in features}
        df_input = pd.DataFrame([input_data])
        prediction = model.predict(df_input)[0]
        result_label.config(text=f"Prediction: {'Diabetic (1)' if prediction else 'Non-Diabetic (0)'}",
                            foreground="red" if prediction else "green", font=LARGE_FONT)
    except Exception as e:
        messagebox.showerror("Error", f"Prediction failed:\n{e}")

button_frame = ttk.Frame(main_frame, padding=10)
button_frame.grid(row=1, column=0, columnspan=2)
style = ttk.Style()
style.configure('Big.TButton', font=('Arial', 16), padding=10)
ttk.Button(button_frame, text="Predict", command=predict, style='Big.TButton').pack(pady=10)

result_label = ttk.Label(main_frame, text="Prediction: N/A", font=LARGE_FONT)
result_label.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
