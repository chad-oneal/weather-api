from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Reads CSV file, station ID and station name only
stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

# Renders the home page with the stations formatted in HTML
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

# API that returns data complied in Jupyter to return data for one station, date & temperature
@app.route("/api/<station>/<date>")
def station_date_temperature_api(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {'station': station,
            'date': date,
            'temperature': temperature}

# API that returns data complied in Jupyter to return all data for one station
@app.route("/api/<station>/")
def all_data_api(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

# API that returns data for one station for a specified year
@app.route("/api/yearly/<station>/<year>/")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)