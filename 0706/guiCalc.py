import tkinter as tk

root = tk.Tk()
root.title("계산기")
root.geometry("350x500")

# 창 크기 변경 시 버튼도 함께 확대
for i in range(5):
    root.rowconfigure(i + 1, weight=1)
for i in range(4):
    root.columnconfigure(i, weight=1)

expression = tk.StringVar()


def press(value):
    expression.set(expression.get() + value)


def clear():
    expression.set("")


def backspace():
    expression.set(expression.get()[:-1])


def calculate():
    try:
        exp = (
            expression.get()
            .replace("×", "*")
            .replace("÷", "/")
        )
        result = eval(exp)
        expression.set(str(result))
    except Exception:
        expression.set("Error")


display = tk.Entry(
    root,
    textvariable=expression,
    font=("Arial", 24),
    justify="right"
)
display.grid(row=0, column=0, columnspan=4,
             sticky="nsew", padx=5, pady=5)

buttons = [
    ["C", "←", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""]
]

for r, row in enumerate(buttons, start=1):
    for c, text in enumerate(row):

        if text == "":
            continue

        if text == "=":
            cmd = calculate
        elif text == "C":
            cmd = clear
        elif text == "←":
            cmd = backspace
        else:
            cmd = lambda t=text: press(t)

        btn = tk.Button(
            root,
            text=text,
            font=("Arial", 18),
            command=cmd
        )

        # 0 버튼을 두 칸 차지하게
        if r == 5 and c == 0:
            btn.grid(row=r, column=c, columnspan=2,
                     sticky="nsew", padx=2, pady=2)
        elif r == 5 and c == 1:
            continue
        else:
            col = c if r != 5 or c < 2 else c + 1
            btn.grid(row=r, column=col,
                     sticky="nsew", padx=2, pady=2)

root.mainloop()