import sqlite3


def connect():
    return sqlite3.connect("contacts.db")


def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_contact():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email (optional): ").strip()

    if name == "" or phone == "":
        print("Name and phone are required!")
        return
    if not phone.isdigit():
        print("Phone must contain digits only!")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
        (name, phone, email)
    )
    conn.commit()
    conn.close()
    print("Contact saved!")


def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return
    print(f"\n{'ID':<5}{'Name':<20}{'Phone':<15}{'Email':<25}")
    print("-" * 65)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<20}{r[2]:<15}{(r[3] or ''):<25}")


def view_contacts():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    print_rows(rows)


def search_contact():
    keyword = input("Search by name: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM contacts WHERE name LIKE ?",
        (f"%{keyword}%",)
    )
    rows = cur.fetchall()
    conn.close()
    print_rows(rows)


def update_contact():
    view_contacts()
    try:
        cid = int(input("\nEnter ID to update: "))
    except ValueError:
        print("ID must be a number!")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = ?", (cid,))
    row = cur.fetchone()

    if row is None:
        print("No contact with that ID.")
        conn.close()
        return

    name = input(f"New name [{row[1]}]: ").strip() or row[1]
    phone = input(f"New phone [{row[2]}]: ").strip() or row[2]
    email = input(f"New email [{row[3] or ''}]: ").strip() or row[3]

    if not phone.isdigit():
        print("Phone must contain digits only!")
        conn.close()
        return

    cur.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
        (name, phone, email, cid)
    )
    conn.commit()
    conn.close()
    print("Contact updated!")


def delete_contact():
    view_contacts()
    try:
        cid = int(input("\nEnter ID to delete: "))
    except ValueError:
        print("ID must be a number!")
        return

    confirm = input("Are you sure? (y/n): ").lower()
    if confirm != "y":
        print("Cancelled.")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = ?", (cid,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()

    if deleted == 0:
        print("No contact with that ID.")
    else:
        print("Contact deleted!")


def main():
    create_table()

    while True:
        print("\n=== Contact Book ===")
        print("1. Add contact")
        print("2. View all contacts")
        print("3. Search contact")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose (1-6): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose 1 to 6.")


main()