import tkinter as tk

# =============================================================================
# STEP 1: Create the main window
# =============================================================================
root = tk.Tk()
root.title("Simple Tkinter Demo")   # Title shown in the window title bar
root.geometry("500x400")            # Width x Height of the window

# =============================================================================
# STEP 2: Add a Label (text that is displayed but cannot be edited)
# =============================================================================
label = tk.Label(root, text="Hello! This is a Label widget.")
label.pack(pady=10)                 # pady adds vertical spacing around it

# =============================================================================
# STEP 3: Add an Entry (a text field where the user can type)
# =============================================================================
entry = tk.Entry(root, width=40)    # width = visible character count
entry.pack(pady=10)
entry.insert(0, "Type something here...")  # Default placeholder text

# =============================================================================
# STEP 4: Functions that run when buttons are clicked
# =============================================================================
def on_click():
    """Read text from entry and update the label with it."""
    user_text = entry.get()                 # Get whatever user typed
    label.configure(text=f"You typed: {user_text}")  # Change label text

def clear_text():
    """Clear the entry field and reset the label."""
    entry.delete(0, tk.END)                 # Remove all text from entry
    label.configure(text="Cleared! Type again.")  # Reset label

# =============================================================================
# STEP 5: Add Buttons (clickable elements that run a function)
# =============================================================================
click_btn = tk.Button(root, text="Show Text", command=on_click)
click_btn.pack(pady=5)

clear_btn = tk.Button(root, text="Clear", command=clear_text)
clear_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.destroy)
exit_btn.pack(pady=5)

# =============================================================================
# STEP 6: Start the app (keeps the window open)
# =============================================================================
root.mainloop()
