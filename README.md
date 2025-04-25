# Email Verifier GUI

A simple Python/Tkinter application to verify email addresses in bulk (from a CSV/XLSX file) or individually using SMTP and DNS MX record checks.

---

## Features

- **Bulk Verification**: Load a spreadsheet (`.csv` or `.xlsx`) with an `Email` column, verify each address, and save results with an added `Email (verified)` column.
- **Single Email Check**: Enter a single email address to test validity and receive immediate feedback.
- **MX Record Validation**: Ensures the domain has valid mail exchange (MX) records before attempting SMTP.
- **SMTP Verification**: Connects to the mail server and issues an `RCPT` command to confirm delivery acceptance.
- **Security Block Detection**: Recognizes when a server explicitly rejects with a security-related refusal.

## Requirements

- Python 3.7+
- [pandas](https://pandas.pydata.org/)
- [dnspython](https://www.dnspython.org/)
- No external GUI libraries beyond the standard `tkinter` (bundled with Python)

Install dependencies via pip:

```bash
pip install pandas dnspython
```

## Usage

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/email-verifier-gui.git
cd email-verifier-gui
```

2. **Run the App**
```bash
python email_verifier_gui.py
```

3. **Bulk Verify**
   - Click **Select and Verify File**.
   - Choose a `.csv` or `.xlsx` file containing an `Email` column.
   - After processing, choose where to save the output.

4. **Single Email Verification**
   - Type an email address into the text box under **Verify Single Email**.
   - Click **Verify Email** to see the result.

## Notes & Tips

- **Timeout**: SMTP connections use a 10-second timeout; large lists may take several minutes.
- **Threading**: For very large files, consider integrating threading or a progress bar.
- **Error Handling**: Invalid formats or missing columns prompt a dialog box.

## Contributing

Contributions and improvements are welcome! Please open issues or submit pull requests.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

*Created by Zane Graper*
