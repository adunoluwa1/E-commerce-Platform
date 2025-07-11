"""Order module to respresent a customer's order"""
from datetime import date
from .products import Product


class Order:
    """
    The Order class represents a customer's order, containing a list of Product objects,
    order status, creation date, and methods to manage products within the order.
    """
    orders: list[object] = []

    def __init__(self, *products):
        self._products = list()
        self._id = Order.order_id()
        self._total = 0
        self._created_date = str(date.today())
        self._checkout_date = None
        self._checkout_status = False
        Order.orders.append(self)

        for item in products:
            if isinstance(item, tuple) and len(item) == 2 \
                and isinstance(item[0], Product) \
                    and isinstance(item[1], int):   # If item is a tuple (prod, int):
                self.add_product(item[0], item[1])  # Call add_product with specified quantity
            elif isinstance(item, Product):
                self.add_product(item, 1)           # Default to quantity 1 if only product object is given
            else:
                raise TypeError("Initial products must be Product objects or (Product, quantity) tuples.")

    def __str__(self) -> str:
        return f"Order: {self.total_price}, {self.status}, {self.created_date}"

    def __repr__(self) -> str:
        return f"Order({self.products})"

    @classmethod
    def order_id(cls):
        """Generate and return a unique order ID for each new order."""
        if not hasattr(cls, "_order_id"):
            cls._order_id = 10000
        else:
            cls._order_id += 1
        return cls._order_id

    @property
    def id(self):
        """Gets the unique order ID for each order"""
        return self._id

    @property
    def products(self):
        """Returns a list of products for each order"""
        return self._products

    @products.setter
    def products(self, products_list):
        if not isinstance(products_list, list):
            raise TypeError("Products must be a list.")
        for prod in list(products_list):
            if not isinstance(prod, Product):
                raise TypeError("Invalid product type")
        self._products = products_list

    @staticmethod
    def order_validation(function):
        """Decorator to validate the order. The function is run if the order\
              has not been checked out and exists in the orders list."""
        def wrapper(self, *args, **kwargs):
            if self.checkout_status:
                raise ValueError("Unable to edit order, you have already checked out!")
            if self not in Order.orders:
                raise ValueError("Order does not exist")
            # idx: int = Order.orders.index(self)
            # result: Order = function(self, *args, **kwargs)
            return function(self, *args, **kwargs)
        return wrapper

    @order_validation
    def add_product(self, product: Product, qty: int = 1):
        """Adds product to order cart"""
        if qty > product.quantity:
            raise ValueError(f"Only {product.quantity} items available")
        try:
            prod = product.new(qty)
            if not prod:
                raise ValueError("Unable to add product")
            prod.in_cart = True
            self.products.append(prod)
            return self
        except ValueError as e:
            print(f"Product Addition Error: {e}")
            return

    @order_validation
    def remove_product(self, product):
        """Removes product from the order cart

        :param product: Product to remove
        :type product: Product object
        :raise ValueError: If the product does not exist in cart
        :return: An Order object with updated product list
        :rtype: Order object
        """
        if product not in self.products:
            raise ValueError("Product not in order cart")
        idx = self.products.index(product)
        product.in_cart = False
        self.products.pop(idx)
        return self

    @order_validation
    def update_product_quantity(self, product: Product, new_qty: int):
        """
        Updates the quantity of a specified product in the order.

        Parameters:
            product (Product): The product whose quantity is to be updated.
            qty (int): The new quantity to set for the product.

        Raises:
            ValueError: If the product is not in the order or if the quantity is invalid.
        """
        if product not in self.products:
            raise ValueError("Product not in order cart")
        if not new_qty or new_qty <= 0 or not isinstance(new_qty, int) or new_qty == product.quantity:
            raise ValueError("Enter a valid quantity")
        
        global_prod = next((p for p in Product.products if p.parent_id == product.parent_id and not p.in_cart),None)

        if global_prod is None:
            raise ValueError(f"Original product '{product.name}' not found in global inventory. Cannot validate stock.")
       
        stock_adjustment_amount = abs(product.quantity - new_qty)
       
        if new_qty > global_prod.quantity:
            raise ValueError(f"Cannot set quantity to {new_qty} for '{product.name}'."
                             f"Only {global_prod.quantity} items are available")
        if new_qty > product.quantity:
            product.quantity = new_qty
            global_prod.remove_inventory(stock_adjustment_amount)
        elif new_qty < product.quantity:
            product.quantity = new_qty
            global_prod.add_inventory(stock_adjustment_amount)


        # idx = self.products.index(product)
        # # self.products[idx].quantity = qty
        # self.products[idx] = product.new(qty,False)
        return self

    @order_validation
    def clear_products(self):
        """Removes all products from the order, clearing the cart."""
        self.products = []
        return self

    @order_validation
    def delete(self) -> None:
        """Removes the current order instance from the list of all orders."""
        idx = Order.orders.index(self)
        Order.orders.pop(idx)


    @property
    def total_price(self) -> str|None:
        """Calculates and returns the total price of all products\
              in the order as a formatted string."""
        if self not in Order.orders:
            raise ValueError("Order does not exist")
        self._total = 0
        for prod in self.products:
            self._total += prod.quantity * prod.price
        return f"${self._total:,.2f}"

    @property
    def created_date(self) -> str:
        """Returns the creation date of the order as a string."""
        return self._created_date

    @property
    def checkout_date(self) -> str|None:
        """Returns the checkout date of the order as a string."""
        if not self._checkout_date:
            print("Order is pending checkout")
            return None
        return self._checkout_date

    @property
    def checkout_status(self) -> bool:
        """Returns the current status of the order as a string."""
        return self._checkout_status

    @property
    def status(self) -> str:
        """Returns the current status of the order as a string."""
        if self.checkout_status:
            return "Order completed"
        return "Pending"

    def checkout(self) -> None:
        """Marks the order as checked out, sets the checkout date,\
              and prints a confirmation message."""
        if self.checkout_status:
            raise ValueError(f"Already checked out. Checkout date: {self._checkout_date}")
        if len(self.products) == 0:
            print("Unable to checkout. No product in cart")
            return
        self._checkout_status = True
        self._checkout_date = str(date.today())
        print(f"Check out successful. Order Number: {self.id}; Price: {self.total_price}")
