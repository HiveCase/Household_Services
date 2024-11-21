from flask_login import UserMixin
from . import db
from flask import current_app
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String)
    role = db.Column(db.Numeric())
    address = db.Column(db.String)
    pincode = db.Column(db.String)

    # @staticmethod
    # def create_dummy_admin():
    #     with current_app.app_context():
    #         if User.query.filter_by(username='admin').first is None:
    #             admin_user = User(name='Administrator', username='admin',password='123489',role=0)
    #             db.session.add(admin_user)
    #             db.session.commit()
    #             print('Admin Created')
    #         else:
    #             print('Admin User already present')
class Service(db.Model):
    __tablename__ ='service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(500))
    base_price = db.Column(db.Float)
    time_required = db.Column(db.String(50))  # Example: "30 mins", "2 hours"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Assigned professional
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(20), default='requested')  # requested/assigned/closed
    remarks = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)  # Rating provided by the customer

    # Relationships
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_requests')
    professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_requests')


class Review(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    service_request = db.relationship('ServiceRequest', backref='reviews')
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_reviews')
    professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_reviews')


