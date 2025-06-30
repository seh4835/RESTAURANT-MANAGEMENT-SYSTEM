import mysql.connector

class DatabaseConnector:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shruti18",
                database="restaurant_management"
            )
            self.cursor = self.conn.cursor()
            self.create_tables()
        except mysql.connector.Error as e:
            print(f"Database connection failed: {e}")

    def create_tables(self):             # Entire function OOP concept: Abstraction 
                         #(The details of table creation and database interaction are abstracted in this method).
        if not self.cursor:
            return
        queries = [
            """
            CREATE TABLE IF NOT EXISTS buffet_menu (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100),
                section VARCHAR(100),
                item VARCHAR(255),
                price DECIMAL(10,2),
                UNIQUE (category, section, item, price)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS a_la_carte_menu (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item VARCHAR(255) UNIQUE,
                price DECIMAL(10,2)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item VARCHAR(255),
                quantity INT,
                total_price DECIMAL(10,2)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100),
                review_text TEXT
            )
            """
        ]
        for query in queries:
            self.cursor.execute(query)
        self.conn.commit()
    
    def close(self):  # method closes the database connection and the cursor when they are no longer needed.
        if self.cursor:          # OOP concept: Encapsulation (Manages the connection and closure logic within the class).
            self.cursor.close()
        if self.conn:
            self.conn.close()
from abc import ABC, abstractmethod

class AbstractMenuManager(ABC):

    @abstractmethod
    def fetch_a_la_carte_menu(self):
        pass

class MenuManager(AbstractMenuManager):
    def __init__(self, db):
        self.db = db
    
    def fetch_buffet_menu(self):
        if not self.db.cursor:      # method fetches all buffet menu items from the buffet_menu table in the database
            return []                                           # OOP concept: Encapsulation 
        self.db.cursor.execute("SELECT * FROM buffet_menu") # (It hides the database interaction from the outside and provides an interface to fetch the buffet menu).
        return self.db.cursor.fetchall()
    
    # Add item to buffet_menu
    def add_buffet_item(self, item_name, section, price):  # OOP Concept: Encapsulation 
        try:
            query = "INSERT INTO buffet_menu (item_name, section, price) VALUES (%s, %s, %s)" # query to insert data into the buffet_menu table
            self.db.cursor.execute(query, (item_name, section, price))  # Refers to the database cursor and Executes the query with values
            self.db.conn.commit() # commits the transaction(saves the changes) to the database.
        except Exception as e:
            print(f"Error adding item to buffet_menu: {str(e)}")

    # Add item to a_la_carte_menu
    def add_a_la_carte_item(self, item_name, price): # OOP Concept: Encapsulation 
        try:
            query = "INSERT INTO a_la_carte_menu (item_name, price) VALUES (%s, %s)" # query to insert data into the a_la_carte table
            self.db.cursor.execute(query, (item_name, price)) # Refers to the database cursor and Executes the query with values
            self.db.conn.commit() # commits the transaction(saves the changes) to the database.
        except Exception as e:
            print(f"Error adding item to a_la_carte_menu: {str(e)}")
    
    def fetch_a_la_carte_menu(self):  # method fetches all the A La Carte menu items from the a_la_carte_menu table and prints the result for debugging purposes.
        if not self.db.cursor:  # OOP concept: Abstraction
            return []              # (Abstracts away the database fetching process and provides a simple interface).
        self.db.cursor.execute("SELECT item_name, price FROM a_la_carte_menu")  # Fetch menu items and prices
        result = self.db.cursor.fetchall()
        print(f"🔍 Retrieved A La Carte Menu: {result}")  # Debugging log   # Debugging log
        return result 
    
    def add_menu_item(self, item, category, section, price):  # method adds a new menu item to either the buffet_menu or a_la_carte_menu table based on the category. If an item already exists, it updates the price.
        if not self.db.cursor:
            return                        # OOP concept: Encapsulation
        try:                             # (The method hides the database details and provides a simple interface for adding items to the menu).
 
            if category == "buffet":
                self.db.cursor.execute(
                    "INSERT INTO buffet_menu (category, section, item, price) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=VALUES(price)",
                    (category, section, item, price)
                )
            else:
                self.db.cursor.execute(
                    "INSERT INTO a_la_carte_menu (item, price) VALUES (%s, %s) ON DUPLICATE KEY UPDATE price=VALUES(price)",
                    (item, price)
                )
            self.db.conn.commit()
            print(f"✅ Item '{item}' added successfully to {category} menu.")  # Debug log
        except Exception as e:
            print(f"Error adding menu item: {e}")
    
    def update_menu_item(self, item, new_price):  # method updates the price of an existing menu item in the a_la_carte_menu table.
        if not self.db.cursor:
            return                      # Polymorphism: implementing method overriding
        try:
            self.db.cursor.execute(
                "UPDATE a_la_carte_menu SET price = %s WHERE item = %s", (new_price, item)
            )
            self.db.conn.commit()
        except Exception as e:
            print(f"Error updating menu item: {e}")
    
    def delete_menu_item(self, item):  # method deletes a menu item from both the buffet_menu and a_la_carte_menu tables.
        if not self.db.cursor:
            return
        try:
            self.db.cursor.execute("DELETE FROM buffet_menu WHERE item = %s", (item,))
            self.db.cursor.execute("DELETE FROM a_la_carte_menu WHERE item = %s", (item,))
            self.db.conn.commit()
        except Exception as e:
            print(f"Error deleting menu item: {e}")


class OrderManager:
    def __init__(self, db):
        self.db = db

    @classmethod                      # Class Method
    def place_order(cls, db, item, quantity):
        try:
            if not db.cursor:
                raise Exception("Database connection not available")

            # Correct query for fetching price
            db.cursor.execute(
                "SELECT price FROM a_la_carte_menu WHERE item=%s", (item,)
            )
            price = db.cursor.fetchone()

            if price:
                total_price = quantity * price[0]
                db.cursor.execute(
                    "INSERT INTO orders (item, quantity, total_price) VALUES (%s, %s, %s)",
                    (item, quantity, total_price),
                )
                db.conn.commit()
                print(f"✅ Order placed: {item} x{quantity} for ${total_price}")
            else:
                raise ValueError(f"Item '{item}' not found in A La Carte Menu.")
        except Exception as e:
            print(f"⚠️ Order failed: {e}")


class ReviewManager:
    def __init__(self, db): 
        self.db = db
    
    def insert_review(self, name, review_text):  # method inserts a customer review into the reviews table.
        try:
            if not self.db.cursor:  # OOP concept: Encapsulation
                raise Exception("Database connection not available") #  (Hides the details of review insertion and provides a simple interface).
            self.db.cursor.execute(
                "INSERT INTO reviews (customer_name, review_text) VALUES (%s, %s)", (name, review_text)
            )
            self.db.conn.commit()
        except Exception as e:
            print(f"Failed to insert review: {e}")
    
    def fetch_reviews(self):  # method retrieves all the reviews from the reviews table.
        if not self.db.cursor:
            return []
        self.db.cursor.execute("SELECT review_text FROM reviews")  # Fetch only reviews
        result = self.db.cursor.fetchall()
        print(f"🔍 Retrieved Reviews: {result}")  # Debugging log
        return result 

