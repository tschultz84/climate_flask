# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 06:44:28 2022

@author: 14154
"""
#LOad up FLASK and the HTML templates.
#from flask import Flask
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import json
import pandas as pd
f=open('C:\\Users\\14154\\OneDrive\\Python\\climate-projects\\climate_flask_page\\filedirs.json')
data = json.load(f)
FLASKDIR = data['FLASKDIR']
IMAGEDIR = data['IMAGEDIR']
ROOTDIR = data['ROOTDIR']
f.close()
app = Flask(__name__)
#You have to direct the FLask application to the right place to load. 
#flask_dir = "C:\\Users\\14154\\OneDrive\\Python\\climate-projects\\climate_flask_page\\templates\\"
flask_dir=FLASKDIR
app=Flask(__name__,template_folder=flask_dir)
#Load climate stuff. 
import os
import json

import Station_analyzer_ts_flask as analyze
import importlib
importlib.reload(analyze)
#import Station_Loader_ts as load
from IPython.display import Image



#menu_header= <a href="url">link text</a>


""". https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
The two strange @app.route lines above the function are decorators, 
a unique feature of the Python language. A decorator modifies the function 
that follows it. A common pattern with decorators is to use them to register
 functions as callbacks for certain events. In this case, the @app.route 
 decorator creates an association between the URL given as an argument 
 and the function. In this example there are two decorators, which 
 associate the URLs / and /index to this function. This means that 
 when a web browser requests either of these two URLs, Flask is going 
 to invoke this function and pass the return value of it back to the browser as a response."""
#Index is the homepage wher data is entered.
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')
    #This is the output page.
  
@app.route('/output', methods=['GET', 'POST'])
def output():
    
    #Assign the latitude/longitude variables to pass.
    lat1=float(request.form['latitude'])
    long1=float(request.form['longitude'])

    #Find if there's a quick analysis selection
    quick=request.form['quick_search']
    if quick == "custom":
        #Assign others according to custom variables. 
        fbaseyear=int(request.form['fbaseyear'])
        #lbaseyear=int(request.form['lbaseyear'])
        lbaseyear=int(fbaseyear + 35)

        frefyear=int(request.form['frefyear'])
        lrefyear=int(request.form['lrefyear'])

        frefmo=int(request.form['frefmo'])
        frefday=int(request.form['frefday'])

        lrefmo=int(request.form['lrefmo'])
        lrefday=int(request.form['lrefday'])

        #bdate1="1-1-2011" bdate syntax
        bdate1=f'{frefmo}-{frefday}-{frefyear}'
        #edate1="12-31-2021"
        edate1=f'{lrefmo}-{lrefday}-{lrefyear}'
    #If quick select is not custom. 
    elif quick != "custom":
        timedesc="Custom"
        #First, define the variables you need for all calculations. 
        #Grab the date and year.
        from datetime import date
        todayts=date.today()
        thisyear=todayts.year
        thismonth=todayts.month
        thisday=todayts.day

        #The dataset is usually current within the past 3-5 days. Choose a buffer number of days
        # to make sure you don't ask for days too much before that.
        bufferdays = 7

        #Baseline years will default to the following, if custom is not chosen. 
        fbaseyear=int(1910)
        lbaseyear=int(fbaseyear + 35)

        #If the user chose the prior year analysis.
        if quick == "yearprior":
            timedesc="Last year"
            frefyear,lrefyear=int(thisyear-1),int(thisyear-1)
            frefmo,frefday=1,1
            lrefmo,lrefday=12,31

            #bdate1="1-1-2011" bdate syntax
            bdate1=f'{frefday}-{frefday}-{frefyear}'
            #edate1="12-31-2021"
            edate1=f'{lrefmo}-{lrefday}-{lrefyear}'
        
        if quick == "priordecade":
            timedesc="Last 10 years"
            frefyear,lrefyear=int(thisyear-10),int(thisyear-1)
            frefmo,frefday=1,1
            lrefmo,lrefday=12,31

            #bdate1="1-1-2011" bdate syntax
            bdate1=f'{frefday}-{frefday}-{frefyear}'
            #edate1="12-31-2021"
            edate1=f'{lrefmo}-{lrefday}-{lrefyear}'

        #YTD or latest two week  analysis.
        if (quick == "ytd") | (quick == "lastmonth"):
            #The edate is the same. 
            #If you're late in the month, your end date is just the date, minus the number of buffer days.
            if thisday > bufferdays:
                lrefday=thisday-bufferdays
                lrefmo=thismonth
            #If not, then go to 7 days before the end of last month.
            if thisday <=bufferdays:
                lrefday = 28-bufferdays+thisday
                #Unless it's January, then roll back to the prior year.
                if thismonth == 1:
                    lrefmo = 12
                    lrefyear = thisyear-1
                    
                if thismonth > 1:
                    lrefmo = thismonth-1
                    lrefyear = thisyear
            lrefyear=int(thisyear)
            #edate1="12-31-2021"
            edate1=f'{lrefday}-{lrefmo}-{lrefyear}'

            #Define the beginning dates now, first for Year to Date.
            if quick == "ytd":
                timedesc="Year-to-date"
                #Start defining it this way.
                frefyear=int(thisyear)
                #Unless you are in the first week of the year, then roll back to the prior year.
                if (thismonth == 1) & (thisday <= bufferdays):
                    frefyear=int(thisyear-1)
                frefday,frefmo=1,1
                bdate1 = f'{frefday}-{frefmo}-{frefyear}' 
            
            if quick == "lastmonth":
                timedesc="Last month"
                #Set the beginning analysis date.
                frefyear=thisyear
                #The analysis begins last month.
                frefmo=thismonth-1
                #If you are late in the month, then your beginning date is in the last month.
                if thisday > (bufferdays): frefday=thisday-bufferdays #If late in the month, then begin on the same date minus buffer.
                if thisday <=(bufferdays): frefday = 1 #If early, then just start on day 1
                    
                #Unless it's January, then roll back to the prior year.
                if thismonth == 1:
                    frefmo = 12
                    frefyear = thisyear-1
                        
                bdate1=f'{frefday}-{frefmo}-{frefyear}'

    #Now, analyze.
    print(os.getcwd())
    calc = analyze.StationAnalyzer([lat1,long1],Firstyear=fbaseyear,Lastbaseyear=lbaseyear)
    calc.change_ref_dates([frefyear,lrefyear],[[frefmo,frefday],[lrefmo,lrefday]])
    calc.key_data
    calc.key_stats
    data = calc.stationobj #Data on the station itself.  
    yearsofdata=int(lrefyear)-int(calc.baseperiod_all[0,1].year)

    #Save the charts.
    calc.key_charts().savefig(f'{IMAGEDIR}tempcharts.png')    

    #Record the search.
    df = pd.DataFrame(data={
        "Latitude": [lat1],
        "Longitude":[long1],
        "Begining Date":[bdate1],
        "Ending Date":[edate1],
        "Period of search":[timedesc],
        "First baseline year":[fbaseyear],
        "Last baseline year":[lbaseyear],
        "Day of search":[date.today()]


    }) 
    df.to_csv(f'{ROOTDIR}search_records.csv',mode='a', index=False, header=False)
                
    
    return render_template('output.html', 
                           
                           lat=lat1, long=long1,bdate=bdate1,edate=edate1,yearsofdata=yearsofdata,
                           #THese are dataframes and series, refer tot he documentation for
                           #station_analyzer and station_loader to review their meaning. 

                           station_info=data.station_information,
                           key_data=calc.key_data,
                           key_stats=calc.key_stats,
                           timedesc=timedesc
                           )


   
if __name__ == '__main__':
  # app.run()
  # app.debug = True
   app.run()
   #app.run(debug = True)

