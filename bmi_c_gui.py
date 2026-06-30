import tkinter as tk
from tkinter import messagebox


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


def on_calculate():
    try:
        height = float(entry_height.get())
        weight = float(entry_weight.get())

        if height <= 0 or weight <= 0:
            messagebox.showerror("입력 오류", "키와 몸무게는 0보다 커야 합니다.")
            return

        bmi = calculate_bmi(height, weight)
        category, color = get_bmi_category(bmi)

        label_bmi_value.config(text=f"{bmi}", fg=color)
        label_category_value.config(text=category, fg=color)
        frame_result.config(highlightbackground=color)

    except ValueError:
        messagebox.showerror("입력 오류", "숫자를 올바르게 입력해주세요.")


def on_reset():
    entry_height.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    label_bmi_value.config(text="-", fg="#555555")
    label_category_value.config(text="-", fg="#555555")
    frame_result.config(highlightbackground="#cccccc")
    entry_height.focus()


# 메인 윈도우
root = tk.Tk()
root.title("BMI 계산기")
root.geometry("380x460")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

# 타이틀
label_title = tk.Label(root, text="BMI 계산기", font=("맑은 고딕", 20, "bold"),
                       bg="#f5f5f5", fg="#2c3e50")
label_title.pack(pady=(30, 20))

# 입력 프레임
frame_input = tk.Frame(root, bg="#ffffff", bd=0, highlightthickness=1,
                       highlightbackground="#dddddd")
frame_input.pack(padx=30, fill="x")

# 키 입력
row_height = tk.Frame(frame_input, bg="#ffffff")
row_height.pack(fill="x", padx=20, pady=(20, 10))
tk.Label(row_height, text="키", font=("맑은 고딕", 12), bg="#ffffff",
         fg="#555555", width=6, anchor="w").pack(side="left")
entry_height = tk.Entry(row_height, font=("맑은 고딕", 12), width=12,
                        bd=1, relief="solid", justify="center")
entry_height.pack(side="left", padx=(0, 8))
tk.Label(row_height, text="cm", font=("맑은 고딕", 12), bg="#ffffff",
         fg="#888888").pack(side="left")

# 몸무게 입력
row_weight = tk.Frame(frame_input, bg="#ffffff")
row_weight.pack(fill="x", padx=20, pady=(0, 20))
tk.Label(row_weight, text="몸무게", font=("맑은 고딕", 12), bg="#ffffff",
         fg="#555555", width=6, anchor="w").pack(side="left")
entry_weight = tk.Entry(row_weight, font=("맑은 고딕", 12), width=12,
                        bd=1, relief="solid", justify="center")
entry_weight.pack(side="left", padx=(0, 8))
tk.Label(row_weight, text="kg", font=("맑은 고딕", 12), bg="#ffffff",
         fg="#888888").pack(side="left")

# 버튼
frame_buttons = tk.Frame(root, bg="#f5f5f5")
frame_buttons.pack(pady=16)

btn_calc = tk.Button(frame_buttons, text="계산하기", font=("맑은 고딕", 12, "bold"),
                     bg="#2c3e50", fg="white", width=10, height=1,
                     bd=0, cursor="hand2", command=on_calculate)
btn_calc.pack(side="left", padx=6)

btn_reset = tk.Button(frame_buttons, text="초기화", font=("맑은 고딕", 12),
                      bg="#95a5a6", fg="white", width=8, height=1,
                      bd=0, cursor="hand2", command=on_reset)
btn_reset.pack(side="left", padx=6)

# 결과 프레임
frame_result = tk.Frame(root, bg="#ffffff", bd=0, highlightthickness=2,
                        highlightbackground="#cccccc")
frame_result.pack(padx=30, fill="x")

tk.Label(frame_result, text="BMI 수치", font=("맑은 고딕", 10),
         bg="#ffffff", fg="#888888").pack(pady=(16, 2))
label_bmi_value = tk.Label(frame_result, text="-", font=("맑은 고딕", 32, "bold"),
                            bg="#ffffff", fg="#555555")
label_bmi_value.pack()

tk.Label(frame_result, text="판정", font=("맑은 고딕", 10),
         bg="#ffffff", fg="#888888").pack(pady=(10, 2))
label_category_value = tk.Label(frame_result, text="-", font=("맑은 고딕", 18, "bold"),
                                 bg="#ffffff", fg="#555555")
label_category_value.pack(pady=(0, 16))

# 기준표
frame_guide = tk.Frame(root, bg="#f5f5f5")
frame_guide.pack(pady=14)

guide_items = [
    ("● 저체중", "~ 18.4", "#3498db"),
    ("● 정상",   "18.5 ~ 22.9", "#2ecc71"),
    ("● 과체중", "23.0 ~ 24.9", "#f39c12"),
    ("● 비만",   "25.0 ~", "#e74c3c"),
]
for label_text, range_text, color in guide_items:
    row = tk.Frame(frame_guide, bg="#f5f5f5")
    row.pack(anchor="w")
    tk.Label(row, text=label_text, font=("맑은 고딕", 10), bg="#f5f5f5",
             fg=color, width=8, anchor="w").pack(side="left")
    tk.Label(row, text=range_text, font=("맑은 고딕", 10), bg="#f5f5f5",
             fg="#888888").pack(side="left")

entry_height.focus()
root.mainloop()
