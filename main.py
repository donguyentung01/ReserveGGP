import argparse 
import sys 
from HELPER.helper import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script that reserves pickleball courts in Golden Gate Park, San Francisco, CA.") 

    #parser.add_argument('-c', '--court', type=str, required=True, help="Court, e.g. Balboa") 
    parser.add_argument('-d', '--date', type=str, required=True, help="Date, e.g. 3/2/2025") 
    #parser.add_argument('-s', '--sport', type=str, required=True, help="Sport, either pickleball or tennis") 
    parser.add_argument('-t', '--time', type=str, required=True, help = "Time, e.g. 07:30:00") 
    parser.add_argument('-u', '--username', type=str, required=True, help="Your GGP email")
    parser.add_argument('-p', '--password', type=str, required=True, help="Your GGP password") 

    args = parser.parse_args()

    username, password, date, time = (
        args.username, args.password, args.date, args.time
    )

    book_court(username, password, date, time)



    
