from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import pymongo
import pymongo

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db
mars = db.mars

@app.route("/")
def main():
    data = mars.find_one()
    return(render_template("index.html", dict = data))

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_data()

    mars.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)