from flask import Flask, render_template, request, redirect
import DataCollection
from geojson import Feature, FeatureCollection, Point
import json
import time

global test

app = Flask(__name__)
@app.route('/', methods = ["POST","GET"])
def test():
    if request.method == "POST":
        start = time.perf_counter()
        Name = request.form["name"]
        with open('data/Data_List.txt') as f:
            lines = f.readlines()
        lines = lines[0]
        names = lines.split(',')
        if Name in names or ',' in Name:
            return render_template("Invalid_name_page.html")


        FlightDistance = str(request.form["flightDistance"])
        shape = json.loads(request.form["shape"])
        Flights = False
        if len(shape["features"]) == 1 and shape["features"][0]["geometry"]["type"] == "Polygon":
            Flights = False
        elif len(shape["features"]) == 2 and shape["features"][0]["geometry"]["type"] == "Polygon" and shape["features"][1]["geometry"]["type"] == "Point":
            Flights= True
        elif len(shape["features"]) == 2 and shape["features"][1]["geometry"]["type"] == "Polygon" and shape["features"][0]["geometry"]["type"] == "Point":
            Flights = False
        else:
            return render_template("test2.html")
        DataCollection.main(shape,Flights,FlightDistance,Name)
        with open('data/Data_List.txt', 'a') as f:
            f.write(","+ str(Name))
        stop = time.perf_counter()
        print("Runtime: " + str(stop-start))
        return render_template("Successful_submission.html")
    return render_template("map2.html")

@app.route('/map', methods = ["POST","GET"])
def airport():
    # BLlat,BLlon,RTlat,RTlon,AirPort,Kiosk,Name
    # print("got to here")
    if request.method == "POST":
        # print("check")
        test = request.form["shape"]
        test = json.loads(test)
        if len(test["features"]) == 1 and test["features"][0]["geometry"]["type"] == "Polygon":
            conversiontest.test(test)
        elif len(test["features"]) == 2 and test["features"][0]["geometry"]["type"] == "Polygon" and test["features"][1]["geometry"]["type"] == "Point":
            conversiontest.test(test)
        elif len(test["features"]) == 2 and test["features"][1]["geometry"]["type"] == "Polygon" and test["features"][0]["geometry"]["type"] == "Point":
            conversiontest.test(test)
        else:
            return render_template("test2.html")

        return render_template("test.html")
    else: return render_template("test2.html")


        
if __name__ == '__main__':
    app.run()



