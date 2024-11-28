from flask import Flask, render_template, request, url_for, redirect, make_response, flash, session
import random


app = Flask(__name__)

title = "Cookie baking Session!"



# Not sharing my secret ingredients so easily!


flagval = open("./flag").read().rstrip()
secret_ingredients = open("./secret_ingredients").read().splitlines()
app.secret_key = random.choice(secret_ingredients)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/thekitchen")
def kitchen():
	if session.get("role"):
		check = session["role"]
		if check == "junior_apprentice_chef":
			return render_template("thekitchen.html", title=title)
		else:
			return make_response(redirect("/head_chef_kitchen"))
	else:
		resp = make_response(redirect("/thekitchen"))
		session["role"] = "junior_apprentice_chef"
		return resp

@app.route("/kitchen_entrance", methods=["GET", "POST"])
def checking():
	if "name" in request.form and request.form["name"] in secret_ingredients:
		resp = make_response(redirect("/head_chef_kitchen"))
		session["role"] = request.form["name"]
		return resp
	else:
		message = "Not a valid secret ingredient!"
		category = "danger"
		flash(message, category)
		resp = make_response(redirect("/thekitchen"))
		session["role"] = "junior_apprentice_chef"
		return resp

@app.route("/reset")
def reset():
	resp = make_response(redirect("/"))
	session.pop("role", None)
	return resp

@app.route("/head_chef_kitchen", methods=["GET"])
def flag():
	if session.get("role"):
		check = session["role"]

        # Only the head chef can see the ultimate ingredient!
        
		if check == "head_chef":
			resp = make_response(render_template("flag.html", value=flagval, title=title))
			return resp

		flash("Valid secret ingredient, but you are still not allowed to access the head chef's kitchen...", "success")
		return render_template("not-the-head-chef.html", title=title, role=session["role"])
	else:
		resp = make_response(redirect("/"))
		session["role"] = "junior_apprentice_chef"
		return resp

if __name__ == "__main__":
	app.run()