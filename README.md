# 🛒 Python E-commerce Platform

This project is a foundational e-commerce platform built in Python, demonstrating core concepts of object-oriented programming, inventory management, and customer interaction. It's designed to be a clear and extensible example of how to manage products, orders, and customer experiences in a console-based application.



## ✨ Features

* **Customer Management:**
    * Create new customers with unique names.
    * Browse all available products.
    * Search for products by name or category.
    * View detailed product information.
    * Add products to a shopping cart (Order).
    * View cart contents and total price.
    * Checkout process to finalize an order.
    * Start a new order or review previous orders after checkout.
* **Product & Inventory Management:**
    * Define products with names, categories, prices, and quantities.
    * Unique product ID generation.
    * Add or remove inventory from products.
    * Separate product instances for inventory vs. items in a cart.
    * Overloaded operators (`+`, `-`, `==`, `!=`) for intuitive product quantity manipulation and comparison.
* **Order Management:**
    * Create new orders (shopping carts) for customers.
    * Add, remove, and update quantities of products within an order.
    * Automatic order ID generation.
    * Track order status (pending, completed) and dates.
    * Calculate the total price of an order.
    * Validation to prevent editing checked-out orders.
* **Robust Validation:** Extensive use of property setters, decorators, and custom methods to ensure data integrity and proper system behavior across all classes.
* **Pandas Integration:** Utilizes `pandas` DataFrames for clear and readable display of product catalogs and cart contents.



## 🏗️ Architecture

The Simple Python E-commerce Platform is an illustration of OOP concepts in Python. It consists of three primary classes, each serving a specific purpose:

### Customer

The `Customer` class represents an e-commerce platform customer's interaction with Orders and Products. It manages the customer's shopping experience, including:

* Browse all available products.
* Searching for products by name or category.
* Viewing detailed product information.
* Adding items to a shopping cart (Order).
* Viewing cart contents and total price.
* Initiating the checkout process to finalize an order.
* Starting a new order or reviewing previous orders after checkout.

### Order

The `Order` class represents a customer's shopping cart, containing a list of `Product` objects. It manages the order's status and provides functionalities such as:

* Adding, removing, and updating quantities of products within the order.
* Generating unique order IDs.
* Tracking order status (pending, completed) and creation/checkout dates.
* Calculating the total price of the order.
* Applying validation to prevent editing orders that have already been checked out.

### Product

The `Product` class defines the properties and behaviors of individual inventory items. It includes attributes and functionalities for:

* Managing product details like name, category, price, and quantity.
* Generating unique product IDs and `parent_id` for tracking original items.
* Adding or removing inventory from products.
* Creating separate product instances for items in global inventory versus those placed in a customer's cart.
* Overloading standard Python operators (`+`, `-`, `==`, `!=`) for intuitive product quantity manipulation and comparison.



## 🚀 How to Run

To get this project up and running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/your-repo-name.git](https://github.com/YourUsername/your-repo-name.git) # Replace with your actual repo URL
    cd your-repo-name
    ```
2.  **Install dependencies:**
    This project requires the `pandas` library.
    ```bash
    pip install pandas
    ```
3.  **Run the application:**
    Assuming you have a `main.py` file that initializes and runs the customer interface, you can start the application with:
    ```bash
    python main.py
    ```

    **Example `main.py` content (if you need to create one):**
    ```python
    # main.py
    from products import Product
    from customer import Customer

    # Initialize some example products
    Product("Laptop", "Electronics", 1200.00, 10)
    Product("Keyboard", "Electronics", 75.00, 25)
    Product("Mouse", "Electronics", 30.00, 50)
    Product("Desk Chair", "Furniture", 150.00, 5)
    Product("Coffee Maker", "Appliances", 80.00, 15)

    # Create a customer and start the interaction loop
    customer = Customer("Toby")
    customer.run()

    print("\nThank you for shopping!")
    ```



## 💡 Future Enhancements

This project serves as a solid foundation, and there are many ways it could be expanded:

* **Persistence:** Implement saving and loading product and order data to a file (e.g., CSV, JSON) or a small database (e.g., SQLite) so data persists between runs.
* **User Authentication:** Add a basic login and registration system for multiple customer accounts.
* **Admin Interface:** Develop a separate command-line or basic GUI interface for administrators to manage products, view all customer orders, and adjust global inventory.
* **More Complex Product Attributes:** Support for product variations (size, color), sales/discounts, and customer reviews.
* **Comprehensive Order History:** A dedicated feature for customers to view *all* their past orders, not just the most recently checked-out one.
* **Refined Inventory Model:** Implement a more explicit separation between the global master inventory and the specific instances of products within a customer's cart to improve stock tracking precision and clarity.
* **Error Handling Refinements:** Consistently raise exceptions for validation errors rather than printing and returning `None`, allowing for more robust error management by calling code.

---
