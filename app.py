from flask import Flask, render_template, request
from ticketmaster_data import get_data_frame_from_ticketmaster
from seatgeek_data import get_data_frame_from_seatgeek
from stubhub_data import get_data_frame_from_stubhub
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("search.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    
    result_seatgeek = get_data_frame_from_seatgeek(query)
    result_ticketmaster = get_data_frame_from_ticketmaster(query)
    result_stubhub = get_data_frame_from_stubhub(query)

    return render_template("comparison_table.html", template1=render_template("results.html", result=result_ticketmaster.to_dict(orient='records'), tablename='seatgeek'), template2=render_template("results.html", result=result_seatgeek.to_dict(orient='records'), tablename="ticketmaster"),template3=render_template("results.html", result=result_stubhub.to_dict(orient='records'), tablename="stubhub"))

if __name__ == "__main__":
    app.run(debug=True)
