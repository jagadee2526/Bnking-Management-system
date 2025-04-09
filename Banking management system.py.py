import mysql.connector as db
con=db.connect(user='root',password='Jagadeesh@123',host='localhost',database='testing')
cur=con.cursor()

def check_user(ac_num,pas):
    cur.execute('select * from table1 where account_number=%s and password=%s',(ac_num,pas))
    return cur.fetchone()

def check_admin(n,p):
    cur.execute('select * from table3 where name=%s and password=%s',(n,p))
    return cur.fetchone()

def new_user():
    print('WELCOME TO BANK OF SPAIN')
    name=input('enter your name:')
    email=input('enter your mail id:')
    number=int(input('enter your mobile number:'))
    account_number=input('create your new account number:')
    password=input('create a strong password:')

    try:
        cur.execute('insert into table1 (name,email,phone_number,account_number,password) values (%s,%s,%s,%s,%s)', (name,email,number,account_number,password))
        con.commit()
        print('Account Created Successfully')
        
    except db.Error as e:
        print(f'error:{e}')

def existing_user():
    print('WELCOME TO BANK OF SPAIN')
    account_number=input('enter your account number:')
    password=input('enter your password:')
    user=check_user(account_number,password)
    if user:
        print("LOGIN SUCCESSFULL")
        user_menu(user)
    else:
        print('invalid account_number or password')

def user_menu(user):
    while True:
        try:
            print('USER_MENU')
            print('1. ACCOUNT DETAILS')
            print('2. CREDIT AMOUNT')
            print('3. DEBIT AMOUNT')
            print('4. TRANSACTION HISTORY')
            print('5. PIN CHANGE')
            print('6. LOGOUT')
            ch=int(input('choose one option:'))
            if ch == 1:
                print(f"\nAccount_Details: \nName: {user[1]} \nEmail: {user[2]} \nPhone: {user[3]} \nAccount_number: {user[4]} \nBalance: {user[6]}")
                print()
            elif ch == 2:
                credit(user[0])
            elif ch == 3:
                debit(user[0])
            elif ch == 4:
                history(user[0])
            elif ch == 5:
                change(user[0])
            elif ch == 6:
                print('Logged out')
                break
            else:
                print('choose valid option')
        except Exception as e:
            print('error:',e)
            
def credit(user_id):
    amount=float(input('Enter amount to deposit:'))
    cur.execute('update table1 set balance=balance+%(amt)s where id=%(idx)s',{'amt':amount,'idx':user_id})
    cur.execute('insert into table2 (user_id,transaction_type,amount) values (%s,"deposit",%s)',(user_id,amount))
    con.commit()
    print('Credited Successfull')

def debit(user_id):
    amount=float(input('enter amount to withdraw:'))
    cur.execute('select balance from table1 where id=%s',(user_id,))
    balance=cur.fetchone()[0]
    if amount <= balance:
        cur.execute('update table1 set balance=balance-%(amt)s',{'amt':amount})
        cur.execute('insert into table2 (user_id,transaction_type,amount) values (%s,"withdraw",%s)',(user_id,amount))
        con.commit()
        print('Withdrawal Successfull')
    else:
        print('insufficiant balance')

def history(user_id):
    cur.execute('select transaction_type,amount,timestamp from table2 where user_id=%s',(user_id,))
    data=cur.fetchall()
    if data:
        print('\nTransaction History:')
        for i in data:
            print(f"{i[0].capitalize()} : {i[1]} on {i[2]}")
    else:
        print('No data found')

def change(user_id):
    pas=input('enter new password:')
    cur.execute('update table1 set password=%s where id=%s',(pas,user_id))
    con.commit()
    print('Pin changed Successfully')
    

def admin():
    userid=input('enter your user id:')
    password=input('enter your password:')
    admin=check_admin(userid,password)
    if admin:
        print('WELCOME MANAGER')
        admin_menu()
    else:
        print('invalid username or password')

def admin_menu():
    while True:
        try:
            print('ADMIN_MENU')
            print('1. VIEW ALL USERS')
            print('2. DELETE A USER')
            print('3. VIEW ALL TRANSACTIONS')
            print('4. USER DETAILS')
            print('5. USER TRANSACTIONS')
            print('6. DAY TRANSACTIONS')
            print('7. LOGOUT')
            ch=int(input('choose one option:'))
            if ch == 1:
                view_users()
            elif ch == 2:
                delete_user()
            elif ch == 3:
                view_all_history()
            elif ch==4:
                particular_user()
            elif ch == 5:
                user_id=int(input('enter your user id:'))
                history(user_id)
            elif ch == 6:
                day_transaction()
            elif ch == 7:
                print('logged out')
                break
            else:
                print('select valid option from above')
        except Exception as e:
            print('error:',e)
            

def view_users():
    cur.execute('select id,name,email,account_number,balance from table1')
    users=cur.fetchall()
    if users:
        for i in users:
            print(f"Id: {i[0]}, Name: {i[1]}, Email: {i[2]}, Account_No: {i[3]}, Balance: {i[4]}")
    else:
        print('No users found')

def delete_user():
    user_id=int(input('enter user id to delete:'))
    cur.execute('select name from table1 where id=%s',(user_id,))
    name=(cur.fetchone()[0]).upper()
    cur.execute('delete from table2 where user_id=%s',(user_id,))
    cur.execute('delete from table1 where id=%s',(user_id,))
    con.commit()
    print(f"Accout Deleted Successfully for the User : {name}")


def view_all_history():
    cur.execute('select * from table2')
    data=cur.fetchall()
    if data:
        for i in data:
            print(f"Id: {i[1]}, Type: {i[2]}, Amount: {i[3]}, Date: {i[4]}")
    else:
        print('No Transactions found')

def particular_user():
    name=input('enter the customer name:')
    cur.execute('select * from table1 where name=%s',(name,))
    user = cur.fetchone()
    if user:
            print(f"Id: {user[0]}, Name: {user[1]}, Email: {user[2]}, Phone: {user[3]}, Account: {user[4]}, Balance: {user[6]}")
    else:
        print('no user found')

def day_transaction():
    date=input('enter the date:')
    cur.execute('select * from table2 where date(timestamp)=%s',(date,))
    data=cur.fetchall()
    if data:
        for i in data:
            print(f"Id: {i[1]}, Type: {i[2]}, Amount: {i[3]}, Date: {i[4]}")
            
    else:
        print('No Transactions Found')
        
      
def user():
    while True:
        try:
            print('1. NEW USER')
            print('2. EXISTING USER')
            print('3. EXIT')
            ch=int(input('enter one option:'))
            if ch == 1:
                new_user()
            elif ch == 2:
                existing_user()
            elif ch == 3:
                print('exiting')
                break
            else:
                print('choose valid option:')
        except Exception as e:
            print('error:',e)

def main():
    while True:
        try:
            print('BANK OF SPAIN')
            print('1. USER')
            print('2. ADMIN')
            print('3. EXIT')
            ch=int(input('choose one option:'))
            if ch == 1:
                user()
            elif ch == 2:
                admin()
            elif ch == 3:
                print('logged out')
                break
            else:
                print('choose valid option:')
        except Exception as e:
            print('error:',e)

if __name__== '__main__':
    main()


#table1=id,name,email,phone_number,account_number,password,balance,created at
#table2=id,user_id,transaction_type,amount,timestamp
#table3=id,name,password
