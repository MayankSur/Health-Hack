from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)
app.secret_key ="ICHACK_2020"
from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.debug = True

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
	if request.method=="POST":
		user = request.form["nm"]
		session["user"] = user
		flash("Login Succesful!")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash("Already logged in")
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/user")
def user():
	if "user" in session:
		user = session["user"]
		return render_template("user.html",user=user)
	else:
		flash("You Are not logged in")
		return redirect(url_for("login"))

@app.route("/tests")
def tests():
	if "user" in session:
		return render_template("tests.html")
	else:
		flash("You Are not logged in")
		return redirect(url_for("login"))

@app.route("/gp")
def gp():
	if "user" in session:
		return render_template("gp.html")
	else:
		flash("You Are not logged in")
		return redirect(url_for("login"))		

@app.route("/logout")
def logout():
	if "user" in session:
		user = session["user"]
		flash(f"You have been logged out, {user}!", "info")
	session.pop("user",None)
	return redirect(url_for("login"))

if __name__=="__main__":
     app.run(debug=True)