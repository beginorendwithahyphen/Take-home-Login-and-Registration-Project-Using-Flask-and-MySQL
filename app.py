from flask import Flask, render_template, session, request, redirect
import sqlite3
import os
app = Flask(__name__)
app.secret_key="Better to have than to not"
db_name="name_of_database.db"
def get_db_connection():
   conn = sqlite3.connect(db_name)
   conn.row_factory=sqlite3.Row
   return conn
with get_db_connection() as conn:
   cursor=conn.cursor()
   cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)""")
   conn.commit()
@app.route('/index')
def index():
	return render_template("/index.html")
@app.route('/login',methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		username=request.form.get("username")
		password=request.form.get("password")
		conn=get_db_connection()
		cursor=conn.cursor()
		cursor.execute("" "SELECT username from users WHERE username=? AND password =?",(username,password))
		user=cursor.fetchone()
		conn.close()
		if user:
			session["username"]=username
			return render_template("/index.html",user="")
		else:
			return render_template("/login.html",message="Incorrect name or password.")
	return render_template("login.html",user="")
@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=='POST':
		username=request.form.get("username")
		password=request.form.get("password")
		confirm_password=request.form.get("confirm-password")
		if password != confirm_password:
			return render_template("/register.html",message="Password does not match confirm password")
		conn=get_db_connection()
		cursor=conn.cursor()
		cursor.execute("SELECT username from users WHERE username=?",(username,))
		if cursor.fetchone():
			conn.close()
			return render_template("/register.html",message="Username already in use")
		cursor.execute("INSERT INTO users(username,password) VALUES (?,?)", (username,password))
		conn.commit()
		conn.close()
		session[username]=username
		return render_template("/index.html",user="")
	return render_template("/register.html")
@app.route("/")
def none():
	return render_template("/index.html")
@app.route("/logout")
def logout():
	session.pop("user", None)
	return render_template("/register.html")
if __name__ == "__main__":
    app.run(debug=True)