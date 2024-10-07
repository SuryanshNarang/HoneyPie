##Libraries
#logging library for getting username, password and ipAddress
import logging
from logging.handlers import RotatingFileHandler



#Constants
logging_format= logging.Formatter('%(message)s')


#Loggers & Logging Files
funnel_logger= logging.getLogger('FunnelLogger') #this is going to capture these usernames,passwords and IP addresses
funnel_logger.setLevel(logging.INFO) #(added a logging level).info method provides what's going on with your program.
#setting a handler (basically a file where we want to log the info to)
funnel_handler= RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5) #provide filename inside this
funnel_handler.setFormatter(logging_format)
#now taking the above settings and putting them in the logger 
funnel_logger.addHandler(funnel_handler)




#Emulated Shell
#SSH Server + Sockets
#Provision SSH based Honeypot
