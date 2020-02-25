from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

user = {}
admin = {}

user['user@gmail.com'] = 'password'
admin['admin@gmail.com'] = 'password'

app = Flask(__name__)
global active
global email
global visit
global location
global status
global courier
status = {
    'courier1' : 'reached',
    'courier2' : 'out for delivery',
    'courier3' : 'dispatched'
}
location = {
    'courier1' : 'Chennai',
    'courier2' : 'Bangalore',
    'courier3' : 'Coimbatore'
}
active = None
visit = 0
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    global active
    global email
    if request.form['choice'] == 'user':
        if request.form['username'] in user and user[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home.html',email=active)

    elif request.form['choice'] == 'admin':
        if request.form['username'] in admin and admin[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home.html',email=active)

@app.route('/home',methods = ["POST"])
def home_page():
    global visit
    visit = visit + 1
    if request.form['submit_button'] == 'View visits':
        return render_template('visitors.html', v=visit)
    if request.form['submit_button'] == 'Log out':
        return logout()
    if request.form['submit_button'] == 'Contact':
        return render_template('contact.html')

@app.route('/contactexp',methods=["GET"])
def contactexp():
    return render_template('contactexp.html')

@app.route('/imgvideos',methods=["GET"])
def imgvideos():
    return render_template('imgvideos.html')

@app.route('/visitors',methods = ["POST"])
def visitors():
    if request.form['submit_button'] == 'For package details':
        return render_template('details.html')

@app.route('/details',methods = ["POST"])
def details():
    global courier
    courier = request.form['courier']
    l = location[courier]
    s = status[courier]
    if request.form['submit_button'] == 'Get Details':
        return "Location & Status of the package are : "+l+" and "+s

@app.route('/error')
def err():
    flash("Wrong password entered")
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    global active
    active = None
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=3600)