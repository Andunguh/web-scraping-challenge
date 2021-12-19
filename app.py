# imports
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# use flask pymongo to set up the connection to the database
print('hello')

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

print('hello')

@app.route("/")
def index():
    # access information from the database
    print('hello')
    mars_data = mongo.db.marsData.find_one()
    print('hello')
    #print(mars_data)
    return render_template("index.html", mars=mars_data)

    #return "you reached the index"



@app.route("/scrape")

def scrape():

    # refrence to the database collection (table)
    marsTable = mongo.db.marsData

    # drop the table if it exists

    mongo.db.marsData.drop()

    # test to call scrape mars script
    mars_data = scrape_mars.scrape_all()

    # take the dict and load into mongoDB

    marsTable.insert_one(mars_data)

    # go back to the index route

    return redirect("/")


if __name__ == "__main__":
    app.run()