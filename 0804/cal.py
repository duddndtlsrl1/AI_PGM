import tkinter as tk
from math import sqrt


# =============================
# 계산기 상태
# =============================

current = "0"
operand = None
operator = None
new_number = True

# 숫자 타입 정규화
def normalize_number(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)

# =============================
# 순수 계산 함수
# =============================

def perform_operation(a, b, op):
    if op == "+":
        return a + b

    elif op == "-":
        return a - b

    elif op == "×":
        return a * b

    elif op == "÷":
        if b == 0:
            raise ZeroDivisionError

        return a / b


# =============================
# 화면 갱신
# =============================

def update():
    display.config(text=current)

    if operand is None or operator is None:
        history.config(text="")
    else:
        history.config(
            text=f"{operand:g} {operator}"
        )


# =============================
# 숫자 입력
# =============================

def number(n):
    global current, new_number

    if new_number:
        current = str(n)
        new_number = False

    else:
        if current == "0":
            current = str(n)
        else:
            current += str(n)

    update()


# =============================
# 소수점
# =============================

def dot():
    global current, new_number

    if new_number:
        current = "0."
        new_number = False

    elif "." not in current:
        current += "."

    update()


# =============================
# 연산자 입력
# =============================

def operation(op):
    global operand, operator, current, new_number

    # 이미 계산할 숫자가 있는 경우만 계산
    if operand is None:
        operand = float(current)

    elif not new_number:
        operand = perform_operation(
            operand,
            float(current),
            operator
        )

        current = normalize_number(operand)

    # 새로운 연산자 저장
    operator = op
    new_number = True

    update()


# =============================
# = 버튼
# =============================

def calculate():
    global operand, operator, current, new_number

    if operand is None or operator is None:
        return

    try:
        result = perform_operation(
            operand,
            float(current),
            operator
        )

        current = normalize_number(result)

        if current.endswith(".0"):
            current = current[:-2]

        operand = None
        operator = None
        new_number = True

        update()

    except ZeroDivisionError:
        current = "Error"

        operand = None
        operator = None
        new_number = True

        update()


# =============================
# Clear
# =============================

def clear():
    global current, operand, operator, new_number

    current = "0"
    operand = None
    operator = None
    new_number = True

    update()


# =============================
# Backspace
# =============================

def backspace():
    global current

    if len(current) > 1:
        current = current[:-1]

    else:
        current = "0"

    update()


# =============================
# ±
# =============================

def sign():
    global current

    if current != "0":

        if current.startswith("-"):
            current = current[1:]

        else:
            current = "-" + current

    update()


# =============================
# %
# =============================

def percent():
    global current

    current= normalize_number(float(current)/100)

    update()


# =============================
# 제곱
# =============================

def square():
    global current

    current= normalize_number(float(current)**2)

    update()


# =============================
# 루트
# =============================

def root():
    global current

    value = float(current)

    if value < 0:
        current = "Error"

    else:
        current= normalize_number(sqrt(value))

    update()


# =============================
# 역수
# =============================

def inverse():
    global current

    value = float(current)

    if value == 0:
        current = "Error"

    else:
        current= normalize_number(1/value)

    update()



# =============================
# GUI
# =============================

window = tk.Tk()

window.title("Calculator")
window.geometry("380x600")
window.configure(bg="#202020")
window.resizable(False, False)


for i in range(4):
    window.grid_columnconfigure(i, weight=1)

for i in range(8):
    window.grid_rowconfigure(i, weight=1)



history = tk.Label(
    window,
    text="",
    anchor="e",
    bg="#202020",
    fg="#AAAAAA",
    font=("Segoe UI", 14)
)

history.grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="nsew"
)


display = tk.Label(
    window,
    text="0",
    anchor="e",
    bg="#202020",
    fg="white",
    font=("Segoe UI", 32)
)

display.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="nsew"
)



def create_button(text, row, col, command):

    tk.Button(
        window,
        text=text,
        command=command,
        bg="#303030",
        fg="white",
        font=("Segoe UI", 14),
        bd=0
    ).grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=1,
        pady=1
    )


# 버튼 배치

buttons = [
    ("%", percent, 2,0),
    ("CE", clear, 2,1),
    ("C", clear, 2,2),
    ("⌫", backspace, 2,3),

    ("1/x", inverse, 3,0),
    ("x²", square, 3,1),
    ("√x", root, 3,2),
    ("÷", lambda:operation("÷"), 3,3),

    ("7", lambda:number(7), 4,0),
    ("8", lambda:number(8), 4,1),
    ("9", lambda:number(9), 4,2),
    ("×", lambda:operation("×"), 4,3),

    ("4", lambda:number(4), 5,0),
    ("5", lambda:number(5), 5,1),
    ("6", lambda:number(6), 5,2),
    ("-", lambda:operation("-"), 5,3),

    ("1", lambda:number(1), 6,0),
    ("2", lambda:number(2), 6,1),
    ("3", lambda:number(3), 6,2),
    ("+", lambda:operation("+"), 6,3),

    ("±", sign, 7,0),
    ("0", lambda:number(0), 7,1),
    (".", dot, 7,2),
    ("=", calculate, 7,3),
]


for text, cmd, row, col in buttons:
    create_button(text, row, col, cmd)


update()

window.mainloop()