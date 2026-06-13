import tkinter as tk
from tkinter import messagebox
import os
from google_auth_oauthlib.flow import InstalledAppFlow

# The scope defines what information you want to request from the Google account
SCOPES = ['https://googleapis.com']

def convert_to_login():
    # 1. Clear all existing home page widgets
    entry.pack_forget()
    button.pack_forget()
    label.pack_forget()
    
    # 2. Change main window background to white
    root.configure(bg="white")
    root.geometry("400x600")
    
    # 3. Create Login Page components inside the white window
    login_title = tk.Label(
        root, 
        text="Google Account Link", 
        bg="white", 
        fg="black", 
        font=("Arial", 16, "bold")
    )
    login_title.pack(pady=30)
    
    info_label = tk.Label(
        root, 
        text="Click below to sign in securely through your browser.", 
        bg="white", 
        fg="gray",
        wraplength=300
    )
    info_label.pack(pady=10)
    
    # Secure Login Trigger
    def attempt_google_login():
        if not os.path.exists('credentials.json'):
            messagebox.showerror("Error", "credentials.json file missing! Please download it from Google Cloud Console.")
            return
            
        try:
            # This handles launching the browser securely for user consent
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
            # If successful, you now have a temporary security token
            messagebox.showinfo("Success", "Successfully connected to your Google account!")
            print("Access Token acquired securely:", creds.token)
            
        except Exception as e:
            messagebox.showerror("Authentication Failed", f"Could not login: {str(e)}")

    # Styled Google Sign-In Button
    login_button = tk.Button(
        root, 
        text="Sign in with Google", 
        command=attempt_google_login,
        bg="#1a73e8",       
        fg="white", 
        font=("Arial", 11, "bold"),
        width=20,
        pady=8
    )
    login_button.pack(pady=20)

# Create main window
root = tk.Tk()
root.title("My First Desktop App")
root.geometry("400x600")

# Add components
entry = tk.Entry(root)
entry.pack(pady=20)

button = tk.Button(root, text="Enter", command=convert_to_login)
button.pack(pady=10)

label = tk.Label(root, text="Enter your name above")
label.pack(pady=10)

# Start the application loop
root.mainloop()
