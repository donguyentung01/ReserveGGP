import argparse 
import sys 
from HELPER.helper import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script that reserves pickleball courts in Golden Gate Park, San Francisco, CA.") 

    #parser.add_argument('-c', '--court', type=str, required=True, help="Court, e.g. Balboa") 
    parser.add_argument('-d', '--date', type=str, required=True, help="Date, e.g. 3/2/2025") 
    #parser.add_argument('-l', '--slot', type=str, default='morning,afternoon,evening', help="Time slot, either morning, afternoon, or evening. You can also chain time slots with comma as a separator, like 'morning,afternoon'")
    #parser.add_argument('-s', '--sport', type=str, required=True, help="Sport, either pickleball or tennis") 
    parser.add_argument('-t', '--time', type=str, required=True, help = "Time, e.g. 07:30:00") 
    parser.add_argument('-u', '--username', type=str, required=True, help="Your GGP email")
    parser.add_argument('-p', '--password', type=str, required=True, help="Your GGP password") 
    #parser.add_argument('-n', '--phone', type=str, required=True, help="Twilio phone number")
    #parser.add_argument('-i', '--sid', type=str, required=True, help="Twilio account SID") 
    #parser.add_argument('-a', '--authtoken', type=str, required=True, help="Twilio auth token")

    args = parser.parse_args()

    #court, time, email, password, phone_number, sid, auth_token, date, sport, slot = (
    #    args.court, args.time, args.email, args.password, args.phone, args.sid, args.authtoken, args.date, args.sport, args.slot
    #)

    username, password, date, time = (
        args.username, args.password, args.date, args.time
    )

    book_court(username, password, date, time)



    
