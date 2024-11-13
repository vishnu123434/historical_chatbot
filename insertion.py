import mysql.connector
from docx import Document

# MySQL database connection
try:
    connection = mysql.connector.connect(
        host="localhost",     # Replace with your host
        user="root", # Replace with your MySQL username
        password="root", # Replace with your MySQL password
        database="history_db"  # Replace with your MySQL database name
    )
    print("Connected to database successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Define the file path (file in the same directory)
file_path = 'Zoroastrianism.docx'

# Open the document from the same directory
doc = Document(file_path)
print("Document opened successfully")

# Extract text from the .docx file
full_text = []
for para in doc.paragraphs:
    full_text.append(para.text)

# Join all paragraphs into a single string
history_data = '\n'.join(full_text)
print("Text extracted from document successfully")

# Prepare SQL insert query
insert_query = "INSERT INTO hist_data (topic_id, history_text) VALUES (%s, %s)"
data = (27, history_data)  # topic_id = 1 for Alexander Empire

# Insert data into MySQL database
try:
    cursor = connection.cursor()
    cursor.execute(insert_query, data)
    connection.commit()
    print("Data inserted successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("MySQL connection closed")
