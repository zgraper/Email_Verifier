import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import smtplib
import dns.resolver

# Email verification functions
def has_mx_records(domain):
    """Check if a domain has MX records."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False


def verify_email_smtp(email):
    """Verify a single email via SMTP. Returns True, False, or "Security Block"."""
    try:
        local_part, domain = email.split('@', 1)
    except ValueError:
        return False

    if not has_mx_records(domain):
        return False

    try:
        # Get mail server from MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        mail_server = str(mx_records[0].exchange)

        # Connect to SMTP
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)
        server.connect(mail_server)
        server.helo()
        server.mail(f'test@{domain}')  # Dummy sender
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return True
        elif code == 550 and 'security' in message.decode().lower():
            return "Security Block"
        else:
            return False

    except Exception:
        return False


# GUI Application
def run_file_verification():
    """Handle file selection, email verification, and saving output."""
    file_path = filedialog.askopenfilename(
        title="Select Email List",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*")]        
    )
    if not file_path:
        return

    try:
        # Load into DataFrame
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return

    # Ensure 'Email' column exists
    if 'Email' not in df.columns:
        messagebox.showerror("Error", "No column named 'Email' found in file.")
        return

    # Process each email
    verified = []
    for email in df['Email']:
        result = verify_email_smtp(str(email))
        if result is True:
            verified.append(email)
        elif result == "Security Block":
            verified.append("Security Block")
        else:
            verified.append("")

    # Add result column
    df['Email (verified)'] = verified

    # Ask for save location
    save_path = filedialog.asksaveasfilename(
        title="Save Verified Emails",
        defaultextension='.csv',
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
    )
    if not save_path:
        return

    try:
        if save_path.lower().endswith('.csv'):
            df.to_csv(save_path, index=False)
        else:
            df.to_excel(save_path, index=False)
        messagebox.showinfo("Success", f"Verified file saved to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")


def run_single_verification():
    """Verify a single email entered by the user."""
    email = single_email_var.get().strip()
    if not email:
        messagebox.showwarning("Input Required", "Please enter an email to verify.")
        return

    result = verify_email_smtp(email)
    if result is True:
        messagebox.showinfo("Result", f"{email} is valid.")
    elif result == "Security Block":
        messagebox.showinfo("Result", f"{email} was blocked by security.")
    else:
        messagebox.showinfo("Result", f"{email} is not valid.")


# Set up the main window
root = tk.Tk()
root.title("Email Verifier")
root.geometry("450x250")

# File verification section
file_frame = tk.LabelFrame(root, text="Verify Emails in File", padx=10, pady=10)
file_frame.pack(fill="both", expand="yes", padx=10, pady=10)

file_button = tk.Button(file_frame, text="Select and Verify File", command=run_file_verification)
file_button.pack(pady=5)

# Single email verification section
single_frame = tk.LabelFrame(root, text="Verify Single Email", padx=10, pady=10)
single_frame.pack(fill="both", expand="yes", padx=10, pady=10)

single_email_var = tk.StringVar()
single_entry = tk.Entry(single_frame, textvariable=single_email_var, width=40)
single_entry.pack(side="left", padx=(0,10))

single_button = tk.Button(single_frame, text="Verify Email", command=run_single_verification)
single_button.pack(side="left")

root.mainloop()
