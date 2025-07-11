"""Class to represent an e-Commerce platform customer's interaction with Orders and Product"""
import pandas as pd
import re
from .order import Order
from .products import Product

class Customer:
    """
    Represents an e-Commerce platform customer's interaction with Orders and Products.

    This class manages the customer's shopping experience, including Browse products,
    searching, viewing product details, adding items to a cart (order), viewing the cart,
    and initiating checkout.
    """
    def __init__(self,name:str):
        """
        Initializes a new Customer instance.

        A customer is initialized with a unique name and an empty shopping order.

        Args:
            name (str): The name of the customer.
        """
        self._order = Order()
        self.name = name

    @property
    def name(self)-> str:
        """
        Gets the customer's name.

        Returns:
            str: The name of the customer.
        """
        return self._name
    @name.setter
    def name(self, value):
        """
        Sets the customer's name. The name is converted to title case. 
        Raises a ValueError if the name is empty.

        Args:
            value (str): The new name for the customer.

        Raises:
            ValueError: If the provided name is empty or evaluates to False.
        """
        if not value:
            raise ValueError("Missing name")
        self._name = value.title()

    @property
    def order(self):
        """
        Gets the customer's current shopping order.

        Returns:
            Order: The Order object representing the customer's current cart.
        """
        return self._order

    def run(self):
        """
        Executes the main program loop for customer interaction.

        This method manages the primary application flow for the customer, 
        including initial Browse, searching, and handling post-checkout options 
        like creating new orders or reviewing past ones.

        The loop continues until the user chooses to exit.
        """
        while True:
            if self.order.checkout_status:
                response = self.checked_out_menu()
                match response:
                    case "1":
                        self._order = Order()
                        continue
                    case "2":
                        print(self.order)
                        continue
                    case "3"|"":
                        return
                
            response = self.menu()
            match response:
                case "1":
                    self.browse()
                case "2":
                    name = input("Enter product name: ").title()
                    self.browse(name,"Name")
                case "3":
                    category = input("Enter product category: ").title()
                    self.browse(category,"Category")
                # case "4":
                #     return self.order.checkout()
                case "x"|"":
                    return

    def menu(self):
        """
        Prompts the user with main menu options and returns their response.

        The menu displays options for Browse, searching, and exiting.

        Returns:
            str: The user's input response.
        """
        response = input(
            f"""
    ====================
        Welcome {self.name}
    ====================

    1. Browse all Products
    2. Search by Product name
    3. Search by category
    x. Exit

""")
        return response

    def checked_out_menu(self):
        """
        Prompts the user with check-out menu options and returns their response.

        The menu displays options to create a new order, view previous order, and exit.

        Returns:
            str: The user's input response.
        """
        response = input(
            f"""
    ===================================
         Welcome {self.name}
    ===================================

      You have successfully checked out


    1. New order  2.view order  x. Exit

""")
        return response

    def browse(self, value:str|None = None,column:str|None = None):
        """
        Allows the customer to browse products, potentially after a search.

        This method fetches the product list (all or filtered by search criteria),
        displays it, and then enters a sub-loop for viewing specific product details
        or managing the cart. If no results are found, it returns.

        Args:
            value (str | None): The value to search for (e.g., product name, category).
                                If None, all products are displayed.
            column (str | None): The column to search within (e.g., "Name", "Category").
                                  Required if 'value' is provided.
        """
        while True:
            if self.order.checkout_status:
                return
            table = self.search(value,column)
            if table is None:
                return
            
            print(table)
            response = input(
            """
    ===================================
              Browse Products
    ===================================

    Enter a product index to view its details

        v: View cart        x: Exit
""").lower()
            match response:
                case "v":
                    self.view_cart()
                case "x":
                    return
                case _:
                    if not response.isnumeric():
                        print("Enter a valid product index")
                        continue
                    if int(response) not in table.index.to_list():
                        print(f"{response} not in table index. Enter a valid product index")
                        continue
                    self.view_product(response,table)


    def search(self, value=None, column:str|None = None, table: pd.DataFrame|None = None) \
        -> pd.DataFrame|None:
        """
        Searches for partial and full matches of products within a given table\
based on a value in a specified column.

        If no search criteria (value or column) are provided, it returns the full product table.
        If a filter is applied and no results are found, it prints a message and returns None.

        Args:
            value (Any): The value to filter the table by (e.g., product name, category).
                         If None and 'column' is also None, the full product table is returned.
            column (str | None): The column name in which to search for the 'value'.
                                 Must be provided if 'value' is provided.
            table (pd.DataFrame | None): The DataFrame to search within. If None,
                                         'self.product_table()' is used as the base table.

        Returns:
            pd.DataFrame | None: A filtered DataFrame containing matching records,
                                 the full product DataFrame if no search criteria are given,
                                 or None if no results are found.

        Raises:
            ValueError: If the specified column does not exist in the table, or if
                        a search value is provided without a column.
        """
        # by default the table to filter is the product table
        if table is None:
            table = self.product_table()

        # if no arguments are entered return the product table
        # Handles the "browse all products" case
        if column is None and value is None:
            return self.product_table()

        # Validate that both value and column are present for a search
        if value is None or column is None:
            print("Error: Both value and column must be provided for a specific search.")
            return None

        if column not in table.columns:
            raise ValueError(f"{column} does not exist in the product table")

        filtered_table = table[table[column].str.contains(re.escape(value),case=False, na=False, regex=True)]
        # filtered_table = table[table[column]==value]

        if len(filtered_table) == 0:
            print("No results found for your search criteria")
            return None
        return filtered_table

    @classmethod
    def product_table(cls):
        """
        Generates and returns a Pandas DataFrame listing all available products.

        This DataFrame includes product Name, Category, Price, Available Quantity,
        and the actual Product object for easy retrieval.

        Returns:
            pd.DataFrame: A DataFrame with product details and Product objects.
        """
        df = pd.DataFrame(columns=["Name","Category","Price","Avail Qty.","Object"])
        for idx, prod in enumerate([prod for prod in Product.products if not prod.in_cart]):
            df.loc[idx] = [prod.name, prod.category, f"${prod.price:,.2f}", prod.quantity, prod]
        # df.set_index(keys="idx",drop=True,inplace=True)
        return df

    def view_product(self, idx:str, table: pd.DataFrame|None = None):
        """
        Displays details for a specific product and allows adding it to the cart.

        Args:
            idx (str): The string representation of the product's index in the displayed table.
            table (pd.DataFrame | None): The DataFrame from which the product was selected.
                                         Defaults to the full product table if not provided.

        Raises:
            ValueError: If the provided index is not a valid integer.
            IndexError: If the integer index is not found in the table.
        """
        if table is None:
            table = self.product_table()
        try:
            int_idx = int(idx)
        except ValueError as e:
            print(f"Input Error: {idx} is not a valid number: {e}")
            return

        if int_idx not in table.index:
            raise IndexError(f"Product index '{int_idx}' not found in the current index list")

        df_prod = table.loc[int_idx]
        prod:Product = df_prod["Object"]

        print(df_prod.to_frame())
        c = input(
f"""
    ===================================
         {int_idx}. {df_prod["Name"]}
    ===================================

    1. Add to cart    2. View Cart
    
    x. press any other button to exit

""")
        if c == "1":
            while True:
                try:
                    qty = input("Quantity or [x to exit]: ")
                    if qty == "x" or not qty:
                        return
                    self.add_to_cart(prod,int(qty))
                    break
                except ValueError as e:
                    print(f"Invalid Input. Please enter a whole number for quantity: {e}")
                    continue
        elif c == "2":
            self.view_cart()
            if self.order.checkout_status: # if customer checks out return to main menue
                return
        else:
            return

    def add_to_cart(self, prod:Product, quantity:int):
        """
        Adds a specified quantity of a product to the customer's current order (cart).

        Args:
            prod (Product): The Product object to add to the cart.
            quantity (int): The quantity of the product to add.
        """
        self.order.add_product(prod,quantity)
        print(f"{quantity} x {prod.name} added to cart successfully!")

    def view_cart(self) -> pd.DataFrame|None:
        """
        Displays the current items in the customer's shopping cart.

        If the cart is empty, it prints a message and returns None.
        Otherwise, it displays a DataFrame of cart items and offers checkout options.

        Returns:
            pd.DataFrame | None: A DataFrame representing the cart items if not empty,
                                 or None if the cart is empty.
        """
        df = pd.DataFrame(columns=["Name","Category","Quantity","Unit Price","Total Price","Object"])
        for idx, prod in enumerate(self.order.products):
            df.loc[idx] = [prod.name, prod.category, prod.quantity, prod.price, prod.quantity * float(prod.price), prod]
        if len(df) == 0:
            print("No product in cart")
            return None
        print(df)
        response = input(
f"""
    ===================================
                Your Cart
    ===================================
        1. Checkout         2. Back
    
""")
        match response:
            case "1":
                self.order.checkout()
                return
            case _:
                return 

