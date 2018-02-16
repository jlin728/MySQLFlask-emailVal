from flask import Flask, render_template, request, redirect, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key="SecretKeyPassword"
# connect and store the connection in "mysql"; note that you pass the database name to the function i.e. replace 'flasksql'
mysql = MySQLConnector(app, 'emailVal')

# an example of running a query
# print mysql.query_db('SELECT * FROM users')

@app.route('/')
def index():
    query = 'SELECT * FROM users'                             # define your query
    users = mysql.query_db(query)                             # run query with query_db()
    return render_template('index.html', all_users=users)     # pass data to our template

@app.route('/validate', methods=['POST'])
def validate():
    query = 'SELECT * FROM users'
    users = mysql.query_db(query)
    if len(request.form['email']) < 1:
        flash('Email cannot be empty')
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid Email')
        print "purple"
        return redirect('/')
    else:
        exist = False
        for i in users:
            if i['email'] == request.form['email']:
                exist = True
                break
        if exist:
            flash("Email Already Exists")
            return redirect('/')
        else:
            query = 'INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW())'
            data = {
                'email': request.form['email']
            }
            mysql.query_db(query, data)
            session['email'] = request.form['email']
            print '2'
            return redirect('/success')

@app.route('/success')
def success():
    print "blue"
    query = 'SELECT * FROM users'
    users = mysql.query_db(query)
    print "blick"                                                      
    return render_template('success.html', email=session['email'], all_users=users)

@app.route('/remove', methods=['POST'])
def delete():
    users = mysql.query_db(query)
    query = "DELETE FROM users WHERE id = :id"
    data = {'id': users.id}
    mysql.query_db(query, data)
    return redirect('/success')

@app.route("/remove/<id>", methods=["POST"])
def remove(id):
	query = "DELETE FROM users (id, email, created_at, updated_at) VALUES({}, :email, NOW(), NOW());".format(id)
	mysql.query_db(query, request.form)
	return redirect("/user/{}".format(id))


    user = mysql.query_db("SELECT * FROM users WHERE id={};".format(id))
	users = mysql.query_db("SELECT * FROM users;")
	delete = mysql.query_db("DELETE email, users.created_at, users.updated_at WHERE users.id = {};".format(id))

app.run(debug=True) # run our server