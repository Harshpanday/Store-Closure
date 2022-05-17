from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement, BarChartModule

from mesa.visualization.UserParam import UserSettableParameter
from main import ABM,erhc,erlc,lrhc,lrlc,cspm,spm
from mesa_geo.visualization.MapModule import MapModule

def abm_draw(agent):
    potrayal = dict()

    #if agent.atype is None:
        #potrayal["color"] = "Grey"
    #elif agent.atype == 0:
        #potrayal["color"] = "Red"
    if type(agent) is erhc:
        potrayal["color"] = "Red"
    if type(agent) is erlc:
        potrayal["color"] = "Blue"
    if type(agent) is lrhc:
        potrayal["color"] = "Green"
    if type(agent) is lrlc:
        potrayal["color"] = "Orange"
    if type(agent) is spm:
        potrayal["color"] = "Black"
    elif type(agent) is cspm:
        potrayal["color"] = "Purple"
    return potrayal

#happy_element = HappyElement()
map_element = MapModule(abm_draw,ABM.Map_coordinates, 9,700,700)
model_params = { "density" : UserSettableParameter("slider","Agent density",0.6,0.1,1.0,0.1),
                 "minority_pc": UserSettableParameter("slider","Fraction minority",0.2,0.00,0.1,0.05),
                 }

abm_chart = BarChartModule(
    [{"Label": "ERHC_FA", "Color": "blue"},{"Label": "ERLC_FA", "Color": "green"},
     {"Label": "LRHC_FA", "Color": "red"},{"Label": "LRLC_FA", "Color": "pink"}],canvas_height=300, canvas_width=500,
    data_collector_name="datacollector"

)


server = ModularServer(
    ABM, [map_element,abm_chart], "ABM",model_params
)

