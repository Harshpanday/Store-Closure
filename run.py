import os
os.chdir("./ABM/")
from .server import server
from .main import ABM
import profile
def runabm():
    abm_steps = ABM()
    for i in range(1):
        abm_steps.step()
    print("running")
    #profile.run(server.launch())
