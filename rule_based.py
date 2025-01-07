class DiabetesIdentificationSystem:
    def __init__(self, fpg, ppbg, dbp, bmi, hba1c, rbs=None):
        self.fpg = fpg  # Fasting Plasma Glucose
        self.ppbg = ppbg  # Postprandial Blood Glucose
        self.dbp = dbp  # Diastolic Blood Pressure
        self.bmi = bmi  # Body Mass Index
        self.hba1c = hba1c  # HbA1c
        self.rbs = rbs  # Random Blood Sugar (optional)

    def identify(self):
        if self.is_normal():
            return "NORMAL"
        elif self.is_pre_diabetes():
            return "PRE-DIABETES"
        elif self.is_diabetes():
            return "DIABETES"
        else:
            return "UNDETERMINED"

    def is_normal(self):
        return (
            self.fpg <= 99 and
            self.ppbg <= 139 and
            self.dbp <= 80 and
            self.bmi <= 24 or
            self.hba1c <= 5.6
        )

    def is_pre_diabetes(self):
        return (
            100 <= self.fpg <= 125 and
            140 <= self.ppbg <= 199 and
            80 <= self.dbp <= 90 and
            25 <= self.bmi <= 29 or
            5.7 <= self.hba1c <= 6.4
        )

    def is_diabetes(self):
        return (
            self.fpg >= 125 and
            (self.ppbg >= 200 or (self.rbs is not None and self.rbs >= 200)) and
            self.dbp >= 90 and
            self.bmi >= 30 or
            self.hba1c >= 6.5
        )

def get_user_input():
    print("Please enter the following values for diabetes diagnosis:")
    
    while True:
        try:
            fpg = float(input("Fasting Plasma Glucose (FPG) in mg/dL: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    while True:
        try:
            ppbg = float(input("Postprandial Blood Glucose (PPBG) in mg/dL: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    while True:
        try:
            dbp = float(input("Diastolic Blood Pressure (DBP) in mmHg: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    while True:
        try:
            bmi = float(input("Body Mass Index (BMI): "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    while True:
        try:
            hba1c = float(input("HbA1c percentage: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    # Random Blood Sugar (optional)
    rbs = input("Random Blood Sugar (RBS) in mg/dL (Press Enter to skip): ")
    if rbs.strip() == "":
        rbs = None
    else:
        try:
            rbs = float(rbs)
        except ValueError:
            print("Invalid input for RBS. It will be set to None.")
            rbs = None

    return fpg, ppbg, dbp, bmi, hba1c, rbs


if __name__ == "__main__":
    fpg, ppbg, dbp, bmi, hba1c, rbs = get_user_input()
    print("\nInputs received:")
    print(f"FPG: {fpg} mg/dL")
    print(f"PPBG: {ppbg} mg/dL")
    print(f"DBP: {dbp} mmHg")
    print(f"BMI: {bmi}")
    print(f"HbA1c: {hba1c}%")
    print(f"RBS: {rbs if rbs is not None else 'Not provided'}")

    system = DiabetesIdentificationSystem(fpg, ppbg, dbp, bmi, hba1c, rbs)
    result = system.identify()
    print(f"Diagnosis: {result}")
