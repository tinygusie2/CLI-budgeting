# Budget Tracker
A simple Python-based budget tracker that logs transactions to a Google Sheets document. This tool helps you keep track of your income and expenses, calculate your total balance, and update transaction records, all in one place.

# Features
Add Transactions: Easily log your income and expenses.
View Transactions: See a complete list of all your transactions.
View Balance: Automatically calculate and display your current balance.
Update Transactions: Modify any existing transactions.


# Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.7 or later installed on your system.
Google Cloud account to create and manage API credentials.
pip package installer.
Installation

 # 1. Clone the Repository


git clone https://github.com/your-username/budget-tracker.git
cd budget-tracker


# 2. Set Up a Virtual Environment (Not optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


# 3. Install Required Packages
pip install -r requirements.txt


# 4. Set Up Google API Credentials
To interact with Google Sheets, you need to set up OAuth 2.0 credentials.

Go to the Google Cloud Console.
Create a new project (or select an existing one).
Navigate to APIs & Services > Credentials.
Click Create Credentials > OAuth 2.0 Client IDs.
Set the application type to Desktop app and name it appropriately.
Download the credentials.json file.
Place the credentials.json file in the root directory of the project.


# 5. Configure Environment Variables
Create a .env file in the root directory with the following content:



GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URIS=["http://localhost"]
Replace your-client-id, your-client-secret, and your-redirect-uris with the values from your credentials.json file.

# 6. Run the Application
bash
Copy code
python main.py
Follow the on-screen instructions to interact with the budget tracker.

# Usage
Add Transaction: Enter the amount (positive for income, negative for expenses) and a description.
View Transactions: Display all logged transactions.
View Balance: Calculate and display the total balance based on logged transactions.
Update Transaction: Update the amount or description of a specific transaction.
Contributing
Contributions are always welcome! Please feel free to submit a pull request or open an issue to report bugs or suggest new features.


# Acknowledgements
This project was inspired by the need for a simple, yet effective way to track personal finances using Google Sheets.

# Additional Notes
Ensure that the Google Sheets document you want to use is shared with the email associated with the Google API service account.



![image](https://github.com/user-attachments/assets/fa81a797-008c-43cc-beb3-4464929bfc45)
