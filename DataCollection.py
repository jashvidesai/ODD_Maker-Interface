
import os
import pandas as pd
import math
import haversine as hs
import warnings
warnings.filterwarnings("ignore")
from geojson import Polygon, Feature, FeatureCollection, Point
from collections import OrderedDict
import json
import datetime
import time
from geopy.geocoders import Nominatim
import random
import requests
import urllib
from shapely.geometry import Polygon as P, shape



# Defines functions
def stationsearch(lat, long):
  for a in range(0,len(Stations)):
    # Using the GC Distance is more accurate but slighly slower
    if hs.haversine((lat,long),(Stations[a][9],Stations[a][8]),unit=hs.Unit.MILES) < Max_Walkto_Train_Outside_ODD:
      global station
      station = Stations[a][5]
      global line
      line = Stations[a][7]
      return True
  return False

def countyCheck(Additional_Countys_Fips):
  if len(Additional_Countys_Fips) == 0:
    return False
  for a in Additional_Countys_Fips:
    if sheet["OFIPS"][x] == a[0] or sheet["DFIPS"][x] == a[0]:
      global station
      global line
      station = a[2]
      line = a[1]
      return True
  return False
  

def toCord(lat, long):
  xpixel = math.floor(138.348 * (long + 97.5) * math.cos(math.radians(lat)))
  ypixel = math.floor(138.348 * (lat - 37.0))
  return xpixel, ypixel

def toFips(state):
  return(Fips_Code[state])

def format_Numbers(number):
  return "{:,.0f}".format(number)


def getArea(Polygon_Area):
   lng1, lat1, lng2, lat2 = Polygon_Area.bounds
   x1, y1 = toCord(lat1,lng2)
   

   
   x2, y2 = toCord(lat2,lng1)

   

   
   pixels = []
   allpixels = []
   
   for x in range(x2,x1):
    for y in range(y1,y2):
        allpixels.append((x,y))
        
   
   




   for x in allpixels:
    i = x[0]
    j = x[1]
    bottom_left_lat = 37.0 + 0.00722814*(j)
    bottom_left_lng = -97.5 + 0.00722814*(i)/math.cos(math.radians(bottom_left_lat))
    bottom_left = (bottom_left_lng, bottom_left_lat)

    bottom_right_lat = 37.0 + 0.00722814*(j)
    bottom_right_lng = -97.5 + 0.00722814*(i+1)/math.cos(math.radians(bottom_right_lat))
    bottom_right = (bottom_right_lng, bottom_right_lat)

    top_right_lat = 37.0 + 0.00722814*(j+1)
    top_right_lng = -97.5 + 0.00722814*(i+1)/math.cos(math.radians(top_right_lat))
    top_right = (top_right_lng, top_right_lat)

    top_left_lat = 37.0 + 0.00722814*(j+1)
    top_left_lng = -97.5 + 0.00722814*(i)/math.cos(math.radians(top_left_lat))
    top_left = (top_left_lng, top_left_lat)

    

    pixel = P([bottom_left, bottom_right, top_right, top_left])
    if Polygon_Area.intersects(pixel):
        pixels.append((i,j))
    
   return pixels
    



Fips_Code = {"Alabama":1,"Alaska":2,"Arizona":4,"Arkansas":5,"California":6,"Colorado":8,"Connecticut":9,"Delaware":10,"Florida":12,"Georgia":13,"Hawaii":15,
"Idaho":16,"Illinois":17,"Indiana":18,"Iowa":19,"Kansas":20,"Kentucky":21,"Louisiana":22,"Maine":23,"Maryland":24,"Massachusetts":25,"Michigan":26,
"Minnesota":27,"Mississippi":28,"Missouri":29,"Montana":30,"Nebraska":31,"Nevada":32,"New Hampshire":33,"New Jersey":34,"New Mexico":35,"New York":36,
"North Carolina":37,"North Dakota":38,"Ohio":39,"Oklahoma":40,"Oregon":41,"Pennsylvania":42,"Rhode Island":44,"South Carolina":45,"South Dakota":46,
"Tennessee":47,"Texas":48,"Utah":49,"Vermont":50,"Virginia":51,"Washington":53,"West Virginia":54,"Wisconsin":55,"Wyoming":56}







# Takes input from Interface

def main(shape, Flights, MinFlightDist, Name):

    print("got to main")

    for x in range(0,len(shape["features"])):
        if shape["features"][x]["geometry"]["type"] == "Point":
            ODD_AirPort_Location = shape["features"][x]["geometry"]["coordinates"][0] # may need to do this by hand and reverse
        elif shape["features"][x]["geometry"]["type"] == "Polygon":
            S_Polygon = P(shape["features"][x]["geometry"]["coordinates"][0])
            

    # Sets starting pixels to be examined
    pixels_start = getArea(S_Polygon)
       



    # Initializes Input
    Train_Lines = []
    States = ["Florida"]
    Additional_Countys_Fips = []
    #Additional_Countys_Fips = [(36061,"Manhattan","NY Penn Station")]
    ODD_MaxWalk= .5
    Max_Walkto_Train_Outside_ODD = .707
    AirLink_Station = "Newark Liberty International Airport"
    AirLink_Line = "NORTHEAST CORRIDOR LINE"
    #directory = "C:/Users/hawke/Downloads/34_NewJersey"
    directory = "C:/Users/hawke/Dropbox/NationWideTrips'20"
    #directory = "NEC to Trenton Trips\memtest"
    GetLocal = True
    GetTrain = False
    ODD_Fips_string = []
    ODD_Fips_number = []
    ODD_Airport = Flights
    Train_Airport = False
    # ODD_AirPort_Location = (float(AirportLat), float(AirportLon))
    Home_Station_Name = "TRENTON"
    # Kiosk_Number = KioskNumber
    getOutDriving = False
    #All_Stations = pd.read_csv("C:/Users/hawke/OneDrive/Documents/Trenton Moves/FilteredTransitStations.csv")
    Stations = []
    Home_station = []
    master = []
    master_local = []
    lst_pixels = []
    origins = []
    destinations = []
    origins_local = []
    destinations_local = []
    school_origins = []
    school_destinations = []
    Count_Test_O = 0
    Count_Test_D = 0
    lst_features = []
    Final = []
    All = []
    DrivingTrips = []
    school_destinations = []
    school_origins = []
    origins_flights = []
    destinations_flights = []
    origins_trains = []
    destinations_trains = []
    origins_local = []
    destinations_local = []
    lst_features = []
    lst_feature_centerofmass = []
    All = []
    Centers_of_Mass = {}
    lst_pixels = []
    lst_pixels_forCOM = []


# Gets fips codes from corners
    lng1, lat1, lng2, lat2 = S_Polygon.bounds
    corners = [(lat1, lng1),(lat2, lng2),(lat1,lng2),(lat2,lng1)]
    tempFips = []
    for x in corners:

        lat = x[0]
        lon = x[1]

        print("Lat: " + str(lat))
        print("Lng: " + str(lon))

        #Contruct request URL
        url = 'https://geo.fcc.gov/api/census/block/find?latitude=' + str(lat) + "&longitude=" + str(lon) + "&format=json"

       

        #Get response from API
        response = None
        while str(response) != "<Response [200]>":
            response = requests.get(url)
    

        #Parse json in response
        data = response.json()

        #Print FIPS code
        tempFips.append(data['County']['FIPS'])
    
    tempFips = list(OrderedDict.fromkeys(tempFips)) 
    for x in tempFips:
        print("test: " + str(x))
        ODD_Fips_string.append(str(x))
        ODD_Fips_number.append(int(x))




    if GetTrain or ODD_Airport:
        if GetTrain:
            #Pulls stations in selected lines
            for row in All_Stations.itertuples():
                for a in Train_Lines:
                    if a in row.RTS_SRVD:
                        Stations.append(row)
            for row in All_Stations.itertuples():
                for state in States:
                    if row.STFIPS == toFips(state):
                        Stations.append(row)
            #Sets home station
            for x in range(0,len(Stations)):
                if Stations[x][5] == Home_Station_Name:
                    Home_station = Stations[x]
            #Collects trips from files
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                name = f[len(f)-11:len(f)-6]
                if name in ODD_Fips_string:
                    sheet = pd.read_csv(f)
                    print(f)
                    x = -1
                    sheet['OriginFile'] = pd.NaT
                    sheet['OGlobalLat'] = pd.NaT
                    sheet['OGlobalLon'] = pd.NaT
                    sheet['DGlobalLat'] = pd.NaT
                    sheet['DGlobalLon'] = pd.NaT
                    sheet['ODepartureTime_Military'] = pd.NaT
                    sheet['RailLink_Station'] = pd.NaT
                    sheet['RailLink_Line'] = pd.NaT
                    for row in sheet.itertuples():
                        x = x + 1
                        dpoint = (row.DXCoord,row.DYCoord)
                        opoint = (row.OXCoord,row.OYCoord)
                        if row.GCDistance > ODD_MaxWalk:
                            if opoint in pixels_start and dpoint not in pixels_start:
                                DrivingTrips.append(opoint)
                                if GetTrain:
                                    if stationsearch(row.DLat,row.DLon):
                                        xcoord,ycoord = toCord(Home_station[9],Home_station[8])
                                        sheet['OGlobalLat'][x] = row.OLat
                                        sheet['OGlobalLon'][x] = row.OLon
                                        sheet['DGlobalLat'][x] = row.DLat
                                        sheet['DGlobalLon'][x] = row.DLon
                                        sheet['Trip Type'][x] = 'T'
                                        sheet["DXCoord"][x] = xcoord
                                        sheet["DYCoord"][x] = ycoord
                                        sheet["DLat"][x] = Home_station[9]
                                        sheet["DLon"][x] = Home_station[8]
                                        sheet["GCDistance"][x] = hs.haversine((row.OLat,row.OLon),(Home_station[9],Home_station[8]),unit=hs.Unit.MILES)
                                        sheet['ODepartureTime_Military'][x] = str(datetime.timedelta(seconds=row.ODepartureTime))
                                        sheet['RailLink_Station'][x] = station
                                        sheet['RailLink_Line'][x] = line
                                        continue
                                if countyCheck(Additional_Countys_Fips):
                                    xcoord,ycoord = toCord(Home_station[9],Home_station[8])
                                    sheet['OGlobalLat'][x] = row.OLat
                                    sheet['OGlobalLon'][x] = row.OLon
                                    sheet['DGlobalLat'][x] = row.DLat
                                    sheet['DGlobalLon'][x] = row.DLon
                                    sheet['Trip Type'][x] = 'T'
                                    sheet["DXCoord"][x] = xcoord
                                    sheet["DYCoord"][x] = ycoord
                                    sheet["DLat"][x] = Home_station[9]
                                    sheet["DLon"][x] = Home_station[8]
                                    sheet["GCDistance"][x] = hs.haversine((row.OLat,row.OLon),(Home_station[9],Home_station[8]),unit=hs.Unit.MILES)
                                    sheet['ODepartureTime_Military'][x] = str(datetime.timedelta(seconds=row.ODepartureTime))
                                    sheet['RailLink_Station'][x] = station
                                    sheet['RailLink_Line'][x] = line
                                if ODD_Airport or Train_Airport: 
                                    if row.GCDistance > int(MinFlightDist):
                                        sheet['OriginFile'][x] = f
                                        if ODD_Airport:
                                            lat = ODD_AirPort_Location[0]
                                            lon = ODD_AirPort_Location[1]
                                        else:
                                            lat = Home_station[9]
                                            lon = Home_station[8]
                                            sheet['RailLink_Station'][x] = AirLink_Station
                                            sheet['RailLink_Line'][x] = AirLink_Line
                                        xcoord,ycoord = toCord(lat,lon)
                                        sheet['OGlobalLat'][x] = row.OLat
                                        sheet['OGlobalLon'][x] = row.OLon
                                        sheet['DGlobalLat'][x] = row.DLat
                                        sheet['DGlobalLon'][x] = row.DLon
                                        sheet['Trip Type'][x] = 'F'
                                        sheet["DXCoord"][x] = xcoord
                                        sheet["DYCoord"][x] = ycoord
                                        DrivingTrips.append((xcoord,ycoord))
                                        sheet["DLat"][x] = lat
                                        sheet["DLon"][x] = lon
                                        sheet["GCDistance"][x] = hs.haversine((row.OLat,row.OLon),(lat,lon),unit=hs.Unit.MILES)
                                        sheet['ODepartureTime_Military'][x] = str(datetime.timedelta(seconds=row.ODepartureTime))
                    sheet.rename(columns = {'Trip Type':'Trip_Type'}, inplace = True)
                    sheet['Intra_ODD'] = False
                    filtered2 = []
                    filtered2 = sheet[(sheet.Trip_Type == 'F')]
                    filtered1 = []
                    filtered1 = sheet[(sheet.Trip_Type == 'T')]
                    master.append(filtered1)
                    master.append(filtered2)
        Trips = pd.concat(master)
        Trips = Trips[(Trips.GCDistance > ODD_MaxWalk)]
        Trips.rename(columns = {'Trip_Type':'Trip Type'}, inplace = True)
        Final.append(Trips)


    if GetLocal:
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            name = f[len(f)-11:len(f)-6]
            if name in ODD_Fips_string:
                if os.path.isfile(f):
                    sheet = pd.read_csv(f)
                    print("here")
                    sheet['Intra_ODD'] = pd.NaT
                    sheet['School'] = pd.NaT
                    sheet['School_Name'] = pd.NaT
                    sheet['ODepartureTime_Military'] = pd.NaT
                    sheet.rename(columns = {'Trip Type':'Trip_Type'}, inplace = True)
                    x = 0
                    for row in sheet.itertuples():
                        dpoint = (row.DXCoord,row.DYCoord)
                        opoint = (row.OXCoord,row.OYCoord)
                        if opoint in pixels_start and dpoint in pixels_start:
                            if row.GCDistance > ODD_MaxWalk:
                                DrivingTrips.append(opoint)
                            sheet['Intra_ODD'][x] = True
                            sheet['Trip_Type'][x] = 'I'
                            if row.OType == 'S':
                                sheet['School'][x] = 1
                                sheet['School_Name'][x] = row.OName
                                sheet['Trip_Type'][x] = 'S'
                            if row.DType == 'S' and row.OType != 'S':
                                sheet['School'][x] = 1
                                sheet['School_Name'][x] = row.DName
                                sheet['Trip_Type'][x] = 'S'
                        else: sheet['Intra_ODD'][x] = False
                        sheet['ODepartureTime_Military'][x] = str(datetime.timedelta(seconds=row.ODepartureTime))
                        x = x + 1
                    sheet = sheet[(sheet.Intra_ODD == True)]
                    sheet = sheet[(sheet.GCDistance > ODD_MaxWalk)]
                    sheet['OGlobalLat'] = sheet['OLat']
                    sheet['OGlobalLon'] = sheet['OLon']
                    sheet['DGlobalLat'] = sheet['DLat']
                    sheet['DGlobalLon'] = sheet['DLon']
                    master_local.append(sheet)
        Trips_Local = pd.concat(master_local)
        Trips_Local.rename(columns = {'Trip_Type':'Trip Type'}, inplace = True)
        Final.append(Trips_Local)  

    Data = pd.concat(Final)   


    # AllEndpoint_Pixels = []
    # for row in Data.itertuples():
    #     AllEndpoint_Pixels.append((row.OXCoord,row.OYCoord))
    #     AllEndpoint_Pixels.append((row.DXCoord,row.DYCoord))
    # Endpoint_PixelList = list(OrderedDict.fromkeys(AllEndpoint_Pixels))

    # Pixels_with_Count = []
    # ODD_Pixels = []
    # for a in Endpoint_PixelList:
    #     Pixels_with_Count.append((a,AllEndpoint_Pixels.count(a)))
    # Pixels_with_Count.sort(key = lambda x: x[1],reverse=True)
 

    # for h in range(0,Kiosk_Number): # put back to (0,Kiosk_Number) later
    #     ODD_Pixels.append(Pixels_with_Count[h][0])
    # if ODD_Airport:
    #     if toCord(ODD_AirPort_Location[0],ODD_AirPort_Location[1]) not in ODD_Pixels:
    #         ODD_Pixels = ODD_Pixels[0:Kiosk_Number-1]
    #         ODD_Pixels.append(toCord(ODD_AirPort_Location[0],ODD_AirPort_Location[1]))

    Data.to_csv("data/" + str(Name) + "_ALLtripsExtended.csv")


    # Data['Take'] = pd.NaT
    # Data.reset_index(inplace = True, drop = True)
    # b = 0
    # for row in Data.itertuples():
    #     dpoint = (row.DXCoord,row.DYCoord)
    #     opoint = (row.OXCoord,row.OYCoord)
    #     if opoint in ODD_Pixels and dpoint in ODD_Pixels:
    #         Data['Take'][b] = 1
    #     else:
    #         Data['Take'][b] = 0
    #     b = b + 1
    # NewDriving = Data[(Data.Take == 0)]
    # Data = Data[(Data.Take == 1)]
    # Data.to_csv("data/" + str(Name) + "_Top_" + str(KioskNumber) + ".csv")
    Data.rename(columns = {'Trip Type':'Trip_Type'}, inplace = True)






    for row in Data.itertuples():
        lst_pixels.append((toCord(row.OGlobalLat,row.OGlobalLon)))
        lst_pixels.append((toCord(row.DGlobalLat,row.DGlobalLon)))
        lst_pixels_forCOM.append((row.OXCoord,row.OYCoord))
        lst_pixels_forCOM.append((row.DXCoord,row.DYCoord))
        if row.Trip_Type == 'S':
            school_origins.append((row.OXCoord,row.OYCoord))
            school_destinations.append((row.DXCoord,row.DYCoord))
            origins_local.append((row.OXCoord,row.OYCoord))
            destinations_local.append((row.DXCoord,row.DYCoord))
        if row.Trip_Type == 'I':
            origins_local.append((row.OXCoord,row.OYCoord))
            destinations_local.append((row.DXCoord,row.DYCoord))
        if row.Trip_Type == 'F':
            origins_flights.append((toCord(row.OGlobalLat,row.OGlobalLon)))
            destinations_flights.append((toCord(row.DGlobalLat,row.DGlobalLon)))
        if row.Trip_Type == 'T':
            origins_trains.append((toCord(row.OGlobalLat,row.OGlobalLon)))
            destinations_trains.append((toCord(row.DGlobalLat,row.DGlobalLon)))
        All.append((row.OXCoord,row.OYCoord))
        All.append((row.DXCoord,row.DYCoord))
    if ODD_Airport or Train_Airport:
        lst_pixels.append(toCord(ODD_AirPort_Location[0],ODD_AirPort_Location[1]))

    lst_pixels = list(OrderedDict.fromkeys(lst_pixels))
    for x in lst_pixels:
        
        i = x[0]
        j = x[1]
        O_Count = origins.count((i,j))
        D_Count = destinations.count((i,j))
        O_Count_Local = origins_local.count((i,j))
        D_Count_Local = destinations_local.count((i,j))
        O_Count_School = school_origins.count((i,j))
        D_Count_School = school_destinations.count((i,j))

        Count_All_Adjusted = All.count((i,j))

        bottom_left_lat = 37.0 + 0.00722814*(j)
        bottom_left_lng = -97.5 + 0.00722814*(i)/math.cos(math.radians(bottom_left_lat))
        bottom_left = (bottom_left_lng, bottom_left_lat)

        bottom_right_lat = 37.0 + 0.00722814*(j)
        bottom_right_lng = -97.5 + 0.00722814*(i+1)/math.cos(math.radians(bottom_right_lat))
        bottom_right = (bottom_right_lng, bottom_right_lat)

        top_right_lat = 37.0 + 0.00722814*(j+1)
        top_right_lng = -97.5 + 0.00722814*(i+1)/math.cos(math.radians(top_right_lat))
        top_right = (top_right_lng, top_right_lat)

        top_left_lat = 37.0 + 0.00722814*(j+1)
        top_left_lng = -97.5 + 0.00722814*(i)/math.cos(math.radians(top_left_lat))
        top_left = (top_left_lng, top_left_lat)


        xypixel = Polygon([[bottom_left, bottom_right, top_right, top_left, bottom_left]])
        new_feature = Feature(geometry=xypixel, properties={"x_coord": i, "y_coord": j, "Train OPersonTrips": 
        origins_trains.count((i,j)), "Train DPersonTrips": destinations_trains.count((i,j)),"Flight OPersonTrips": origins_flights.count((i,j)),
        "Flight DPersonTrips": destinations_flights.count((i,j)),"Total Train/Flight PersonTrips": origins_trains.count((i,j))
        + destinations_trains.count((i,j)) + origins_flights.count((i,j)) + destinations_flights.count((i,j)),"IntraODD OPersonTrips":
        O_Count_Local, "IntraODD DPersonTrips": D_Count_Local,"Total IntraODD PersonTrips": O_Count_Local + D_Count_Local,
        "School OPersonTrips": O_Count_School,"School DPersonTrips": D_Count_School,"School PersonTrip Total": O_Count_School + 
        D_Count_School, "Daily Person Trips":Count_All_Adjusted,"Driving Trips Not Served by ODD": DrivingTrips.count((i,j))
        - Count_All_Adjusted})
        lst_features.append(new_feature)

    feature_collection = FeatureCollection(lst_features)
    with open("data/" + str(Name) + "_Pixels_" + ".geojson", "w") as outfile:
        json.dump(feature_collection, outfile)

    lst_pixels_forCOM = list(OrderedDict.fromkeys(lst_pixels_forCOM))
    for x in lst_pixels_forCOM:
        i = x[0]
        j = x[1]
        pixel_data_origins = Data[(Data.OXCoord == i)]
        pixel_data_origins = pixel_data_origins[(pixel_data_origins.OYCoord == j)]
        pixel_data_destinations = Data[(Data.DXCoord == i)]
        pixel_data_destinations = pixel_data_destinations[(pixel_data_destinations.DYCoord == j)]




        if pixel_data_origins.empty:
            center_of_mass_lat = (pixel_data_destinations["DLat"].mean())
            center_of_mass_lon = (pixel_data_destinations["DLon"].mean())
        elif pixel_data_destinations.empty:
            center_of_mass_lat = (pixel_data_origins['OLat'].mean())
            center_of_mass_lon = (pixel_data_origins['OLon'].mean())
        else:
            center_of_mass_lat = (pixel_data_origins['OLat'].mean() + pixel_data_destinations["DLat"].mean())/2
            center_of_mass_lon = (pixel_data_origins['OLon'].mean() + pixel_data_destinations["DLon"].mean())/2
        Centers_of_Mass[(i,j)] = (center_of_mass_lat,center_of_mass_lon)
        center = Point((center_of_mass_lon,center_of_mass_lat))

        distances_from_COM = []
        for row in pixel_data_origins.itertuples():
            distances_from_COM.append(hs.haversine((center_of_mass_lat,center_of_mass_lon),(row.OLat,row.OLon),unit=hs.Unit.MILES))
        for row in pixel_data_destinations.itertuples():
            distances_from_COM.append(hs.haversine((center_of_mass_lat,center_of_mass_lon),(row.DLat,row.DLon),unit=hs.Unit.MILES))
        distances_from_COM.sort()

        lst_feature_centerofmass.append(Feature(geometry=center, properties={"Pixel": (i,j), "Number of PersonTrips": len(pixel_data_origins) + 
        len(pixel_data_destinations), "Cum. Dist. at 10% (Miles)": distances_from_COM[math.floor(len(distances_from_COM)*.1)],"Cum. Dist. at 50% (Miles)": 
        distances_from_COM[math.floor(len(distances_from_COM)*.5)],"Cum. Dist. at 90% (Miles)": distances_from_COM[math.floor(len(distances_from_COM)*.9)]}))



    feature_collection_centerofmass = FeatureCollection(lst_feature_centerofmass)
    with open("data/" + str(Name) + "_pixelCOMs.geojson", "w") as outfile:
        json.dump(feature_collection_centerofmass, outfile)

    station_points = []
    if GetTrain:
        for x in range(0,len(Stations)):
            spot = (Stations[x][8],Stations[x][9])
            shape = Point(spot)
            station_points.append(Feature(geometry=shape, properties={"Station": Stations[x][5],"Lines Served": Stations[x][7]}))
        All_Spots = FeatureCollection(station_points)
        with open("data/Stationsfor_"+ str(Name) + ".geojson", "w") as outfile:
            json.dump(All_Spots, outfile)
