#import threading
import multiprocessing
import numpy as np
#import atpbar

#class StepThread(threading.Thread):
class StepThread(multiprocessing.Process):
    """
    [Class] StepThread
    Class for doing pathfinding in multithreading like process.
    
    Properties:
        - name = [string] name of this thread
        - agents = [array] array of agents
        - stepCount = [int] current step count which represent how many simulated seconds from the beggining of the simulation
        - stepValue = [int] how many step forward do we want to 
        - timeStamp = [array]  the timestamp of the history proporties
        - threadNumber = [int] how many thread this simulator allowed to create when doing pathfinding
        - activitiesDict = [dict] dictionary to store the activity type of the agent during this hour. key = agent's id
        - returnDict = [dict] dictionary to store the extracted movement sequence of the agent. key = agent's id
        - pathfindDict = [dict] dictionary to check for already calculated paths
        
    Deprecated Properties:
        - state = [string] current state (Deprecated, will be removed soon)
        - finished = [boolean] flag if the process is finished or not 
        
    TO DO: remove unused pipeline
    """
    def __init__(self, name, agents,timeStamp,returnDict,activitiesDict,businessesDict,pathfindDict,nodeHashIdDict,seed):
        """
        [Constructor] 
        Constructor for StepThread class

        Parameters:
            - name = [string] name of this thread
            - agents = [array] array of agents
            - stepCount = [int] current step count
            - returnDict = [dict] dictionary to store the extracted movement sequence of the agent. key = agent's id
            - activitiesDict = [dict] dictionary to store the activity type of the agent during this hour. key = agent's id
            - businessesDict = [dict] dictionary that maps the an array of business by their type. key = business's id
            - pathfindDict = [dict] dictionary to check for already calculated paths
        """
        #threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)
        self.name = name
        self.agents = agents
        self.state = "step"
        self.timeStamp = timeStamp
        self.stepValue = 24*3600
        self.activitiesDict = activitiesDict
        self.returnDict = returnDict
        self.finished = False
        self.businessDict = businessesDict
        self.rng = np.random.default_rng(seed)
        self.pathfindDict = pathfindDict
        self.nodeHashIdDict = nodeHashIdDict
        
    def setStateToStep(self,stepValue):
        """
        [Method] setStateToStep 
        mark that the stepthread is going to do pathfinding 

        Parameters:
            - stepValue : [int] How many seconds we want to step forward
        """
        self.state = "step"
        self.stepValue = stepValue
        
    def run(self):
        """
        [Method] run 
        main function that the MultiProcess class will run
        
        TO DO: remove unused pipeline
        """
        if self.state == "step":
            self.step()
        self.finished = True
        # print(f'{self.name} finished')

    def step(self):
        """
        [Method] step 
        pathfind function
        
        TO DO: merge with run
        """
        day = self.timeStamp.getDayOfWeek()
        hour = self.timeStamp.getHour()
        availableRestaurants = [x for x in self.businessDict["restaurant"] if x.isOpen(day, hour)]
        availableHospitals = [x for x in self.businessDict["hospital"] if x.isOpen(day, hour)]
        for i in range(0,len(self.agents)):
            result = self.agents[i].checkSchedule(self.timeStamp,self.rng,self.stepValue,availableRestaurants,availableHospitals,self.pathfindDict,self.nodeHashIdDict)
            self.activitiesDict[f"{self.agents[i].agentId}"] = self.agents[i].activities
            if result is not None:
                self.returnDict[f"{self.agents[i].agentId}"] = result
        

