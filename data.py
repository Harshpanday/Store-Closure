import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
df = pd.read_csv("practice_data.csv")
df['id'] = range(0, len(df))
df = df.drop(range(999,len(df)-1))
df_cspm = pd.read_csv("f.csv")


#erhc_data= df[df['id']<5].reset_index()
#erlc_data=df[(df['id']>=5) & (df['id']<10)].reset_index()
#lrhc_data=df[(df['id']>=10) & (df['id']<15)].reset_index()
#lrlc_data=df[(df['id']>=15) & (df['id']<20)].reset_index()
#spm_data = df[(df['id']>=20) & (df['id']<24)].reset_index()
erhc=[]
erlc=[]
lrhc=[]
lrlc=[]
for i in range(len(df)):
    if any(df.iloc[i]["hhinc8"] == ele for ele in [5, 6, 7, 8]):
        if df.iloc[i]["owncar"] == 2:
            erhc.append(df.iloc[i])
        else:
            erlc.append(df.iloc[i])
    else:
        if df.iloc[i]["owncar"] == 2:
            lrhc.append(df.iloc[i])
        else:
            lrlc.append(df.iloc[i])
erhc_data = pd.DataFrame(erhc)
erhc_data = erhc_data.reset_index()

erlc_data = pd.DataFrame(erlc)
erlc_data = erlc_data.reset_index()

lrhc_data = pd.DataFrame(lrhc)
lrhc_data = lrhc_data.reset_index()

lrlc_data = pd.DataFrame(lrlc)
lrlc_data = lrlc_data.reset_index()

spm_data = pd.read_csv("spm.csv")
cspm_data = df_cspm[df_cspm['id']>=30005].reset_index()
datas=[]
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
    data_rough = {'id': erhc_data['id'][i], 'geometry': erhc_coordinates,"name":"EERRHHCC"}
    erhc_list_rough.append(data_rough)
    data = {'id': erhc_data['id'][i], 'geometry': Polygon(erhc_coordinates),"name":"EERRHHCC"}
    erhc_list.append(data)


erhc_df = pd.DataFrame.from_dict(erhc_list)
erhc_df_rough = pd.DataFrame.from_dict(erhc_list_rough)
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
    data = {'id': erlc_data['id'][i], 'geometry': Polygon(erlc_coordinates)}
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
    data = {'id': lrhc_data['id'][i], 'geometry': Polygon(lrhc_coordinates)}
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
    data = {'id': lrlc_data['id'][i], 'geometry': Polygon(lrlc_coordinates)}
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
    data = {'id': spm_data['id'][i], 'geometry': Polygon(spm_coordinates),"name": spm_data['OnSite'][i]}
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
    data = {'id': cspm_data['id'][i], 'geometry': Polygon(cspm_coordinates)}
    cspm_list.append(data)

cspm_df = pd.DataFrame.from_dict(cspm_list)
cspm_values = geopandas.GeoDataFrame(cspm_df,crs="EPSG:4326")

#x=erhc_df['geometry'].loc[(erhc_df['id']==1) & (erhc_df['name']=='EERRHHCC')].iloc[0]
#print(x)

#print(erhc_df['geometry'].loc[(erhc_df['id']==1) & (erhc_df['name']=='EERRHHCC')].iloc[0])
#print(erlc_values)
#print(lrhc_values)
#print(lrlc_values)
#print(spm_values)
#print(cspm_values)


























#data['geometry'] = 'POLYGON '+data['geometry'].astype(str)
#print(datas)
#print(len(latitude))


#print(df)
#print(df.head(df.shape[0]).to_string())
#Polygon[[-82.991945,40.046500],[-82.991835,40.046610],[-82.991825,40.046620],[-82.991815, 40.046630]]
#d = {'id':[9,10,11,12], 'col1': ['name1', 'name2','name3','name 4'],'geometry': [Polygon([[-82.991945,40.046500],[-82.991835,40.046610],[-82.991825,40.046620],[-82.991815,40.046630]]),
                                                                #Polygon([[-82.995847,40.037385],[-82.995737,40.037495],[-82.995727,40.037505],[-82.995717,40.037515]]),
                                                                #Polygon([[-82.996863,40.026852],[-82.996853,40.026862],[-82.996843,40.026872],[-82.996973,40.026742]]),
                                                                #Polygon([[-82.991604,40.036130],[-82.991494,40.036240],[-82.991484,40.036250],[-82.991474,40.036260]])]}
#q = {'id':[30,31,32,33],'col1': ['name1', 'name2','name 3','name 4'],'geometry': [Polygon([[-82.995847,40.030751],[-82.995736,40.030862],[-82.995725,40.030873],[-82.995714,40.030884]]),
                                                                                  #Polygon([[-82.996273,40.036955],[-82.996162,40.037066],[-82.996151,40.037077],[-82.996140,40.037088]]),
                                                                                  #Polygon([[-82.994106,40.035592],[-82.993995,40.035703],[-82.993984,40.035714],[-82.993973,40.035725]]),
                                                                                  #Polygon([[-82.991390,40.038808],[-82.991279,40.038919],[-82.991268,40.038930],[-82.991257,40.038941]])]}
#print(d)
#dd = pd.DataFrame.from_dict(d)
#print(dd.head(dd.shape[0]).to_string())

#print(ee.head(ee.shape[0]).to_string())

#qf = geopandas.GeoDataFrame(q,crs="EPSG:4326")


#print(ee.dtypes)
#print(dd.dtypes)
#gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
#gdf.crs = "EPSG:3637"
#print(gdf)

#gdf.to_file('file.geojson', driver='GeoJSON')