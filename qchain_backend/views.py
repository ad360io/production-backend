import time
import datetime
import random
import unicodedata
import numpy as np
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from qchain_backend.models import Adspace, Ad, Website, Contract,\
    RequestForAdv, AD_TYPES, GENRE_CHOICES, Stat, Agent

from qchain_backend.serializers import AdspaceSerializer, \
    AdSerializer, RequestForAdvSerializer, WebsiteSerializer, \
    ContractSerializer, StatSerializer
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


@api_view(["POST"])
def create_adspace(request):
    if request.method == 'POST':
        print("It is a post request!")
    else :
        print("not a post request")
    return response.Response({"success":"achieved"})

@api_view(["GET"])
def dashboard_tables(request):
    context = {}
    if(request.GET.get("userMode") and request.GET.get("currencyType") and request.GET.get("userName")):
        userMode = request.GET.get("userMode").lower()
        currencyType = request.GET.get("currencyType").lower()
        userName = request.GET.get("userName")
        currentAgent = Agent.objects.filter(user__username=userName)
        currentUser = currentAgent[0].user
        t = Agent.objects.all()

        if(userMode == "publisher"):
            my_cont_list = Contract.objects.filter(adspace__publisher=currentUser,
                                                   currency=currencyType)

            my_adsp_list = Adspace.objects.filter(publisher=currentUser)

            context['t2_col1'] = [str(a_cont.ad.advertiser) for a_cont in my_cont_list]
            context['t2_col2'] = [a_cont.start_time.date() for a_cont in my_cont_list]
            context['t1_col1'] = [an_adsp.website.name for an_adsp in my_adsp_list]
            context['t1_col2'] = [an_adsp.adtype for an_adsp in my_adsp_list]
            context['t1_col3'] = [an_adsp.genre for an_adsp in my_adsp_list]
            print(context)
            return response.Response(context)
        elif (userMode == "advertiser"):
            my_cont_list = Contract.objects.filter(ad__advertiser=currentUser,
                                                   currency=currencyType)
            my_ad_list = Ad.objects.filter(advertiser=currentUser)
            context['t2_col1'] = [str(a_cont.adspace.publisher) for a_cont in my_cont_list]
            context['t2_col2'] = [a_cont.start_time.date() for a_cont in my_cont_list]
            context['t1_col1'] = [ad.content for ad in my_ad_list]
            context['t1_col2'] = [an_ad.adtype for an_ad in my_ad_list]
            context['t1_col3'] = [an_ad.genre for an_ad in my_ad_list]
            print(context)
            return response.Response(context)
    else:
        return response.Response({"error" : "Incorrect parameters specified"})

@api_view(["GET"])
def display_marketplace(request):
    ## As a publisher, I am looking for Ads paying me x.
    ##
    context = {}
    context['ferrors'] = []
    my_adreq_list = RequestForAdv.objects.all()
    userMode = request.GET.get("userMode").lower()
    currencyType = request.GET.get("currencyType").lower()
    adTypeList = request.GET.get("adType")
    adGenreList = request.GET.get("adGenre")
    print(type(adTypeList))
    print(type(request.GET.getlist("adGenre")))
    minrate = int(request.GET.get("minrate"))
    maxrate = int(request.GET.get("maxrate"))
    print("Length of adreq list is L ",len(my_adreq_list))
    if currencyType != "" :
        my_adreq_list = my_adreq_list.filter(currency__iexact=
                                             currencyType)
    print(AD_TYPES)
    print("my_adreq_list is "+str(my_adreq_list))
    if adTypeList != [] :
        print(adTypeList)
        qstr2 = str(adTypeList).split(",")
        print(qstr2)
        print("--------------------------------------")
        qstr = [dict(AD_TYPES)[a_type] for a_type in
                qstr2]
        print([x.adsp.all()[0].adtype for x in my_adreq_list])
        my_adreq_list = my_adreq_list.filter(adsp__adtype__in=qstr)
    if adGenreList != []:
        print(adGenreList)
        genreList = str(adGenreList).split(",")
        genreList2 = [dict(GENRE_CHOICES)[a_genre] for a_genre in
                genreList]
        print(genreList2)
        #qstr = adGenreList
        my_adreq_list = my_adreq_list.filter(adsp__genre__in=genreList2)

    if minrate > maxrate:
        print("incorrect rates")
        context['ferrors'].append(("Invalid rates. Min rate should"
                                   " be less than max rate"))

    my_adreq_list = my_adreq_list.filter(asking_rate__gte=
                                         minrate)

    my_adreq_list = my_adreq_list.filter(asking_rate__lte=
                                     maxrate)

    if not(context['ferrors']):
        temp = [my_adreq.adsp.all()[0] for my_adreq in my_adreq_list]
        ser = AdspaceSerializer(temp, many=True)
        context['adspaces'] = ser.data
        ser = RequestForAdvSerializer(my_adreq_list, many=True)
        context['adreqs'] = ser.data
        # context['my_both_list'] = zip(my_adreq_list,my_adsp_list)
        # context['my_adreq_list'] = my_adreq_list
        return response.Response(context)
    else:
        my_ad_list = Adspace.objects.all()
        context = {'my_ad_list': my_ad_list}
        return response.Response(context)

@api_view(["GET"])
def dashboard_stats(request):
    context = {}
    if(request.GET.get("userMode") and request.GET.get("currencyType") and request.GET.get("userName")):
        userMode = request.GET.get("userMode").lower()
        currencyType = request.GET.get("currencyType").lower()
        userName = request.GET.get("userName")
        print("username="+userName+" currencyType="+currencyType+"userMode="+userMode)
        currentAgent = Agent.objects.filter(user__username=userName)
        print(currentAgent)
        currentUser = currentAgent[0].user
        eqc_balance = currentAgent[0].e_balance
        xqc_balance = currentAgent[0].x_balance
        context["eqc_balance"]=eqc_balance
        context["xqc_balance"]=xqc_balance
        if( userMode == "publisher" ):
            user_stats_list = Stat.objects.filter(contract__adspace__publisher=currentUser,contract__currency=currencyType)
            today_stats = user_stats_list.filter(stat_date=datetime.date.today())
            if today_stats:
                nstats = len(today_stats)
                context['topstat_revenue_today'] = round(sum([today_stats[ind].revenue for ind in range(nstats)])/nstats,8)
                context['topstat_clicks_today'] = round(sum([today_stats[ind].clicks for ind in range(nstats)])/nstats,8)
                context['topstat_impressions_today'] = round(sum([today_stats[ind].impressions for ind in range(nstats)])/nstats,8)
                context['topstat_rpm_today'] = round(sum([today_stats[ind].rpm for ind in range(nstats)])/nstats,8)
            else:
                context['topstat_revenue_today'] = 0
                context['topstat_clicks_today'] = 0
                context['topstat_impressions_today'] = 0
                context['topstat_rpm_today'] = 0

            month_stats = user_stats_list.filter(stat_date__gte=datetime.date.today()-datetime.timedelta(30))
            if month_stats:
                nstats = len(month_stats)
                context['topstat_revenue_30day'] = round(sum([month_stats[ind].revenue for ind in range(nstats)])/nstats,8)
                context['topstat_clicks_30day'] =  round(sum([month_stats[ind].clicks for ind in range(nstats)])/nstats,0)
                context['topstat_impressions_30day'] =  round(sum([month_stats[ind].impressions for ind in range(nstats)])/nstats,0)
                context['topstat_rpm_30day'] =  round(sum([month_stats[ind].rpm for ind in range(nstats)])/nstats,8)
            else:
                context['topstat_revenue_30day'] = 0
                context['topstat_clicks_30day'] = 0
                context['topstat_impressions_30day'] = 0
                context['topstat_rpm_30day'] = 0
            print("------------------------------------------------------------------")
            return response.Response(context)
            #print(dashboard_stats)
        elif( userMode.lower() == "advertiser" ):
            print(userMode.lower())
            user_stats_list = Stat.objects.filter(contract__ad__advertiser=currentUser,contract__currency=currencyType)
            today_stats = user_stats_list.filter(stat_date=datetime.date.today())
            if today_stats:
                nstats = len(today_stats)
                context['topstat_clicks_today'] = round(sum([today_stats[ind].clicks for ind in range(nstats)])/nstats,8)
                context['topstat_impressions_today'] = round(sum([today_stats[ind].impressions for ind in range(nstats)])/nstats,8)
            else:
                context['topstat_clicks_today'] = 0
                context['topstat_impressions_today'] = 0
            month_stats = user_stats_list.filter(stat_date__gte=datetime.date.today()-datetime.timedelta(30))
            if month_stats:
                nstats = len(month_stats)
                context['topstat_clicks_30day'] =  round(sum([month_stats[ind].clicks for ind in range(nstats)])/nstats,0)
                context['topstat_impressions_30day'] =  round(sum([month_stats[ind].impressions for ind in range(nstats)])/nstats,0)
            else:
                context['topstat_clicks_30day'] = 0
                context['topstat_impressions_30day'] = 0
            return response.Response(context)

        else:
            print("Unknown mode specified")
    else:
        print("Incorrect parameters specified. What should I do now?")
        return response.Response({"error":"Incorrect parameters specified"})

    return response.Response({"j":"jetti"})


@api_view(["GET","POST"])
def login3210(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return response.Response({"error": "Login failed"})

    token, _ = Token.objects.get_or_create(user=user)
    return response.Response({"token": token.key})
#    return response.Response({"j":"jetti"})



@api_view(["GET"])
def dashboard_charts(request):
    if(request.GET.get("userMode") and request.GET.get("currencyType") and request.GET.get("userName")):
        userMode = request.GET.get("userMode")
        currencyType = request.GET.get("currencyType")
        userName = request.GET.get("userName")
        currentAgent = Agent.objects.filter(user__username=userName)
        currentUser = currentAgent[0].user
        context = {}
        if( userMode.lower() == "publisher" ):
            my_stat_list = Stat.objects.filter(contract__adspace__publisher=currentUser,contract__currency=currencyType.lower())
            my_cont_list = Contract.objects.filter(adspace__publisher=currentUser,
                                                   currency=currencyType.lower())
            my_adsp_list = Adspace.objects.filter(publisher=currentUser)

            # Times
            # set retrieves unique elements, no internal oredering
            # cast to list again, because list is convenient.
            times = list(set([int(time.mktime(a_stat.stat_date.timetuple())*1000) for a_stat in my_stat_list]))
            times2 = list(set([a_stat.stat_date for a_stat in my_stat_list]))
            ## SHIVA: Don't know which format you want time in, replace times with
            ## times2 in the next line if needed. Seems like times is more versatile
            ## and can be converted to other formats in front end as was happening
            ## earlier. Times2 is more restricted but is hard to transform.
            print(times2)
            # sort by ascending order
            context['c1_x'] = sorted(times)

            # array with zeros
            temp = [0]*len(my_adsp_list)
            # Find top 5 that are nonzero
            #enum gives index (loop var) and objects
            for ind1,an_adsp in enumerate(my_adsp_list):
                related_cont_list = my_cont_list.filter(adspace=an_adsp)
                for a_cont in related_cont_list:
                    related_stat_list = my_stat_list.filter(contract=a_cont)
                    for a_stat in related_stat_list:
                        # Lists have .index() which returns index of elem in brackets
                        # ['a','b','c'].index('b') -> 1
                        # time_index = times2.index(a_stat.stat_date)
                        temp[ind1]+=float(a_stat.revenue)
            print(temp)
            # From list of all adspace revenues, get indices of top 5 adspaces
            # [13,11,12] -> np.sort() will give [11,12,13]
            # np.argsort gives [2,0,1]
            # [-5:] return last 5 elements (e.g, 10,20,30,40,50)
            # reversed will make it (50,40,30,20,10)
            chosen_inds = list(reversed(np.argsort(temp)[-5:]))
            print("Chosen indices are : ", chosen_inds)
            adspno = 0
            context['c1_y_revenue'],context['c1_y_clicks'] = [], []
            context['c1_y_impressions'],context['c1_y_rpm'] = [], []
            # choseninds is a list of indices of top5 adspaces in descending order
            for ind1 in range(len(chosen_inds)):
                # Find all contracts with this adspace, and get all the stats for
                # those contracts and sum. Should do all the revenue sums and then add
                # only the top 5 to the list.
                an_adsp = my_adsp_list[chosen_inds[ind1]]
                # revenue0 is the list of y values for the top contract
                context['c1_y_revenue'].append({'data': [0]*len(times), 'label':an_adsp.name})
                context['c1_y_clicks'].append({'data': [0]*len(times), 'label':an_adsp.name})
                context['c1_y_impressions'].append({'data': [0]*len(times), 'label':an_adsp.name})
                context['c1_y_rpm'].append({'data': [0]*len(times), 'label':an_adsp.name})
                # context['c1_y_clicks'+str(ind1)] = {"data" : [0]*len(times)}
                # context['c1_y_impression'+str(ind1)] = [0]*len(times)
                # context['c1_y_rpm'+str(ind1)] = [0]*len(times)
                # context['c1_adspnames'].append(an_adsp.name)
                related_cont_list = my_cont_list.filter(adspace=an_adsp)
                for a_cont in related_cont_list:
                    related_stat_list = my_stat_list.filter(contract=a_cont)
                    related_stat_list = sorted(related_stat_list, key= lambda a_stat: a_stat.stat_date)
                    for a_stat in related_stat_list:
                        time_index = times2.index(a_stat.stat_date)
                        context['c1_y_revenue'][ind1]["data"][time_index]+=float(a_stat.revenue)
                        context['c1_y_clicks'][ind1]["data"][time_index]+=float(a_stat.clicks)
                        context['c1_y_impressions'][ind1]["data"][time_index]+=float(a_stat.impressions)
                        context['c1_y_rpm'][ind1]["data"][time_index]+=float(a_stat.rpm)
                        # context['c1_y_impression'+str(ind1)][time_index]+=float(a_stat.impressions)
                        # context['c1_y_rpm'+str(ind1)][time_index]+=float(a_stat.rpm)
            # print(context['c1_adspnames'])

            xdata = []
            context['c2_y_weekrevenue'] = {"data":[0]*len(my_cont_list)}
            context['c2_y_day30revenue'] = {"data":[0]*len(my_cont_list)}
            context['c2_y_alltimerevenue'] = {"data":[0]*len(my_cont_list)}
            for ind in range(len(my_cont_list)):
                xdata.append(my_cont_list[ind].name)
                related_stat_list = my_stat_list.filter(contract=my_cont_list[ind])
                week_list = related_stat_list.filter(stat_date__gte=datetime.date.today()+datetime.timedelta(-7))
                day30_list = related_stat_list.filter(stat_date__gte=datetime.date.today()+datetime.timedelta(-30))
                alltime_list = related_stat_list.filter(stat_date__gte=datetime.date.today()+datetime.timedelta(-10000))
                context['c2_y_weekrevenue']["data"][ind] = sum([a_stat.revenue for a_stat in week_list])
                context['c2_y_day30revenue']["data"][ind] = sum([a_stat.revenue for a_stat in day30_list])
                context['c2_y_alltimerevenue']["data"][ind] = sum([a_stat.revenue for a_stat in alltime_list])
                # In the front end, sum up the correct list, round to 0 places and display.
            context['c2_xdata'] = xdata
            print("------------------------------------------------------------------")
            return response.Response(context)

        elif( userMode.lower() == "advertiser" ):
            my_stat_list = Stat.objects.filter(contract__ad__advertiser=currentUser,contract__currency=currencyType.lower())
            my_cont_list = Contract.objects.filter(ad__advertiser=currentUser,
                                                   currency=currencyType.lower())
            my_ad_list = Ad.objects.filter(advertiser=currentUser)

            print("Ads : "+str(my_ad_list))
            print("Contracts : ", my_cont_list)
            print("Stats : ", my_stat_list)

            # Times
            times = list(set([int(time.mktime(a_stat.stat_date.timetuple())*1000) for a_stat in my_stat_list]))
            times2 = list(set([a_stat.stat_date for a_stat in my_stat_list]))

            context['c1_x'] = sorted(times)
            print(context['c1_x'])
            context['c1_adnames'] = []
            temp = [0]*len(my_ad_list)
            # Find  top 5 ranked by no. of clicks
            for ind1,an_ad in enumerate(my_ad_list):
                related_cont_list = my_cont_list.filter(ad=an_ad)
                for a_cont in related_cont_list:
                    related_stat_list = my_stat_list.filter(contract=a_cont)
                    for a_stat in related_stat_list:
                        time_index = times2.index(a_stat.stat_date)
                        temp[ind1]+=float(a_stat.clicks)
            print(temp)
            chosen_inds = list(reversed(np.argsort(temp)[-5:]))
            print("Chosen indices are : ", chosen_inds)
            adspno = 0
            context['c1_y_clicks'] = []
            context['c1_y_impressions'],context['c1_y_rpm'] = [], []
            for ind1 in range(len(chosen_inds)):
                # Find all contracts with this ad, and get all the stats for
                # those contracts and sum. Should do all the clicks sums and then add
                # only the top 5 to the list.
                an_ad = my_ad_list[chosen_inds[ind1]]
                context['c1_y_clicks'].append({"data":[0]*len(times), 'label':an_ad.name})
                context['c1_y_impressions'].append({"data":[0]*len(times), 'label':an_ad.name})
                context['c1_adnames'].append(an_ad.name)
                related_cont_list = my_cont_list.filter(ad=an_ad)
                for a_cont in related_cont_list:
                    related_stat_list = my_stat_list.filter(contract=a_cont)
                    related_stat_list = sorted(related_stat_list, key= lambda a_stat: a_stat.stat_date)
                    for a_stat in related_stat_list:
                        time_index = times2.index(a_stat.stat_date)
                        context['c1_y_clicks'][ind1]["data"][time_index]+=float(a_stat.clicks)
                        context['c1_y_impressions'][ind1]["data"][time_index]+=float(a_stat.impressions)
            print(context['c1_adnames'])


            xdata = []
            context['c2_y_weekclicks'] = {"data":[0]*len(my_cont_list)}
            context['c2_y_day30clicks'] = {"data":[0]*len(my_cont_list)}
            context['c2_y_alltimeclicks'] = {"data":[0]*len(my_cont_list)}
            for ind in range(len(my_cont_list)):
                xdata.append(my_cont_list[ind].name)
                related_stat_list = my_stat_list.filter(contract=my_cont_list[ind])
                week_list = related_stat_list.filter(stat_date__gte=datetime.date.today()+datetime.timedelta(-7))
                day30_list = related_stat_list.filter(stat_date__gte=datetime.date.today()+datetime.timedelta(-30))
                alltime_list = related_stat_list.filter(stat_date__gte=datetime.date.today()+datetime.timedelta(-10000))
                context['c2_y_weekclicks']["data"][ind] = sum([a_stat.clicks for a_stat in week_list])
                context['c2_y_day30clicks']["data"][ind] = sum([a_stat.clicks for a_stat in day30_list])
                context['c2_y_alltimeclicks']["data"][ind] = sum([a_stat.clicks for a_stat in alltime_list])
                # In the front end, sum up the correct list, round to 0 places and display.
            context['c2_xdata'] = xdata
            return response.Response(context)
            print("------------------------------------------------------------------")

        else:
            print("Unknown mode specified")
    else:
        print("Incorrect parameters specified. What should I do now?")
        return response.Response({"error":"Incorrect parameters specified"})

    return response.Response({"j":"jetti"})
