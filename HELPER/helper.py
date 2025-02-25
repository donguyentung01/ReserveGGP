from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs
import requests
import sys  
import time as t
import json
from datetime import datetime

def convert_time(time): 
    time_obj = datetime.strptime(time, "%H:%M:%S")
    formatted_time = time_obj.strftime("%I:%M %p")
    formatted_time_with_encoding = formatted_time.replace(" ", "%20")
    return formatted_time_with_encoding

def extract_day(date): 
    day = date.split("/")[1] 
    return day 

def spawn_driver(weblink): #create a web driver at the weblink provided 
    """
    Return a Chrome webdriver at the specified weblink 

    Parameters:
    weblink (string): link for driver to navigate to (e.g. "google.com")

    Returns:
    driver (webdriver.Chrome())
    """
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_experimental_option('w3c', False)
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = '/Users/tungdo/Downloads/chromedriver-mac-arm64/chromedriver' 
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options) 
    driver.get(weblink)
    return driver 

def login(driver, username, password): 
    """
    Log in GGP website with specified username and password. 

    Parameters:
    driver (webdriver.Chrome()): Chrome driver
    username (string): Golden Gate Park email/username
    password (string): Golden Gate Park password

    Returns:
    None 
    """
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'UserNameOrEmail'))
        )
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Password')) 
        )
        password_field.send_keys(password) 

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        )
        login_button.click()

        print("-" * 20)
        print("LOGGED IN SUCCESSFULLY")
        print("-" * 20)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Error: Failed at login")
        sys.exit(1)

def set_cookies(driver, session): 
    """
    Set cookies of the current session to be the same as of the driver's current weblink

    Parameters:
    driver
    session

    Returns:
    None
    """
    cookies = driver.get_cookies()
    print("SETTING ALL COOKIES")
    print("-"*20)
    for cookie in cookies:
        print("Setting Cookie " + cookie["name"] + " to " + cookie['value'])
        session.cookies.set(cookie['name'], cookie['value'])
    print("-"*20)


def create_data_form(verification_token, request_data, date, time, email): 
    """
    Create a dictionary representing the data form to submit reservation

    Parameters:
    verification_token (string): Verification token, derived from <input> tag with id ="_RequestVerificationToken"
    request_data (string): Request Data, derived from <input> tage with id="RequestData"
    date (string): Date you want to reserve the court (format: month/date/year, e.g. 3/2/2025) 
    time (string): Time you want to reserve court (format: hour:minute:second, e.g. 7:30:00)
    email (string): Golden Gate Park email

    Returns:
    A dictionary representing the data form to submit reservation.
    """
    print("SETTING UP DATA FORM")
    print("-"*20)
    print("Setting request data to " + request_data)
    print("Setting verification token to " + verification_token)

    with open('HELPER/disclosure.html', 'r') as file:
        disclosure_content = file.read()
    SelectedMembers = [
        {
            "OrgMemberId": 6471138, #constant for users
            "MemberId": 7235872, #constant for users
            "OrgMemberFamilyId": 1685674, 
            "FirstName": "Tung", 
            "LastName": "Do", 
            "Email": email,
            "MembershipNumber": 6471138, 
            "PaidAmt": "",
            "PriceToPay": 5.5
        }
    ]
    data = {
        "__RequestVerificationToken": verification_token,
        "Id": 12465, #constant for SF
        "OrgId": 12465, #constant for SF
        "MemberId":7235872, #constant for user
        "MemberIds": "",
        "IsConsolidatedScheduler": True, 
        "HoldTimeForReservation": 15, 
        "RequirePaymentWhenBookingCourtsOnline": False, 
        "AllowMemberToPickOtherMembersToPlayWith": False,
        "ReservableEntityName:": "Court", 
        "IsAllowedToPickStartAndEndTime": False,
        "CustomSchedulerId": 16834,
        "IsConsolidated": True,
        "isToday": False, 
        "IsFromDynamicSlots": False, 
        "InstructorId:": "", 
        "InstructorName": "",
        "canSelectCourt": False, 
        "IsCourtRequired": False, 
        "CostTypeAllowOpenMatches": False,
        "IsMultipleCourtRequired": False,
        "ReservationQueueId": "", 
        "ReservationQueueSlotId": "",
        "RequestData": request_data,
        "Id": 12465, 
        "OrgId": 12465,
        "Date": date + " 12:00:00 AM" ,
        "SelectedCourtType": "Pickleball", #constant for everyone
        "SelectedCourtTypeId": 9, #constant for everyone
        "SelectedResourceId": "", 
        "DisclosureText": disclosure_content,
        "DisclosureName": "Court Reservations",
        "isResourceReservation": False, 
        "StartTime": time,
        "CourtTypeEnum": "9", #constant for everyone
        "MembershipId": 139864, 
        "CustomSchedulerId": 16834,
        "IsAllowedToPickStartAndEndTime": False,
        "UseMinTimeByDefault": False, 
        "IsEligibleForPreauthorization": False, 
        "MatchMakerSelectedRatingIdsString": "",
        "DurationType": "",
        "MaxAllowedCourtsPerReservation": 1, 
        "SelectedResourceName": "",
        "ReservationTypeId": 68963, #constant
        "Duration": 30,
        "CourtId": "",
        "OwnersDropdown_input": "", 
        "OwnersDropdown": "",
        "SelectedMembers": SelectedMembers, 
        "SelectedNumberOfGuests": "",
        "DisclosureAgree": True, 
        "DisclosureAgree": False, 
        "X-Requested_with": "XMLHttpRequest"
    }

    print("Finished setting data form")
    print("-"*20)

    return data 

def send_request_book(session, data_form, URL_submit_reservation="https://reservations.courtreserve.com//Online/ReservationsApi/CreateReservation/12465?uiCulture=en-US"): 
    """
    Send request to submit reservation at Golden Gate Park

    Parameters:
    driver: Chrome webdriver 
    form_data (dictionary): dictionary representing data form to send with POST request
    URL_submit_reservation (string): URL to send POST request to for submitting reservation

    Returns:
    POST request response text (string)
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Origin": "https://app.courtreserve.com",
        "Referer": "https://app.courtreserve.com/",  
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    session.headers.update(headers)

    #URL_submit_reservation = "https://reservations.courtreserve.com//Online/ReservationsApi/CreateReservation/12465?uiCulture=en-US"
    response = session.post(URL_submit_reservation, data=data_form) 
    return response

'''
def create_data_form_get_time(driver): 
    data = {
        "date": "03/02/2025",
        "startTime": "21:30:00",
        "endTime": "10:00 PM",
        "useMinTimeAsDefault": False     
    }
    return data

def send_request_get_time(driver): 
    data = create_data_form(driver) 
    URL = "https://api4.courtreserve.com/api/v1/portalreservationsapi/Api_GetMaxReservationTimeByReservationType?id=12465&reservationTypeId=68963&time=21:30:00&uiCulture=en-US&selectedDate=03/02/2025&courtId=&courtType=9&endTime=10:00%20PM&isDynamicSlot=False"
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Referer": "https://app.courtreserve.com/",  # You should set the actual referer here
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    session.headers.update(headers)
    response = session.post(URL, data=data) 
    return response

def getRequestData(logs):
    for entry in logs:
        message = json.loads(entry['message'])
        if 'message' in message:
            method = message['message']['method']
            
            # Handle Network.request logs
            if 'Network.request' in method:
                request_url = message['message']['params'].get('request', {}).get('url', '')
                if 'CreateReservation' in request_url:
                    # Parse the URL and extract query parameters
                    parsed_url = urlparse(request_url)
                    query_params = parse_qs(parsed_url.query)
                    
                    # Get the value of 'requestData' query parameter
                    request_data = query_params.get('requestData', [None])[0]
                    
                    if request_data:
                        return request_data

'''

def book_court(username, password, date, time): 
    """
    Book Golden Gate Park pickleball court at specified date, time

    Parameters:
    username (string): Golden Gate Park username
    password (string): Golden Gate Park password
    date (string): Date you want to reserve the court (format: month/date/year, e.g. 3/2/2025) 
    time (string): Time you want to reserve court (format: hour:minute:second, e.g. 7:30:00)

    Returns:
    None 
    """
    formatted_time_with_encoding = convert_time(time)
    day = extract_day(date)

    driver = spawn_driver("https://app.courtreserve.com/Online/Reservations/Bookings/12465?sId=16834")

    login(driver, username, password) 

    driver.get("https://app.courtreserve.com/Online/Reservations/Bookings/12465?sId=16834") #Navigate to pickleball tab 
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "k-nav-current"))).click() #click on calendar

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@class='k-link' and text()='{day}']")) #select day
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[contains(@data-href, '{formatted_time_with_encoding}&end')]")) #select timeslot
    ).click()

    verification_token = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))).get_attribute('value') #get verification token
    request_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "RequestData"))).get_attribute('value') #get request_data

    #logs = driver.get_log('performance')
    #request_data = getRequestData(logs)

    session = requests.Session() #create new session 
    set_cookies(driver, session) #set cookies
    
    data_form = create_data_form(verification_token, request_data, date, time, username) 
    res = send_request_book(session, data_form) 

    print("Response Text: " + res.text)

    t.sleep(10) #set sleep timer for debugging
