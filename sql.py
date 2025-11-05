from datetime import datetime
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

def perform_db_actions(db_name, query):
    '''
    This function will be called for any kinds of 
    database interaction from all other files as well.
    @db_name: the name of the database
    @query: the SQL query to be executed
    @values: the values for dynamic query in tuple format
    returns: Select query will return the recordset, other queries will return none
    '''
    connect = pymysql.connect(host=host,
                              user=user,
                              password=password,
                              database=db_name)
    cursorobj = connect.cursor()
    data = cursorobj.execute(query)
    data = cursorobj.fetchall()
    connect.commit()
    connect.close()
    return data

def create_db(db_name):
    '''
    One time create database queries
    '''
    # Table 1 Students getting created
    t1 = '''
        CREATE TABLE IF NOT EXISTS STUDENTS (
        MEMID INTEGER PRIMARY KEY AUTO_INCREMENT,
        NAME VARCHAR(30),
        EMAIL VARCHAR(15),
        PHONE VARCHAR(15),
        JOIN_DATE DATE DEFAULT (CURRENT_DATE)
        );
        '''
    # call DB action
    perform_db_actions(db_name, t1)
    # Table 2 Books getting created
    t2 = '''
        CREATE TABLE IF NOT EXISTS BOOKS (
        BOOKID INTEGER PRIMARY KEY AUTO_INCREMENT,
        TITLE VARCHAR(50),
        AUTHOR VARCHAR(30),
        PUBLISHER VARCHAR(30),
        PRICE REAL,
        COPIES SMALLINT
        );
        '''
    # call DB action
    perform_db_actions(db_name, t2)
    # Table 3 Issued Books getting created
    t3 = '''
        CREATE TABLE IF NOT EXISTS TRANSACTIONS (
        TID INTEGER PRIMARY KEY AUTO_INCREMENT,
        BOOKID INTEGER REFERENCES BOOKS(BOOKID),
        MEMID INTEGER REFERENCES STUDENTS(MEMID),
        ISSUE_DATE DATE,
        RETURN_DATE DATE
        );
        '''
    # call DB action
    perform_db_actions(db_name, t3)
    
    add_students = ['''INSERT INTO STUDENTS (NAME, EMAIL, PHONE)
                    VALUES('Sachin', 'sachin@em.com', '346377')''',
                    '''INSERT INTO STUDENTS (NAME, EMAIL, PHONE)
                    VALUES('Virat', 'virat@em.com', '544343466')''',
                    '''INSERT INTO STUDENTS (NAME, EMAIL, PHONE)
                    VALUES('Dhoni', 'dhoni@ema.com', '5645654')''',
                    '''INSERT INTO STUDENTS (NAME, EMAIL, PHONE)
                    VALUES('Kapil', 'kapil@ema.com', '4576457')'''
                    ]
    for q in add_students:
        perform_db_actions(db_name, q)
    add_books = ['''INSERT INTO BOOKS (TITLE, AUTHOR, COPIES)
                 VALUES('Practice Python', 'Swapnil Saurav', 3)''',
                 '''INSERT INTO BOOKS (TITLE, AUTHOR, COPIES)
                 VALUES('Practice SQL', 'Swapnil Saurav', 3)''',
                 '''INSERT INTO BOOKS (TITLE, AUTHOR, COPIES)
                 VALUES('Practice Data Visualization', 'Swapnil Saurav', 3)''',
                 '''INSERT INTO BOOKS (TITLE, AUTHOR, COPIES)
                 VALUES('Practice Machine Learning', 'Swapnil Saurav', 3)'''
                  ]
    for q in add_books:
        perform_db_actions(db_name, q)
        
    print("Your data has been created successfully!")
    
def check_outbooks(db_name):
    print("Borrowed list of books:")
    heading = ('Transaction ID', 'Member ID', 'Book ID', 'Issue Date')
    print(heading)
    q1 = '''SELECT TID, MEMID, BOOKID, ISSUE_DATE FROM TRANSACTIONS WHERE RETURN_DATE IS NULL;'''
    rows = perform_db_actions(db_name, q1)
    if rows == 0:
        print("No books is pending to be returned.")
    else:
        for r1 in rows:
            print(r1)

def issue_book(db_name):
    memid = int(input("Enter Member ID: "))
    bookid = int(input("Enter Book ID: "))
    book_count = -1
    
    # checking Member ID validity
    q1 = f'''SELECT MEMID FROM STUDENTS WHERE MEMID = {memid};'''
    row1 = perform_db_actions(db_name, q1)
    
    # checking Book ID validity and availability
    q1 = f'''SELECT COPIES FROM BOOKS WHERE BOOKID = {bookid};'''
    row2 = perform_db_actions(db_name, q1)
    
    if len(row1) < 1 or len(row2) < 1:
        print("Invalid Member ID or Book ID.")
    elif row2[0][0] < 1:
        print("Currently no more copies available.")
    else:
        print('Adding data...')
        book_count = row2[0][0]
        q2 = '''INSERT INTO TRANSACTIONS (MEMID, BOOKID, ISSUE_DATE)
                VALUES ('%d', '%d', '%s');''' % (memid, bookid, str(datetime.now().strftime('%Y-%m-%d')))
        perform_db_actions(db_name, q2)
        
        # Update the count of copies
        q2 = '''UPDATE BOOKS SET COPIES = %d WHERE BOOKID = %d;''' % (book_count - 1, bookid)
        perform_db_actions(db_name, q2)
        print("Book issued successfully!")
        
def return_book(db_name):
    check_outbooks(db_name)
    given_id = input("Above are the list of transactions for borrowed.\
        \nEnter the Transaction ID alone or the Member ID and Book ID (Mem ID,BookID) to return the book: ")
    val1 = 0
    tid = -1
    bookid = -1
    try:
        if ',' in given_id:
            print('Member ID and Books ID entered.')
            val1 = given_id.split(',')
            val1[0] = int(val1[0])
            val1[1] = int(val1[1])
            val1 = tuple(val1)
            
            q1 = f'''SELECT TID, BOOKID FROM TRANSACTIONS
                    WHERE MEMID = {val1[0]} 
                    AND BOOKID = {val1[1]} 
                    AND RETURN_DATE IS NULL;'''
            rows = perform_db_actions(db_name, q1)
            if len(rows) >= 1:
                tid = rows[0][0]
                bookid = val1[1]
            else:
                print("No such transaction found.")
        else:
            print('Transaction ID entered.')
            val1 = int(given_id)
            q1 = f'''SELECT TID, BOOKID FROM TRANSACTIONS
                    WHERE RETURN_DATE IS NULL AND TID = {val1};'''
            rows = perform_db_actions(db_name, q1)
            if len(rows) >= 1:
                tid = val1
                bookid = rows[0][1]
            else:
                print("No such transaction found.")
    except Exception:
        print("Invalid input format.")
    else:
        print("Updating the database...")
        # increase copies count
        q1 = f'''SELECT COPIES FROM BOOKS WHERE BOOKID = {bookid};'''
        rows = perform_db_actions(db_name, q1)
        q1 = f'''UPDATE BOOKS
                SET COPIES = {(rows[0][0])+1} WHERE BOOKID = {bookid};'''
        perform_db_actions(db_name, q1)
        
        # update return date
        q1 = '''UPDATE TRANSACTIONS 
                SET RETURN_DATE = '%s' WHERE TID = %d;''' % (str(datetime.now().strftime('%Y-%m-%d')), tid)
        rows = perform_db_actions(db_name, q1)
        print("Book returned successfully!")
        
if __name__ == "__main__":
    create_db('libraryms') #Onetime