"""Product class to represent a product or inventory item"""

class Product:
    """Product class to create, manage, and handle product inventory and catalog."""

    products: list[object] = []
    # catalog = []

    def __init__(self, name: str, category: str, price: int | float, quantity: int =1,):
        self.name = name.title()
        self.quantity = quantity
        self.price = price
        self._product_id = Product.generate_id()
        self._parent_id = self.product_id
        self.category = category
        self.in_cart = False
        Product.products.append(self)
        # Product.catalog.append({"name": self.name, "category": self.category})

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:,.2f}, {self.quantity}pcs"

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, category={self.category!r}, \
price=${self.price:.2f}, quantity={self.quantity:,})"

    @property
    def name(self) -> str:
        """Get the product's name."""
        return self._name

    @name.setter
    def name(self, name) -> None:
        if not name:
            raise ValueError("Missing product name")
        self._name = name.title().strip()

    @property
    def category(self) -> str:
        """Get the product's category"""
        return self._category

    @category.setter
    def category(self, category) -> None:
        if not category:
            raise ValueError("Missing product category")
        self._category = category.title().strip()

    @property
    def product_id(self) -> str:
        """Get the product id"""
        return self._product_id

    @property
    def parent_id(self) -> str:
        """Get the product parent id"""
        return self._parent_id

    @property
    def quantity(self) -> int:
        """Get the product quantity"""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity) -> None:
        """Set the product quantity, ensuring it is a valid integer."""
        if not quantity or not isinstance(quantity, int):
            raise ValueError("Missing or invalid product quantity")
        self._quantity = quantity

    @property
    def price(self) -> float:
        """Get the product price as a float"""
        return self._price

    @price.setter
    def price(self, price) -> None:
        """Set the product price, ensuring it is a valid integer or float."""
        if not price or not isinstance(price, (int, float)):
            raise ValueError("Missing or invalid product price")
        self._price = price

    @property
    def in_cart(self) -> bool:
        """Get the status of the product if it's currently in a cart"""
        return self._in_cart

    @in_cart.setter
    def in_cart(self, value) -> None:
        """Set the in-cart status of the product , ensuring it is a valid bool."""
        if not isinstance(value, bool):
            raise ValueError("Missing or invalid product cart status")
        self._incart = value

    @staticmethod
    def validate_product(function):
        """Decorator to check and validate that the product exists in the Products list."""
        def wrapper(self, *args, **kwargs):
            if self not in Product.products:
                raise ValueError("Unable to update product inventory. Product does not exist")
            return function(self,*args,**kwargs)
        return wrapper

    @validate_product
    def add_inventory(self, value: int):
        """
        Add a specified quantity to the product's inventory.

        :param value: The number of items to add to inventory.
        :type value: int
        :raises ValueError: If the value is not a positive integer.
        :return: The updated product instance.
        :rtype: Product
        """
        if not isinstance(value, int) and value <= 0:
            raise ValueError("Invalid quantity")
        self += value
        return self

    @validate_product
    def remove_inventory(self, value: int):
        """
        Remove a specified quantity from the product's inventory.

        :param value: The number of items to remove from inventory.
        :type value: int
        :raises ValueError: If the value is not a positive integer or exceeds\
              available quantity.
        :return: The updated product instance or result of product deletion\
              if quantity reaches zero.
        :rtype: Product or None 
        """
        if not isinstance(value, int) or value <= 0 or value > self.quantity:
            raise ValueError("Invalid quantity")
        self -= value
        return self
        # if value < self.quantity:
        #     self.quantity -= value
        #     return self
        # if value == self.quantity:
        #     Product.delete_product(self)
        #     return None

    def new(self, qty: int, update_original=True):
        """Creates a new instance of the current Product \
with the same attributes but a different quantity"""
        try:
            if not qty or qty > self.quantity:
                raise ValueError("Invalid quantity")
            new = Product(self.name,self.category,self.price,qty)
            new._parent_id = self.product_id
            if update_original:
                self.remove_inventory(qty)
            return new
        except ValueError as e:
            print(f"New Product Error: {e}")
            return
    

    @classmethod
    def generate_id(cls) -> str:
        """Generate and return a unique product ID as a string."""
        if not hasattr(cls, "_id_counter"):
            cls._id_counter = 100000
        else:
            cls._id_counter += 1
        return str(cls._id_counter)


    @classmethod
    def list_product(cls) -> list:
        """
        Return the list of all product instances.
        """
        # display(cls.products)
        return cls.products

    @classmethod
    def delete_product(cls, prod: object) -> None:
        """
        Remove a product from the products list.

        :param prod: The product instance to remove.
        :type prod: object
        :raises ValueError: If the product does not exist in the products list.
        :return: None
        """
        if prod not in cls.products:
            raise ValueError("Product does not exist")
        idx = cls.products.index(prod)
        cls.products.pop(idx)

    def __add__(self,other) :
        """
        Adds a Product instance to another Product or an integer quantity.

    Parameters:
        other (Product or int): 
            - If a Product, it must have the same name, category, and price.
            - If an int, it represents the quantity to increase.

    Returns:
        Product: The current Product instance with updated quantity.

    Raises:
        TypeError: 
            - If `other` is neither a Product nor an int.
            - If `other` is a Product with mismatched name, category, or price.

    Side Effects:
        - Mutates the current Product's quantity in-place.
    """
        if not isinstance(other,(Product,int)):
            raise TypeError("Cannot add items of different types")
        if isinstance(other,Product) and self != other:
            # (other.name != self.name or other.category != self.category \
            #     or other.price != self.price):
            raise TypeError("Cannot add Products of different names, categories, or price")
        if isinstance(other, int):
            self._quantity += other
            return self
        self.quantity += other.quantity
        return self

    def __sub__(self,other):
        """
    Subtracts a Product instance or an integer quantity from the current Product.

    Parameters:
        other (Product or int): 
            - If a Product, it must match the name, category, and price.
            - If an int, it represents the quantity to subtract.

    Returns:
        Product or None:
            - Returns the current Product with updated quantity if some quantity remains.
            - Returns None if the resulting quantity is zero and the product is deleted.

    Raises:
        TypeError: 
            - If `other` is neither a Product nor an int.
            - If `other` is a Product with mismatched name, category, or price.
        ValueError:
            - If the quantity to subtract exceeds the available quantity.

    Side Effects:
        - Mutates the current Product’s quantity in-place.
        - May call `Product.delete_product()` and remove the product from the system if quantity becomes zero.
    """
        if not isinstance(other,(Product,int)):
            raise TypeError("Cannot subtract items of different types")
        if isinstance(other,Product) and self != other:
            # (other.name != self.name or other.category != self.category \
            #     or other.price != self.price):
            raise TypeError("Cannot add Products of different types")
        if isinstance(other, int):
            if other > self.quantity:
                raise ValueError("Cannot subtract more than the available quantity")
            if other == self.quantity:
                Product.delete_product(self)
                return None
            self.quantity -= other
            return self
        if other.quantity > self.quantity:
            raise ValueError("Cannot subtract more than the available quantity")
        if other.quantity == self.quantity:
            Product.delete_product(self)
            return None
        self.quantity -= other.quantity
        return self

    def __eq__(self, other):
        """
    Compares two Product instances for equality based on their unique product ID.

    Parameters:
        other (Product): Another Product object to compare against.

    Returns:
        bool: True if both products have the same product ID, False otherwise.

    Raises:
        TypeError: If `other` is not a Product instance.
        """
        if not isinstance(other, Product):
            raise TypeError("Cannot compare items of different types")
        return self.product_id == other.product_id or self.parent_id == other.parent_id 

    def __ne__(self, other):
        """
    Compares two Product instances for equality based on their unique product ID.

    Parameters:
        other (Product): Another Product object to compare against.

    Returns:
        bool: True if both products dont have the same product ID, False otherwise.

    Raises:
        TypeError: If `other` is not a Product instance.
        """
        if not isinstance(other, Product):
            raise TypeError("Cannot compare items of different types")
        return self.parent_id != other.parent_id 

    @classmethod
    # @property
    def catalog(cls) -> list[dict]:
        """Returns a dynamic catalog of products containing product names and categories."""
        Product._catalog = []
        for prod in cls.products:
            Product._catalog.append({"Name":prod.name, "Category":prod.category})
        return Product._catalog
