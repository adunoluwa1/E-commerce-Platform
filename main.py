from customer import Customer
from products import Product
from order import Order

p1 = Product("Laptop", "Electronics", 1200.00, 10)
p2 = Product("Keyboard", "Electronics", 75.00, 25)
p3 = Product("Mouse", "Electronics", 30.00, 50)
p4 = Product("Desk Chair", "Furniture", 150.00, 5)


if __name__=="__main__":
    main = Customer("Toby")
    main.run()