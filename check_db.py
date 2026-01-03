import sqlite3

# Connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=" * 60)
print("USERS TABLE")
print("=" * 60)
cursor.execute("SELECT id, username, email, created_at FROM users")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user[0]} | Username: {user[1]} | Email: {user[2]} | Created: {user[3]}")

print("\n" + "=" * 60)
print("STUDY SESSIONS TABLE")
print("=" * 60)
cursor.execute("SELECT id, user_id, subject, duration, date FROM study_sessions")
sessions = cursor.fetchall()
if sessions:
    for session in sessions:
        print(f"ID: {session[0]} | User ID: {session[1]} | Subject: {session[2]} | Duration: {session[3]}min | Date: {session[4]}")
else:
    print("No study sessions found")

print("\n" + "=" * 60)
print("EXPENSES TABLE")
print("=" * 60)
cursor.execute("SELECT id, user_id, category, amount, date FROM expenses")
expenses = cursor.fetchall()
if expenses:
    for expense in expenses:
        print(f"ID: {expense[0]} | User ID: {expense[1]} | Category: {expense[2]} | Amount: ₹{expense[3]} | Date: {expense[4]}")
else:
    print("No expenses found")

print("\n" + "=" * 60)
print("DATABASE SUMMARY")
print("=" * 60)
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM study_sessions")
session_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM expenses")
expense_count = cursor.fetchone()[0]

print(f"Total Users: {user_count}")
print(f"Total Study Sessions: {session_count}")
print(f"Total Expenses: {expense_count}")
print("=" * 60)

conn.close()
