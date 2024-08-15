import json
import os.path
import time
import random
import sys
from tabulate import tabulate

# Creating Dictionary to store data
available_products = {
    1001: {"name": "avocado", "price": 230, "category": "grocery", "quantity": 10, "date": "10/03/2021"},
    1002: {"name": "lotion", "price": 250, "category": "beauty & personal", "quantity": 100, "date": "15/07/2021"},
    1003: {"name": "pain reliever", "price": 500, "category": "health", "quantity": 200, "date": "12/04/2021"},
    1004: {"name": "dry pasta", "price": 20, "category": "grocery", "quantity": 50, "date": "27/06/2021"},
    1005: {"name": "toothbrush", "price": 700, "category": "beauty & personal", "quantity": 100, "date": "30/01/2021"},
    1006: {"name": "halloween candy", "price": 33, "category": "grocery", "quantity": 56, "date": "22/02/2021"},
    1007: {"name": "mascara", "price": 765, "category": "beauty & personal", "quantity": 70, "date": "11/03/2021"},
    1008: {"name": "capsicum", "price": 764, "category": "grocery", "quantity": 90, "date": "16/02/2021"},
    1009: {"name": "blush", "price": 87, "category": "beauty & personal", "quantity": 50, "date": "17/07/2021"},
    1010: {"name": "granola bars", "price": 24, "category": "grocery", "quantity": 60, "date": "20/05/2021"},
}

# Formatting Dictionary into JSON format
js = json.dumps(available_products)

# Create Json File for DataBase and Write data Into File
with open("data.json", 'w') as fd:
    fd.write(js)

#Admin function for carrying out all CRUD operations
def admin():
    print("======== Welcome to the Admin Inventory Management System ================")
    while True:
        print("1) Display DataBase/All Products with their details")
        print("2) Display Specific Product with its details")
        print("3) Insert Data Into DataBase")
        print("4) Update Product in Database")
        print("5) Delete Product in DataBase")
        print("6) Display User Purchase Reports")
        print("7) Exit")
        print("------------------------------------------------------------------------------------------------------")
        try:
            n = int(input("Enter Your Choice :- "))
        except ValueError:
            print("Invalid input, please enter a number.")
            continue
        print("------------------------------------------------------------------------------------------------------")

        if n == 1:
            display_data()
        elif n == 2:
            display_specific_data()
        elif n == 3:
            add_new()
        elif n == 4:
            update_prod_data()
        elif n == 5:
            delete_prod()
        elif n == 6:
            display_reports_admin()
        elif n == 7:
            sys.exit("Exitted successfully")
        else:
            print("Invalid Choice...!!!")


def display_data():
    with open("data.json", 'r') as fd:
        data = json.load(fd)
    prompt=False
    print("------------------------------------------------------------------------------------------------------")
    if prompt:
        n = int(input("Enter '0' To Display Data Category Wise or '1' To Show Data As its Sequence Of Insertion :- "))
    else:
        n = 1
    print("------------------------------------------------------------------------------------------------------")
    print("\n")

    # Display All Records
    if n == 1:
        headers = ['ID', 'name', 'price', 'category', 'quantity', 'date']
        rows = []
        for key, value in data.items():
            row = [key, value['name'], value['price'], value['category'], value['quantity'], value['date']]
            rows.append(row)
        print(tabulate(rows, headers=headers, tablefmt='grid'))

        print("\n")

    elif n == 0:
        categories = set([value['category'] for value in data.values()])
        for category in categories:
            print(f"Data Of Products Of Category {category} is:- ")
            headers = ['ID', 'name', 'price', 'category', 'quantity', 'date']
            rows = []
            for key, value in data.items():
                if value['category'] == category:
                    row = [key, value['name'], value['price'], value['category'], value['quantity'], value['date']]
                    rows.append(row)
            print(tabulate(rows, headers=headers, tablefmt='grid'))

            print("\n")

    else:
        print("Enter Valid Choice...!!!")


def display_specific_data():
    with open("data.json", 'r') as fd:
        data = json.load(fd)

    i = input("Enter Product ID Whose Details You Want to Have a Look on :- ")

    print("\n")

    # Filter out Product ID from Records
    if i in data.keys():
        headers = ['ID', 'name', 'price', 'category', 'quantity', 'date']
        rows = [[i, data[i]['name'], data[i]['price'], data[i]['category'], data[i]['quantity'], data[i]['date']]]
        print(tabulate(rows, headers=headers, tablefmt='grid'))
    else:
        print("You Have Entered Wrong Product ID that is not Present in DataBase...!!!")

    print("\n")


def add_new():
    with open("data.json", 'r') as fd:
        data = json.load(fd)

    id = input("Enter New Product ID :- ")

    print("\n")

    if id not in data.keys():
        name = input("Enter Product Name :- ")
        price = input("Enter Price of Product (price for product quantity as 1) :- ")
        category = input("Enter Category of Product :- ")
        quantity = input("Enter Quantity of Product :- ")
        date = input("Enter The Date on Which Product is Added in Inventory :- ")

        data[id] = {'name': name, 'price': price, 'category': category, 'quantity': quantity, 'date': date}
        print("Product ID " + str(id) + " Added Successfully...!!!")
    else:
        print("The Product ID you Have Entered Is Already Present in DataBase Please Check...!!!")

    with open("data.json", 'w') as fd:
        json.dump(data, fd)


def delete_prod():
    with open("data.json", 'r') as fd:
        data = json.load(fd)

    temp = input("Enter The Product ID of The Product Which You Want To Delete :- ")

    if temp in data.keys():
        data.pop(temp)  # Remove the product
        print("Product ID " + str(temp) + " Deleted Successfully...!!!")
    else:
        print("Invalid Product ID...!!!")

    with open("data.json", 'w') as fd:
        json.dump(data, fd)


def update_prod_data():
    with open("data.json", 'r') as fd:
        data = json.load(fd)

    temp = input("Enter The Product ID of The Product Which You Want To Update :- ")

    if temp in data.keys():
        q = int(input("Want to update whole product data press '0' else '1' for specific data :- "))

        if q == 0:
            name = input("Enter Product Name :- ")
            price = input("Enter Price of Product (price for product quantity as 1) :- ")
            category = input("Enter Category of Product :- ")
            quantity = input("Enter Quantity of Product :- ")
            date = input("Enter The Date on Which Product is Added in Inventory :- ")

            data[temp] = {'name': name, 'price': price, 'category': category, 'quantity': quantity, 'date': date}
            print("Product ID " + str(temp) + " Updated Successfully...!!!")

        elif q == 1:
            p = input("Enter Which Attribute of Product You want to Update :- ")

            if p in data[temp].keys():
                print("Enter " + str(p) + " of Product :- ")
                u = input()
                data[temp][p] = u
                print("Product ID " + str(temp) + "'s attribute " + str(p) + " is Updated Successfully...!!!")
            else:
                print("Invalid Product Attribute...!!!")
        else:
            print("Invalid Choice...!!!")
    else:
        print("Invalid Product ID...!!!")

    with open("data.json", 'w') as fd:
        json.dump(data, fd)


def display_reports_admin():
    if not os.path.isfile("user_data.json"):
        print("No User Reports are Present")
        print("------------------------------------------------------------------------------------------------------")

        return

    with open("user_data.json", 'r') as fd:
        user_data = json.load(fd)

    n = int(input("Enter '0' to Check All Bills/Reports and '1' To Check Specific User Bills/Reports :- "))
    if n == 1:
        i = input("Enter User ID Whose Details You Want to Have a Look on")

        if i in user_data.keys():
            headers = ['User ID', 'Purchase Number', 'time_date', 'name', 'product_id', 'quantity', 'price']
            rows = []
            for purchase_number, purchase_data in user_data[i].items():
                row = [i, purchase_number, purchase_data['time_date'], purchase_data['name'], purchase_data['product_id'],
                       purchase_data['quantity'], purchase_data['price']]
                rows.append(row)
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print("Invalid User ID...!!!")

    elif n == 0:
        headers = ['User ID', 'Purchase Number', 'time_date', 'name', 'product_id', 'quantity', 'price']
        rows = []
        for user_id, purchases in user_data.items():
            for purchase_number, purchase_data in purchases.items():
                row = [user_id, purchase_number, purchase_data['time_date'], purchase_data['name'], purchase_data['product_id'],
                       purchase_data['quantity'], purchase_data['price']]
                rows.append(row)
        print(tabulate(rows, headers=headers, tablefmt='grid'))

    else:
        print("Invalid Choice...!!!")


def user():
    print("============== Welcome To Inventory Management System =================")
    while True:
        print("1) Search Product by its name")
        print("2) Search Product by its Category")
        print("3) Purchase Product")
        print("4) Exit")

        print("------------------------------------------------------------------------------------------------------")
        try:
            choice = int(input("Enter Your Choice :- "))
        except ValueError:
            print("Invalid input, please enter a number.")
            continue
        print("------------------------------------------------------------------------------------------------------")

        if choice == 1:
            search_prod()
        elif choice == 2:
            search_prod_cat()
        elif choice == 3:
            purchase_product()
        elif choice == 4:
            break
        else:
            print("Invalid Choice...!!!")


def search_prod():
    with open("data.json", 'r') as fd:
        data = json.load(fd)

    names = set()
    for key, value in data.items():
        names.add(value['name'])

    product_rows = [[name] for name in names]
    headers = ["Available Products"]

    print(tabulate(product_rows, headers=headers, tablefmt='grid'))

    prod_name = input("Enter Product Name to search :- ").lower()

    print("\n")

    headers = ['ID', 'name', 'price', 'category', 'quantity', 'date']
    rows = []
    for key, value in data.items():
        if prod_name.lower() in value['name'].lower():
            row = [key, value['name'], value['price'], value['category'], value['quantity'], value['date']]
            rows.append(row)

    if rows:
        print(tabulate(rows, headers=headers, tablefmt='grid'))
    else:
        print("No Products Found Matching the Given Name...!!!")


def search_prod_cat():
    with open("data.json", 'r') as fd:
        data = json.load(fd)

    categories = set()
    for key, value in data.items():
        categories.add(value['category'])

    cat_rows = [[category] for category in categories]
    headers = ["Available Categories"]

    print(tabulate(cat_rows, headers=headers, tablefmt='grid'))


    prod_cat = input("Enter Category Name to search :- ").lower()

    print("\n")

    headers = ['ID', 'name', 'price', 'category', 'quantity', 'date']
    rows = []
    for key, value in data.items():
        if prod_cat.lower() in value['category'].lower():
            row = [key, value['name'], value['price'], value['category'], value['quantity'], value['date']]
            rows.append(row)

    if rows:
        print(tabulate(rows, headers=headers, tablefmt='grid'))
    else:
        print("No Products Found Matching the Given Category...!!!")


def purchase_product():
    if not os.path.isfile("user_data.json"):
        user_data = {}
    else:
        with open("user_data.json", 'r') as fd:
            user_data = json.load(fd)

    with open("data.json", 'r') as fd:
        data = json.load(fd)

    display_data()

    total_price = 0

    while True:
        user_id = input("Enter User ID: ")
        purchase_number = str(random.randint(1000, 9999))
        time_date = time.strftime("%Y-%m-%d %H:%M:%S")

        product_id = input("Enter Product ID Which You Want to Purchase: ")

        if product_id in data.keys():
            quantity = int(input("Enter Quantity: "))

            if quantity <= data[product_id]['quantity']:
                price = data[product_id]['price'] * quantity
                total_price += price

                if user_id not in user_data.keys():
                    user_data[user_id] = {}

                user_data[user_id][purchase_number] = {'time_date': time_date, 'name': data[product_id]['name'],
                                                    'product_id': product_id, 'quantity': quantity, 'price': price}

                data[product_id]['quantity'] -= quantity

                print("Purchase Successful!")
                print(f"Total Price for Current Purchase: {price}")
                print(f"Accumulated Total Price: {total_price}")

                print("------------------------------------------------------------------------------------------------------")

                with open("data.json", 'w') as fd:
                    json.dump(data, fd)

                with open("user_data.json", 'w') as fd:
                    json.dump(user_data, fd)

                ch = int(input("Enter 0 to add more items or 1 to print bill: "))
                if ch == 1:
                    break
            else:
                print("Requested Quantity Not Available!")

        else:
            print("Invalid Product ID!")

    # Print the final bill
    print("===================================")
    print("Billing Details")
    print("===================================")
    print(f"Total Amount Payable: {total_price}")
    print("===================================")


def main():
    while True:
        print("===================================")
        print("Inventory Management System")
        print("===================================")
        print("1) Admin")
        print("2) User")
        print("3) Exit")
        print("===================================")

        n = int(input("Enter Your Choice :- "))

        if n == 1:
            admin()
        elif n == 2:
            user()
        elif n == 3:
            print("Thank you for using the Inventory Management System!")
            sys.exit()
        else:
            print("Invalid Choice...!!!")


if __name__ == "__main__":
    main()
