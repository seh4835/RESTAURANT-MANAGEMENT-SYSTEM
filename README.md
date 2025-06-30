# 🍽️ Amour Bistro – Restaurant Management System

📅 Project Duration
January 2025 – April 2025

Institution: Atlas SkillTech University

Team Size: 4 Members

Project Type: Full-Stack Web Application

Technologies: Flask · Python · MySQL · HTML · CSS · Regex

# 📌 Project Overview
Amour Bistro is a full-stack Restaurant Management System developed to simulate real-world restaurant operations through a user-friendly digital platform. Designed for both customers and administrators, this web application enables efficient ordering, menu management, and customer feedback handling.

This project was part of our academic coursework at Atlas SkillTech University and aimed to combine core concepts of web development, databases, backend logic, and object-oriented programming to create a dynamic and interactive system.

# 🧩 Key Features
👨‍🍳 Customer Side:
🔄 Dynamic Menu Switching: Customers can toggle between buffet and à la carte menus dynamically.

🛒 Order Placement: Enables selection of items with automated total price calculation.

✍️ Review Submission: Allows customers to leave feedback, ratings, and comments.

👀 Review Display: View and read other customer reviews for transparency and trust-building.

# 🛠️ Admin Panel:
🔐 Authentication System: Secured login for admin users with password validation using Regular Expressions.

🧾 CRUD Functionality: Admins can Create, Read, Update, and Delete menu items.

🧪 Exception Handling: Errors such as duplicate entries, invalid inputs, or server issues are caught gracefully.

💡 OOP Concepts: Employed Abstraction and Encapsulation in backend logic for maintainability and scalability.

# 🛠️ Technologies Used
Technology	Purpose
Flask (Python)	Web server and route handling
MySQL	Persistent database for orders, menu items, and reviews
HTML/CSS	Frontend structure and styling
Regex	Admin password validation rules
OOP Principles	Clean and modular backend logic

# 🧠 Project Architecture
csharp
Copy
Edit
📁 AmourBistro/
├── app.py               # Main Flask app
├── templates/           # HTML templates
├── static/              # CSS and images
├── db_config.py         # MySQL connection settings
├── models/              # OOP classes for menu, orders, admin
├── utils/               # Validation, helper methods
└── README.md            # You're here!
# 👩‍💻 Contributions
This was a collaborative team project involving 4 contributors.
My personal contributions included:

⚙️ Developing Flask backend routes

🔐 Implementing admin panel authentication & validation

📄 Designing database schema in MySQL

🧪 Writing exception handling logic and input sanitization

🚀 How to Run Locally
Clone the repo
bash
Copy
Edit
git clone https://github.com/yourusername/amour-bistro.git
cd amour-bistro
Set up a virtual environment & install dependencies
bash
Copy
Edit
python -m venv venv  
source venv/bin/activate  # or venv\Scripts\activate on Windows  
pip install -r requirements.txt  
Start your MySQL server and import the schema
sql
Copy
Edit
CREATE DATABASE amour_bistro;  
USE amour_bistro;  
-- Import schema.sql file
Run the app
bash
Copy
Edit
python app.py

# 📢 Future Enhancements
🍕 Integration of images for menu items

📱 Responsive mobile UI using Bootstrap

📊 Analytics dashboard for admins

✉️ Email confirmation for orders and reviews

# 🤝 Acknowledgements
Thanks to Dr. Shashikant Patil for mentoring us and Atlas SkillTech University for the opportunity and support.

💬 Feel free to fork this project, suggest features, or collaborate!
