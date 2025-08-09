# Import the required library
import psycopg2
from dotenv import load_dotenv
import os


# Method to create a connection object
# It creates a pointer cursor to the database 
# and returns it along with Connection object
def create_connection():
    load_dotenv()
    # Connect to the database
    # using the psycopg2 adapter.
    # Pass your database name ,# username , password , 
    # hostname and port number
    conn = psycopg2.connect(user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        host=os.getenv("db_host"),
        port=os.getenv("db_port"),  
        database=os.getenv("db_database"))
    # Get the cursor object from the connection object

    curr = conn.cursor()
    return conn, curr

def create_table():
    try:
        # Get the cursor object from the connection object
        conn, curr = create_connection()
        try:
            # Fire the CREATE query
            curr.execute("CREATE TABLE IF NOT EXISTS \
            cartoon(cartoonID INTEGER, name TEXT,\
            cartoonImg BYTEA)")
            
        except(Exception, psycopg2.Error) as error:
            # Print exception
            print("Error while creating cartoon table", error)
        finally:
            # Close the connection object
            conn.commit()
            conn.close()
    finally:
        # Since we do not have to do anything here we will pass
        pass

def write_blob(cartoonID,file_path,name):
    try:
        # Read data from a image file
        drawing = open(file_path, 'rb').read()
        # Read database configuration
        conn, cursor = create_connection()
        try:           
            # Execute the INSERT statement
            # Convert the image data to Binary
            cursor.execute("INSERT INTO cartoon\
            (cartoonID,name,cartoonImg) " +
                    "VALUES(%s,%s,%s)",
                    (cartoonID,name, psycopg2.Binary(drawing)))
            # Commit the changes to the database
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting data in cartoon table", error)
        finally:
            # Close the connection object
            conn.close()
    finally:
        # Since we do not have to do
        # anything here we will pass
        pass
      
# Call the create table method      
create_table()
# Prepare sample data, of images, from local drive
write_blob(1,r"D:\OneDrive - 1CloudHub\Desktop\full-blog-app\backend\app\assets\pikachu.jpg","pikachu")
# write_blob(2,"F:\\TeachPytho\\GFGPhotos\\archie.jpg","Archie")
# write_blob(3,"F:\\TeachPytho\\GFGPhotos\\tintin.png","Tintin")
# write_blob(4,"F:\\TeachPytho\\GFGPhotos\\pikachu.jpg","Pikachu")
# write_blob(5,"F:\\TeachPytho\\GFGPhotos\\kungfupanda.jpg","Kung Fu Panda")