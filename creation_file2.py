from qchain_backend.models import Agent, Website, Adspace, Ad, Contract, AD_TYPES, Stat
from qchain_backend.models import Contract, RequestForAdv, GENRE_CHOICES
from django.contrib.auth.models import User
from datetime import timedelta, datetime, tzinfo, date
import random
import numpy as np



adGenres = ["Gaming", "Auto", "Porn","Movies"]
adTypes = ["bl","btw","popup","br"]
adTypeNames = ["ban_left","ban_right","ban_top_wide","popup"]
heights =[400,20,300,500,100,300,250,450,340,640,650]
widths =[400,20,300,500,100,300,250,450,340,640,650]

adNamesGaming = ["half-life-3","left-for-dead","Call-Of-Duty","Overwatch","Dota2","Counterstrike"]
adNamesAuto = ["Volvo","Tesla","Subaru","Nissan","Honda","BMW"]
adNamesMovies = ["GoodFellas","Godfather","ToyStory","GameOfThrones","InfinityWar"]
adNamesPorn = ["xx","xxx","xxxx","newxxx","oldxxx"]

adSpaceNames= ["travel","luxury","new","aid","first","fire","lost","paradise","burgers","cheese","food"]
adspaceadTypeDictionary= {"bl":"Left banner","br":"Right banner","btw":"Left banner","bl":"Left banner"}
websiteWords = ["blue","eyes","fun","hiking","paddle","new","heavy","cat","paradise","tuna","food","awesome","funny","dogs","pets","game","spots","weather"]

usersList = User.objects.all()
websiteList = Website.objects.all()
adSpaceList = Adspace.objects.all()
adsList = Ad.objects.all()
curList = ["eqc","xqc"]

# User Creation
usersList =[]
for i in range(1,10):
    user = User.objects.create_user(username='demoUser'+i, password='demopassword'+i)
    user.is_superuser=False
    user.is_staff=False
    user.save()

usersList = User.objects.all()

#Creation of Websites with random names
for i in range (1,10):
    websiteName = random.choice(websiteWords)+random.choice(websiteWords)
    temp_website = Website(user=random.choice(usersList), link="http://www."+websiteName+".com",
                name=websiteName, description="The website on which the ad is \
    displayed", genres=random.choice(adGenres))
    temp_website.save()

#Create ads
for i in range (1,10):
    genreChosen = random.choice(adGenres)
    adName = ""
    if (genreChosen == "Gaming"):
        adName = random.choice(adNamesGaming)
    if (genreChosen == "Auto"):
        adName = random.choice(adNamesAuto)
    if (genreChosen == "Movies"):
        adName = random.choice(adNamesMovies)
    temp_ad = Ad(advertiser=usersList[random.randint(0,len(usersList)-1)], name=adName+str(i), adtype=random.choice(adTypeNames), genre=genreChosen,content="www."+adName+str(i)+"website.com", height=random.choice(heights), width=random.choice(widths))
    temp_ad.save()

#Create adspaces
websiteList = Website.objects.all()
for i in range (1,10):
    temp_adsp = Adspace(publisher=usersList[random.randint(0,len(usersList)-1)],website = websiteList[random.randint(0,len(websiteList)-1)], name=random.choice(adSpaceNames),
                adtype=random.choice(adTypeNames), genre = random.choice(adGenres),
                height=random.choice(heights), width=random.choice(widths))
    temp_adsp.save()

for i in range (3,len(usersList)-1):
    temp_agent = Agent(user=usersList[i])
    temp_agent.save()


adSpaceList = Adspace.ojects.all()
adsList = Ad.objects.all()
curList = ["eqc","xqc"]

# Create contracts
temp_ad_list = random.sample(adsList,10)
temp_adspace_list = random.sample(adSpaceList,10)
for ind1 in range(0,9):
    start_month = random.randint(7,10)
    end_month = start_month + random.randint(1,2)
    start_date = random.randint(1,20)
    end_date = start_date + random.randint(1,10)
    cont = Contract(ad=temp_ad, # assign the randomly selected ad
                    adspace=temp_adspace,
                    name="Cont. btwn. "+str(temp_ad.name)+" on "+str(temp_adspace.name),
                    # all contracts sart on junedata of June (06) 2017 at 05:05:05.
                    # as a simple task, modify the code so that the start and end dates
                    # are completely randomized (5 marks)
                    start_time=datetime(2017,start_month,start_date,5,5,5,5),
                    end_time=datetime(2017,end_month,end_date,5,5,5,5),
                    active=True,
                    # pick a random currency
                    currency=random.choice(curList),
                    payout_cap=np.random.rand()*10)
    print(cont)
    cont.save()


# Create Stat
# if no stat exists, set start number to 1,otherwise set to whatever..
t = Stat.objects.all()
if len(t) == 0:
    stat_pk_startno = 1
else:
    stat_pk_startno = t[len(t)-1].pk+1 #whatever



# get all contracts
contracts_list = Contract.objects.all()
# for EVERY contract
for ind1 in range(len(contracts_list)):
    stats = Stat.objects.all()
    if len(stats) == 0:
        stat_pk_startno = 1
    else:
        stat_pk_startno = stats[len(stats)-1].pk+1
    # 31 days a month.
    for ind2 in range(31):
        try:
        # note that this is date object and doesn't have seconds etc
        # the impression etc are just random numbers generated with numpy.
        # 8 is the month,change to 9 for september.
            temp_stat = Stat(stat_date=date(2017,9,ind2+1),
                         impressions=np.random.randint(0,5000),
                         clicks=np.random.randint(0,1000),
                         rpm=2+np.random.randn(),
                         revenue=3+np.random.randn())
            # save the stat object
            temp_stat.save()
            # retrieve from database
            temp_stat = Stat.objects.last()
            # assign a contract (since it's a many to many field.)
            temp_stat.contract.add(contracts_list[ind1])
        except ValueError:
            print("No."+str(ind2+1+20)+"on")
