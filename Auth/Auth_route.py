from flask import Flask , Blueprint , url_for ,render_template,session

auth_bp = Blueprint(
    "auth", 
    __name__,
    template_folder="templates",
    url_prefix="/authenticate" 
)

@auth_bp.route("/")
def log():
    return render_template("login.html",username=session.get("username"),role=session.get("role"))

@auth_bp.route("/register")
def reg():
    return render_template("register.html",username=session.get("username"),role=session.get("role"))