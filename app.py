from flask import *
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
from functions import *

app = Flask(__name__)
app.secret_key = "kddjhdkvudhdjsdjpms"

@app.route('/')
def home():
    
    return render_template("home.html")


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        email = request.form["email"]
        photo = request.files["photo"]
        photo.save("static/images/" + photo.filename)
        photo_name = photo.filename
        password = request.form["password"]
        password2 = request.form["password2"]
        hashed_password = hash_salt_password(password)


        if len(password) <8:
            return render_template("register.html", error = "Password is too short")
        elif password != password2:
            return render_template("register.html", error = "Passwords do not match")
        else:
            connection = pymysql.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
            )
            cursor = connection.cursor()
            # sql = "select * from users where username = ? and email =?"
            # cursor.execute(sql, (username, email))
            # username = cursor.fetchone()
            
            sql = "Insert into users(username, email, photo_name, password) values(%s, %s, %s, %s)"
            cursor.execute(sql, (username, email, photo_name, hashed_password))
            connection.commit()

            if request.method == "POST":
                session['key'] = username
                return redirect('/')
            else:
                return render_template("register.html", error = "Username already exists")

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hash_salt_password(password)


        connection = pymysql.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
        )
        
        cursor = connection.cursor()
        sql = "select * from users where username = %s and password = %s"
        cursor.execute(sql, (username, hashed_password))

        if cursor.rowcount == 0:
            return render_template("login.html", message = "Invalid credentials!!")
        else:
            session['key'] = username
            return redirect('/')
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if "__main__" == __name__:
    app.run(debug=True)