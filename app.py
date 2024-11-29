from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

def create_con():
    log= sqlite3.connect("login.db")
    return log


def create_tables():
    log=create_con()
    cure = log.cursor()
    cure.execute('CREATE TABLE IF NOT EXISTS login(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,number TEXT)')
    log.commit()
    log.close()
    
def create_dash():
    dash= sqlite3.connect("dashboard.db")
    return dash


def create_dashtables():
    dash=create_dash()
    board = dash.cursor()
    board.execute('CREATE TABLE IF NOT EXISTS dashboard(id INTEGER PRIMARY KEY AUTOINCREMENT,expenditure TEXT,amount TEXT)')
    dash.commit()
    dash.close()



@app.route('/')
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the login form
        name_input = request.form['email']
        number_input = request.form['password']

        # Connect to the database
        log = create_con()
        cure = log.cursor()

        # Query the database to find a matching record
        cure.execute("SELECT * FROM login WHERE name = ? AND number = ?", (name_input, number_input))
        result = cure.fetchone()  # Fetch a single matching record

        log.close()
        print(name_input, number_input)

        # If a match is found, render the home page
        if result:
            return render_template("dashboard.html")
        else:
            
            return render_template("login.html")

    # Render the login page if the request method is GET
    return render_template("login.html")

@app.route("/register", methods=['GET','POST'])
def registation():
    if request.method == 'POST':
        name1=request.form['email1']
        num2=request.form['password1'] 
        key2=request.form['key'] 
        log= create_con()
        cure=log.cursor()
        cure.execute('''INSERT INTO login(name , number,key)VALUES(?,?,?)''',(name1,num2,key2)) 
        log.commit()
        log.close()
        print(name1,num2)
    return render_template("register.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        dash1=request.form['expense_name']
        dash2=request.form['expense_amount'] 
        dash= create_dash()
        board=dash.cursor()
        board.execute('''INSERT INTO dashboard(expenditure , amount)VALUES(?,?)''',(dash1,dash2)) 
        dash.commit()
        dash.close()
        print(dash1,dash2)
    return render_template("dashboard.html")



if __name__ == '__main__':
    create_tables()
    create_con()
    create_dashtables()
    create_dash()
  
    app.run(debug=True)
