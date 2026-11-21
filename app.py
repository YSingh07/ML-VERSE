from flask import Flask , render_template , request,flash,redirect,url_for,jsonify,session

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash , check_password_hash

from Auth.Auth_route import auth_bp
from Projects.project_routes import project_bp

from model.project_db import MLWiki
from model.user_db import User
from database.database import db

app= Flask(__name__)

load_dotenv()
#---------------sql---------#
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

print(os.getenv("app_secret_key"))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('con_string')

db.init_app(app)






#------------------routes-----------#
app.register_blueprint(auth_bp)

app.register_blueprint(project_bp)

@app.route("/")
def home():
    
    return redirect(url_for("project_page.wiki_list"))

#----------register_route------------------
@app.route("/insert", methods=["POST"])
def add_user():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    role = request.form.get("role")

    # Validate username
    if not username:
        flash("Username required!", "danger")
        return redirect(url_for("auth.reg"))

    # Validate email
    if not email:
        flash("Email required!", "danger")
        return redirect(url_for("auth.reg"))

    # Validate password
    if not password:
        flash("Password required!", "danger")
        return redirect(url_for("auth.reg"))

    # Check password confirmation
    if password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect(url_for("auth.reg"))

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create user object
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )

    try:
        db.session.add(user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for("auth.reg"))

    except Exception as e:
        db.session.rollback()
        print("Registration error:", e)

        flash("Registration failed. Username may already exist.", "danger")
        return redirect(url_for("auth.reg"))
    
#------------login---------------------------
    
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        # Check whether user exists
        if user is None:
            flash("Username or password is incorrect!", "danger")
            return redirect(url_for("auth.log"))

        # Check password
        if not check_password_hash(user.password, password):
            flash("Username or password is incorrect!", "danger")
            return redirect(url_for("auth.log"))

        # Store user details in session
        session.clear()
        session["id"] = user.id
        session["username"] = user.username
        session["email"] = user.email
        session["role"] = user.role

        flash("Login successful!", "success")
        return redirect(url_for("home"))

    return redirect(url_for("auth.log"))

#------------------logout----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

#---------------not_found---------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

#----------------server_error-------------
@app.errorhandler(500)
def server_issue(error):
    flash(f" server issue!! \n {error}","danger")
    return redirect(url_for('home')),500


#--------------run_app--------------------
if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)