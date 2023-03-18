from mesa_geo.visualization.ModularVisualization import ModularServer
#from mesa_geo.visualization.templates.js import BarChartModule
#from mesa.visualization.modules import BarChartVisualization
#import BarChartVisualization 
from mesa.visualization.UserParam import UserSettableParameter
from .main import ABM,erhc,erlc,lrhc,lrlc,cspm,spm
from mesa_geo.visualization.MapModule import MapModule
import os
#os.chdir("/fs/ess/PAS2271/Store_Closure_ABM")

def abm_draw(agent):
    potrayal = dict()
    if type(agent) is erhc:
        potrayal["color"] = "Red"
    if type(agent) is erlc:
        potrayal["color"] = "Blue"
    if type(agent) is lrhc:
        potrayal["color"] = "Green"
    if type(agent) is lrlc:
        potrayal["color"] = "Yellow"
    if type(agent) is spm:
        potrayal["color"] = "Black"
    elif type(agent) is cspm:
        potrayal["color"] = "Purple"
    return potrayal

#happy_element = HappyElement()
map_element = MapModule(abm_draw,ABM.Map_coordinates, 9,700,700)
model_params = { }

# abm_chart = BarChartVisualization.BarChartModule(
#     [{"Label": "ERHC_FA", "Color": "Red"},{"Label": "ERLC_FA", "Color": "Blue"},
#      {"Label": "LRHC_FA", "Color": "Green"},{"Label": "LRLC_FA", "Color": "Yellow"}],canvas_height=300, canvas_width=500,
#     data_collector_name="datacollector"

# )

server = ModularServer(
    ABM, [map_element], "ABM",model_params
)

