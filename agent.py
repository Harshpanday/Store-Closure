import math
import pandas as pd
from mesa_geo.geoagent import GeoAgent, AgentCreator
import numpy as np
import random
import networkx as nx
import osmnx as ox

ox.settings.use_cache=True
ox.settings.cache_folder = "C:/Users/user/Desktop/RA/pythonProject20/cache"
filepath_drive = "./data/columbus.graphml"
G = ox.load_graphml(filepath_drive)  #DRIVE GRAPH
filepath_walk = "./data/columbus_walk.graphml"
A = ox.load_graphml(filepath_walk)  #WALK GRAPH
global household_data,step,distance_data
household_data=[]
distance_data=[]
global df_distance
#columns_for_distance = ['household', 'market', 'distance']
#df_distance = pd.DataFrame(columns=columns_for_distance)
df_distance = pd.read_csv("distance_data.csv")


class erhc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,fsa_sum,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        self.fsa_sum=fsa_sum
        global step
        step = 0

    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,16889,center=False, relation="intersects") #neighbors within 10 miles
        list_of_spm = []
        list_of_cspm=[]
        columns_for_results=['Type','id','fa','took food from(markets unique id)']
        global household_data,step,distance_data,df_distance,columns_for_distance
        step = step + 1
        if step==1:
            household_data = []#contingency when we reset the model, the dataframe should be cleared
        orig = ox.distance.nearest_nodes(G, X=self.longitude, Y=self.latitude)
        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                if ((df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)).any():
                    distance = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)].iloc[0]
                else:
                    dest = ox.distance.nearest_nodes(G, X=neighbor.longitude, Y=neighbor.latitude)
                    route = ox.shortest_path(G, orig, dest, weight="")
                    if route is not None:
                        edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
                    else:
                        edge_lengths = [math.inf]
                    distance = sum(edge_lengths)*0.000621371
                    df_distance.loc[len(df_distance)] = [self.unique_id,neighbor.unique_id,distance]
                if distance<10 and neighbor.FSA >= 20:
                    if type(neighbor) is spm:
                        list_of_spm.append([neighbor,distance])
                    else:
                        list_of_cspm.append([neighbor,distance])

        if len(list_of_cspm) >= 1 or len(list_of_spm)>=1:
            list_of_cspm.sort(key=lambda x:x[1])
            list_of_spm.sort(key=lambda x:x[1])
            if list_of_cspm and list_of_spm:
                if list_of_cspm[0][1] < list_of_spm[0][1]:
                    chosen_market_list = random.choices([list_of_cspm[0],list_of_spm[0]],weights=(24,76),k=1)[0]
                else:
                    chosen_market_list = random.choices([list_of_cspm[0], list_of_spm[0]], weights=(20, 80),k=1)[0]
            elif not list_of_cspm:
                chosen_market_list = list_of_spm[0]
            elif not list_of_spm:
                chosen_market_list = list_of_cspm[0]
            chosen_market = chosen_market_list[0]
            dis = chosen_market_list[1]
            #df_distance.loc[len(df_distance)] = [self.unique_id,chosen_market.unique_id,dis]
            self.fsa_sum += chosen_market.FSA
            self.fa = (self.fsa_sum/ 700) * 100
            chosen_market.fa = round(chosen_market.fa,2)
            print("Agent - ", type(self),"-",self.unique_id," ", "-", round(self.fa,2)," ")
            print("Market - ", type(chosen_market),chosen_market.unique_id," ", "-", chosen_market.FSA)
            #distance_chosen = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==chosen_market.unique_id)].iloc[0]
            
            print("Distance by car between them is ",round(dis,4)," miles\n")
            household_data.append(["erhc",self.unique_id,self.fa,chosen_market.unique_id])

        else:
            if (self.fa > 0):
                self.fa -= 1.25
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
                household_data.append(["erhc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self),self.unique_id," ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data,columns=columns_for_results)
        #print(df_distance)
        #print(self.steps)
        df_distance.to_csv("distance_data.csv",index=False)
        df.to_csv("household_data.csv")

class erlc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,fsa_sum,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        self.fsa_sum = fsa_sum


    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,6889,center=False, relation="intersects") #neighbors within 5 miles
        list_of_cspm = []
        list_of_spm=[]
        columns_for_results = ['Type','id', 'fa', 'took food from(markets unique id)']
        global household_data,distance_data,df_distance,columns_for_distance

        orig = ox.distance.nearest_nodes(A, X=self.longitude, Y=self.latitude)
        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                if ((df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)).any():
                    distance = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)].iloc[0]
                else:
                    dest = ox.distance.nearest_nodes(A, X=neighbor.longitude, Y=neighbor.latitude)
                    route = ox.shortest_path(A, orig, dest, weight="")
                    if route is not None:
                        edge_lengths = ox.utils_graph.get_route_edge_attributes(A, route, "length")
                    else:
                        edge_lengths = [math.inf]
                    distance = sum(edge_lengths) * 0.000621371
                    
                    df_distance.loc[len(df_distance)] = [self.unique_id, neighbor.unique_id, distance]
                    
                if distance < 8 and neighbor.FSA >= 20:
                    if type(neighbor) is spm:
                        list_of_spm.append([neighbor,distance])
                    else:
                        list_of_cspm.append([neighbor,distance])

        if len(list_of_cspm) >= 1 or len(list_of_spm)>=1:
            list_of_cspm.sort(key=lambda x: x[1])
            list_of_spm.sort(key=lambda x: x[1])
            if list_of_cspm and list_of_spm:
                chosen_market_list = random.choices([list_of_cspm[0],list_of_spm[0]],weights=(28,72),k=1)[0]
            elif not list_of_cspm:
                chosen_market_list = list_of_spm[0]
            elif not list_of_spm:
                chosen_market_list = list_of_cspm[0]
            chosen_market = chosen_market_list[0]
            dis = chosen_market_list[1]
            #df_distance.loc[len(df_distance)] = [self.unique_id,chosen_market.unique_id,dis]
            self.fsa_sum += chosen_market.FSA
            self.fa = (self.fsa_sum/ 640) * 100
            
            chosen_market.fa = round(chosen_market.fa, 2)
            print("Agent - ", type(self), "-", self.unique_id, " ", "-", round(self.fa,2), " ")
            print("Market - ", type(chosen_market), chosen_market.unique_id, " ", "-", chosen_market.FSA)
            
            print("Distance by walk between them is ", round(dis,4), " miles\n")
            household_data.append(["erlc", self.unique_id, self.fa, chosen_market.unique_id])
    

        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self), self.unique_id, " ", "-", self.fa, "\n")
                household_data.append(["erlc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self), self.unique_id, " ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data, columns=columns_for_results)
        df_distance.to_csv("distance_data.csv",index=False)
        df.to_csv("household_data.csv")


class lrhc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,fsa_sum,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        self.fsa_sum=fsa_sum

    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,16889,center=False, relation="intersects")#neighbors within 10 miles
        list_of_cspm = []
        list_of_spm=[]
        columns_for_results = ['Type', 'id', 'fa', 'took food from(markets unique id)']
        global household_data,df_distance,columns_for_distance
        orig = ox.distance.nearest_nodes(G, X=self.longitude, Y=self.latitude)
        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                if ((df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)).any():
                    distance = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)].iloc[0]
                else:
                    dest = ox.distance.nearest_nodes(G, X=neighbor.longitude, Y=neighbor.latitude)
                    route = ox.shortest_path(G, orig, dest, weight="")
                    if route is not None:
                        edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
                    else:
                        edge_lengths = [math.inf]
                    distance = sum(edge_lengths) * 0.000621371
                    df_distance.loc[len(df_distance)] = [self.unique_id, neighbor.unique_id, distance]
                    
                if distance < 10 and neighbor.FSA >= 20:
                    if type(neighbor) is spm:
                        list_of_spm.append([neighbor,distance])
                    else:
                        list_of_cspm.append([neighbor,distance])

        if len(list_of_cspm) >= 1 or len(list_of_spm) >= 1:
            list_of_cspm.sort(key=lambda x: x[1])
            list_of_spm.sort(key=lambda x: x[1])
            if list_of_cspm and list_of_spm:
                chosen_market_list = random.choices([list_of_cspm[0],list_of_spm[0]],weights=(36,64),k=1)[0]
            elif not list_of_cspm:
                chosen_market_list = list_of_spm[0]
            elif not list_of_spm:
                chosen_market_list = list_of_cspm[0]
            chosen_market = chosen_market_list[0]
            dis = chosen_market_list[1]
            #df_distance.loc[len(df_distance)] = [self.unique_id,chosen_market.unique_id,dis]
            self.fsa_sum+=chosen_market.FSA
            self.fa = (self.fsa_sum/600) * 100

            chosen_market.fa = round(chosen_market.fa, 2)
            print("Agent - ", type(self), "-", self.unique_id, " ", "-", round(self.fa,2), " ")
            print("Market - ", type(chosen_market), chosen_market.unique_id, " ", "-", chosen_market.FSA)
            
            print("Distance by car between them is ", round(dis,4), " miles\n")
            household_data.append(["lrhc", self.unique_id, self.fa, chosen_market.unique_id])


        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self), self.unique_id, " ", "-", self.fa, "\n")
                household_data.append(["lrhc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self), self.unique_id, " ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data, columns=columns_for_results)
        # print(self.steps)
        df_distance.to_csv("distance_data.csv", index=False)
        df.to_csv("household_data.csv")

class lrlc(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,fsa_sum,latitude = None, longitude=None):
        super().__init__(unique_id, model, shape)
        #self.atype = agent_type
        #self.model = model
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        self.fsa_sum=fsa_sum

    def step(self):
        neighbors = self.model.grid.get_neighbors_within_distance(self,6889,center=False, relation="intersects")#neighbors within 5 miles
        list_of_spm = []
        list_of_cspm=[]
        columns_for_results = ['Type', 'id', 'fa', 'took food from(markets unique id)']
        global household_data,df_distance,columns_for_distance
        orig = ox.distance.nearest_nodes(A, X=self.longitude, Y=self.latitude)
        for neighbor in neighbors:
            if type(neighbor) is spm or type(neighbor) is cspm:
                if ((df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)).any():
                    distance = df_distance['distance'].loc[(df_distance['household']==self.unique_id) & (df_distance['market']==neighbor.unique_id)].iloc[0]
                else:
                    dest = ox.distance.nearest_nodes(A, X=neighbor.longitude, Y=neighbor.latitude)
                    route = ox.shortest_path(A, orig, dest, weight="")
                    if route is not None:
                        edge_lengths = ox.utils_graph.get_route_edge_attributes(A, route, "length")
                    else:
                        edge_lengths = [math.inf]
                    distance = sum(edge_lengths) * 0.000621371
                    df_distance.loc[len(df_distance)] = [self.unique_id, neighbor.unique_id, distance]
                if distance < 8 and neighbor.FSA >= 20:
                    if type(neighbor) is spm:
                        list_of_spm.append([neighbor,distance])
                    else:
                        list_of_cspm.append([neighbor,distance])


        if len(list_of_cspm) >= 1 or len(list_of_spm) >= 1:
            list_of_cspm.sort(key=lambda x: x[1])
            list_of_spm.sort(key=lambda x: x[1])
            if list_of_cspm and list_of_spm:
                chosen_market_list = random.choices([list_of_cspm[0],list_of_spm[0]],weights=(40,60),k=1)[0]
            elif not list_of_cspm:
                chosen_market_list = list_of_spm[0][0]
            elif not list_of_spm:
                chosen_market_list = list_of_cspm[0][0]
            chosen_market = chosen_market_list[0]
            dis = chosen_market_list[1]
            #df_distance.loc[len(df_distance)] = [self.unique_id,chosen_market.unique_id,dis]
            self.fsa_sum+=chosen_market.FSA
            self.fa = (self.fsa_sum/480) * 100
            chosen_market.fa = round(chosen_market.fa, 2)
            print("Agent - ", type(self), "-", self.unique_id, " ", "-",round(self.fa,2), " ")
            print("Market - ", type(chosen_market), chosen_market.unique_id, " ", "-", chosen_market.FSA)
            
            print("Distance by walk between them is ", round(dis,4), " miles\n")
            household_data.append(["lrlc", self.unique_id, self.fa, chosen_market.unique_id])
            # print(st)

        else:
            if (self.fa > 0):
                self.fa -= 1
                print("Agent - ", type(self), self.unique_id, " ", "-", self.fa, "\n")
                household_data.append(["lrlc", self.unique_id, self.fa, "No Market"])
            else:
                print("Agent - ", type(self), self.unique_id, " ", "-", self.fa, "\n")
        df = pd.DataFrame(household_data, columns=columns_for_results)
        # print(self.steps)
        df_distance.to_csv("distance_data.csv", index=False)
        df.to_csv("household_data.csv")

class spm(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None,FSA=None):
        super().__init__(unique_id, model, shape)
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        self.FSA = FSA
    def step(self):
        if self.fa <= 0:
            self.model.grid.remove_agent(self)

class cspm(GeoAgent):
    def __init__(self, unique_id, model, shape,fa,latitude = None, longitude=None,FSA=None):
        super().__init__(unique_id, model, shape)
        self.fa = fa
        self.latitude = latitude
        self.longitude = longitude
        self.FSA = FSA
    def step(self):
        if self.fa <= 0:
            self.model.grid.remove_agent(self)
