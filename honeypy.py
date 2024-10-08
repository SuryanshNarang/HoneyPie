#Libraries
import argparse
from ssh_honeypot import *
from web_honeypot import *
#Parse Arguments
if __name__=="__main__":
    #creating new parser or object
    parser= argparse.ArgumentParser()
    parser.add_argument('-a','--address',type=str,required=True)
    parser.add_argument('-p','--port',type=int,required=True)
    parser.add_argument('-u','--username',type=str)
    parser.add_argument('-pw','--password',type=str)
    
    #add two more arguments: one for the ssh based honeypot and other for HTTP:
    parser.add_argument('-s','--ssh', action='store_true')
    parser.add_argument('-h','--http', action='store_true')
    
    #combining them all together
    args=parser.parse_args()
    
    #we have two types of honeypots defining the logic now:
    try:
        if args.ssh:
            print("[-]Hey we are running the SSH based HoneyPot")
            honeypot(args.address,args.port,args.username,args.password)
            if not args.username:
                username=None
            if not args.password:
                password=None
        elif args.http:
            print("[-]Hey we are running the HTTP based honeyPot")
            if not args.username:
                args.username="admin"
            if not args.password:
                args.password="password"
            print(f"Port: {args.port} Username:{ args.username} Password: {args.password}")
            run_web_honeypot(args.port, args.username, args.password)
        else:
            print("[-] Hey choose a honeypot Type (SSH --ssh) or (HTTP --http).")
    except:
        print("[-] Exiting honeypot")
        