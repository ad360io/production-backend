from qchain_backend.models import Adspace, Ad, Website, Contract,RequestForAdv, AD_TYPES, GENRE_CHOICES, Stat, Agent, AdListing
from django.contrib.auth.models import User
from datetime import datetime
import random

currencyList = ['eqc', 'xqc']
#Access demouser
demoUser = User.objects.filter(username = 'demouser')[0]

#Retrieve the ads and the adspaces of all other users
adsList = Ad.objects.exclude(advertiser = demoUser)
adspaceList = Adspace.objects.exclude(publisher = demoUser)


for temp_ad in adsList:
    date1 = random.randint(1, 28)
    date2 = random.randint(1,28)
    to_month = random.randint(1,12)
    date_from = datetime(2017,11,date1,5,5,5,5)
    date_to = datetime(2018,to_month,date2, 5,5,5,5)
    temp_adlisting = AdListing(ad = temp_ad, name = temp_ad.name + ' listing',currency = random.choice(currencyList),ask_date_from = date_from , ask_date_to = date_to, cpi = random.uniform(10,50), cpm = random.uniform(5,50), msg = 'This is a sample adlisting for the ad' + temp_ad.name)
    #print(temp_adlisting)
    temp_adlisting.save()
