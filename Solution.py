#import required libraries
import sqlite3
import csv
import pandas as pd

# Connect to the SQLite database 
conn = sqlite3.connect('your_database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Now you can execute SQL queries using the cursor
# For example, to select data from a table:
query = '''SELECT c.customer_id AS Customer, c.age AS Age, i.item_name AS Item, CAST(SUM(o.quantity) AS INTEGER) AS total_quantity
           FROM Customer c
           JOIN Sales s ON c.customer_id = s.customer_id
           JOIN Orders o ON s.sales_id = o.sales_id
           JOIN Items i ON o.item_id = i.item_id
           WHERE c.age BETWEEN 18 AND 35
           GROUP BY c.customer_id, c.age, i.item_id, i.item_name
           HAVING total_quantity > 0;
        '''

#Lets make two functions for 2 solutions 

def pure_sql_solution():
    #execute the query 
    cursor.execute(query)

    rows = cursor.fetchall()

    # Define the filename for the CSV file
    csv_filename = 'Query_solution_sql.csv'

    # Write data to CSV file
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerows(rows)


def pandas_solution():
    #execute the query using pandas library
    df = pd.read_sql_query(query, conn)

    # Define the path to save the CSV file
    csv_file_path = 'Query_solution_pandas.csv'

    # Save the DataFrame to a CSV file with semicolon delimiter
    df.to_csv(csv_file_path, sep=';', index=False)


#Call the functions to run the solution respectively 
print("The extracted data from the database using the two solutions!")
pure_sql_solution()
pandas_solution()


# Close the database connection
conn.close()


#ASSUMPTION : The database has been created already and the tables i.e Customer, Sales,Order,Item have the required data.