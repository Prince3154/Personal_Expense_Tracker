import csv
import json
import datetime
import matplotlib.pyplot as plt

# Expense data structure
expenses = []

# Load existing expenses from file
def load_expenses(filename):
    global expenses
    try:
        with open(filename, 'r') as file:
            if filename.endswith('.csv'):
                reader = csv.reader(file)
                for row in reader:
                    expense = {
                        'amount': float(row[0]),
                        'category': row[1],
                        'date': datetime.datetime.strptime(row[2], '%Y-%m-%d')
                    }
                    expenses.append(expense)
            elif filename.endswith('.json'):
                expenses = json.load(file)
                for expense in expenses:
                    expense['date'] = datetime.datetime.strptime(expense['date'], '%Y-%m-%d')
    except FileNotFoundError:
        pass

# Save expenses to file
def save_expenses(filename):
    with open(filename, 'w', newline='') as file:
        if filename.endswith('.csv'):
            writer = csv.writer(file)
            for expense in expenses:
                writer.writerow([expense['amount'], expense['category'], expense['date'].strftime('%Y-%m-%d')])
        elif filename.endswith('.json'):
            for expense in expenses:
                expense['date'] = expense['date'].strftime('%Y-%m-%d')
            json.dump(expenses, file)

# Add an expense
def add_expense():
    while True:
        try:
            amount = float(input("Enter the amount: $"))
            break
        except ValueError:
            print("Please enter a valid number.")

    category = input("Enter the category: ")
    date = datetime.datetime.now()
    expense = {
        'amount': amount,
        'category': category,
        'date': date
    }
    expenses.append(expense)
    print("Expense added successfully!")

# View summaries
def view_summaries():
    if not expenses:
        print("No expenses to display.")
        return

    total_spending = sum(expense['amount'] for expense in expenses)
    print(f"Total overall spending: ${total_spending:.2f}")

    categories = {}
    for expense in expenses:
        if expense['category'] not in categories:
            categories[expense['category']] = 0
        categories[expense['category']] += expense['amount']
    
    for category, amount in categories.items():
        print(f"Total spending for {category}: ${amount:.2f}")

    # Show graphical summary
    plot_category_expenses(categories)
    plot_daily_expenses()

# Plot spending by category
def plot_category_expenses(categories):
    labels = list(categories.keys())
    sizes = list(categories.values())

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular.
    plt.show()

# Plot daily spending
def plot_daily_expenses():
    daily_spending = {}
    for expense in expenses:
        date = expense['date'].date()
        if date not in daily_spending:
            daily_spending[date] = 0
        daily_spending[date] += expense['amount']

    dates = list(daily_spending.keys())
    amounts = list(daily_spending.values())

    plt.figure(figsize=(10, 6))
    plt.bar(dates, amounts)
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.title('Daily Expenses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Delete an expense
def delete_expense():
    view_summaries()
    if not expenses:
        print("No expenses to delete.")
        return
    
    try:
        expense_index = int(input("Enter the number of the expense to delete: ")) - 1
        if 0 <= expense_index < len(expenses):
            deleted_expense = expenses.pop(expense_index)
            print(f"Deleted expense: {deleted_expense['amount']} in category '{deleted_expense['category']}'")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Please enter a valid number.")

# Main program
def main():
    load_expenses('expenses.csv')

    while True:
        print("\nPersonal Expense Tracker Menu:")
        print("1. Add an expense")
        print("2. View summaries")
        print("3. Delete an expense")
        print("4. Exit the program")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_summaries()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            save_expenses('expenses.csv')
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
