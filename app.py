from flask import Flask, render_template, request, Response
from ticketmaster_data import get_data_frame_from_ticketmaster
from seatgeek_data import get_data_frame_from_seatgeek
from stubhub_data import get_data_frame_from_stubhub
import requests
from flask_cors import CORS, cross_origin
from json import dumps
import pandas as pd
# import flask

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("search.html")

@app.route("/search")
@cross_origin()
def search():
    query = request.args.get("query")
    
    result_seatgeek = get_data_frame_from_seatgeek(query).to_dict(orient='records')
    result_ticketmaster = get_data_frame_from_ticketmaster(query).to_dict(orient='records')
    result_stubhub = get_data_frame_from_stubhub(query).to_dict(orient='records')
    data = {'result_seatgeek': result_seatgeek, 'result_ticketmaster': result_ticketmaster, 'result_stubhub': result_stubhub}
    
    return Response(dumps(data, default=str))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
