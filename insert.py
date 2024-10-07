import pymysql
import docx

# MySQL database connection
def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='history_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to extract text from the .docx file
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    content = ""
    for para in doc.paragraphs:
        content += para.text + "\n"
    return content

# Function to insert data into MySQL
def insert_data_into_db(title, content):
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "INSERT INTO history_data (title, content) VALUES (%s, %s)"
    cursor.execute(sql, (title, content))
    
    connection.commit()
    connection.close()

# Main function to extract data and insert into the database
def process_docx_and_insert(docx_path, title):
    content = extract_text_from_docx(docx_path)
    insert_data_into_db(title, content)
    print(f"Data inserted for: {title}")

# Example usage
if __name__ == '__main__':
    # Path to your .docx file
    docx_path = 'Mesopotamia.docx'
    
    # Provide a suitable title or identifier for the entry
    title = 'History of Mesopotamia'

    # Extract data and insert into MySQL
    process_docx_and_insert(docx_path, title)
