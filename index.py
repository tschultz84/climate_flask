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
    #This one works for sure.
    #return render_template('output.html', lat=request.form['latitude'])
    return render_template('output.html', lat=request.form['latitude'], long=request.form['longitude'])
#    return render_template('output.html', long=request.form['longitude'])
    #return render_template('output.html')
   
   
if __name__ == '__main__':
  # app.run()
  # app.debug = True
   app.run()
   #app.run(debug = True)

