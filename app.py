import MySQLdb
import flask
import yaml
from flask import Flask, render_template, session, redirect, request, flash, url_for
from flask_mysqldb import MySQL
import os

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'tajni_kljuc'

db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/base/')
def base():
    return render_template('base.html')


@app.route('/contact/')
def contact():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments")
    appointments = cur.fetchall()
    cur.close()

    return render_template('contact.html', appointments=appointments)



@app.route('/contact/', methods=['POST'])
def add_appointment():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        vehicle_id = request.form['vehicle_id']
        service_id = request.form['service_id']
        appointment_date = request.form['appointment_date']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO appointments (customer_id, vehicle_id, service_id, appointment_date) VALUES (%s, %s, %s, %s)",
                    (customer_id, vehicle_id, service_id, appointment_date))
        mysql.connection.commit()
        cur.close()

        flash('Appointment added successfully!', 'success')
        return redirect('/contact/')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments")
    appointments = cur.fetchall()
    cur.close()

    return render_template('contact.html', appointments=appointments)




@app.route('/customers/')
def customers():

    db = MySQLdb.connect(host='localhost', user='root', passwd='petar', db='car_service_db')
    cur = db.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    cur.close()
    db.close()


    return render_template('customers.html', customers=customers)


@app.route('/service/')
def view_service():
    db = MySQLdb.connect(host='localhost', user='root', passwd='petar', db='car_service_db')
    cur = db.cursor()

    cur.execute("SELECT * FROM service")
    rows = cur.fetchall()
    cur.close()
    db.close()

    return render_template('services.html', rows=rows)





@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        terms = request.form.get('terms')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('registration.html')

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash('Email already exists. Please enter another email.', 'danger')
            return render_template('registration.html')

        cur.execute("INSERT INTO user (username, password, email, name) VALUES (%s, %s, %s, %s)",
                    (username, password, email, name))

        mysql.connection.commit()
        cur.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect('/login/')

    return render_template('registration.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and password == user[2]:
            session['username'] = username
            return redirect('/profile/')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect('/login/')

    return render_template('login.html')



@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,username,password,email,name,photo FROM user WHERE username = %s", (username,))
        user_tuple = cur.fetchone()

        if request.method == 'POST':


            cur.execute("SELECT id, username, password, email, name,  photo FROM user WHERE username = %s", (username,))
            user_tuple = cur.fetchone()

        cur.close()

        if user_tuple:
            user = {
                'email': user_tuple[3],
                'username': user_tuple[1],
                'name': user_tuple[4],
                'photo': user_tuple[5],
                'password': user_tuple[2]
            }
            return render_template('profile.html', user=user)
        else:
            flash('User not found.', 'danger')
            return redirect('/login/')
    else:
        return redirect('/login/')

from flask import flash, redirect

@app.route('/change_password', methods=['POST'])
def change_password():
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect('/profile')

    hashed_password = generate_password_hash(new_password)

    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE user SET password = %s WHERE username = %s", (hashed_password, username))
    mysql.connection.commit()
    cur.close()

    flash('Password updated successfully!', 'success')
    return redirect('/profile')



@app.route('/logout')
def logout():
    session.clear()

    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
