# Import dependencies
from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import pymongo
import pymongo

# Initialize app
app = Flask(__name__)

# Connect to the database
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create/connect to a mars_db and a mars collection
db = client.mars_db
mars = db.mars

# First route
@app.route("/")
def main():
    data = mars.find_one()
    return(render_template("index.html", dict = data))

# Scrape function
@app.route("/scrape")
def scrape():
    # Define a variable to hold scraped data
    mars_data = scrape_mars.scrape_data()

    # Update the mars db with the scraped data
    mars.update({}, mars_data, upsert=True)

    # Redirect back to the main page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)