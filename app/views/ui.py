from flask import current_app, render_template

@current_app.route("/")
def home():
    
    return render_template("index.html"), 200