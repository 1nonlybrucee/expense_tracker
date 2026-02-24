import sqlite3

with sqlite3.connect('tracker.db') as connection:
    cursor = connection.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )'''
    )

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )'''
    )


    def add_category():
        new_category = input('Enter category name: ').strip()
        cursor.execute('INSERT INTO categories (name) VALUES(?)', (new_category,))
        connection.commit()

    def add_transaction():
        cursor.execute('SELECT * FROM categories')
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]} | Category: {row[1]}')
        category = int(input('Enter category id: '))
        amount = float(input('Enter amount you spent: '))
        cursor.execute('INSERT INTO transactions (amount, category_id) VALUES (?, ?)', (amount, category,))
        connection.commit()

    def show_transaction():
        cursor.execute(
        '''SELECT 
            transactions.transaction_id,
            transactions.amount, 
            transactions.date, 
            categories.name
            FROM transactions
            JOIN categories 
            ON transactions.category_id = categories.category_id
        '''
        )
        rows = cursor.fetchall()
        for row in rows:
            print(f'Transaction ID: {row[0]} | Amount: {row[1]} | Date: {row[2]} | Category: {row[3]}')


    def get_total_by_category():
        total = 0
        cursor.execute('''
            SELECT categories.name, SUM(transactions.amount)
            FROM transactions
            JOIN categories ON transactions.category_id = categories.category_id
            GROUP BY categories.name
        ''')
        rows = cursor.fetchall()
        for row in rows:
            print(f"Category: {row[0]} | Total: {row[1]}")
            total += row[1]
        print('Total: ' + str(total))
    
    def exit_program():
        exit()
    menu = {
        '1': add_category,
        '2': add_transaction,
        '3': show_transaction,
        '4': get_total_by_category,
        '5': exit_program
    }

    while True:
        print('1. Add category\n2. Add transaction\n3. Print transactions\n4. Print total\n5. Exit program')
        choice = input('Enter choice(1-5): ')
        action = menu.get(choice)
        if action:
            action()
        else: 
            print('Invalid choice')
