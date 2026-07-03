import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class CalorieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker App")
        self.root.geometry("650x550")
        self.root.configure(bg="#f5f5f5")
        
        # Track targeted selection ID for updates
        self.selected_record_id = None
        
        # Connect to Database
        self.connect_db()
        
        # UI Component Styles
        style = ttk.Style()
        style.theme_use("clam")
        
        # --- INPUT FRAME ---
        input_frame = ttk.LabelFrame(root, text=" Food Entry Form ", padding=15)
        input_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(input_frame, text="Food Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.food_entry = ttk.Entry(input_frame, width=22)
        self.food_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Calories:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.calorie_entry = ttk.Entry(input_frame, width=12)
        self.calorie_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Action Layout inside Form
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Entry", command=self.add_entry)
        self.add_btn.pack(side="left", padx=5)
        
        self.update_btn = ttk.Button(btn_frame, text="Update Entry", command=self.update_entry, state="disabled")
        self.update_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Clear Fields", command=self.clear_fields)
        clear_btn.pack(side="left", padx=5)

        # --- DATA DISPLAY (TREEVIEW) ---
        table_frame = ttk.Frame(root, padding=15)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("id", "food", "calories", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("food", text="Food Item")
        self.tree.heading("calories", text="Calories (kcal)")
        self.tree.heading("date", text="Date Logged")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("food", width=250, anchor="w")
        self.tree.column("calories", width=120, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind row selection to load data into entries
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        
        # --- ACTION FRAME ---
        action_frame = ttk.Frame(root, padding=10)
        action_frame.pack(fill="x")
        
        delete_btn = ttk.Button(action_frame, text="Delete Selected Entry", command=self.delete_entry)
        delete_btn.pack(side="right", padx=15, pady=5)
        
        # Refresh table with existing data on startup
        self.fetch_data()

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="caloryapp",
                user="postgres",
                password="admin"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
            self.root.destroy()

    def fetch_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            self.cursor.execute("SELECT id, food_name, calorie_count, date_added FROM calories ORDER BY id DESC;")
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve data:\n{e}")

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
            
        item_values = self.tree.item(selected_item, "values")
        self.selected_record_id = item_values[0]
        
        # Load values into Entry fields
        self.food_entry.delete(0, tk.END)
        self.food_entry.insert(0, item_values[1])
        
        self.calorie_entry.delete(0, tk.END)
        self.calorie_entry.insert(0, item_values[2])
        
        # Switch button status state
        self.add_btn.configure(state="disabled")
        self.update_btn.configure(state="normal")

    def clear_fields(self):
        self.food_entry.delete(0, tk.END)
        self.calorie_entry.delete(0, tk.END)
        self.selected_record_id = None
        self.tree.selection_remove(self.tree.selection()) # Unhighlight row
        
        # Restore button layout states
        self.add_btn.configure(state="normal")
        self.update_btn.configure(state="disabled")

    def add_entry(self):
        food = self.food_entry.get().strip()
        calories = self.calorie_entry.get().strip()
        
        if not food or not calories:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        if not calories.isdigit():
            messagebox.showwarning("Input Error", "Calorie count must be a valid whole number.")
            return
            
        try:
            self.cursor.execute(
                "INSERT INTO calories (food_name, calorie_count) VALUES (%s, %s);",
                (food, int(calories))
            )
            self.conn.commit()
            self.clear_fields()
            self.fetch_data()
            messagebox.showinfo("Success", "Food entry saved successfully!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Database Error", f"Could not save entry:\n{e}")

    def update_entry(self):
        if not self.selected_record_id:
            messagebox.showwarning("Selection Error", "No entry targeted for update.")
            return
            
        food = self.food_entry.get().strip()
        calories = self.calorie_entry.get().strip()
        
        if not food or not calories:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        if not calories.isdigit():
            messagebox.showwarning("Input Error", "Calorie count must be a valid whole number.")
            return
            
        try:
            self.cursor.execute(
                "UPDATE calories SET food_name = %s, calorie_count = %s WHERE id = %s;",
                (food, int(calories), self.selected_record_id)
            )
            self.conn.commit()
            self.clear_fields()
            self.fetch_data()
            messagebox.showinfo("Success", "Entry updated successfully!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Database Error", f"Could not update entry:\n{e}")

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an entry from the list to delete.")
            return
            
        item_values = self.tree.item(selected_item, "values")
        record_id = item_values[0]
        food_name = item_values[1]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{food_name}'?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM calories WHERE id = %s;", (record_id,))
                self.conn.commit()
                self.clear_fields()
                self.fetch_data()
                messagebox.showinfo("Success", "Entry deleted successfully.")
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Database Error", f"Could not delete entry:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieApp(root)
    root.mainloop()