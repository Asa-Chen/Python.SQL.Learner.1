from Utility.DBConnection import DBConnection #Local imports of sqlite3 context manager
from datetime import datetime
intro = "Welcome to the gen 0.1 fitness journal app."
options = """
Log - Log workout
Print - Display all workouts
Search - Search for an entry
Update - Update a log entry
Delete - Delete Entry
Quit - Quit application
Your Choice: """
entry_prompt = """Input your workout entry, do not include the warmup.
Enter exercises as 'Sets x Reps @ Weight' or 'time @ exercise' type 'end' to stop the entry.
 Input:"""



class Journal: #Journal object which houses all functions and local data
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
        date = input("Input the date as YYYY-MM-DD or type 'exit': ")
        if date.lower() == 'exit':
            return
        entry = ""
        date = datetime.strptime(date, "%Y-%m-%d").date()
        date = date.strftime("%Y-%m-%d")
        self.load_list()
        for dict in self.journal:
            if date == dict["date"]:
                print("That date is already logged.")
                break
        else:
            print("Input your entry: ")
            entry += self.entry_input()
            notes = input("Please add any notes: ")
            with DBConnection('data.db') as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Journal VALUES (?, ?, ?)", (date, entry, notes))
                connection.commit()

    def load_list(self):
        with DBConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Journal ORDER BY date")
            self.journal = [{'date': journ[0], 'entry': journ[1], 'notes': journ[2]} for journ in cursor.fetchall()]

    def print(self):
        self.load_list()
        for entry in self.journal:
            print(f"On {entry['date']} you logged:\n {entry['entry']}\n With these notes: {entry['notes']}")

    def delete_entry(self):
        target = input("Please input a date you'd like to delete as YYYY-MM-DD or type 'exit': ")
        if target.lower() == 'exit':
            return
        target = datetime.strptime(target, "%Y-%m-%d").date()
        target = target.strftime("%Y-%m-%d")
        with DBConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Journal WHERE date =?", (target,))

    def search_entry(self):
        self.load_list()
        target = input("Please input a date you'd like to search for as YYYY-MM-DD or type 'exit': ")
        if target.lower() == 'exit':
            return
        target = datetime.strptime(target, "%Y-%m-%d").date()
        target = target.strftime("%Y-%m-%d")
        for dict in self.journal:
            if target == dict['date']:
                print(f"{dict['date']} has this entry: \n{dict['entry']} \nWith these notes: {dict['notes']}")
                break
        else:
            print("No entry with that date was found.")

    def update_entry(self):
        self.load_list()
        target = input("Please input a date you'd like to update as YYYY-MM-DD or type 'exit': ")
        if target.lower() == 'exit':
            return
        target = datetime.strptime(target, "%Y-%m-%d").date()
        target = target.strftime("%Y-%m-%d")
        for dict in self.journal:
            if target == dict['date']:
                print(f"Your entry for {dict['date']} is:\n{dict['entry']}\nWith this note: {dict['notes']}\n"
                      f"Input entire entry with changes: ")
                new_entry = self.entry_input()
                new_notes = input("Please add any notes: ")
                with DBConnection('data.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE Journal SET entry=?, notes=? WHERE date=?", (new_entry, new_notes, target,))
                    connection.commit()
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
        elif choice == 'search':
            fitJournal.search_entry()
        elif choice == 'update':
            fitJournal.update_entry()
        elif choice == 'delete':
            fitJournal.delete_entry()
        else:
            print('Invalid choice, please try again.')

menu()