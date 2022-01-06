# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up flask
app = Flask(__name__)

# Use flask_pymongo to set up a mongo connection
# tells python our app will connect to ongo using a URI
# this is the URI we will be using 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

# create a flast route 
@app.route('/')
def index():
    # use pymongo to find the 'mars'collection in oru db
    # assign it to the mars db for later
    mars = mongo.db.mars.find_one()

    # tells flask to return html template using an index html file
    return render_template("index.html".mars=mars)


@app.route("/scrape")
def scrape(): 
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code302)

if __name__ == "__main__":
   app.run()