import os
import tkinter as tk
from tkinter import messagebox

def remove_student():
    selected_name = listbox.get(tk.ACTIVE)
    if not selected_name:
        messagebox.showwarning("No Selection", "Please select a student to remove.")
        return

    file_path = os.path.join("data", f"{selected_name}.png")
    try:
        os.remove(file_path)
        messagebox.showinfo("Success", f"Removed {selected_name} successfully.")
        listbox.delete(tk.ACTIVE)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No image found for {selected_name}.")

# GUI Setup
root = tk.Tk()
root.title("Remove Student")

label = tk.Label(root, text="Select a student to remove:")
label.pack(pady=10)

listbox = tk.Listbox(root, width=40)
listbox.pack(padx=10, pady=10)

# Load names from data/ folder
data_folder = "data"
student_names = [f[:-4] for f in os.listdir(data_folder) if f.endswith(".png")]
for name in student_names:
    listbox.insert(tk.END, name)

remove_button = tk.Button(root, text="Remove", command=remove_student)
remove_button.pack(pady=10)

root.mainloop()
