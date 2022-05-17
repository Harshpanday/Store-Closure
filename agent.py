import itertools
import pandas as pd
from mesa.datacollection import DataCollector
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
import numpy as np
import sys
#import matplotlib.pyplot as plt
import requests
from shapely.geometry import Polygon
import requests
import json
import functools
from collections import defaultdict
def cached(function):
    cache={}

    @functools.wraps(function)
    def wrapper(*args,**kwargs):
        signature = (function,args)

        if signature in cache:
            result = cache[signature]
        else:
            result = function(*args,**kwargs)
            cache[signature] = result
        return result
    return wrapper

global household_data,step,distance_data
household_data=[]
distance_data=[]

class erhc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        global step
        step = 0
        global df_distance
        columns_for_distance = ['household', 'market', 'distance']
        df_distance = pd.DataFrame(columns=columns_for_distance)
    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,80467,center=False, relation="intersects")
        list_of_markets = []
        columns_for_results=['Type','id','fa','took food from(markets unique id)']
        columns_for_distance = ['household','market','distance']
        global household_data,step,distance_data,df_distance
        step = step + 1
        if step==1:
            household_data = []#contingency when we reset the model, the dataframe should be cleared

        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                if ((df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)).any():
                    distance = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)].iloc[0]
                else:
                    r = requests.get(
                        f"http://router.project-osrm.org/route/v1/car/{self.longitude},{self.latitude};{neighbor.longitude},{neighbor.latitude}?overview=false""")
                    routes = json.loads(r.content)
                    route_1 = routes.get("routes")[0]
                    distance = route_1["distance"]
                    distance_data = []
                    distance_data.extend((self.unique_id,neighbor.unique_id,distance))
                    df_distance.loc[len(df_distance)] = distance_data
                if distance<32186.9:
                    list_of_markets.append(neighbor)
        #print(distance_data)

        if len(list_of_markets) >= 1:
            chosen_market = np.random.choice(list_of_markets)
            self.fa += 2
            chosen_market.fa -= 2
            print("Agent - ", type(self),"-",self.unique_id," ", "-", self.fa," ")
            print("Market - ", type(chosen_market),chosen_market.unique_id," ", "-", chosen_market.fa)
            distance_chosen = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==chosen_market.unique_id)].iloc[0]
            print("Distance by car between them is ",distance_chosen/1609," miles\n")
            household_data.append(["erhc",self.unique_id,self.fa,chosen_market.unique_id])
            #print(st)

        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
                household_data.append(["erhc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data,columns=columns_for_results)
        #print(self.steps)
        df.to_csv("household_data.csv")

class erlc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude


    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,1607,center=False, relation="intersects")
        list_of_markets = []
        columns = ['Type','id', 'fa', 'took food from(markets unique id)']
        global household_data

        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                list_of_markets.append(neighbor)
        if len(list_of_markets) >= 1:
            chosen_market = np.random.choice(list_of_markets)
            self.fa += 2
            chosen_market.fa -= 2
            print("Agent - ", type(self),self.unique_id," ", "-", self.fa)
            print("Market - ", type(chosen_market),chosen_market.unique_id," ", "-", chosen_market.fa,"\n")
            household_data.append(["erlc", self.unique_id, self.fa, chosen_market.unique_id])
        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
                household_data.append(["erlc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data, columns=columns)
        df.to_csv("household_data.csv")
class lrhc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude

    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,1607,center=False, relation="intersects")
        list_of_markets = []
        columns = ['Type', 'id', 'fa', 'took food from(markets unique id)']
        global household_data
        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                list_of_markets.append(neighbor)
        if len(list_of_markets) >= 1:
            chosen_market = np.random.choice(list_of_markets)
            self.fa += 2
            chosen_market.fa -= 2
            print("Agent - ", type(self),self.unique_id," ", "-", self.fa)
            print("Market - ", type(chosen_market),chosen_market.unique_id," ", "-", chosen_market.fa, "\n")
            household_data.append(["lrhc", self.unique_id, self.fa, chosen_market.unique_id])
        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
                household_data.append(["lrhc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data, columns=columns)
        df.to_csv("household_data.csv")
class lrlc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude

    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,1607,center=False, relation="intersects")
        list_of_markets = []
        columns = ['Type', 'id', 'fa', 'took food from(markets unique id)']
        global household_data
        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                list_of_markets.append(neighbor)
        if len(list_of_markets) >= 1:
            chosen_market = np.random.choice(list_of_markets)
            self.fa += 2
            chosen_market.fa -= 2
            print("Agent - ", type(self),self.unique_id," ", "-", self.fa)
            print("Market - ", type(chosen_market),chosen_market.unique_id," ", "-", chosen_market.fa, "\n")
            household_data.append(["lrlc", self.unique_id, self.fa, chosen_market.unique_id])
        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self), "-", self.fa, "\n")
                household_data.append(["lrlc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self), "-", self.fa, "\n")
        df = pd.DataFrame(household_data, columns=columns)
        df.to_csv("household_data.csv")
class spm(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
    def step(self):
        if self.fa <= 0:
            self.model.grid.remove_agent(self)

class cspm(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
    def step(self):
        if self.fa <= 0:
            self.model.grid.remove_agent(self)
