# Saebom Kwon, saebom, 38120092, SI507 Waiver

import sys
import sqlite3

sqlite_file = '/Users/kwonSaebom/Documents/GitHub/si-507-waiver-assignment-f18-saebomk/Northwind_small.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

employee_table = 'EMPLOYEE'
customer_table = 'CUSTOMER'
order_table = 'ORDER'

function_name = sys.argv[1]

def customer_rows(cursor):
    customer_list = {}
    cursor = conn.execute("SELECT Id, CompanyName from customer")
    for row in cursor:
        customer_list[row[0]] = row[1]
    customer_list = sorted(customer_list.items(), key = lambda x:x[1])
    return customer_list

def employee_rows(cursor):
    employee_dict = {}
    cursor = conn.execute("SELECT Id, LastName, FirstName FROM employee")
    for row in cursor:
        employee_dict[row[0]] = row[2] + " " + row[1]
    return employee_dict

def order_cust_rows(cursor, cust_id):
    order_list = []
    cursor = conn.execute("SELECT OrderDate FROM [Order] JOIN Customer ON [Order].customerId = Customer.id WHERE Customer.id = ?", (cust_id,))
    for row in cursor:
        order_list.append(row[0])
    return order_list

def order_emp_rows(cursor, emp_lastName):
    order_list = []
    cursor = conn.execute("SELECT OrderDate FROM [Order] JOIN Employee ON [Order].EmployeeId = Employee.id WHERE Employee.LastName = ?", (emp_lastName,))
    for row in cursor:
        order_list.append(row[0])
    return order_list

if len(sys.argv) == 2:
    if function_name == "customers":
        cust_list = customer_rows(c)
        print("ID\tCustomer Name")
        for cust in cust_list:
            print('{}\t{}'.format(cust[0], cust[1]))
    elif function_name == "employees":
        emp_dict = employee_rows(c)
        print("ID\tEmployee Name")
        for name, age in emp_dict.items():
            print('{}\t{}'.format(name, age))

if len(sys.argv) == 3:
    function_argv = sys.argv[2]
    if function_name == "orders":
        if function_argv.startswith("cust="):
            order_cust_list = order_cust_rows(c, function_argv.replace("cust=", ""))
            print("Order dates")
            for order in order_cust_list:
                print(order)
        elif function_argv.startswith("emp="):
            order_emp_list = order_emp_rows(c, function_argv.replace("emp=", ""))
            print("Order dates")
            for order in order_emp_list:
                print(order)

conn.close()
