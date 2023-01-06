from flask import Flask, render_template, request
import DataCollection

global test

app = Flask(__name__)
@app.route('/', methods = ["POST","GET"])
def test():
    if request.method == "POST":
        BLlat = float(request.form["BLlat"])
        BLlon = float(request.form["BLlon"])
        RTlat = float(request.form["TRlat"])
        RTlon = float(request.form["TRlon"])
        FIPS = int(request.form["FIPS"])
        Kiosk = int(request.form["kiosk#"])
        Name = request.form["name"]
        DataCollection.main(BLlat,BLlon,RTlat,RTlon,FIPS,Kiosk,Name)
        return render_template("test.html")
    else: return render_template("test.html")

@app.route('/map', methods = ["POST","GET"])
def map():
    if request.method == "POST":
        print()
    return render_template("map.html")


        
if __name__ == '__main__':
    app.run()



