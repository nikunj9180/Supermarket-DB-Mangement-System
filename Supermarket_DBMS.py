import mysql.connector
import datetime
# mysql password 
mysqlPass = "password" #<--Enter MySQL Password here

db = mysql.connector.connect(host='localhost',user='root',passwd=mysqlPass)
mycursor = db.cursor()
mycursor.execute("create database if not exists Bigbazar")
db = mysql.connector.connect(host='localhost',user='root',passwd=mysqlPass,database='Bigbazar')
mycursor = db.cursor()
mycursor.execute("CREATE TABLE if not exists Admin(username varchar(50), password varchar(50))")
mycursor.execute("CREATE TABLE if not exists Stock(pcode int PRIMARY KEY, pname varchar(50), quantity int, price int)")
mycursor.execute("CREATE TABLE if not exists Purchase(cust_name varchar(50), cust_number bigint, order_date DATE, total_amnt int )")

def check_pcode(pcode):
    mycursor.execute("Select pcode from Stock where pcode=%s",(pcode,))
    rec = mycursor.fetchall()
    for i in rec:
        a = i[0]
        return(a)


def create_new_stock():
    pcode = int(input("Enter the product code:"))
    prev_code = check_pcode(pcode)
    if prev_code!=pcode:
        pname = input("Enter the name of the product:").upper()
        quantity = int(input("Enter the product quantity:"))
        price = int(input("Enter Product price:"))
        query = "insert into Stock(pcode,pname,quantity,price)values(%s,%s,%s,%s)"
        value = (pcode,pname,quantity,price)
        mycursor.execute(query,value)
        db.commit()
    else:
        print("Already product exist in thi code!! Enter some other code")
        create_new_stock()

def update_quantity():
    upcode = int(input("Enter the product code for updating:"))
    uquantity = int(input("Enter the new quantity of the product:"))
    query = "update stock set quantity=%s where pcode=%s"
    mycursor.execute(query,(uquantity,upcode))
    print("Record updated successfully")
    db.commit()


def update_price():
    upcode = int(input("Enter the product code to be updated:"))
    uprice = int(input("Enter the product price for updating:"))
    mycursor.execute("update stock set price=%s where pcode=%s",(uprice,upcode))
    print("Record update successfully")
    db.commit()

def delete_stock():
    dpcode = int(input("Enter the product code for deleting:"))
    mycursor.execute("delete from stock where pcode=%s",(dpcode,))
    print("Record deleted succesfully")
    db.commit()

def fetchdata():
    mycursor.execute("SELECT * FROM Stock")
    rec = mycursor.fetchall()
    for x in rec:
        print(x)


def stock_menu():
    choice = 'y'
    while choice == 'Y' or choice == 'y':
        print("1. Create a new stock")
        print("2. Update stock quantity")
        print("3. Update stock price")
        print("4. Delete stock")
        print("5. Show data")
        ch = int(input("Enter the choice:"))
        if ch == 1:
            create_new_stock()
        elif ch == 2:
            update_quantity()
        elif ch == 3:
            update_price()
        elif ch == 4:
            delete_stock()
        elif ch == 5:
            fetchdata()
        choice = input("Do you want to continue (y/n)?")
    flow_managemnet()


def signup():
    user_name = input("Enter new user name:")
    paswd = input("Create password:")
    confirmpass = input("Confirm your password:")
    if paswd == confirmpass:
        mycursor.execute("insert into Admin values(%s,%s)",(user_name,paswd))
        db.commit()
        print("Account created succesfuly")
        main_menu()
    else:
        print("Confirm password and password should be same!!")


def login():
    uname = input("Enter your username:")
    pas = input("Enter your password:")
    mycursor.execute("SELECT * FROM Admin")
    rec = mycursor.fetchall()
    login_dic = {}
    for i in rec:
        login_dic[i[0]] = i[1]
    key,value = uname, pas
    a = key in login_dic and value == login_dic[key]
    return a


def decrease(depcode,dequantity):
        upqua="update stock set quantity=quantity-%s where pcode=%s"
        up2=dequantity,depcode
        mycursor.execute(upqua,up2)
        db.commit()

def code_check(pccode):                                         
        cp="select pcode from stock where pcode=%s"
        mycursor.execute(cp,(pccode,))
        rc=mycursor.fetchall()
        for i in rc:
                return(i[0])

def product_availability(bil_quant,pcode):
        mycursor.execute("SELECT * FROM Stock WHERE pcode=%s",(pcode,))
        stav=mycursor.fetchall()
        for k in stav:
                l1=list(k)
                if l1[2]<bil_quant:
                    print("Product unavailable")
                    print("Kindly update the product!!!")
                    stock_menu()

def table_format(text,length):
    if len(text) > length:
        text = text[:length]
    elif len(text)< length:
        text = (text + " " * length)[:length]
    return text


def check_phoneno(cphoneno):
        spn=str(cphoneno)
        if len(spn)==10:
                pass
        else:
                print("Please check the correct no")
                billing()

def check(scpcode):
        wm="select pcode,pname,quantity from stock where pcode=%s and quantity<5"
        mycursor.execute(wm,(scpcode,))
        r=mycursor.fetchall()
        for i in r:
                print(i)
                print("Product quantity less than 5")

def billing():
    amnt = 0
    icount = 0
    dic_bill = {}
    cust_name = input("Enter the name of the customer:")
    cust_num = int(input("Enter the number of the customer:"))
    now=datetime.datetime.now()
    odate=now.strftime("%y-%m-%d")
    ch = 'y'
    while ch == 'y' or ch == 'Y':
        pcode_in = int(input("Enter the product code of item bought:"))
        repcode = check_pcode(pcode_in)
        if pcode_in == repcode:
            mycursor.execute("SELECT * FROM Stock where pcode=%s",(pcode_in,))
            rec = mycursor.fetchall()
            for i in rec:
                print("Name of the product:",i[1])
                print("Price of single unit:",i[3])
            pprice = i[3]
            bil_quantity = int(input("Enter the quantity of item bought:"))
            product_availability(bil_quantity,pcode_in)
            dic_bill[pcode_in] = bil_quantity
            amnt += (bil_quantity*pprice)
            icount += 1
            check(pcode_in)
            decrease(pcode_in,bil_quantity)
        else:
            print("Please check the product code!!!\nProduct is not in list")
        ch = input("Do you want to enter more products (y/n)?:")
    query = "insert into purchase(cust_name, cust_number, order_date, total_amnt)values(%s,%s,%s,%s)"
    value = (cust_name, cust_num, odate, amnt)
    mycursor.execute(query,value)
    db.commit()
    print("DONE BILLING!!")
    choice = input("Do you want to print the bill (y/n)?")
    if choice == 'y' or choice == 'Y':
        mycursor.execute("SELECT * FROM purchase WHERE cust_name=%s",(cust_name,))
        record = mycursor.fetchall()
        for i in record:
            print("The bill for the customer:",i[0])
            print("Customer mobile number:",i[1])
            print("Date of the order:",i[2])
            print("Total payable amount:",i[3])
            print("List of items bought -->")
        l1 = ["Sno","ItemName","Rate","Quantity","Amount"]
        print("*"*125)
        print("* ",end = " ")
        for column in l1:
            print(table_format(column,20), end = " * ")
        print()
        print("*"*125)
        sno = 1
        list1 = []
        l = dic_bill.keys()
        for i in l:
            mycursor.execute('SELECT * FROM Stock where pcode=%s',(i,))
            data = mycursor.fetchall()
            for x in data:
                list2 = [str(sno),str(x[1]),str(x[3]),str(dic_bill[i]),str(x[3]*dic_bill[i])]
                list1.append(list2)
                sno+=1

        for row in list1:
                print("*", end = " ")
                for column in row:
                    print(table_format(column,20), end = " * ")
                print()
        print("*"*125)
        print("Total Amount ->",'\t\t\t\t\t\t\t\t\t\t',amnt)
        print("*"*125)
        print("Thank you for shopping at BIGBAZAR!!")
        user_choice = int(input("Press 1 for main menu or 2 to continue billing:"))
        if user_choice == 1:
            flow_managemnet()
        else:
            billing()

    else:
        print("Thank you for shopping at BIGBAZAR!!")
        user_choice = int(input("Press 1 for main menu or 2 to continue billing:"))
        if user_choice == 1:
            flow_managemnet()
        else:
            billing()



def flow_managemnet():
    print("Welcome to the BIGBAZAR Billing management system!!")
    print("1. Edit Stock")
    print("2. Purchase")
    print("3. Back")
    ch1 = int(input("Enter your choice:"))
    if ch1 == 1:
        stock_menu()
    elif ch1 == 2:
        billing()
    elif ch1 == 3:
        pass
    else:
        print("Wrong input")
        main_menu()

def intro():
    str="BIG BAZAR"
    str1=str.center(80) 
    print(50*'*')
    print(str1)
    print(50*'*')

def main_menu():
    choice = 'y'
    while choice == 'y' or choice == 'Y':
        print("1. Already a user? Login")
        print("2. Create new account")
        print("3. Exit")
        ch = int(input("Enter your choice:"))
        if ch == 1:
            login_check = login()
            if login_check == True:
                flow_managemnet()
            else:
                print("Wrong username or password")
                main_menu()

        elif ch == 2:
            signup()
        elif ch == 3:
            break
        else:
            print("Wrong Input")
            main_menu()


intro()
main_menu()
