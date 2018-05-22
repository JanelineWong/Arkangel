# import libraries
import urllib2
from bs4 import BeautifulSoup
import time


import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

import pprint

# specify the url
quote_page = input()

#query the website and return the html to the variable 
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

imgarray = soup.find_all('img')
img_url = []

for i in imgarray:
    url = "https:" + i['src'].encode("ascii")
    if (url.endswith(".jpg") or url.endswith(".jpeg")):
        img_url += [url]

pprint.pprint(img_url)

def detect_properties_uri(uri):
    """Detects image properties in the file located in Google Cloud Storage or
    on the Web."""
    # print(uri)
    client = vision.ImageAnnotatorClient()
    with io.open('out.csv', 'w') as readthis:
        image = types.Image()
        image.source.image_uri = uri

        response = client.image_properties(image=image)
        props = response.image_properties_annotation
        print('Properties:')

        for color in props.dominant_colors.colors:
            print('frac: {}'.format(color.pixel_fraction))
            print('\tr: {}'.format(color.color.red))
            print('\tg: {}'.format(color.color.green))
            print('\tb: {}'.format(color.color.blue))
            print('\ta: {}'.format(color.color.alpha))

        for color in props.dominant_colors.colors:
            readthis.write(u'{}'.format(color.pixel_fraction)+',')
            readthis.write(u'{}'.format(color.color.red)+',')
            readthis.write(u'{}'.format(color.color.green)+',')
            readthis.write(u'{}'.format(color.color.blue)+'\n')

def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    with io.open('safe.csv', 'w') as readit:
        image = types.Image()
        image.source.image_uri = uri

        response = client.safe_search_detection(image=image)
        safe = response.safe_search_annotation

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
        print('Safe search:')

        print('adult: {}'.format(likelihood_name[safe.adult]))
        print('medical: {}'.format(likelihood_name[safe.medical]))
        print('spoofed: {}'.format(likelihood_name[safe.spoof]))
        print('violence: {}'.format(likelihood_name[safe.violence]))

        readit.write(u'{}'.format(likelihood_name[safe.adult])+',')
        readit.write(u'{}'.format(likelihood_name[safe.medical])+',')
        readit.write(u'{}'.format(likelihood_name[safe.spoof])+',')
        readit.write(u'{}'.format(likelihood_name[safe.violence]))

for i in range(len(img_url)):
    time.sleep(3)
    detect_properties_uri(img_url[i])
    detect_safe_search_uri(img_url[i])
    i+=3


