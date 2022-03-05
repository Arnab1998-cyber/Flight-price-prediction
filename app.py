from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
from datetime import datetime



app = Flask(__name__)
model = pickle.load(open("flight_price_model.pkl", "rb"))

@app.route('/', methods=['POST','GET'])
@cross_origin()
def home():
    if request.method=="POST":
        try:
            date_dep=request.form['Depurture Time']
            journey_day=pd.to_datetime(date_dep).date().day
            journey_month=pd.to_datetime(date_dep).date().month
            dep_hour=pd.to_datetime(date_dep).hour
            dep_minute=pd.to_datetime(date_dep).minute
            date_arr=request.form['Arrival Time']
            arrival_hour=pd.to_datetime(date_arr).hour
            arrival_minute=pd.to_datetime(date_arr).minute
            if arrival_minute<dep_minute:
                duration_minute=(arrival_minute+60)-dep_minute
            else:
                duration_minute=arrival_minute-dep_minute
            if arrival_hour<dep_hour:
                if arrival_minute < dep_minute:
                    duration_hour=((arrival_hour+24)-dep_hour)-1
                if arrival_minute >= dep_minute:
                    duration_hour=(arrival_hour+24)-dep_hour
            if arrival_hour>=dep_hour:
                if arrival_minute < dep_minute:
                    duration_hour=(arrival_hour-dep_hour)-1
                if arrival_minute >= dep_minute:
                    duration_hour=arrival_hour-dep_hour
            airline=request.form['Airlines']
            d = {'Jet Airways': 0, 'IndiGo': 1, 'Air India': 2, 'Multiple carriers': 3, 'SpiceJet': 4, 'Vistara': 5,
             'Air Asia': 6, 'GoAir': 7,
             'Multiple carriers Premium economy': 8, 'Jet Airways Business': 9, 'Vistara Premium economy': 10,
             'Trujet': 11}
            for i in d:
                if i==airline:
                    airline=d[i]
            source=request.form['Source']
            destination=request.form['Destination']
            d1 = {'Delhi': 0, 'Kolkata': 1, 'Banglore': 2, 'Mumbai': 3, 'Chennai': 4}
            for i in d1:
                if i==source:
                    source=d1[i]
            d2 = {'Cochin': 0, 'Banglore': 1, 'Delhi': 2, 'New Delhi': 3, 'Hyderabad': 4, 'Kolkata': 5}
            for i in d2:
                if i==destination:
                    destination=d2[i]
            total_stops=request.form['Total Stops']
            l=[]
            m=[]
            m.append(journey_day)
            m.append(journey_month)
            m.append(dep_hour)
            m.append(dep_minute)
            m.append(arrival_hour)
            m.append(arrival_minute)
            m.append(duration_hour)
            m.append(duration_minute)
            m.append(airline)
            m.append(source)
            m.append(destination)
            m.append(total_stops)
            l.append(m)
            print(l)
            prediction=model.predict(l)
            output=round(prediction[0],2)
            print('fare is ', output)
            return render_template('results.html', prediction=output)
        except Exception as e:
            print(e)
            return 'something went wrong'
    else:
        return render_template('index.html')
#https://github.com/Mandal-21/Flight-Price-Prediction
if __name__=='__main__':
    app.run()

