from flask import Blueprint
from model.home import Home

home = Blueprint("home", __name__)

homeObj = Home()

home.add_url_rule("/", view_func=homeObj.homePage, methods=['GET'])