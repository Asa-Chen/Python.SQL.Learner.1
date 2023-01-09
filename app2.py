import Utility.Database as Connection
from datetime import datetime
INPUT_PROMPT = """Please choose an action:
Add - Add an entry
Delete - Delete an entry
Update - Update an entry
All - Display all entries
Quit - Quit program
----------: """
def terminal():
    while (choice := input(INPUT_PROMPT)).lower() != 'quit':
        if choice == 'add':
            entry(Connection.check_presense)

def entry(func):
    date = input("Please input an entry date: ")
    date = datetime.strptime(date, "%Y-%m-%d").date()
    date = date.strftime("%Y-%m-%d")
    if func(date):
        print("Entry already exists!")
        return

terminal()