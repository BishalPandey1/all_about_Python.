import tkinter as tk
from tkinter import messagebox
import math

class SquareRootCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Root Calculator")

        self.entry = tk.Entry(root, font=("Arial", 18), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4)

        self.button_sqrt = tk.Button(root, text="Calculate Square Root", command=self.calculate_sqrt)
        self.button_sqrt.grid(row=1, column=0, columnspan=4)

        self.label_result = tk.Label(root, text="")
        self.label_result.grid(row=2, column=0, columnspan=4)

    def calculate_sqrt(self):
        try:
            user_input = float(self.entry.get())

            result = math.sqrt(user_input)

            self.label_result.config(text=f"Square root of {user_input:.2f} is {result:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareRootCalculator(root)
    root.mainloop()
