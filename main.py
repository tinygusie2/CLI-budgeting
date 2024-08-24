import os
import pickle
from datetime import datetime
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the scope for the Google API you're working with
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Path to your credentials.json file
CREDS_PATH = r"path\to\your\credentials.json/file"
TOKEN_PATH = r"path\to\where\your\token.pickle\file\should\be\generated"

def authorize_google_sheets():
    """Authorize and return the gspread client."""
    creds = None

    # Check if the token.pickle file exists
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    # Authorize gspread with the credentials
    client = gspread.authorize(creds)
    return client

def setup_sheet(client):
    """Open the Google Sheet."""
    try:
        sheet = client.open("your_google_sheet_name").sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        print(Fore.RED + "Error: Google Sheet not found. Please check the sheet name.")
        raise

    return sheet

def view_transactions_and_balance(sheet):
    """Display all transactions from Google Sheets and calculate balance."""
    try:
        all_values = sheet.get_all_values()
        
        if len(all_values) == 0:
            print(Fore.RED + "No transactions found.")
            return

        transactions = all_values
        total_balance = 0.0
        valid_transactions = []

        for idx, row in enumerate(transactions):
            date, amount, description = row
            amount = amount.replace(',', '.')
            try:
                amount = float(amount)
                total_balance += amount
                valid_transactions.append((date, amount, description))
            except ValueError:
                print(Fore.YELLOW + f"Warning: Non-numeric amount found: '{amount}'")

        print(Fore.CYAN + "\nTransactions:")
        print(Fore.CYAN + "=" * 50)
        for idx, transaction in enumerate(valid_transactions, 1):
            date, amount, description = transaction
            amount_type = Fore.GREEN + "Income" if amount > 0 else Fore.RED + "Expense"
            print(Fore.CYAN + f"{idx}. Date: {date}")
            print(f"   {amount_type}: ${amount:.2f}")
            print(Fore.CYAN + f"   Description: {description}")
            print(Fore.CYAN + "-" * 50)

        print(Fore.CYAN + "\nTotal Balance:")
        print(Fore.CYAN + "=" * 50)
        print(Fore.GREEN + f"${total_balance:.2f}" if total_balance >= 0 else Fore.RED + f"${total_balance:.2f}")
        print(Fore.CYAN + "=" * 50)
    except Exception as e:
        print(Fore.RED + "An error occurred:", str(e))

def add_transaction(sheet, amount, description):
    """Add a transaction to Google Sheets."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([date, amount, description])
    print(Fore.GREEN + f"Added transaction: Date: {date}, Amount: {amount}, Description: {description}")

def update_transaction(sheet, row_num, new_amount, new_description):
    """Update a specific transaction by row number."""
    try:
        sheet.update_cell(row_num + 1, 2, new_amount)  # Update amount (row_num + 1 to adjust for header row)
        sheet.update_cell(row_num + 1, 3, new_description)  # Update description
        print(Fore.GREEN + "Transaction updated in Google Sheets!")
    except gspread.exceptions.CellNotFound:
        print(Fore.RED + "Error: Cell not found. Please check the row number.")

def main():
    client = authorize_google_sheets()
    sheet = setup_sheet(client)

    while True:
        print(Fore.MAGENTA + "\n1. Add Transaction")
        print(Fore.MAGENTA + "2. View Transactions and Balance")
        print(Fore.MAGENTA + "3. Update Transaction")
        print(Fore.MAGENTA + "4. Exit")
        choice = input(Fore.YELLOW + "Choose an option: ")

        if choice == '1':
            try:
                amount = float(input("Enter amount (positive for income, negative for expense): ").replace(',', '.'))
                description = input("Enter description: ")
                add_transaction(sheet, amount, description)
            except ValueError:
                print(Fore.RED + "Invalid amount. Please enter a numeric value.")
        elif choice == '2':
            view_transactions_and_balance(sheet)
        elif choice == '3':
            try:
                row_num = int(input("Enter the transaction number to update: ")) - 1
                new_amount = float(input("Enter new amount: ").replace(',', '.'))
                new_description = input("Enter new description: ")
                update_transaction(sheet, row_num, new_amount, new_description)
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid number.")
        elif choice == '4':
            print(Fore.CYAN + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
