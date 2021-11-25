import sqlite3
from sqlite3.dbapi2 import Error

# Create connection with databse with sqlite3
# db_file is file name
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# Insert one new customer with name and email
def add_customer(name, email):
    database = r"betsy.db"
    #Create connection with database
    conn = create_connection(database)
    #Oopen the cursor
    cursor = conn.cursor()

    sql = 'insert into customer (customer_id, name, email) values (null, ?, ?)'
    #Execute the sql statement
    cursor.execute(sql, (name, email))
    #Commit the execution
    conn.commit()
    #Close the connection
    conn.close()

# Select one customer by name
def check_customer_by_name(name):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql = 'select * from customer where name = ?'
    cursor.execute(sql, (name,))
    conn.commit()
    customer = cursor.fetchone()
    conn.close()
    if (customer==None):
        return False
    else:
        return True

# Select one customer by email
def check_customer_by_email(email):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql = 'select * from customer where email = ?'
    cursor.execute(sql, (email,))
    conn.commit()
    customer = cursor.fetchone()
    conn.close()
    if (customer==None):
        return False
    else:
        return True

# Create on new order by customer name, order number, create time, type of table and arrival time
def add_order(customer_name, order_number, create_time, type_of_table, arrival_time):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql1 = 'select customer_id from customer where name=?'
    cursor.execute(sql1, (customer_name,))
    conn.commit()
    customer_id = cursor.fetchone()[0]
    sql2 = 'insert into book_order (order_id, customer_id, order_number, create_time, type_of_table, arrival_time) values (null, ?, ?, ?, ?, ?)'
    cursor.execute(sql2, (customer_id, order_number, create_time, type_of_table, arrival_time))
    conn.commit()
    conn.close()

# Select one order by order number
def select_order_by_number(order_number):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql = 'select bo.create_time, bo.type_of_table, bo.arrival_time, d.dish_name FROM ordered_dish od INNER JOIN book_order bo ON od.order_number=? INNER JOIN dish d ON od.dish_id=d.dish_id'
    cursor.execute(sql, (order_number,))
    conn.commit()
    order = cursor.fetchone()
    conn.close()
    return order

# Select dishes by style, flavor and if special
def select_dishes(style, flavor, if_special):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql = 'select dish_name, price, order_times from dish where style=? and flavor=? and special_dish=?'
    cursor.execute(sql, (style, flavor, if_special,))
    conn.commit()
    dishes = cursor.fetchall()
    conn.close()
    return dishes

# Select dishes by if special
def select_dishes_by_if_special(if_special):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql = 'select dish_name, price, order_times, style from dish where special_dish=?'
    cursor.execute(sql, (if_special,))
    conn.commit()
    dishes = cursor.fetchall()
    conn.close()
    return dishes

# Select dishes by style
def select_dishes_by_style(style, if_special):
    database = r"betsy.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    sql = 'select dish_name, price, order_times from dish where style=? and special_dish=?'
    cursor.execute(sql, (style, if_special,))
    conn.commit()
    dishes = cursor.fetchall()
    conn.close()
    return dishes

# if __name__ == '__main__':
#     print(check_customer_by_name("yjq"))
    # add_customer("yjx", "1347256906@qq.com", "12345")
    # add_order(1, "000001", "2021-11-13 12:34:56", 3, "2021-11-14 12:00:00", "Beijing coast duck")
    # print(select_order_by_number("000001"))
    # select_order_by_number("000001")
    # print(show_dish_if_special(1))