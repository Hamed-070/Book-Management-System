import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import uuid

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x600")

        # Set modern dark theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#1e3a8a", foreground="white", padding=10, font=("Arial", 10))
        #style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Arial",  HXadd_page(self):self.add_page())
        style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Arial", 10))
        style.configure("TEntry", fieldbackground="#2a2a3a", foreground="white", insertcolor="white")
        style.configure("TFrame", background="#1e1e2e")
        style.map("TButton", background=[("active", "#3b82f6")])
        self.root.configure(bg="#1e1e2e")

        # CSV file path
        self.csv_file = "./storage.csv"
        self.create_csv()

        # Sidebar menu
        self.sidebar = ttk.Frame(root, width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)
        self.sidebar.configure(style="TFrame")

        # Main content area
        self.container = ttk.Frame(root)
        self.container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Sidebar buttons
        self.buttons = [
            ("Add Book", self.show_add_page),
            ("Show Books", self.show_books_page),
            ("Search Book", self.show_search_page),
            ("Edit Book", self.show_edit_page),
            ("Delete Book", self.show_delete_page),
            ("Refresh All", self.refresh_all_pages)
        ]

        for text, command in self.buttons:
            btn = ttk.Button(self.sidebar, text=text, command=command, width=20)
            btn.pack(pady=10, padx=10, fill="x")

        # Create frames for each page
        self.frames = {}
        for page_name in ("add", "show", "search", "edit", "delete"):
            frame = ttk.Frame(self.container)
            self.frames[page_name] = frame
            frame.pack(fill="both", expand=True)

        # Initialize pages
        self.create_add_page()
        self.create_show_page()
        self.create_search_page()
        self.create_edit_page()
        self.create_delete_page()

        # Show default page
        self.show_add_page()

    def create_csv(self):
        if not os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Title", "Author", "Year", "ISBN", "Price"])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")

    def hide_all_frames(self):
        for frame in self.frames.values():
            frame.pack_forget()

    def refresh_all_pages(self):
        # Clear all input fields
        for entry in getattr(self, "add_entries", {}).values():
            entry.delete(0, tk.END)
        for entry in getattr(self, "search_entries", {}).values():
            entry.delete(0, tk.END)
        for entry in getattr(self, "edit_entries", {}).values():
            entry.delete(0, tk.END)
        
        # Clear listboxes
        if hasattr(self, "edit_listbox"):
            self.edit_listbox.delete(0, tk.END)
        if hasattr(self, "delete_listbox"):
            self.delete_listbox.delete(0, tk.END)
        
        # Clear search results
        for widget in getattr(self, "search_frame", tk.Frame()).winfo_children():
            widget.destroy()
        
        # Refresh book displays
        self.display_books()
        self.display_books_for_edit()
        self.display_books_for_delete()
        messagebox.showinfo("Success", "All pages refreshed!")

    def show_add_page(self):
        self.hide_all_frames()
        self.frames["add"].pack(fill="both", expand=True)

    def show_books_page(self):
        self.hide_all_frames()
        self.frames["show"].pack(fill="both", expand=True)
        self.display_books()

    def show_search_page(self):
        self.hide_all_frames()
        self.frames["search"].pack(fill="both", expand=True)

    def show_edit_page(self):
        self.hide_all_frames()
        self.frames["edit"].pack(fill="both", expand=True)
        self.display_books_for_edit()

    def show_delete_page(self):
        self.hide_all_frames()
        self.frames["delete"].pack(fill="both", expand=True)
        self.display_books_for_delete()

    def create_add_page(self):
        frame = self.frames["add"]
        ttk.Label(frame, text="Add a New Book", font=("Arial", 16, "bold")).pack(pady=10)

        fields = ["Title", "Author", "Year", "ISBN", "Price"]
        self.add_entries = {}
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10, padx=20, fill="x")

        for field in fields:
            row = ttk.Frame(input_frame)
            row.pack(pady=5, fill="x")
            ttk.Label(row, text=f"{field}:", width=12, anchor="w").pack(side="left")
            entry = ttk.Entry(row, width=30)
            entry.pack(side="left", padx=5, fill="x", expand=True)
            self.add_entries[field.lower()] = entry

        ttk.Button(frame, text="Add Book", command=self.add_book).pack(pady=20)

    def add_book(self):
        title = self.add_entries["title"].get().strip()
        author = self.add_entries["author"].get().strip()
        year = self.add_entries["year"].get().strip()
        isbn = self.add_entries["isbn"].get().strip()
        price = self.add_entries["price"].get().strip()

        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required!")
            return

        try:
            year = str(int(year)) if year else ""
            price = str(float(price)) if price else ""
            book_id = str(uuid.uuid4())[:8]  # Generate unique ID

            with open(self.csv_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([book_id, title, author, year, isbn, price])
            messagebox.showinfo("Success", "Book added successfully!")
            for entry in self.add_entries.values():
                entry.delete(0, tk.END)
            self.display_books()
            self.display_books_for_edit()
            self.display_books_for_delete()
        except ValueError:
            messagebox.showerror("Error", "Year must be a valid integer and Price must be a valid number!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_show_page(self):
        frame = self.frames["show"]
        ttk.Label(frame, text="All Books", font=("Arial", 16, "bold")).pack(pady=10)
        self.books_canvas = tk.Canvas(frame, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.books_canvas.yview)
        self.books_frame = ttk.Frame(self.books_canvas)
        
        # Bind canvas resizing
        self.books_canvas.bind("<Configure>", lambda e: self.books_canvas.configure(scrollregion=self.books_canvas.bbox("all")))
        self.books_frame.bind("<Configure>", lambda e: self.books_canvas.configure(scrollregion=self.books_canvas.bbox("all")))
        
        self.books_canvas.create_window((0, 0), window=self.books_frame, anchor="nw")
        self.books_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.books_canvas.pack(pady=10, padx=10, fill="both", expand=True)

    def display_books(self):
        for widget in self.books_frame.winfo_children():
            widget.destroy()

        try:
            if not os.path.exists(self.csv_file):
                ttk.Label(self.books_frame, text="No books found.", font=("Arial", 10)).pack(pady=5)
                return

            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header
                if not header:
                    return
                for row in reader:
                    if len(row) < 6:
                        continue
                    book_frame = ttk.Frame(self.books_frame)
                    book_frame.pack(pady=5, padx=10, fill="x")
                    book_info = f"ID: {row[0]}\nTitle: {row[1]}\nAuthor: {row[2]}\nYear: {row[3] if row[3] else 'N/A'}\nISBN: {row[4] if row[4] else 'N/A'}\nPrice: ${row[5] if row[5] else 'N/A'}"
                    ttk.Label(book_frame, text=book_info, font=("Arial", 10), wraplength=600, justify="left").pack(anchor="w", padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying books: {str(e)}")

    def create_search_page(self):
        frame = self.frames["search"]
        ttk.Label(frame, text="Search Books", font=("Arial", 16, "bold")).pack(pady=10)

        fields = ["Title", "Author", "Year", "ISBN", "Min Price", "Max Price"]
        self.search_entries = {}
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10, padx=20, fill="x")

        for field in fields:
            row = ttk.Frame(input_frame)
            row.pack(pady=5, fill="x")
            ttk.Label(row, text=f"{field}:", width=12, anchor="w").pack(side="left")
            entry = ttk.Entry(row, width=30)
            entry.pack(side="left", padx=5, fill="x", expand=True)
            self.search_entries[field.lower().replace(" ", "_")] = entry

        ttk.Button(frame, text="Search", command=self.search_book).pack(pady=10)
        self.search_canvas = tk.Canvas(frame, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.search_canvas.yview)
        self.search_frame = ttk.Frame(self.search_canvas)
        
        self.search_frame.bind("<Configure>", lambda e: self.search_canvas.configure(scrollregion=self.search_canvas.bbox("all")))
        self.search_canvas.create_window((0, 0), window=self.search_frame, anchor="nw")
        self.search_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.search_canvas.pack(pady=10, padx=10, fill="both", expand=True)

    def search_book(self):
        for widget in self.search_frame.winfo_children():
            widget.destroy()

        title = self.search_entries["title"].get().strip().lower()
        author = self.search_entries["author"].get().strip().lower()
        year = self.search_entries["year"].get().strip()
        isbn = self.search_entries["isbn"].get().strip()
        min_price = self.search_entries["min_price"].get().strip()
        max_price = self.search_entries["max_price"].get().strip()

        try:
            if not os.path.exists(self.csv_file):
                ttk.Label(self.search_frame, text="No books found.", font=("Arial", 10)).pack(pady=5)
                return

            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                found_books = False
                for row in reader:
                    if len(row) < 6:
                        continue
                    matches = (
                        (not title or title in row[1].lower()) and
                        (not author or author in row[2].lower()) and
                        (not year or (row[3] and year == row[3])) and
                        (not isbn or isbn in row[4]) and
                        (not min_price or (row[5] and float(row[5]) >= float(min_price))) and
                        (not max_price or (row[5] and float(row[5]) <= float(max_price)))
                    )
                    if matches:
                        found_books = True
                        book_frame = ttk.Frame(self.search_frame)
                        book_frame.pack(pady=5, padx=10, fill="x")
                        book_info = f"ID: {row[0]}\nTitle: {row[1]}\nAuthor: {row[2]}\nYear: {row[3] if row[3] else 'N/A'}\nISBN: {row[4] if row[4] else 'N/A'}\nPrice: ${row[5] if row[5] else 'N/A'}"
                        ttk.Label(book_frame, text=book_info, font=("Arial", 10), wraplength=600, justify="left").pack(anchor="w", padx=5)
                if not found_books:
                    ttk.Label(self.search_frame, text="No books match the search criteria.", font=("Arial", 10)).pack(pady=5)
        except ValueError:
            messagebox.showerror("Error", "Year and Price must be valid numbers!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

    def create_edit_page(self):
        frame = self.frames["edit"]
        ttk.Label(frame, text="Edit Book", font=("Arial", 16, "bold")).pack(pady=10)
        self.edit_listbox = tk.Listbox(frame, height=10, width=80, bg="#2a2a3a", fg="white", font=("Arial", 10), selectmode=tk.SINGLE)
        self.edit_listbox.pack(pady=10, padx=10, fill="both", expand=True)
        self.edit_listbox.bind("<<ListboxSelect>>", self.load_book_to_edit)

        fields = ["Title", "Author", "Year", "ISBN", "Price"]
        self.edit_entries = {}
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10, padx=20, fill="x")

        for field in fields:
            row = ttk.Frame(input_frame)
            row.pack(pady=5, fill="x")
            ttk.Label(row, text=f"{field}:", width=12, anchor="w").pack(side="left")
            entry = ttk.Entry(row, width=30)
            entry.pack(side="left", padx=5, fill="x", expand=True)
            self.edit_entries[field.lower()] = entry

        ttk.Button(frame, text="Update Book", command=self.update_book).pack(pady=20)
        self.selected_book_id = None

    def display_books_for_edit(self):
        self.edit_listbox.delete(0, tk.END)
        try:
            if not os.path.exists(self.csv_file):
                self.edit_listbox.insert(tk.END, "No books available.")
                return

            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) < 6:
                        continue
                    book_info = f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Year: {row[3] if row[3] else 'N/A'} | ISBN: {row[4] if row[4] else 'N/A'} | Price: ${row[5] if row[5] else 'N/A'}"
                    self.edit_listbox.insert(tk.END, book_info)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading books: {str(e)}")

    def load_book_to_edit(self, event):
        selection = self.edit_listbox.curselection()
        if not selection:
            return
        selected = self.edit_listbox.get(selection[0])
        self.selected_book_id = selected.split("|")[0].replace("ID:", "").strip()

        try:
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) < 6:
                        continue
                    if row[0] == self.selected_book_id:
                        for field in self.edit_entries.values():
                            field.delete(0, tk.END)
                        self.edit_entries["title"].insert(0, row[1])
                        self.edit_entries["author"].insert(0, row[2])
                        self.edit_entries["year"].insert(0, row[3])
                        self.edit_entries["isbn"].insert(0, row[4])
                        self.edit_entries["price"].insert(0, row[5])
                        break
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading book details: {str(e)}")

    def update_book(self):
        if not self.selected_book_id:
            messagebox.showerror("Error", "Please select a book to edit!")
            return

        title = self.edit_entries["title"].get().strip()
        author = self.edit_entries["author"].get().strip()
        year = self.edit_entries["year"].get().strip()
        isbn = self.edit_entries["isbn"].get().strip()
        price = self.edit_entries["price"].get().strip()

        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required!")
            return

        try:
            year = str(int(year)) if year else ""
            price = str(float(price)) if price else ""
            books = []
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)
                books.append(header)
                for row in reader:
                    if len(row) < 6:
                        continue
                    if row[0] == self.selected_book_id:
                        books.append([self.selected_book_id, title, author, year, isbn, price])
                    else:
                        books.append(row)
            with open(self.csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(books)
            messagebox.showinfo("Success", "Book updated successfully!")
            self.display_books_for_edit()
            self.display_books()
            self.display_books_for_delete()
            for entry in self.edit_entries.values():
                entry.delete(0, tk.END)
            self.selected_book_id = None
        except ValueError:
            messagebox.showerror("Error", "Year must be a valid integer and Price must be a valid number!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating book: {str(e)}")

    def create_delete_page(self):
        frame = self.frames["delete"]
        ttk.Label(frame, text="Delete Book", font=("Arial", 16, "bold")).pack(pady=10)
        self.delete_listbox = tk.Listbox(frame, height=15, width=80, bg="#2a2a3a", fg="white", font=("Arial", 10), selectmode=tk.SINGLE)
        self.delete_listbox.pack(pady=10, padx=10, fill="both", expand=True)
        ttk.Button(frame, text="Delete Selected Book", command=self.delete_book).pack(pady=20)

    def display_books_for_delete(self):
        self.delete_listbox.delete(0, tk.END)
        try:
            if not os.path.exists(self.csv_file):
                self.delete_listbox.insert(tk.END, "No books available.")
                return

            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) < 6:
                        continue
                    book_info = f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Year: {row[3] if row[3] else 'N/A'} | ISBN: {row[4] if row[4] else 'N/A'} | Price: ${row[5] if row[5] else 'N/A'}"
                    self.delete_listbox.insert(tk.END, book_info)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading books: {str(e)}")

    def delete_book(self):
        selection = self.delete_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a book to delete!")
            return

        selected = self.delete_listbox.get(selection[0])
        book_id = selected.split("|")[0].replace("ID:", "").strip()

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            try:
                books = []
                with open(self.csv_file, mode="r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    books.append(header)
                    for row in reader:
                        if len(row) < 6:
                            continue
                        if row[0] != book_id:
                            books.append(row)
                with open(self.csv_file, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(books)
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.display_books_for_delete()
                self.display_books()
                self.display_books_for_edit()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting book: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()