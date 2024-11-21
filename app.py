from Pro import create_app,db
from Pro.models import User

app = create_app()

with app.app_context():
    db.create_all()
    # Check if the admin user exists
    if not User.query.filter_by(username="admin").first():
        admin_user = User(
            name="Admin", 
            username="admin", 
            password="123489", 
            role=0
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created!")
if __name__=='__main__':
    app.run(debug=True)