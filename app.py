from flask import Flask , render_template , request,flash,redirect,url_for,jsonify,session
from Auth.Auth_route import auth_bp
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash , check_password_hash


app= Flask(__name__)

load_dotenv()
#---------------sql---------#
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

print(os.getenv("app_secret_key"))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('con_string')

db=SQLAlchemy(app)

#-----------------MODEL---------#

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(255),nullable=False)


#------------------routes-----------#
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    
    if not session :
        return render_template("base.html")
    return render_template("base.html",username=session["username"])


@app.route("/insert", methods=["POST"])
def add_user():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

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
        password=hashed_password
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
    
@app.route("/login",methods=["GET" , "POST"])
def login():
    
    if request.method == "POST":
            username=request.form.get("username")
            password=request.form.get("password")
            query=db.select(User).filter_by(username=username)
            user=db.one_or_404(query,description="user not found!!")
            
            if not check_password_hash(user.password,password):
                flash("Username or Password is incorrect!!","danger")
                return redirect(url_for("auth.log"))
            
            session["id"]=user.id
            session["username"]=user.username
            session["email"]=user.email
            return render_template("base.html",username=session["username"])
    
    print(session)
    
    return redirect(url_for('auth.log'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    flash(f" not found!! \n {error}","danger")
    return redirect(url_for('log')),404

@app.errorhandler(500)
def server_issue(error):
    flash(f" server issue!! \n {error}","danger")
    return redirect(url_for('log')),404

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)