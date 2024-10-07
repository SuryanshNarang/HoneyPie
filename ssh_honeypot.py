##Libraries
#logging library for getting username, password and ipAddress
import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko

#Constants
logging_format= logging.Formatter('%(message)s')
#banner is the version in simple words or any other metadata: 
SSH_BANNER="SSH-2.0-MySSHServer_1.0"
host_key='server.key' 


#Loggers & Logging Files
funnel_logger= logging.getLogger('FunnelLogger') #this is going to capture these usernames,passwords and IP addresses
funnel_logger.setLevel(logging.INFO) #(added a logging level).info method provides what's going on with your program.
#setting a handler (basically a file where we want to log the info to)
funnel_handler= RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5) #provide filename inside this
funnel_handler.setFormatter(logging_format)
#now taking the above settings and putting them in the logger 
funnel_logger.addHandler(funnel_handler)



#As we want one to record hackers activities.(basically it will capture the commands which hacker will enter)
creds_logger= logging.getLogger('FunnelLogger')
creds_logger.setLevel(logging.INFO) 
creds_handler= RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5) 
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)




#Emulated Shell
def emulated_shell(channel,client_ip)   #channel is for communicating(like sending dialogues messages over the SSH connection).
    channel.send(b'corporate-jumpbox2$')
    #importing sockets library.
    #provide opportunity to receive commands.
    #listening to new variable called command
    command= b""   #this variable is baiscally listening for user input(and we want to append each of the characters that's inputted into the shell as command and it puts together all of the characters into one string we can evalautate the logic)
    while True:
        char=channel.recv(1)
        channel.send(char)
        if not char:
            channel.close()
        #making all the character variables into one single string
        command += char
        
        if char==b'\r':
            if command.strip()==b'exit':
                response=b'\n Goodbye! \n'
                channel.close()
            elif command.strip()== b'pwd':
                response= b'\\usr\\local'+ b'\r\n'
            elif command.strip()==b'whoami':
                response= b'\n'+b"corpuser1"+b'\r\n'
            elif command.strip()==b'ls':
                response=b'\n'+b"jumpbox1.conf"+ b"\r\n"
            elif command.strip()==b'cat jumpbox1.conf':
                response=b'\n'+b"Go to xyz.com"+ b"\r\n" 
            else: #any irrelevant command
                response=b"\n"+bytes(command.strip())+ b"\r\n"
        channel.send(response)
        channe.send(b'corporate-jumpbox2$') # it will repopulate the default dialogue box and will listen for our next command.
        command = b""   







#SSH Server + Sockets
#setting up the ssh server: use librarry paramiko(we have both the configs client and server but we are going with Server)
class Server(paramiko.ServerInterface):
    #this class has serveral functions and this provide setting for ssh server
    def __init__(self,client_ip,input_username=None, input_password=None):
        #local variables
        self.client_ip=client_ip
        self.input_username=input_username
        self.input_password=input_password
    def check_channel_request(self, kind: str, chanid: int) -> int:
        #if the channel type is session then the connection is up and running
        if kind=='session':
            return paramiko.OPEN_SUCCEEDED
    
    def get_allowed_auths(self):
        #collecting basic auth credentials password authentication is required.
        return "password"
    def check_auth_password(self, username, password):
        if self.input_username is not None and self.input_password is not None:
            if username==self.input_username and password==self.input_password:
                return paramiko.AUTH_SUCCESSFUL #if username and password are ok then authentication is successful we are logged in shell environment
            else:
                return paramiko.AUTH_FAILED #if username and password are wrong then authentication fails
    
    
    def check_channel_shell_request(self, channel): 
        self.event.set()#This triggers an event, which is likely used to signal other parts of the code that a shell request has been made.( Accepts shell requests from the client.)
        return True  
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True #In simple terms, this method is saying, "Yes, I’ll give you a terminal window with the requested settings." It approves the client’s request for a graphical terminal interface where they can run commands, making it more interactive and user-friendly.(Accepts PTY (terminal) requests from the client.)
    def check_channel_exec_request(self, channel, command):
        command= str(command) #Exact place where we are going to handle the commands that are being input( Handles execute requests (command execution) from the client.)
        
     
        
#creating paramikoSSH instance and using the sockets library we can bind the server to a specific address and port, which will allow clients to come and connect to our server:
#using some constructs from the paramiko library:
def client_handle(client,addr,username,password):
    #creating and mantaining a connection
    #getting the client IP address first
    client_ip=addr[0] #passing in the client IP address
    print(f"{client_ip}has connected to the server")
    
    try:
        #initialize a new transport object: handling the low level ssh connections:
        transport= paramiko.Transport()#Initializes a Paramiko transport object for SSH communication.
        transport.local_version=SSH_BANNER #custom banner
        #now as we are creating a new session let's setup a server now:
        #so we will create instance of that server:
        server=Server(client_ip=client_ip,input_username=username,input_password=password)#as in server class we needed to define 3 paramters. We also need to set client_ip inorder to open the session.
        
        #Passing the ssh server session into the class
        transport.add_server_key(host_key) #hostkey is a public private key pair which allows incoming connection or clients to verify that the server is genuine. We will generate our own key.
        transport.start_server(server=server) #taking the ssh session to start the server
        
        channel=transport.accept(100) #this waits for the client to open a wether a shell cmd and the 100is the ms for the client to req the channel. if its done then a bidirectional tunnel will be created.
        #if not:
        if channel is None:
            print("No channel was opened")
        
        #Proceed to create another SSH BANNER this banner is going to be printed when we attempt to ssh into the honeypot file
        #below message will be displayed when a new session has been established
        
        standard_banner="Welcome to Ubuntu this project is made by Suryansh Narang\r\n\r\n"
        channel.send(standard_banner)
        emulated_shell(channel,client_ip=client_ip)
        
    except Exception as error:
        print(error)
        print("Hey an exception occured.")
    finally:
        try:
            transport.close() #closing the connection
        except Exception as error:
            print("Hey an exception occured.") 
        client.close()
#Provision SSH based Honeypot
``