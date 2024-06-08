import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from supabase_py import create_client

# Initialize Supabase client
supabase_url = "https://ahqrkjkunfioovfmjcfm.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFocXJramt1bmZpb292Zm1qY2ZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc4NjY3ODgsImV4cCI6MjAzMzQ0Mjc4OH0.sbqiMRdmY3ue7-o9ZwyXIVIge2QsHpvVmWTI9u574KU"
supabase = create_client(supabase_url, supabase_key)

class PasswordEntry(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)
        
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = tk.Checkbutton(self, bg='#ffffff', variable=self.show_password_var, command=self.toggle_password)
        self.show_password_check.place(relx=1, rely=0, anchor=tk.NE)
        
    def toggle_password(self):
        if self.show_password_var.get():
            self.config(show="")
        else:
            self.config(show="*")

# Function to handle sign up
def signup():
    # Close the login window
    root.withdraw()

    # Create a new window for sign up
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")
    signup_window.geometry("400x300")
    signup_window.configure(bg='#38B6FF')

    # Create a frame for the form with border
    form_frame = tk.Frame(signup_window, bg='#ffffff', bd=2, relief=tk.SOLID, padx=20, pady=20)
    form_frame.pack(expand=True, fill='both')

    # Title
    label_title = tk.Label(form_frame, text="Sign Up", font=("Helvetica", 16, "bold"), bg='#ffffff')
    label_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Username label and entry
    label_username = tk.Label(form_frame, text="Username", font=("Helvetica", 10), bg='#ffffff')
    label_username.grid(row=1, column=0, pady=5, sticky=tk.E)
    entry_username = ttk.Entry(form_frame)
    entry_username.grid(row=1, column=1, pady=5)

    # Password label
    label_password = tk.Label(form_frame, text="Password", font=("Helvetica", 10), bg='#ffffff')
    label_password.grid(row=2, column=0, pady=5, sticky=tk.E)

    # Password entry with Show Password checkbox
    entry_password = PasswordEntry(form_frame, show="*")
    entry_password.grid(row=2, column=1, pady=5, sticky="ew")

    # Sign up button
    signup_button = ttk.Button(form_frame, text="SIGN UP", command=lambda: create_account(entry_username.get(), entry_password.get(), signup_window))
    signup_button.grid(row=4, column=0, columnspan=2, pady=5)

    # Back button
    back_button = ttk.Button(form_frame, text="Back", command=lambda: back_to_login(signup_window))
    back_button.grid(row=5, column=0, columnspan=2, pady=5)

    # Make the text bold
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 10, 'bold'))

    # Adding some style
    style.configure('TFrame', background='#ffffff')
    style.configure('TButton', padding=6, background="#36B6FF")
    style.configure('TLabel', background='#ffffff')

    # Make the window responsive
    for i in range(6):
        form_frame.grid_rowconfigure(i, weight=1)
    for i in range(2):
        form_frame.grid_columnconfigure(i, weight=1)

# Function to go back to login window
def back_to_login(window):
    window.destroy()
    root.deiconify()

# Function to create a new account
def create_account(username, password, window):
    # Check if username is not empty
    if not username:
        messagebox.showerror("Error", "Please enter a username.")
        return

    # Check if password is not empty
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    # Check if username already exists
    result = supabase.table('users').select().eq('username', username).execute()

    if 'status' in result and result['status'] == 200 and result['data']:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
    else:
        # Insert new user into the database
        new_user = {'username': username, 'password': password}
        response = supabase.table('users').insert([new_user]).execute()
        
        print("Response:", response)  # Print response for debugging

        if 'status' in response and response['status'] == 201:
            messagebox.showinfo("Success", "Account created successfully!")
            window.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.")

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Query user data from Supabase
    result = supabase.table('users').select().eq('username', username).eq('password', password).execute()

    if result.get('data'):
        messagebox.showinfo("Login Success", "Welcome!")
        open_dashboard()  # Proceed to the dashboard upon successful login
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")


        
# Function to open dashboard
def open_dashboard():
    # Close the login window
    root.withdraw()

    # Create a new window for the dashboard
    dashboard = tk.Toplevel()
    dashboard.title("Dashboard")
    dashboard.geometry("400x300")
    dashboard.configure(bg='#38B6FF')

    # Add widgets to the dashboard window
    label_dashboard = tk.Label(dashboard, text="Welcome to the Dashboard!", font=("Helvetica", 14, "bold"), bg='#ffffff')
    label_dashboard.pack(pady=20)

    # Logout button
    logout_button = ttk.Button(dashboard, text="Logout", command=lambda: logout(dashboard))
    logout_button.pack(side="bottom", pady=25)

# Function to logout
def logout(window):
    # Close the dashboard window
    window.destroy()

    # Show the login window
    root.deiconify()


# Create the main window
root = tk.Tk()
root.title("Login Window")
root.geometry("400x350")
root.configure(bg='#38B6FF')

# Create a frame for the form with border
form_frame = tk.Frame(root, bg='#ffffff', bd=2, relief=tk.SOLID, padx=20, pady=20)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title
label_title = tk.Label(form_frame, text="Wellmeadows", font=("Helvetica", 16, "bold"), bg='#ffffff')
label_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Username label and entry
label_username = tk.Label(form_frame, text="Username", font=("Helvetica", 10), bg='#ffffff')
label_username.grid(row=1, column=0, pady=5, sticky=tk.E)
entry_username = ttk.Entry(form_frame)
entry_username.grid(row=1, column=1, pady=5)

# Password label
label_password = tk.Label(form_frame, text="Password", font=("Helvetica", 10), bg='#ffffff')
label_password.grid(row=2, column=0, pady=5, sticky=tk.E)

# Password entry with Show Password checkbox
entry_password = PasswordEntry(form_frame, show="*")
entry_password.grid(row=2, column=1, pady=5, sticky="ew")

# Login button
login_button = ttk.Button(form_frame, text="SIGN IN", command=login)
login_button.grid(row=4, column=0, columnspan=2, pady=5)

# Sign up link (as a button)
signup_label = tk.Label(form_frame, text="Don't have an account? Sign Up", font=("Helvetica", 8), bg='#ffffff', fg="blue", cursor="hand2")
signup_label.grid(row=5, column=0, columnspan=2, pady=5)
signup_label.bind("<Button-1>", lambda e: signup())

# Adding some style
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10, 'bold'))
style.configure('TFrame', background='#ffffff')
style.configure('TButton', padding=6, background="#36B6FF")
style.configure('TLabel', background='#ffffff')

# Make the window responsive
for i in range(6):
    form_frame.grid_rowconfigure(i, weight=1)
for i in range(2):
    form_frame.grid_columnconfigure(i, weight=1)

# Run the main event loop
root.mainloop()

