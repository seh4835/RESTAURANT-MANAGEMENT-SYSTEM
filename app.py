from flask import Flask, render_template, request, redirect, url_for
from restaurant import DatabaseConnector, MenuManager, OrderManager, ReviewManager

app = Flask(__name__) # Creates an instance of the Flask application
db = DatabaseConnector()
menu_manager = MenuManager(db)
order_manager = OrderManager(db)
review_manager = ReviewManager(db)

@app.route('/') # the route for the homepage when the user visits the root page
def home():
    menu_type = request.args.get('menu_type', 'buffet')  # Retrieves the menu_type parameter from the URL query string. If not provided, it defaults to 'buffet'
    reviews = review_manager.fetch_reviews()  # Fetch reviews
    a_la_carte_items = menu_manager.fetch_a_la_carte_menu()  # Fetch A La Carte menu

    if menu_type == 'buffet':
        menu_items = menu_manager.fetch_buffet_menu() # menu type is "buffet", fetch the buffet menu items.
    else:
        menu_items = a_la_carte_items  # Assign A La Carte menu items
    
    print(f"✅ Sending A La Carte Menu to Template: {a_la_carte_items}")  # Debugging
    return render_template('index.html', menu=menu_items, menu_type=menu_type, reviews=reviews, a_la_carte_menu=a_la_carte_items)

@app.route('/order', methods=['POST'])  # The route for submitting an order. It listens for POST requests.
def order():
    try:
        item_name = request.form['item']  # Get the item name from the form
        quantity = int(request.form['quantity'])  # Get the quantity from the form and convert it to an integer

        # Call the class method correctly
        OrderManager.place_order(db, item_name, quantity)

    except ValueError:
        return "Invalid quantity. Please enter a valid number.", 400
    except KeyError:
        return "Invalid data. Item or quantity not provided.", 400
    except Exception as e:
        return f"Error placing order: {str(e)}", 500

    # Redirect to home after successful order
    return redirect(url_for('home')) # Redirects the user back to the homepage (/) after placing the order.



@app.route('/review', methods=['POST'])  # the route for submitting a review. It listens for POST requests.
def review(): 
    try:
        name = request.form['name']
        review_text = request.form['review']
        review_manager.insert_review(name, review_text) # to insert the review into the database
    except Exception as e:
        return f"Error submitting review: {str(e)}", 500
    return redirect(url_for('home'))  # Redirects the user back to the homepage (/)

@app.route('/admin') # the route for the admin panel (/admin).
def admin():
    return render_template('admin.html') # page where the admin can manage the menu items.

import re  # Import regex module at the top of app.py

@app.route('/admin/add_item', methods=['POST']) # When a user visits /route_path, call function_name() to handle the request.
def admin_add_item():
    ADMIN_PASSWORD = "Admin@123" # Define a fixed default admin password
    try:
        admin_password = request.form['admin_password']
        # Check if the entered password matches the default password
        if admin_password != ADMIN_PASSWORD:
            return "Invalid admin password. Access denied.", 403

        # Regex pattern for password validation
        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$')

        # Check if password matches regex
        if not password_pattern.match(admin_password):
            return "Invalid admin password. Password must be at least 8 characters, including one uppercase letter, one lowercase letter, and one number.", 400

        # Get data from the form
        item_name = request.form['item']
        category = request.form['category']
        section = request.form['section'] if request.form['section'] else None
        price = float(request.form['price'])

        # Add item to the appropriate menu
        if category.lower() == "buffet":
            db.cursor.execute(
                "INSERT INTO buffet_menu (item_name, section, price) VALUES (%s, %s, %s)",
                (item_name, section, price),
            )
        elif category.lower() == "a la carte":
            db.cursor.execute(
                "INSERT INTO a_la_carte_menu (item_name, price) VALUES (%s, %s)",
                (item_name, price),
            )
        else:
            return "Invalid category. Please choose either 'buffet' or 'a la carte'.", 400

        db.conn.commit()
        return f"Item '{item_name}' added successfully.", 200

    except ValueError:
        return "Invalid price. Please enter a valid number.", 400
    except Exception as e:
        return f"Error adding item: {str(e)}", 500



@app.route('/admin/update', methods=['POST']) # route is for updating an existing menu item.
def admin_update_item():
    if request.form['admin_password'] != "admin123":
        return "Unauthorized", 403
    item = request.form['item'] # name of the item whos price to be chnaged 
    new_price = float(request.form['new_price']) # takes the new price 
    menu_manager.update_menu_item(item, new_price) # updating the list
    return redirect(url_for('admin')) # Redirects the user back to the homepage (/).

@app.route('/admin/delete', methods=['POST'])  # router that handles deleting a menu item.
def admin_delete_item():
    if request.form['admin_password'] != "admin123":
        return "Unauthorized", 403
    item = request.form['item'] # name of the item which is to deleted
    menu_manager.delete_menu_item(item) # Updating the list
    return redirect(url_for('admin'))  # Redirects the user back to the homepage (/).

if __name__ == '_main_': # block checks if the script is being run directly 
    app.run(debug=True)  # Starts the Flask application with debugging enabled


if __name__ == '__main__': # block checks if the script is being run directly 
    app.run(debug=True)  # Starts the Flask application with debugging enabled 

# Important things to remember:
# request.form is used to access form data sent via a POST request.
# request.form behaves like a dictionary where:
#               Keys → Names of the form fields.
#               Values → Data entered by the user in those fields.
# request.form.get() is a safer way to access form data.It works in same way as request.form 
#               If the specified key is not found, it returns None (or a default value if specified) instead of raising an error.