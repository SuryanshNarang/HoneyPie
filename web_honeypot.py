#Libraries
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template,request,redirect,url_for

#Logging Format
logging_format= logging.Formatter('%(asctime)s%(message)s')

#HTTP Logger
#copying from ssh honeypot
funnel_logger = logging.getLogger('Http Logger') #this is going to capture these usernames,passwords and IP addresses
funnel_logger.setLevel(logging.INFO) #(added a logging level).info method provides what's going on with your program.
#setting a handler (basically a file where we want to log the info to)
funnel_handler = RotatingFileHandler('http_audits.log', maxBytes=2000, backupCount=5) #provide filename inside this
funnel_handler.setFormatter(logging_format)
#now taking the above settings and putting them in the logger 
funnel_logger.addHandler(funnel_handler)




#Baseline boneypot
#two functions first one is for static WebPage which is going to accept the username and password(wp-loginpage)
#1st function
def web_honeypot(input_username="admin",password="password"):
    app= Flask(__name__)
    

    #declaring route of webPage
    @app.route('/')
    def index():
        return render_template('wp-admin.html')
    @app.route('/wp-admin-login', methods=['POST']) 
    def login():
        username=request.form['username'] #label names, in the html file.
        password=request.form['password']
        
        ip_address=request.remote_addr
        funnel_logger.info(f'Clients with IP address : {ip_address} entered \n username : {username} password : {password}')
        if username==input_username and password==input_password:
            return "HOORAYYYYYYYYY"
        else:
            return "Invalid username or password"
    return app

#second function will be for our honeypy file so that we can run it in the try block  elif args.http:
#print("[-]Hey we are running the HTTP based honeyPot")
def run_web_honeypot(port=5000, input_username="admin", input_password="password"):
    run_web_honeypot_app= web_honeypot(input_username,input_password)
    run_web_honeypot_app.run(debug=True, port=port,host="0.0.0.0")
    
    return run_web_honeypot_app
    
