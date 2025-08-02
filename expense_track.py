from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import pymysql
import datetime

# connecting to db
def connect_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="your_password", # Enter your mysql password here--
        port=3306,
        database="expense_db"
    )


# ==== Add Entry Function ====
def add_entry():
    amount = round(float(amount_entry.get()),2)
    category = category_combo.get()
    date = date_entry.get()
    desc = desc_entry.get()

    if not (amount and category and date and desc):
        tmsg.showerror("Input Error", "Please fill all fields")
        return

    # Checking date format

    try:
        formatted_date=datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")

        conn = connect_db()
        cursor = conn.cursor()
        if not tmsg.askyesno("Confirm", "Do you want to add this entry?"):
            return
        insert_sql = "insert into expenses(amount, category, date, description) values (%s,%s,%s,%s)"
        cursor.execute(insert_sql, (amount, category, formatted_date, desc))
        conn.commit()
        conn.close()

        tmsg.showinfo("Success", "Expense added successfully")
        load_data()  # Refresh table after adding new entry.
        clear_fields()

    except Exception as e:
        tmsg.showerror("Error", f"Something went wrong-\n{str(e)}")
        clear_fields()
        return


# fetching earlier data from db-
def load_data():
    for item in tree.get_children():  #-> for deleting selected entry through databae...
        tree.delete(item)

    conn = connect_db()
    cur = conn.cursor()
    #cur.execute("SELECT id,amount, category, date, description FROM expenses")  # id must include for
    cur.execute("SELECT * FROM expenses")                                                                       # successfully deleting entries.
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=(row[0],row[1],row[2],row[3],row[4]))
        # row[0] -> id (hidden) on GUI, we maintained it for deleting entry purpose.


# Clear all fields-
def clear_fields():
    amount_entry.delete(0, END)
    category_combo.set('')
    date_entry.delete(0, END)
    desc_entry.delete(0, END)
    amount_entry.focus()

# Deleting entry-
def delete_selected():
    selected = tree.focus()
    if not selected:
        tmsg.showwarning("Select Entry", "Please select a row to delete.")
        return

    confirm = tmsg.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
    if not confirm:
        return

    try:
        item = tree.item(selected)
        entry_id = item['values'][0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = %s", (entry_id,))
        conn.commit()
        conn.close()

        tree.delete(selected)
        tmsg.showinfo("Deleted", "Entry deleted successfully.")
    except Exception as e:
        tmsg.showerror("Error", f"Could not delete entry:\n{e}")

# GUI set-up
root = Tk()
root.title("Expense Tracker")
root.geometry("800x600")
root.iconbitmap("expense.ico")
root.configure(bg="#edf2f4")

# Heading
title = Label(root, text="💰 Expense Tracker", font=("Verdana", 22, "bold"), bg="#edf2f4", fg="#2b2d42")
title.pack(pady=20)

# Input Frame
input_frame = Frame(root, bg="#e8f0fe", bd=2, relief="ridge")
input_frame.pack(pady=10, padx=20, fill="x")

Label(input_frame, text="Amount:", font=("Calibri", 12,"bold"),  bg="#f0f8ff").grid(row=0, column=0, padx=130, pady=10, sticky=W)
amount_entry = Entry(input_frame, font=("Calibri", 12,"bold"),width=30)
amount_entry.grid(row=0, column=1, pady=10, padx=5)

Label(input_frame, text="Category:", font=("Calibri", 12,"bold"), bg="#f0f8ff").grid(row=1, column=0, padx=130, pady=10, sticky=W)
category_combo = ttk.Combobox(input_frame, values=["Food", "Travel", "Shopping", "Rent", "Other"],width=28, font=("Calibri", 12,"bold"))
category_combo.grid(row=1, column=1, pady=10, padx=5)

Label(input_frame, text="Date (DD-MM-YYYY):", font=("Calibri", 12,"bold"), bg="#f0f8ff").grid(row=2, column=0, padx=130, pady=10, sticky=W)
date_entry = Entry(input_frame, font=("Calibri", 12,"bold"),width=30)
date_entry.grid(row=2, column=1, pady=10, padx=5)

Label(input_frame, text="Description:", font=("Calibri", 12,"bold"), bg="#f0f8ff").grid(row=3, column=0, padx=130, pady=10, sticky=W)
desc_entry = Entry(input_frame, font=("Calibri", 12,"bold"),width=30)
desc_entry.grid(row=3, column=1, pady=10, padx=5)

# Add Button
add_btn = Button(input_frame, text="➕ Add Entry", bg="#4caf50", fg="white", font=("Arial", 12, "bold"), width=20, command=add_entry)
add_btn.grid(row=4, column=1, columnspan=2, pady=15)

# Treeview Frame
table_frame = Frame(root, bg="#edf2f4")
table_frame.pack(pady=20)


# Define columns
columns = ("ID","Amount", "Category", "Date", "Description")

# Basic Style
style = ttk.Style()
style.theme_use("default")

# Header styling: dark background, white text
style.configure("Treeview.Heading",
    font=("Calibri", 12, "bold"),
    background="#2b2d42",
    foreground="white"
)

# Table row styling: normal black text, white background, visible grid lines
style.configure("Treeview",
    font=("Arial", 11),
    background="white",
    foreground="black",
    rowheight=30,
    fieldbackground="white",
    bordercolor="black",
    borderwidth=1
)

# Treeview Widget
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

# Headings and column sizes
for col in columns:
    if col=="ID":  # -> so that id is hidden in GUI.
        tree.heading(col, text="")
        tree.column(col, width=0,stretch=False)
    else:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

tree.grid(row=0, column=0, padx=10, pady=10,sticky="nsew")

tree_scroll=Scrollbar(table_frame,orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scroll.set)
tree_scroll.grid(row=0, column=1, sticky="ns")

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# Delete button

delete_btn = Button(table_frame, text="Delete Entry", command=delete_selected, bg="#ff4d4d", fg="white",font=("Calibri", 12, "bold"), width=20)
delete_btn.grid(row=1,column=0, pady=5)

load_data()
root.mainloop()

