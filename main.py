import sys
import os
import yaml
import argparse
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as mmap
from lib.Renderer.Controller import Controller
from lib.Renderer.Controller import View
from lib.Simulation.Simulator import Simulator
import random

configFileName = "config.yml"

requiredConfigs = [
    "OSMfile",
    "jobsFile",
    "businessFile",
    "numberOfAgents",
    "buildingConfigPath",
    "threadNumber",
    "infectedAgent",
    "vaccinationPercentage",
    "windowWidth",
    "windowHeight",
    "reportDir",
    "reportInterval",
]

optionalConfig = [
    "buildConnFile",
    "pathfindFileName",
]

def read_validate_config(file_path):
    config = None
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    err = False
    errMessage = "Missing required attributes in config file: "
    for c in requiredConfigs:
        if c not in config:
            err = True
            errMessage += c + " "
    if err:
        raise NameError(errMessage)
    for c in optionalConfig:
        if c not in config:
            config[c] = None

    return config

def parseArgs():
    global configFileName
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="sets the config file")
    parser.add_argument("-s", "--seed", type=int, help="sets the seed")
    parser.add_argument("--no_infectious_stop", action="store_true", help="Interromps the execution if infection is no longer possible")
    parser.add_argument("-nr", "--no_render",  action="store_true", help="Execute the program without render" )
    args = parser.parse_args()
    
    if args.config_file:
        configFileName = args.config_file
    no_infectious_stop = False
    
    if args.no_infectious_stop:
        no_infectious_stop = True
    render = True
    
    if args.no_render:
        render = False

    seed = 1000
    if args.seed:
        seed = args.seed

    return configFileName, no_infectious_stop, render, seed
    
def main():

    configFileName, no_infectious_stop, render, seed = parseArgs()
    c = read_validate_config(configFileName)

    # Load the data
    gridSize = (c["gridHeight"], c["gridWidth"])
    osmMap = mmap.readFile(
        OSMfilePath = c["OSMfile"], 
        buildConnFile = c["buildConnFile"],
        grid = gridSize,
        buildingCSV = c["buildingConfigPath"])

    # Start Simulator
    sim = Simulator(
        osmMap = osmMap,
        jobCSVPath = c["jobsFile"],
        businessCVSPath = c["businessFile"],
        pathfindFileName = c["pathfindFileName"],
        agentNum = c["numberOfAgents"],
        threadNumber = c["threadNumber"],
        infectedAgent = c["infectedAgent"],
        vaccinationPercentage = c["vaccinationPercentage"],
        reportPath = c["reportDir"],
        reportInterval = c["reportInterval"],
        seed=seed)

    if render:
        # Draw    
        windowSize = (c["windowWidth"], c["windowHeight"])
        view = View(mymap=osmMap, simulation=sim, window_size=windowSize)
        app = Controller(model=sim, view=view)
        app.main_loop()
    else:
        stepSize = c["nr_step_size"] #5 minutes
        dayToSimulate = c["nr_day_to_simulate"]
        for x in range(0, dayToSimulate*24*3600, stepSize):
            sim.step(stepSize = stepSize)   
            _, seirStatus = sim.getAgentStatus()
            if no_infectious_stop and seirStatus["Infectious"] + seirStatus["Exposed"] == 0: 
                break

    sim.extract()
    sim.extractVisitLog() #extract all visit log

if __name__ == "__main__":
    main()
    
