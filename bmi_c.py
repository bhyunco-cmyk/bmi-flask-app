def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "과체중"
    else:
        return "비만"

if __name__ == "__main__":
    height = float(input("키를 입력하세요 (cm): "))
    weight = float(input("몸무게를 입력하세요 (kg): "))

    bmi = calculate_bmi(height, weight)
    category = get_bmi_category(bmi)

    print(f"\nBMI: {bmi}")
    print(f"판정: {category}")
