#!/usr/local/bin/python3

import requests
import os
import sys
import argparse
import json
import time

#constants
face_url = 'https://thispersondoesnotexist.com/'
counter = 0
best_so_far = 0

#arguments
parser = argparse.ArgumentParser(description="Find your face from the void.",epilog="You should apply for the api access from Face++, see more help in README.")
parser.add_argument("-c","--confidence", type = float, default = 60, help = "Set the similarity of your face and the faces you want to save")
parser.add_argument("-n","--how_many", type = int, default = 10, help = "Set the quantity of the faces you want to save")

args = parser.parse_args()
custom_confidence = args.confidence
how_many = args.how_many

APIKEY = "********"
APISEC = "********"
APIURL_CREATE = "https://api-us.faceplusplus.com/facepp/v3/faceset/create"
APIURL_COMPARE = "https://api-us.faceplusplus.com/facepp/v3/compare"
APIURL_DETECT = 'https://api-us.faceplusplus.com/facepp/v3/detect'
IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Seth_MacFarlane_(7607033712).jpg/1200px-Seth_MacFarlane_(7607033712).jpg"

FOUND_DIR = "twinsfound/"
UNDETECTED_DIR = "nofacedetected/"

my_face_post = {'api_key': APIKEY,
                'api_secret': APISEC,
        		'image_url': IMG_URL,
                }

print("Requesting face data...")
try:
    my_face_data = requests.post(url = APIURL_DETECT, data = my_face_post)
except:
    print("Error requesting face data!", my_face_data.status_code, my_face_data.reason)
print("...done with status_code = " + str(my_face_data.status_code))

if my_face_data.status_code != 200:
    print("Abnormal status_code (" + str(my_face_data.status_code) + "), exiting.")
    exit()

try:
    print("Parsing face data JSON...")
    my_face_dict = json.loads(my_face_data.content)
except:
    print("Exception raised while parsing JSON!")
print("...done.")

if not my_face_dict['faces'][0]: # Checking is there any face detected
    print("No face detected on image: ", IMG_URL)
    exit(0)

#create a face set (by offical api document) to store the token id, or the token id would be deleted after 72 hours
face_set_post = {'api_key':APIKEY, 
                'api_secret':APISEC,
                'face_tokens':my_face_dict['faces'][0]['face_token'],
                }

print("Posting face set...")
try:
    postFaceSet = requests.post(url = APIURL_CREATE, data = face_set_post)
except:
    print("Exception raised while posting face set!")
    exit()
print("...done with status_code ", postFaceSet.status_code)

while counter <= how_many:

    print("Getting new thispersondoesnotexist face...")
    try:
        face_image = requests.get(face_url) # Getting new thispersondoesnotexist face
    except:
        print("Error getting new thispersondoesnotexist face!")
    print("...done.")

    face_image_file = {'image_file2':('face',face_image.content)}   #post img file
    post_data = {'api_key':APIKEY, 
                'api_secret':APISEC,
                'face_token1':my_face_dict['faces'][0]['face_token']}

    print("Posting thispersondoesnotexist face for compare...")
    try:
        requests_data = requests.post(APIURL_COMPARE, data = post_data, files = face_image_file)
    except:
        print("Error posting thispersondoesnotexist face!")
    print("...done with status_code ", requests_data.status_code)

    print("Parsing result JSON...")
    try:
        requests_dict = json.loads(requests_data.content)   #convert request data to dict
    except:
        print("Error parsing result JSON!")
    print("...done.")
    
    if 'confidence' in requests_dict:    # "Note: if no face is detected within the image uploaded, this string will not be returned." @API
        if requests_dict['confidence'] > best_so_far :
            best_so_far = requests_dict['confidence']
        print(requests_dict['confidence'],"best:",best_so_far)

        if requests_dict['confidence'] > custom_confidence :
            fileName = FOUND_DIR + str(time.time()) + str(requests_dict['confidence']) + '.jpeg'
            print("Writing face with ", requests_dict['confidence'], " confidence to file...")
            try:
                with open(fileName,'wb') as f:
                    f.write(face_image.content)
                    f.close()
            except:
                print("Error writing file!")
            counter += 1
    else: # This will be weird
        fileName = UNDETECTED_DIR + str(time.time())+'.jpeg'
        print("No face detected, so let's write this image for review to file" + fileName + "...")
        try:
            with open(fileName,'wb') as f:
                f.write(face_image.content)
                f.close()
        except:
            print("Error writing file!")

    print(str(counter) + "/" + str(how_many) + " found")    
