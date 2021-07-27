from flask import render_template

class Home:
    def homePage(self):
        return render_template("home.html")