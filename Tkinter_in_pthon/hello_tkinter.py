import tkinter as tk
root = tk.Tk()
root.title("Hello you mero ho")
lable = tk.Label(root, text = "dsfj asldfj alsdkfjasdkl fjadslkf jadslkfj alsfjaldskfjads lfj ")
lable.pack()
button = tk.Button(root, text="Katta " , command=root.destroy)
button.pack()
root.mainloop()
