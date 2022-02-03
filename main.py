from sqlite3 import Cursor
import MySQLdb
from flask import Flask, redirect, render_template,request,session
from flask_mysqldb import MySQL
import mysql.connector as sql_db
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'
mysql = MySQL(app)
conn = sql_db.connect(host = "localhost", user= "root", password = "", database = "users")
cursor = conn.cursor()
@app.route('/')
def login():
    if 'user_id' in session:
    
        return redirect('/home')
    else:
        return render_template('login.html')
        




@app.route('/register')
def about():
    
    return render_template("register.html")


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

      

@app.route('/login_validation', methods=['POST'])


def login_validation():

    email = request.form.get('email')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM `userbd` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
    .format(email,password))
    users = cur.fetchall()
    
    
    if len(users)>0:
        session['user_id']=users[0][0]
        
        return redirect('/home')

    else:
        return redirect('/')

@app.route('/add_user',methods=['POST'])  
def add_user():
    name = request.form.get('uname') 
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cur = mysql.connection.cursor()
    cursor.execute("""INSERT INTO `userbd` (`user_id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `userbd` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id']=myuser[0][0]

    return redirect('/home')

@app.route('/logout')  
def logout():
    session.pop('user_id')  
    return redirect('/')
    


if __name__ == "__main__":
    app.run(debug=True)