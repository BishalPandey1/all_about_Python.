import tkinter as tk


root = tk.Tk()
root.title("Widgets Example")

label = tk.Label(root, text="Type something below:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Show Text", command=show_text)
button.pack()

root.mainloop()
