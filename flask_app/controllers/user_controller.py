from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models import user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route('/')
def home():
    return render_template ('index.html')


@app.route('/success')
def success():
    if not 'id' in session:
        flash("Please Log In.")
        return redirect ('/')

    data={
        "id":session['id']
    }

    user=user_model.User.find_by_id(data)
    
    return redirect ('/dashboard')

@app.route('/register', methods=['POST'])
def register():

    if not user_model.User.validate_register(request.form):
        return redirect('/')

    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password'],
        'confirm_password':request.form['confirm_password']
    }
    
    user_model.User.create(data)

    user=user_model.User.find_by_email(request.form)
    session['id']=user.id
    session['first_name']=user.first_name

    return redirect ('/success')

@app.route('/login', methods=['POST'])
def login():

    if user_model.User.validate_login(request.form):

        user=user_model.User.find_by_email(request.form)
        session['id']=user.id
        session['first_name']=user.first_name

        return redirect ('/dashboard')
    else:
        return redirect ('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')