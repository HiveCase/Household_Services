from flask import Blueprint, render_template,redirect,url_for,request,flash,session
from . import db
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
import re
from werkzeug.utils import secure_filename
import os

auth = Blueprint("authentication",__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static/docs')
ALLOWED_EXTENSIONS = {'pdf'}

############################  Customer Signup   #################################
@auth.route('/cust-signup',methods=['GET','POST'])
def customer_register():
    if request.method=='POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash("Username exists!!",category='error')
        if len(password)<5:
            flash('Enter Strong Password',category='error')
        else:
            newUser = User(name=name,username=username,password=password,role=1,address=address,pincode=pincode)

            db.session.add(newUser)
            db.session.commit()
    return render_template('signup.html')


#######################################################################
@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        docname = None
        if 'pdf' in request.files:
            file = request.files['pdf']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER,filename))
                docname = filename
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash("Username exists!!",category='error')
        if len(password)<5:
            flash('Enter Strong Password',category='error')
        else:
            newUser = User(name=name,username=username,password=password,role=role,docname=docname)

            db.session.add(newUser)
            db.session.commit()

            login_user(newUser,remember=True)
            flash('User Created')
            return render_template('login.html',user=current_user)
    return render_template('signup.html',user=current_user)
#############################################################
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if (user.password == password):
                if user.role == 0:
                    login_user(user,remember=True)
                    return redirect('/admin_dashboard')
                elif user.role == 1:
                    login_user(user,remember=True)
                    return redirect(url_for('main.user_profile'))
                else:
                    login_user(user,remember=True)
                    return redirect(url_for('main.user_profile'))
        else:
            flash('Username does not exists',category='error')
    return render_template('login.html',user=current_user)


###################################        Admin          ##########################
@auth.route('/admin',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('username')=='admin':
            if request.form.get('password')=='123489':
                render_template('admin_dashboard.html')


#############################################################
@auth.route('/professional_register',methods=['GET','POST'])
def pro_register():
    return render_template('pro-register.html')

####################################    Profile           #########################
@auth.route('/profile',methods=['GET','POST'])
def profile():
    return render_template('profile.html')


#############################################################
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')