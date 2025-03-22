import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pickle

# Feature names and default values
features = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
    "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
    "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
    "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
]
default_values = [0, 0, 1, 40, 1, 0, 0, 0, 0, 1, 0, 1, 0, 3, 10, 15, 0, 1, 20, 4, 3]

# Summarized descriptions for each input field
descriptions = {
    "HighBP": "0 = no high BP, 1 = high BP",
    "HighChol": "0 = no high cholesterol, 1 = high cholesterol",
    "CholCheck": "0 = no check in 5 years, 1 = yes check in 5 years",
    "BMI": "Body Mass Index",
    "Smoker": "Have you smoked at least 100 cigarettes? 0 = no, 1 = yes",
    "Stroke": "Ever told you had a stroke? 0 = no, 1 = yes",
    "HeartDiseaseorAttack": "Coronary heart disease or heart attack? 0 = no, 1 = yes",
    "PhysActivity": "Physical activity in past 30 days (excl. job): 0 = no, 1 = yes",
    "Fruits": "Consume fruit ≥1/day? 0 = no, 1 = yes",
    "Veggies": "Consume vegetables ≥1/day? 0 = no, 1 = yes",
    "HvyAlcoholConsump": "Heavy alcohol: Men ≥14/wk, Women ≥7/wk; 0 = no, 1 = yes",
    "AnyHealthcare": "Have healthcare coverage? 0 = no, 1 = yes",
    "NoDocbcCost": "Needed doctor but couldn’t due to cost? 0 = no, 1 = yes",
    "GenHlth": "General health rating: 1=excellent, 5=poor",
    "MentHlth": "Days of poor mental health (0-30)",
    "PhysHlth": "Days of poor physical health (0-30)",
    "DiffWalk": "Difficulty walking/climbing stairs? 0 = no, 1 = yes",
    "Sex": "0 = female, 1 = male",
    "Age": "Age category: 1=18-24, ..., 13=80+",
    "Education": "Education level (1-6; 1 = never attended, 2 = elementary, etc.)",
    "Income": "Income level (1-8; 1 = < $10k, 5 = < $35k, 8 = ≥ $75k)"
}

# Automatically load the model from XGB_model.pkl
try:
    with open("XGB_model.pkl", "rb") as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")

# Create main window with a slightly smaller width and taller height.
root = tk.Tk()
root.title("Diabetes Prediction")
root.geometry("900x900")
root.configure(bg="#f4f4f4")

# Increase font sizes
LARGE_FONT = ("Arial", 16)
MEDIUM_FONT = ("Arial", 14)
SMALL_FONT = ("Arial", 12)

style = ttk.Style()
style.configure("TButton", font=MEDIUM_FONT, padding=5)
style.configure("TLabel", font=MEDIUM_FONT, background="#f4f4f4")
style.configure("TEntry", font=MEDIUM_FONT, padding=5)

# Main container frame
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Create two sub-frames for left and right columns
left_frame = ttk.Frame(main_frame, padding=10)
left_frame.grid(row=0, column=0, sticky="n")
right_frame = ttk.Frame(main_frame, padding=10)
right_frame.grid(row=0, column=1, sticky="n")

# Dictionary to hold entries
entries = {}

# Functions to handle placeholders
def clear_placeholder(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(foreground="black")

def restore_placeholder(event, entry, default_text):
    if not entry.get():
        entry.insert(0, default_text)
        entry.config(foreground="grey")

# Split features into two groups (left and right)
mid_index = (len(features) + 1) // 2  # Left gets one more if odd
left_features = features[:mid_index]
right_features = features[mid_index:]
left_defaults = default_values[:mid_index]
right_defaults = default_values[mid_index:]

# Create input fields for left side with descriptive texts
for i, (feature, default) in enumerate(zip(left_features, left_defaults)):
    ttk.Label(left_frame, text=f"{feature}:", font=MEDIUM_FONT).grid(row=i*2, column=0, sticky="e", padx=5, pady=4)
    entry = ttk.Entry(left_frame, width=10)
    entry.insert(0, str(default))
    entry.config(foreground="grey", font=MEDIUM_FONT)
    entry.bind("<FocusIn>", lambda event, e=entry, d=str(default): clear_placeholder(event, e, d))
    entry.bind("<FocusOut>", lambda event, e=entry, d=str(default): restore_placeholder(event, e, d))
    entry.grid(row=i*2, column=1, padx=5, pady=4)
    # Descriptive label below the entry
    desc = descriptions.get(feature, "")
    ttk.Label(left_frame, text=desc, font=SMALL_FONT, foreground="gray", background="#f4f4f4")\
        .grid(row=i*2+1, column=0, columnspan=2, sticky="w", padx=5)
    entries[feature] = entry

# Create input fields for right side with descriptive texts
for i, (feature, default) in enumerate(zip(right_features, right_defaults)):
    ttk.Label(right_frame, text=f"{feature}:", font=MEDIUM_FONT).grid(row=i*2, column=0, sticky="e", padx=5, pady=4)
    entry = ttk.Entry(right_frame, width=10)
    entry.insert(0, str(default))
    entry.config(foreground="grey", font=MEDIUM_FONT)
    entry.bind("<FocusIn>", lambda event, e=entry, d=str(default): clear_placeholder(event, e, d))
    entry.bind("<FocusOut>", lambda event, e=entry, d=str(default): restore_placeholder(event, e, d))
    entry.grid(row=i*2, column=1, padx=5, pady=4)
    # Descriptive label below the entry
    desc = descriptions.get(feature, "")
    ttk.Label(right_frame, text=desc, font=SMALL_FONT, foreground="gray", background="#f4f4f4")\
        .grid(row=i*2+1, column=0, columnspan=2, sticky="w", padx=5)
    entries[feature] = entry

# Prediction function
def predict():
    if model is None:
        messagebox.showerror("Error", "Model not loaded. Ensure 'XGB_model.pkl' is in the directory.")
        return

    try:
        # Gather input values with default fallback
        input_data = {}
        for feature, default in zip(features, default_values):
            value = entries[feature].get().strip()
            input_data[feature] = float(value) if value and value != str(default) else default

        df_input = pd.DataFrame([input_data])
        prediction = model.predict(df_input)[0]

        # Display result with color feedback using 'foreground'
        if prediction == 0:
            result_label.config(text="Non-Diabetic (0)", foreground="green", font=LARGE_FONT)
        else:
            result_label.config(text="Diabetic (1)", foreground="red", font=LARGE_FONT)
    except Exception as e:
        messagebox.showerror("Error", f"Prediction failed:\n{e}")

# Predict button frame (spanning both columns)
button_frame = ttk.Frame(main_frame, padding=10)
button_frame.grid(row=1, column=0, columnspan=2)
ttk.Button(button_frame, text="Predict", command=predict).pack(pady=10)

# Result label (spanning both columns)
result_label = ttk.Label(main_frame, text="Prediction: N/A", font=LARGE_FONT)
result_label.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
