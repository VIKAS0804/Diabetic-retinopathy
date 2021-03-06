#Deep learning model to scrape images of diabetic retinopathic fundus as mild or severes using web crawler
#Importing the necessary libraries
from requests import exceptions
import argparse
import requests
import os
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-q","--query", required=True, help='enter query text')
parser.add_argument("-l","--location", required=True,help='path to download')
arguments = vars(parser.parse_args())

#Setting API key and size
API_KEY = 'e43e0677deca47c99ffe4956d40e1e25'
MAX_RESULTS = 250
GROUP_SIZE = 50

URL = 'https://api.cognitive.microsoft.com/bing/v7.0/search[?q][&count][&offset][&mkt][&safesearch]'

#Exception Handling
EXCEPTIONS = set([IOError,FileNotFoundError,exceptions.RequestException,
                  exceptions.HTTPError,exceptions.ConnectionError
                  ,exceptions.Timeout])

#Intializing search of images
search_term = arguments['query']
headers = {'Ocp-Apim-Subscription-Key':API_KEY}
params = {'q':search_term,'offset':0,"count":GROUP_SIZE}

search = requests.get(URL, headers=headers,params=params)
search.raise_for_status()

results = search.json()

total = 0
downloaded_count = min(MAX_RESULTS, results['totalEstimatedMatches'])

#Downloading the fundus images
for offset in range(0,downloaded_count, GROUP_SIZE):
    params['offset'] = 0
    search = requests.get(URL, headers=headers,params=params)
    search.raise_for_status()
    results = search.json()
    for res in results["value"]:
        try:
            r = requests.get(res['contentUrl'], timeout=30)
            ext = res['contentUrl'][res['contentUrl'].rfind('.'):]
            p = 'C:\\Users\\vikas\\Desktop\\project\\images\\'+ str(total).zfill(8) + ext  #Setting path location for downloading images
            print('1 ran')
            fl = open(p,'wb')
            print('2 ran')

            fl.write(r.content)
            fl.close()

            img = cv2.imread(p)
            print('3 ran')
            if img is None:
                print('Bad file detected, deleting')
                os.remove(p)
                continue
            total = total + 1
            print('File number: ' + str(total))
        except Exception as e:
            print(e)
            if type(e) in EXCEPTIONS:
                continue
