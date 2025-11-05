'''Books Example'''
import sql

class Books:
    '''Books Class'''
    def __init__(self, dbname):
        '''Initialize the books class'''
        self.dbname = dbname
        
    def create_book(self):
        '''Create a new book record'''
        title = input('Enter the title of the book: ')
        author = input('Enter the author of the book: ')
        publisher = input('Enter the publisher of the book: ')
        price = float(input('Enter the price of the book: '))
        copies = int(input('Enter the number of copies: '))
        query = f'''INSERT INTO BOOKS (TITLE, AUTHOR, PUBLISHER, PRICE, COPIES)
                    VALUES ('{title}', '{author}', '{publisher}', {price}, {copies});'''
        sql.perform_db_actions(self.dbname, query)
        print('Successfully added the Book record to the database.')
        
    def display_all(self):
        '''Display all book records in the database'''
        query = '''SELECT * FROM BOOKS;'''
        rows = sql.perform_db_actions(self.dbname, query)
        print("Books in the database:")
        for book in rows:
            print(book)
            
    def display_specific(self):
        '''Display a specific book record'''
        book_id = int(input('Enter the Book ID: '))
        query = f'''SELECT * FROM BOOKS WHERE BOOKID = {book_id};'''
        rows = sql.perform_db_actions(self.dbname, query)
        print("Details are:")
        for book in rows:
            print(book)
            
    def modify_book(self):
        '''Modify the details of a specific book record'''
        bid = int(input('Enter the Id of the book record to be updated: '))
        query = f'''SELECT title, author, publisher, price, copies FROM BOOKS WHERE BOOKID = {bid};'''
        rows = sql.perform_db_actions(self.dbname, query)
        
        if rows:
            cols = ['Title', 'Author', 'Publisher', 'Price', 'Copies']
            update_query = f'''UPDATE BOOKS SET'''
            
            if len(rows[0]) > 1:
                for col, value in zip(cols, rows[0]):
                    print(f"Current {col} is {value}")
                    ch = input("Enter y to modify: ")
                    if ch.lower() == 'y':
                        if col in ['title', 'autoher', 'publisher']: #strings
                            inp = input(f"Enter new {col}: ")
                            update_query += f" {col} = '{inp}',"
                        elif col in ['price', 'copies']: # numeric
                            inp = int(input(f"Enter new {col}: "))
                            update_query += f" {col} = {inp},"
            if len(update_query) > 16:
                update_query = update_query[:-1] + f" WHERE BOOKID = {bid};"
                rows = sql.perform_db_actions(self.dbname, update_query)
                print("Data has been updated.")
            else:
                print("Nothing to update!")
        else:
            print("No such data available!")
            
    def delete_book(self):
        '''Delete a specific book record'''
        book_id = int(input('Enter the Book ID to be deleted: '))
        query = f'''SELECT BOOKID FROM BOOKS WHERE BOOKID = {book_id};'''
        rows = sql.perform_db_actions(self.dbname, query)
        if len(rows) == 0:
            print("No such data available!")
        else:
            del_query = f'''DELETE FROM BOOKS WHERE BOOKID = {book_id};'''
            sql.perform_db_actions(self.dbname, del_query)
            print("Book record has been deleted.") 