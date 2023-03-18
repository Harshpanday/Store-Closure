import json
import ast

query = open('demoOutputDict.json')
#query ="[{\"type\": \"remove\", \"qty\": \"1\", \"obj\": \"SPM.\", \"location\": \"Default\"}]"
for i in query:
    a = i.replace("\\","")
q = ast.literal_eval(a[1:-1])

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from geopy.geocoders import Nominatim
import random
import numpy as np
import sys
import plotly.express as px
import uuid
geolocator = Nominatim(user_agent="Tallion22")
place = " Columbus Ohio"

household = pd.read_csv("homedata.csv")
#household = household.drop('Unnamed: 0',axis=1)
#household = household.drop(range(50,len(household)))

market=pd.read_csv("marketdata.csv")

df = pd.concat([household[['longitude','latitude','category']].reset_index(drop=True),market[['longitude','latitude','category']].reset_index(drop=True)],axis=0)
map_before = pd.DataFrame({'lat':df['latitude'],
                    'lon':df['longitude'],
                    'category':df['category']})

fig_before = px.scatter_mapbox(map_before,
                        lat='lat',
                        lon='lon',
                        color='category',
                        center={
                            'lat':40.038013,
                            'lon':-82.982588
                        },
                        zoom=12)
fig_before.update_layout(mapbox_style='open-street-map')
fig_before.write_image('figures/map_before.png')


a_r_m_c_commands=[]
scope_commands=[]
report_commands=[]

def closest(mylist,target_coordinate,qty):
    norms  = [np.linalg.norm(np.array(target_coordinate,float)-np.array(item,float), ord=1) for item in mylist]
    norms = np.array(norms)
    index_of_minimum = norms.argsort()[:qty]
    minimum_items = [mylist[x] for x in index_of_minimum]
    return minimum_items,index_of_minimum

for i in q:
    if i["type"]=="modify" or i["type"]=="convert" or i["type"]=="add" or i["type"]== "remove":
        a_r_m_c_commands.append(i)
    elif i["type"]=="scope":
        scope_commands.append(i)
    elif i["type"]=="report":
        report_commands.append(i)

command=None
qty=None
obj=None
location = None
attr = None
changeType=None
targetValue=None
for i in a_r_m_c_commands:
    command = i["type"]
    qty = int(i["qty"])
    
    location = i["location"]
    if location=="Default":
        loc=None
    else:
        loc = geolocator.geocode(location+place)
        if loc == None:
            loc = geolocator.geocode(location)
        if loc==None:
            loc = geolocator.geocode(" ".join((location+place).split(" ")[1:])) 
        if loc==None:
            print("Place does not exist")
            sys.exit()
        latitude = loc.latitude #Y
        longitude = loc.longitude #X
        #print(longitude,latitude)
    
    if command == "add":
        obj = i["obj"].replace(".","")
        if obj=="ERHC":
            if loc == None:
                while qty>0:
                    household = household.append({
                        'hhinc8':1,
                        'owncar':2,
                        'longitude':random.uniform(-82.992236,-83.025195),
                        'latitude':random.uniform(40.070948,40.004581),
                        'category':"ERHC",
                        'salary':random.randrange(50,100)
                    },ignore_index=True)
                    qty=qty-1
            elif loc != None:
                while qty>0:
                    household = household.append({
                        'hhinc8':1,
                        'owncar':2,
                        'longitude':random.uniform(longitude-0.0005,longitude+0.0005),
                        'latitude':random.uniform(latitude-0.0005,latitude+0.0005),
                        'category':"ERHC",
                        'salary':random.randrange(50,100)
                    },ignore_index=True)
                    qty=qty-1
        elif obj=="ERLC":
            if loc == None:
                while qty>0:
                    household = household.append({
                        'hhinc8':1,
                        'owncar':1,
                        'longitude':random.uniform(-82.992236,-83.025195),
                        'latitude':random.uniform(40.070948,40.004581),
                        'category':"ERLC",
                        'salary':random.randrange(50,100)
                    },ignore_index=True)
                    qty=qty-1
            elif loc != None:
                while qty>0:
                    household = household.append({
                        'hhinc8':1,
                        'owncar':1,
                        'longitude':random.uniform(longitude-0.0005,longitude+0.0005),
                        'latitude':random.uniform(latitude-0.0005,latitude+0.0005),
                        'category':"ERLC",
                        'salary':random.randrange(50,100)
                    },ignore_index=True)
                    qty=qty-1
        elif obj=="LRHC":
            if loc == None:
                while qty>0:
                    household = household.append({
                        'hhinc8':6,
                        'owncar':2,
                        'longitude':random.uniform(-82.992236,-83.025195),
                        'latitude':random.uniform(40.070948,40.004581),
                        'category':"LRHC",
                        'salary':random.randrange(10,49)
                    },ignore_index=True)
                    qty=qty-1
            elif loc != None:
                while qty>0:
                    household = household.append({
                        'hhinc8':6,
                        'owncar':2,
                        'longitude':random.uniform(longitude-0.0005,longitude+0.0005),
                        'latitude':random.uniform(latitude-0.0005,latitude+0.0005),
                        'category':"LRHC",
                        'salary':random.randrange(10,49)
                    },ignore_index=True)
                    qty=qty-1
        elif obj=="LRLC":
            if loc == None:
                while qty>0:
                    household = household.append({
                        'hhinc8':6,
                        'owncar':1,
                        'longitude':random.uniform(-82.992236,-83.025195),
                        'latitude':random.uniform(40.070948,40.004581),
                        'category':"LRLC",
                        'salary':random.randrange(10,49)
                    },ignore_index=True)
                    qty=qty-1
            elif loc != None:
                while qty>0:
                    household = household.append({
                        'hhinc8':6,
                        'owncar':1,
                        'longitude':random.uniform(longitude-0.0005,longitude+0.0005),
                        'latitude':random.uniform(latitude-0.0005,latitude+0.0005),
                        'category':"LRLC",
                        'salary':random.randrange(10,49)
                    },ignore_index=True)
                    qty=qty-1
        elif obj=="SPM":
            if loc==None:
                while qty>0:
                    market = market.append({
                        'longitude':random.uniform(-82.992236,-83.025195),
                        'latitude':random.uniform(40.070948,40.004581),
                        'category':'SPM',
                        'FSA':random.randrange(80,95)
                    },ignore_index=True)
                    qty=qty-1
            elif loc!= None:
                while qty>0:
                    market = market.append({
                        'longitude':random.uniform(longitude-0.0005,longitude+0.0005),
                        'latitude':random.uniform(latitude-0.0005,latitude+0.0005),
                        'category':'SPM',
                        'FSA':random.randrange(80,95)
                    },ignore_index=True)
                    qty=qty-1
        elif obj=="CSPM":
            if loc==None:
                while qty>0:
                    market = market.append({
                        'longitude':random.uniform(-82.992236,-83.025195),
                        'latitude':random.uniform(40.070948,40.004581),
                        'category':'CSPM',
                        'FSA':random.randrange(20,55)
                    },ignore_index=True)
                    qty=qty-1
            elif loc!= None:
                while qty>0:
                    market = market.append({
                        'longitude':random.uniform(longitude-0.0005,longitude+0.0005),
                        'latitude':random.uniform(latitude-0.0005,latitude+0.0005),
                        'category':'CSPM',
                        'FSA':random.randrange(20,55)
                    },ignore_index=True)
                    qty=qty-1



    elif command == "remove":
        obj = i["obj"].replace(".","")
        if loc==None:
            if obj=="ERHC" or obj=="ERLC" or obj=="LRHC" or obj=="LRLC" or obj=="Home":
                drop_house = np.random.choice(household[household['category']==obj].index,size=qty,replace=False)
                household = household.drop(drop_house).reset_index(drop=True)
            elif obj=="SPM" or obj=="CSPM" or obj=="Market":
                drop_market = np.random.choice(market[market['category']==obj].index,size=qty,replace=False)
                market = market.drop(drop_market).reset_index(drop=True)

        elif loc!=None:
            if obj=="Home":
                close_value,close_index = closest(household[['longitude','latitude']].apply(list,axis=1),[longitude,latitude],qty)
                household = household.drop(close_index).reset_index(drop=True)
            elif obj=="ERHC" or obj=="ERLC" or obj=="LRHC" or obj=="LRLC":
                close_value,close_index = closest(household[['longitude','latitude']].loc[household['category']==obj].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                temp = pd.DataFrame(close_value,columns=['longitude1','latitude1'])
                household = household[household.merge(temp,
                                how='left',
                                left_on=['longitude','latitude'],
                                right_on=['longitude1','latitude1']).isna().any(axis=1)].reset_index(drop=True)
            elif obj=="Market":
                close_value,close_index = closest(market[['longitude','latitude']].apply(list,axis=1),[longitude.latitude],qty)
                market = market.drop(close_index).reset_index(drop=True)
            elif obj=="SPM" or obj=="CSPM":
                close_value,close_index = closest(market[['longitude','latitude']].loc[market['category']==obj].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                temp = pd.DataFrame(close_value,columns=['longitude1','latitude1'])
                market = market[market.merge(temp,
                                            how='left',
                                            left_on=['longitude','latitude'],
                                            right_on=['longitude1','latitude1']).isna().any(axis=1)].reset_index(drop=True)

    elif command == "convert":
        source = i['source'].replace(".","")
        target = i['target'].replace(".","")
        if target=="Home":
            target = random.choice(['ERHC','ERLC','LRHC','LRLC'])
        elif target=="Market":
            target = random.choice(['SPM','CSPM'])
        if loc==None:
            if source=="Home" or source=="ERHC" or source=="ERLC" or source=="LRHC" or source=="LRLC":
                if source=="Home":
                    update = household.sample(qty).index
                elif source=="ERHC" or source=="ERLC" or source=="LRHC" or source=="LRLC":
                    update = household.category[household.category.eq(source)].sample(qty).index

                household.loc[update,"category"]=target
                if target=="ERHC":
                    household.loc[update,'hhinc8']=1
                    household.loc[update,'owncar']=2
                    household.loc[update,'salary']=random.randrange(75,120)
                if target=="ERLC":
                    household.loc[update,'hhinc8']=2
                    household.loc[update,'owncar']=1
                    household.loc[update,'salary']=random.randrange(50,74)
                if target=="LRHC":
                    household.loc[update,'hhinc8']=5
                    household.loc[update,'owncar']=2
                    household.loc[update,'salary']=random.randrange(25,49)
                if target=="LRLC":
                    household.loc[update,'hhinc8']=6
                    household.loc[update,'owncar']=1
                    household.loc[update,'salary']=random.randrange(0,24)
                
            else:
                if source=="Market":
                    update = market.sample(qty).index
                    market.loc[update,"category"]=target
                elif source=="SPM" or source=="CSPM":
                    update = market.category[market.category.eq(source)].sample(qty).index
                    market.loc[update,"category"] = target

        elif loc!=None:
            if source=="Home" or source=="ERHC" or source=="ERLC" or source=="LRHC" or source=="LRLC":
                if source=="Home":
                    close_value,close_index = closest(household[['longitude','latitude']].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                elif source=="ERHC" or source=="ERLC" or source=="LRHC" or source=="LRLC":
                    close_value,close_index = closest(household[['longitude','latitude']].loc[household['category']==obj].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                    
                household.loc[close_index,"category"]="target"
                if target=="ERHC":
                    household.loc[close_index,'hhinc8']=1
                    household.loc[close_index,'owncar']=2
                    household.loc[close_index,'salary']=random.randrange(75,120)
                if target=="ERLC":
                    household.loc[close_index,'hhinc8']=2
                    household.loc[close_index,'owncar']=1
                    household.loc[close_index,'salary']=random.randrange(50,74)
                if target=="LRHC":
                    household.loc[close_index,'hhinc8']=5
                    household.loc[close_index,'owncar']=2
                    household.loc[close_index,'salary']=random.randrange(25,49)
                if target=="LRLC":
                    household.loc[close_index,'hhinc8']=6
                    household.loc[close_index,'owncar']=1
                    household.loc[close_index,'salary']=random.randrange(0,24)
            else:
                if source=="Market":
                    close_value,close_index = closest(market[['longitude','latitude']].apply(list,axis=1),[longitude,latitude],qty)
                    market.loc[close_index,"category"]=target
                elif source=="SPM" or source=="CSPM":
                    close_value,close_index = closest(market[['longitude','latitude']].loc[market['category']==obj].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                    market.loc[close_index,"category"] = target
            

    elif command=="modify":
        obj = i["obj"].replace(".","")
        attr = i["attribute"]
        changetype = i['changeType']
        targetvalue = i['targetValue']
        if loc!=None:
            if attr=="resources":
                if obj=="Home":
                    close_value,close_index = closest(household[['longitude','latitude']].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                elif obj=="ERHC" or obj=="ERLC" or obj=="LRHC" or obj=="LRLC":
                    close_value,close_index = closest(household[['longitude','latitude']].loc[household['category']==obj].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                   
                if changetype == "increasing":
                    household.loc[close_index,'salary']+=float(targetvalue.replace(".",''))
                elif changetype=="decreasing":
                    household.loc[close_index,'salary'] -= float(targetvalue.replace(".",''))
                elif changetype=="set":
                    if targetvalue=="high":
                        household.loc[close_index,'salary']=random.randrange(35,120)
                    else:
                        household.loc[close_index,'salary']=random.randrange(0,34)
                for i in close_index:
                    if household.loc[i,'salary']>=35:
                        if household.loc[i,'owncar']==2.0:
                            household.loc[i,'hhinc8']=2
                            household,loc[i,'category']="ERHC"
                        else:
                            household.loc[i,'hhinc8']=3
                            household.loc[i,'category']="ERLC"
                    else:
                        if household.loc[i,'owncar']==2.0:
                            household.loc[i,'hhinc8']=6
                            household.loc[i,'category']="LRHC"
                        else:
                            household.loc[i,'hhinc8']=7
                            household.loc[i,'category']="LRLC"

            if attr=="food_availability":
                if obj=="Market":
                    close_value,close_index = closest(market[['longitude','latitude']].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
                elif obj=="SPM" or obj=="CSPM":
                    close_value,close_index = closest(market[['longitude','latitude']].loc[market['category']==obj].apply(list,axis=1).reset_index(drop=True),[longitude,latitude],qty)
               
                if changetype=="increasing":
                    market.loc[close_index,"FSA"]+=float(targetvalue.replace('%',"").replace(".",''))
                elif changetype=="decreasing":
                    market.loc[close_index,"FSA"]-=float(targetvalue.replace('%',"").replace(".",''))
                elif changetype=="set":
                    if float(targetvalue.strip('%'))>=20:
                        market.loc[close_index]=float(targetvalue.replace('%',"").replace(".",''))
                    else:
                        market.loc[close_index]=20
        if loc==None:
            if attr=="resources":
                if obj=="Home":
                    update = household.sample(qty).index
                elif obj=="ERHC" or obj=="ERLC" or obj=="LRHC" or obj=="LRLC":
                    update = household.category[household.category.eq(obj)].sample(qty).index
                    
                if changetype == "increasing":
                    household.loc[update,'salary']+=float(targetvalue)
                elif changetype=="decreasing":
                    household.loc[update,'salary'] -= float(targetvalue)
                elif changetype=="set":
                    if targetvalue=="high":
                        household.loc[update,'salary']=random.randrange(35,120)
                    else:
                        household.loc[update,'salary']=random.randrange(0,34)
                for i in update:
                    if household.loc[i,'salary']>=35:
                        if household.loc[i,'owncar']==2.0:
                            household.loc[i,'hhinc8']=2
                            household,loc[i,'category']="ERHC"
                        else:
                            household.loc[i,'hhinc8']=3
                            household.loc[i,'category']="ERLC"
                    else:
                        if household.loc[i,'owncar']==2.0:
                            household.loc[i,'hhinc8']=6
                            household.loc[i,'category']="LRHC"
                        else:
                            household.loc[i,'hhinc8']=7
                            household,loc[i,'category']="LRLC"


            if attr=="food_availability":
                if obj=="Market":
                    update = market.sample(qty).index
                elif obj=="SPM" or obj=="CSPM":
                    update = market.category[market.category.eq(obj)].sample(qty).index
                
                if changetype=="increasing":
                    market.loc[update,"FSA"]+=float(targetvalue.replace('%',"").replace(".",''))
                elif changetype=="decreasing":
                    market.loc[update,"FSA"]-=float(targetvalue.replace('%',"").replace(".",''))
                elif changetype=="set":
                    if float(targetvalue.strip('%'))>=20:
                        market.loc[update]=float(targetvalue.replace('%',"").replace(".",''))
                    else:
                        market.loc[update]=20

df = pd.concat([household[['longitude','latitude','category']].reset_index(drop=True),market[['longitude','latitude','category']].reset_index(drop=True)],axis=0)       
map_after = pd.DataFrame({'lat':df['latitude'],
                    'lon':df['longitude'],
                    'category':df['category']})

fig_after = px.scatter_mapbox(map_after,
                        lat='lat',
                        lon='lon',
                        color='category',
                        center={
                            'lat':40.038013,
                            'lon':-82.982588
                        },
                        zoom=12)
fig_after.update_layout(mapbox_style='open-street-map')
fig_after.write_image('figures/map_after.png')


#household['id'] = range(0, len(household))
#market['id'] = range(len(household),len(household)+len(market))

household['id']=None

for i in range(len(household)):
    household.loc[i,'id'] = int(str(round(household.loc[i,'longitude'],5)).replace(".","").replace("-","") + str(round(household.loc[i,'latitude'],5)).replace(".","").replace("-",""))

for i in range(len(market)):
    market.loc[i,'id'] = int(str(round(market.loc[i,'longitude'],5)).replace(".","").replace("-","") + str(round(market.loc[i,'latitude'],5)).replace(".","").replace("-",""))


erhc=[]
erlc=[]
lrhc=[]
lrlc=[]

for i in range(len(household)):
    if household['category'][i]=="ERHC":
        erhc.append(household.iloc[i])
    elif household['category'][i]=="ERLC":
        erlc.append(household.iloc[i])
    elif household['category'][i]=="LRHC":
        lrhc.append(household.iloc[i])
    elif household['category'][i]=="LRLC":
        lrlc.append(household.iloc[i])

erhc_data = pd.DataFrame(erhc)
erhc_data = erhc_data.reset_index()

erlc_data = pd.DataFrame(erlc)
erlc_data = erlc_data.reset_index()

lrhc_data = pd.DataFrame(lrhc)
lrhc_data = lrhc_data.reset_index()

lrlc_data = pd.DataFrame(lrlc)
lrlc_data = lrlc_data.reset_index()

spm_data = market[market["category"]=="SPM"].reset_index()
cspm_data = market[market["category"]=="CSPM"].reset_index()


erlc_coordinates=[]
lrhc_coordinates=[]
lrlc_coordinates=[]
spm_coordinates=[]
cspm_coordinates=[]

erhc_list=[]
erhc_list_rough=[]
for i in range(erhc_data.shape[0]):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    erhc_coordinates=[]
    l1.append(float(format(erhc_data["longitude"][i], ".8f")))
    l1.append(float(format(erhc_data["latitude"][i], ".8f")))

    lg2 = erhc_data["longitude"][i]+0.000111
    lt2 = erhc_data["latitude"][i] + 0.000111
    l2.append(float(format(lg2, ".8f")))
    l2.append(float(format(lt2, ".8f")))

    lg3 = erhc_data["longitude"][i] + 0.000122
    lt3 = erhc_data["latitude"][i] + 0.000122
    l3.append(float(format(lg3, ".8f")))
    l3.append(float(format(lt3, ".8f")))

    lg4 = erhc_data["longitude"][i] + 0.000133
    lt4 = erhc_data["latitude"][i] + 0.000133
    l4.append(float(format(lg4, ".8f")))
    l4.append(float(format(lt4, ".8f")))

    erhc_coordinates.append(l1)
    erhc_coordinates.append(l2)
    erhc_coordinates.append(l3)
    erhc_coordinates.append(l4)
    
    data = {'id': erhc_data['id'][i], 'geometry': Polygon(erhc_coordinates), 'latitude': erhc_data['latitude'][i],'longitude':erhc_data['longitude'][i]}
    erhc_list.append(data)


erhc_df = pd.DataFrame.from_dict(erhc_list)
erhc_values = geopandas.GeoDataFrame(erhc_df,crs="EPSG:4326")

erlc_list=[]
for i in range(erlc_data.shape[0]):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    erlc_coordinates=[]
    l1.append(float(format(erlc_data["longitude"][i], ".8f")))
    l1.append(float(format(erlc_data["latitude"][i], ".8f")))

    lg2 = erlc_data["longitude"][i]+0.000111
    lt2 = erlc_data["latitude"][i] + 0.000111
    l2.append(float(format(lg2, ".8f")))
    l2.append(float(format(lt2, ".8f")))

    lg3 = erlc_data["longitude"][i] + 0.000122
    lt3 = erlc_data["latitude"][i] + 0.000122
    l3.append(float(format(lg3, ".8f")))
    l3.append(float(format(lt3, ".8f")))

    lg4 = erlc_data["longitude"][i] + 0.000133
    lt4 = erlc_data["latitude"][i] + 0.000133
    l4.append(float(format(lg4, ".8f")))
    l4.append(float(format(lt4, ".8f")))

    erlc_coordinates.append(l1)
    erlc_coordinates.append(l2)
    erlc_coordinates.append(l3)
    erlc_coordinates.append(l4)
    data = {'id': erlc_data['id'][i], 'geometry': Polygon(erlc_coordinates),'latitude': erlc_data['latitude'][i],'longitude':erlc_data['longitude'][i]}
    erlc_list.append(data)

erlc_df = pd.DataFrame.from_dict(erlc_list)
erlc_values = geopandas.GeoDataFrame(erlc_df,crs="EPSG:4326")

lrhc_list=[]
for i in range(lrhc_data.shape[0]):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    lrhc_coordinates=[]
    l1.append(float(format(lrhc_data["longitude"][i], ".8f")))
    l1.append(float(format(lrhc_data["latitude"][i], ".8f")))

    lg2 = lrhc_data["longitude"][i]+0.000111
    lt2 = lrhc_data["latitude"][i] + 0.000111
    l2.append(float(format(lg2, ".8f")))
    l2.append(float(format(lt2, ".8f")))

    lg3 = lrhc_data["longitude"][i] + 0.000122
    lt3 = lrhc_data["latitude"][i] + 0.000122
    l3.append(float(format(lg3, ".8f")))
    l3.append(float(format(lt3, ".8f")))

    lg4 = lrhc_data["longitude"][i] + 0.000133
    lt4 = lrhc_data["latitude"][i] + 0.000133
    l4.append(float(format(lg4, ".8f")))
    l4.append(float(format(lt4, ".8f")))

    lrhc_coordinates.append(l1)
    lrhc_coordinates.append(l2)
    lrhc_coordinates.append(l3)
    lrhc_coordinates.append(l4)
    data = {'id': lrhc_data['id'][i], 'geometry': Polygon(lrhc_coordinates),'latitude': lrhc_data['latitude'][i],'longitude':lrhc_data['longitude'][i]}
    lrhc_list.append(data)

lrhc_df = pd.DataFrame.from_dict(lrhc_list)
lrhc_values = geopandas.GeoDataFrame(lrhc_df,crs="EPSG:4326")

lrlc_list=[]
for i in range(lrlc_data.shape[0]):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    lrlc_coordinates=[]
    l1.append(float(format(lrlc_data["longitude"][i], ".8f")))
    l1.append(float(format(lrlc_data["latitude"][i], ".8f")))

    lg2 = lrlc_data["longitude"][i]+0.000111
    lt2 = lrlc_data["latitude"][i] + 0.000111
    l2.append(float(format(lg2, ".8f")))
    l2.append(float(format(lt2, ".8f")))

    lg3 = lrlc_data["longitude"][i] + 0.000122
    lt3 = lrlc_data["latitude"][i] + 0.000122
    l3.append(float(format(lg3, ".8f")))
    l3.append(float(format(lt3, ".8f")))

    lg4 = lrlc_data["longitude"][i] + 0.000133
    lt4 = lrlc_data["latitude"][i] + 0.000133
    l4.append(float(format(lg4, ".8f")))
    l4.append(float(format(lt4, ".8f")))

    lrlc_coordinates.append(l1)
    lrlc_coordinates.append(l2)
    lrlc_coordinates.append(l3)
    lrlc_coordinates.append(l4)
    data = {'id': lrlc_data['id'][i], 'geometry': Polygon(lrlc_coordinates),'latitude': lrlc_data['latitude'][i],'longitude':lrlc_data['longitude'][i]}
    lrlc_list.append(data)

lrlc_df = pd.DataFrame.from_dict(lrlc_list)
lrlc_values = geopandas.GeoDataFrame(lrlc_df,crs="EPSG:4326")

spm_list=[]
for i in range(spm_data.shape[0]):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    spm_coordinates=[]
    l1.append(float(format(spm_data["longitude"][i], ".8f")))
    l1.append(float(format(spm_data["latitude"][i], ".8f")))

    lg2 = spm_data["longitude"][i]+0.000111
    lt2 = spm_data["latitude"][i] + 0.000111
    l2.append(float(format(lg2, ".8f")))
    l2.append(float(format(lt2, ".8f")))

    lg3 = spm_data["longitude"][i] + 0.000122
    lt3 = spm_data["latitude"][i] + 0.000122
    l3.append(float(format(lg3, ".8f")))
    l3.append(float(format(lt3, ".8f")))

    lg4 = spm_data["longitude"][i] + 0.000133
    lt4 = spm_data["latitude"][i] + 0.000133
    l4.append(float(format(lg4, ".8f")))
    l4.append(float(format(lt4, ".8f")))

    spm_coordinates.append(l1)
    spm_coordinates.append(l2)
    spm_coordinates.append(l3)
    spm_coordinates.append(l4)
    data = {'id': spm_data['id'][i], 'geometry': Polygon(spm_coordinates),'latitude': spm_data['latitude'][i],'longitude':spm_data['longitude'][i],'FSA':spm_data['FSA'][i]}
    spm_list.append(data)

spm_df = pd.DataFrame.from_dict(spm_list)
spm_values = geopandas.GeoDataFrame(spm_df,crs="EPSG:4326")


cspm_list=[]
for i in range(cspm_data.shape[0]):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    cspm_coordinates=[]
    l1.append(float(format(cspm_data["longitude"][i], ".8f")))
    l1.append(float(format(cspm_data["latitude"][i], ".8f")))

    lg2 = cspm_data["longitude"][i]+0.000111
    lt2 = cspm_data["latitude"][i] + 0.000111
    l2.append(float(format(lg2, ".8f")))
    l2.append(float(format(lt2, ".8f")))

    lg3 = cspm_data["longitude"][i] + 0.000122
    lt3 = cspm_data["latitude"][i] + 0.000122
    l3.append(float(format(lg3, ".8f")))
    l3.append(float(format(lt3, ".8f")))

    lg4 = cspm_data["longitude"][i] + 0.000133
    lt4 = cspm_data["latitude"][i] + 0.000133
    l4.append(float(format(lg4, ".8f")))
    l4.append(float(format(lt4, ".8f")))

    cspm_coordinates.append(l1)
    cspm_coordinates.append(l2)
    cspm_coordinates.append(l3)
    cspm_coordinates.append(l4)
    data = {'id': cspm_data['id'][i], 'geometry': Polygon(cspm_coordinates),'latitude': cspm_data['latitude'][i],'longitude':cspm_data['longitude'][i],'FSA':cspm_data['FSA'][i]}
    cspm_list.append(data)

cspm_df = pd.DataFrame.from_dict(cspm_list)
cspm_values = geopandas.GeoDataFrame(cspm_df,crs="EPSG:4326")
