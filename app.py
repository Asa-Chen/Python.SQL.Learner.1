import time

from Utility.database import DBConnection
from datetime import datetime
intro = "Welcome to the gen 0.1 fitness journal app."
options = """
Log - Log workout
Print - Display all workouts
Update - Update a log entry
Delete - Delete Entry
Quit - Quit application

Your Choice: """
entry_prompt = """Input your workout entry, do not include the warmup.
Enter exercises as 'Sets x Reps @ Weight' or 'time @ exercise' type 'end' to stop the entry.
 Input:"""



class Journal:
    def __init__(self):
        self.journal = []
        with DBConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Journal(date, entry, notes)")

    def entry_input(self):
        entry = "Warmup"
        while (exercise := input(entry_prompt).lower()) != "end":
            entry = entry + "\n-> " + exercise
        return entry

    def add_entry(self):
        date = input("Input the date as YYYY-MM-DD: ")
        entry = ""
        date = datetime.strptime(date, "%Y-%m-%d").date()
        print("Input your entry: ")
        entry += self.entry_input()
        notes = input("Please add any notes: ")
        with DBConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Journal VALUES (?, ?, ?)", (date, entry, notes))

    def load_list(self):
        with DBConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Journal ORDER BY date")
            self.journal = [{'date': journ[0], 'entry': journ[1]} for journ in cursor.fetchall()]

    def print(self):
        self.load_list()
        for entry in self.journal:
            print(f"On {entry['date']} you logged:\n {entry['entry']}\n With these notes: {entry['notes']}")

    def delete_entry(self):
        target = input("Please input a date you'd like to delete: ")
        with DBConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Journal WHERE date =?", (target,))

    def update_entry(self):
        self.load_list()
        target = input("Please input a date you'd like to update as YYYY-MM-DD: ")
        target = datetime.strptime(target, "%Y-%m-%d").date()
        target = target.strftime("%Y-%m-%d")
        for dict in self.journal:
            if target == dict['date']:
                print(f"Your entry for {dict['date']} is:\n{dict['entry']}\nInput entire entry with changes: ")
                entry = self.entry_input()
                notes = input("Please add any notes: ")
                with DBConnection('data.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE Journal SET entry=? AND notes=? WHERE date=?", (entry, notes, target,))
                break
        else:
            print("That date is not in your log.")



def menu():
    fitJournal = Journal()
    print(intro)
    while (choice := input(options).lower()) != 'quit':
        if choice == 'log':
            fitJournal.add_entry()
        elif choice == 'print':
            fitJournal.print()
        elif choice == 'update':
            fitJournal.update_entry()
        elif choice == 'delete':
            fitJournal.delete_entry()
        else:
            print('Invalid choice, please try again.')

menu()