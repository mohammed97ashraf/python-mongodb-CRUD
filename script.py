from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import string 
import random

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'User'
app.config['MONGO_URI'] = 'mongodb+srv://Ashraf:test123@cluster0.wdux0.mongodb.net/User?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('bookingpage.html')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'email' : request.form['email'] ,'mobile' : request.form['mobile'],'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route("/newbooking")  
def new():  
    return render_template("newbooking.html") 


def get_random_string(length):
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length)) 
    return result_str

@app.route('/newbooking',methods=['POST'])
def booking():
    if request.method == 'POST':
        dbname = session['username']
        bookings = mongo.db
        bookings = bookings[dbname]
        bookingID = get_random_string(8)
        date = request.form['date']
        frm  = request.form['from']
        to   = request.form['To']
        cabtype =  request.form['cars']
        bookings.insert({'bookingid':bookingID,'date':date,'from':frm,'to':to,'cabtype':cabtype})
        return render_template('bookingpage.html')
    return ''

@app.route('/view')
def view(): 
    dbname = session['username']
    bookings = mongo.db
    booking = bookings[dbname]
    rows = booking.find()
    return render_template('view.html',rows = rows)

@app.route("/deletebooking")  
def deletefunc():  
    return render_template("deletebooking.html") 

@app.route('/deletebooking',methods=['POST'])
def delete():
    if request.method == 'POST':
        dbname = session['username']
        bookings = mongo.db
        bookings = bookings[dbname]
        bid = request.form['id']
        bookings.remove( {'bookingid':bid} )
        return   render_template('delete.html', bid = bid)
    return 'id not found'

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=False)
