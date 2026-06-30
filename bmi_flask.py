from flask import Flask, render_template, request

app = Flask(__name__)


def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "저체중", "#3498db"
    elif bmi < 23:
        return "정상", "#2ecc71"
    elif bmi < 25:
        return "과체중", "#f39c12"
    else:
        return "비만", "#e74c3c"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            height = float(request.form["height"])
            weight = float(request.form["weight"])

            if height <= 0 or weight <= 0:
                error = "키와 몸무게는 0보다 커야 합니다."
            else:
                bmi = calculate_bmi(height, weight)
                category, color = get_bmi_category(bmi)
                result = {"bmi": bmi, "category": category, "color": color,
                          "height": height, "weight": weight}
        except ValueError:
            error = "숫자를 올바르게 입력해주세요."

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
