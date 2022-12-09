from flask import Flask,request,render_template
import sqlite3
import requests
import pandas as pd
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,"mydb.db")

with sqlite3.connect("mydb.db") as con: # database set up
    con.execute("""CREATE TABLE IF NOT EXISTS Product
    (Category TEXT,
     Descriptions TEXT,
     Price INTEGER, 
     Code TEXT);""") 
    con.commit()

        
app = Flask(__name__)

@app.route('/',methods=['GET','POST']) # develop a route for home page
def home():
    return render_template("home.html")

@app.route('/entry',methods=['GET','POST']) # develop a route for enter product page
def entry():
    return render_template("entry.html")

@app.route('/retrieve',methods=['GET','POST']) # develop a route for data retrieve page
def retrieve():
    return render_template("retrieve.html")

@app.route('/data1',methods=['GET','POST']) # develop a route to uptake the data of user input
def data1():
    with sqlite3.connect('mydb.db') as con: # insert the data into my database after the form is submitted, then return to the home page
        if request.method == "POST":
            con.execute("INSERT INTO Product (Category,Descriptions,Price,Code) VALUES (:Category,:Descriptions,:Price,:Code)", request.form)
        df = pd.read_sql("select * from Product", con)
        print(df) # print the current data table in the terminal
        return render_template("home.html")

@app.route('/data2', methods=['GET','POST']) # develop a route to retrieve data from the database
def result2():
    with sqlite3.connect('mydb.db') as con: # retrieve data of the category as user input and then print out the table
        if request.method == "POST":
            category = request.form.get('C')
            print(category)    
            result = con.execute("SELECT * FROM Product WHERE Category = '%s'" %category)
            if not category or not len(list(result)): # if the user input for category is empty, then return the whole data table. else return related data as user input category.
                result = con.execute("SELECT * FROM Product")
                return render_template("data2.html",data = result)
            else:
                result = con.execute("SELECT * FROM Product WHERE Category = '%s'" %category) 
                return render_template("data2.html",data = result)

app.run(debug=True,port=8080)