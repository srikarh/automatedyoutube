from scrape_videos import scrapeVideos
from make_compilation import makeCompilation
from upload_ytvid import uploadYtvid
import schedule
import time
import datetime
import os
import shutil
import googleapiclient.errors
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import config
import numpy as np

num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
} 

# USER VARIABLES FILL THESE OUT (fill out username and password in config.py)
IG_USERNAME = config.IG_USERNAME
IG_PASSWORD = config.IG_PASSWORD
print(IG_USERNAME)
print(IG_PASSWORD)

now = datetime.datetime.now()
videoDirectory = "./music_updates_" + num_to_month[now.month].upper() + "_" + str(now.year) + "_V" + str(now.day) + "/"
outputFile = "./" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str(now.day) + ".mp4"

INTRO_VID = '' # SET AS '' IF YOU DONT HAVE ONE
OUTRO_VID = ''
TOTAL_VID_LENGTH = 45
MAX_CLIP_LENGTH = 25
MIN_CLIP_LENGTH = 2
FIRST_TIME = "11:00"
SECOND_TIME = "23:00"
TOKEN_NAME = "token.json" # Don't change

# Setup Google 
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = "googleAPI.json"

def routine():

    # Handle GoogleAPI oauthStuff
    print("Handling GoogleAPI")

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_console()
    googleAPI = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    now = datetime.datetime.now()
    print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    #metadataFile = "./metadata-" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str(now.day) + ".txt"
    description = ""
    print(outputFile)

    if not os.path.exists(videoDirectory):
        os.makedirs(videoDirectory)
    
    title = "Temp Title"
    title += " #shorts"
    # Step 1: Scrape Videos
    print("Scraping Videos...")
    tags = scrapeVideos(username = IG_USERNAME,
                 password = IG_PASSWORD,
                 output_folder = videoDirectory, MAX_CLIP_LENGTH = MAX_CLIP_LENGTH, MIN_CLIP_LENGTH = MIN_CLIP_LENGTH,
                  days=0, hours=24)
    print("Scraped Videos!")
    tags.append("shorts")
    description = "Enjoy the updates! :) \n\n" \
    "like and subscribe to @TuneTrekz for more \n\n" \
    
    # Step 2: Make Compilation
    print("Making Compilation...")
    makeCompilation(path = videoDirectory,
                    introName = INTRO_VID,
                    outroName = OUTRO_VID,
                    totalVidLength = TOTAL_VID_LENGTH,
                    outputFile = outputFile)
    print("Made Compilation!")
    
    description += "\n\nCopyright Disclaimer, Under Section 107 of the Copyright Act 1976, allowance is made for 'fair use' for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.\n\n"

    # Step 3: Upload to Youtube
    print("Uploading to Youtube...")
    uploadYtvid(VIDEO_FILE_NAME=outputFile,
                title=title,
                description=description, tags=tags,
                googleAPI=googleAPI)
    print("Uploaded To Youtube!")
    # Step 4: Cleanup
    print("Removing temp files!")
    # Delete all files made:
    #   Folder videoDirectory
    shutil.rmtree(videoDirectory, ignore_errors=True)
    #   File outputFile
    try:
        os.remove(outputFile)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
    print("Removed temp files!")

def attemptRoutine():
    while(1):
        try:
            routine()
            break
        except OSError as err:
            print("Routine Failed on " + "OS error: {0}".format(err))
            time.sleep(60*60)

#attemptRoutine()
schedule.every().day.at(FIRST_TIME).do(attemptRoutine)
schedule.every().day.at(SECOND_TIME).do(attemptRoutine)

attemptRoutine()
while True:
    schedule.run_pending()  
    time.sleep(60) # wait one min

