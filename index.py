# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 06:44:28 2022

@author: 14154
"""
#LOad up FLASK and the HTML templates.
#from flask import Flask
from flask import Flask, render_template, request
app = Flask(__name__)
#You have to direct the FLask application to the right place to load. 
flask_dir = "C:\\Users\\14154\\OneDrive\\Python\\climate_mapper\\python\\climate_flask_page\\templates\\"
app=Flask(__name__,template_folder=flask_dir)
#Load climate stuff. 
import os
dir1 = "C:\\Users\\14154\\OneDrive\\Python\\climate_mapper\\python\\climate_analyzer_ts\\"
os.chdir(dir1)
import Station_Loader_ts as load
import Station_analyzer_ts as analyze


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
    
    #Assign variables to pass.
    lat1=float(request.form['latitude'])
    long1=float(request.form['longitude'])
    bdate1="1-1-2011"
    edate1="12-31-2021"
    data=load.LoadStation([lat1,long1],True) #Loading in Bozeman, MT coordinates
    
    #Pulls the interesting station metadata.
    #Station Name. 
    name1 = data.name_closest_st                       
    #Station Distance frmo the Referenc Point.
    stdist=data.miles_from_ref
    #Station ID.
    stid  =data.id_closest_station
    #Lat, Lon, of the statoin. 
    stlatlon = data.st_latlon_str
    
    st_info = ["Station ID: "+str(stid),
               "Station Name: "+str(name1),
               "Station Coordinates: "+stlatlon,
               "Distance from Ref Point: "+str(round(stdist,1))+" miles"]
    
    #Then, some other meta data.
    #The number of years in the baseline.
    baseyears = data.yaml['BASENOYEARS']
    #And the first year in the dataset.
    veryfirstyear = int(data.veryfirstyear)
    lastbaseyear = str(int(veryfirstyear+baseyears))
    
    #Now, analyze.
    calc = analyze.StationAnalyzer(data.station_data,bdate1,edate1,display=True)
    #Metrics comparing REference to Baseline Period.
    #A string describing the baseline period.
    basedesc = calc.base_period_string
    alphavalue = str(100*calc.yaml['ALPHA'])+"%"
    #Ref and Baseline data points. 
    abs_temp =[round(calc.refmean,1),round(calc.basemean,1)]
    
    #Difference between temperature inr eference and baseline.
    refdelta = calc.ref_base_delta
    #P value of difference betwen them.
    pvalue = str(round(100*calc.ref_pvalue,2))+"%"
    #And statistical signitfance.
    refsig = calc.ref_stat_sig 
    
    #TREND RELATED DATA
    #The number of years in the recent trend.
    trendyears=calc.yaml['RECENT_TREND_YEARS']
    #The warming trend, in Farenheight degrees per decde.
    trendF = calc.trend_data_str
    #The trend's p-value and whether it is statistically significant.
    trend_p= str(round(100*calc.trend_p ,2))+"%"
    real_trend = calc.trend_is_real
        
    ##THese are key values to return out of the function.
    alltimestr = calc.alltimestr #A string describing all the weather station dates
    whole_mean = calc.whole_mean #Average temperature ove entire record
    whole_max_info = calc.whole_max_info #of form - maxium temperature, whole record, maxdate [whole_tmax,maxdate]
    whole_min_info = calc.whole_min_info # min temp whole record, mindate[ whole_tmin,mindate]
    ref_max_info = calc.ref_max_info # ref max temp, datte [ref_max,rmaxdate]
    ref_min_info =  calc.ref_min_info # ref min temp, date [ref_min,rmindate]
    
    gen_info = [
               "Station Name: "+str(name1),
               "Station ID: "+str(stid),
               "Period of Time Covered by Weather Station Data: "+alltimestr,
               "Average Temperature (TMID) over this Period (F): "+str(round(whole_mean,2)),
               "Maximum Temperature over this Period (F), and date(s): "+str(round(whole_max_info[0],2))+" in "+str(whole_max_info[1]),
               "Minimum Temperature over this Period (F), and date(s): "+str(round(whole_min_info[0],2))+" in "+str(whole_min_info[1])
               ]
               
               
               #"Distance from Ref Point: "+str(round(stdist,1))+" miles"]
    
    #name1="Bozeman"
    #return render_template('output.html', lat=lat1, long=long1,bdate=bdate1,edate=edate1,stname=name1)
    return render_template('output.html', 
                           #These variables deal with the reference point and dates.
                           lat=lat1, long=long1,bdate=bdate1,edate=edate1,
                           #This with the station metadata.
                           st_info=st_info,
                           #And, some other relevant metadata about base period.
                           lastbaseyear=lastbaseyear,veryfirstyear=veryfirstyear,
                           #Then, data comparing reference to baseline.
                           alphavalue = alphavalue,refdelta=refdelta,pvalue=pvalue,basedesc=basedesc,refsig=refsig,
                           abs_temp=abs_temp,
                           #Trend related data.
                           trend_p=trend_p,real_trend=real_trend,trendF=trendF,trendyears=trendyears,
                           #General climate related data
                           gen_info=gen_info
                           )


   
   
if __name__ == '__main__':
  # app.run()
  # app.debug = True
   app.run()
   #app.run(debug = True)

