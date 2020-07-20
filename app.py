from flask import Flask, render_template, url_for, flash,session
from flask import request, redirect
import os
import json
from datetime import datetime, timedelta, date
from flask_pymongo import PyMongo





app = Flask(__name__)





app.config["MONGO_URI"] = "mongodb://aniket:Aniketsprx077@cluster0-shard-00-00-uugt8.mongodb.net:27017,cluster0-shard-00-01-uugt8.mongodb.net:27017,cluster0-shard-00-02-uugt8.mongodb.net:27017/hackathon?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)



app.secret_key = 'aniket'									
app.permanent_session_lifetime = timedelta(days = 28)

@app.route('/')
def main():
	return render_template('index.html')



@app.route('/signup')
def signup():
	return render_template("signup.html")

@app.route('/handle_signup', methods=['POST','GET'])
def handle_signup():

	if request.method == 'POST':
		email = request.form['email']
		name = request.form['name']
		password = request.form['password']
		
		if 'remember' in request.form:
			remember = request.form['remember']
		else:
			remember = 'off'
		# remember has two values on and off

		print("email: ", email)
		print("name: ", name)
		print("password: ", password)
		print("remember: ", remember)
		user = {
		'email': email,
		'name' : name,
		'password' : password
		}

		if mongo.db.user.find_one({"email" : email}) != None:
			#account exits
			return redirect(url_for("signup", msg='email_exists', **request.args))
		else:
			#account does not exits
			mongo.db.user.insert_one(user)
			#account created

			
			session['user'] = email

			if remember == 'off':
				session['forget'] = True

			return redirect(url_for('account'))

	else:
		return redirect(url_for('signup'))


@app.route('/login')
def login():
	if 'user' in session:
		return redirect(url_for('account'))
	else:
		return render_template('login.html')

@app.route('/handle_login', methods=['POST', 'GET'])
def handle_login():

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']


		user = mongo.db.user.find_one({'email' : email})
		print('USER: ', user)
		if user == None:
			#no such email
			return redirect(url_for('login', msg='no_such_email', **request.args))
		else:
			if user['password'] != password:
				#wrong password
				return redirect(url_for('login', msg='wrong_password', **request.args))
			else:
				#login success
				print("login success")
				session['user'] = email
				return redirect(url_for('account'))


	
@app.route('/account')
def account():

	if 'user' in session:
		email = session['user']
		if 'forget' in session:
			session.pop('forget', None)
			session.pop('user', None)
		data = mongo.db.user.find_one({"email" : email})
		del data['_id']
		print("DATA: ",data)
		return render_template('account.html', data=json.dumps(data))
	else:
		return redirect(url_for('main'))
           

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('main'))
	
if __name__ == "__main__":
    app.run(debug=True)
