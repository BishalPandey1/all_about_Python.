import tkinter as tk

def update_label():
    label.config(text="Button Clicked!")

# Create the main window
root = tk.Tk()
root.title("Simple GUI Practice")

# Create a label
label = tk.Label(root, text="Click the button", font=("Arial", 14))
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click Me", command=update_label)
button.pack(pady=5)

# Run the application
root.mainloop()
