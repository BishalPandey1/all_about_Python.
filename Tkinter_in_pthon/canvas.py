import tkinter as tk

root = tk.Tk()
root.title("Canvas Shapes")

# Create a canvas
canvas = tk.Canvas(root, width=300, height=200, bg="green")
canvas.pack()

# Draw a line
canvas.create_line(20, 20, 200, 20, fill="blue", width=2)

# Draw a rectangle
canvas.create_rectangle(50, 50, 150, 100, fill="lightgreen")

# Draw a circle (using oval)
canvas.create_oval(180, 50, 250, 120, fill="pink")

# Draw a polygon (triangle)
canvas.create_polygon(100, 150, 150, 180, 50, 180, fill="yellow")

root.mainloop()
