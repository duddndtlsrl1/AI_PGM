import tkinter as tk
from tkinter import filedialog, messagebox
import os

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("제목 없음 - 메모장")
        self.root.geometry("800x600")

        self.file_path = None

        # -------------------
        # Text Area + Scroll
        # -------------------
        self.text_area = tk.Text(root, undo=True, wrap="word")
        self.text_area.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

        # -------------------
        # Menu
        # -------------------
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="파일", menu=self.file_menu)

        self.file_menu.add_command(label="새로 만들기", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="열기", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="저장", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="다른 이름으로 저장", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="종료", command=root.quit)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="편집", menu=self.edit_menu)

        self.edit_menu.add_command(label="되돌리기", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="잘라내기", command=lambda: self.root.focus_get().event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="복사", command=lambda: self.root.focus_get().event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="붙여넣기", command=lambda: self.root.focus_get().event_generate("<<Paste>>"))

        # -------------------
        # Status Bar
        # -------------------
        self.status = tk.StringVar()
        self.status.set("준비됨")

        self.status_bar = tk.Label(root, textvariable=self.status, anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        # -------------------
        # Shortcuts
        # -------------------
        root.bind("<Control-n>", lambda e: self.new_file())
        root.bind("<Control-o>", lambda e: self.open_file())
        root.bind("<Control-s>", lambda e: self.save_file())

        # Text change tracking
        self.text_area.bind("<KeyRelease>", self.update_status)

    # -------------------
    # File Functions
    # -------------------
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("제목 없음 - 메모장")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())

            self.file_path = path
            self.root.title(f"{os.path.basename(path)} - 메모장")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, tk.END))

            self.file_path = path
            self.root.title(f"{os.path.basename(path)} - 메모장")

    # -------------------
    # Status
    # -------------------
    def update_status(self, event=None):
        text = self.text_area.get(1.0, tk.END)
        chars = len(text) - 1
        lines = text.count("\n")
        self.status.set(f"글자 수: {chars} | 줄 수: {lines}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()