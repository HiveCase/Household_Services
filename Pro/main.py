from flask import Blueprint,render_template,request,redirect,url_for,Flask,abort,flash
from __init__ import db 
from models import User,Service,ServiceRequest,Review
from flask_login import login_required,current_user

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')
