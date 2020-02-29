from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)
app.secret_key ="ICHACK_2020"

user_names=["Ivan"]
user_password=["1hjnf4dpdjl"]

@app.route("/")
def home():
	return render_template("login1.html")

@app.route("/login",methods=["POST","GET"])
def login():
	if request.method=="POST":
		user_test = request.form["nm"]
		password_test = request.form["ps"]
		if user_test==user_names[0] and password_test==user_password[0]:
			session["user"] = user_test
			return render_template("general.html",user=user_test)
		else:
			flash("Wrong username or password! Try again!")
			return render_template("login1.html")
	else:
		if "user" in session:
			flash("Already logged in")
			return redirect(url_for("user"))
		return render_template("login1.html")

@app.route("/general")
def general():
	user=session["user"]
	return render_template("general.html",user=user)

@app.route("/info")
def info():
	user=session["user"]
	return render_template("info.html",user=user)

@app.route("/tests")
def tests():
	user=session["user"]
	return render_template("tests.html",user=user)

@app.route("/settings")
def settings():
	user=session["user"]
	return render_template("settings.html",user=user)

@app.route("/logout")
def logout():
	session.pop("user",None)
	return render_template("login1.html")

if __name__=="__main__":
     app.run(debug=True)