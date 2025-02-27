import os
try:    os.mkdir("debug")
except: pass

def _on_show_jobs(model):
    def __count_jobs(agentlist, jobclasses):
        d = {}
        for job in jobclasses:
            d[job.name] = 0
            
        for agent in agentlist:
            d[agent.mainJob.jobClass.name] +=1
            
        out = "\n".join([f"- {k}: {v}" for k, v in d.items()])
        return out
    
    output = []
    output.append(f"\n====DEBUG====")
    output.append(f"Step Count: {model.timeStamp.stepCount}")
    output.append(f"# Agents: {len(model.agents)}")
    output.append(f"Jobs: \n{__count_jobs(agentlist=model.agents, jobclasses=model.jobClasses)}")
    output.append(f"============\n")

    print("\n".join(output))
    
def _on_show_orders(model, fnameout):
    def __get_worktime(agentlist, jobclass):
        d = {}
        for agent in agentlist:
            if agent.mainJob.jobClass.name == jobclass:
                d[agent.agentId] = f"days {agent.mainJob.workdays} from {agent.mainJob.startHour} to {agent.mainJob.startHour+agent.mainJob.workhour}"
                
        out = "\n".join([f"- agent {k}: {v}" for k, v in d.items()])
        return out

    output = []
    output.append(f"\n====DEBUG====")
    output.append(f"Delivery agents:\n{__get_worktime(agentlist=model.agents, jobclass='delivery_person')}")
    output.append(f"\nOrders Placed: {model.online_shopping.str_orders_history()}")
    output.append(f"============\n")
    
    file=open(f"debug/{fnameout}.txt",'w')
    for v in output:
        file.writelines([v])
    file.close()
    
    print("\n".join(output))
    
    
    
def _on_agents_position(model, save_or_show="save"):
    def __get_locations(agentlist, attr):
        l = []
        for agent in agentlist:
                l.append(getattr(agent, attr).building.coordinate.getLatLon())
                
        if save_or_show=="save":
            return l
        elif save_or_show=="show":
            out = "\n".join(map(str, l))
            return out
        
    
    import pandas as pd
    foutname = "cood"
    output = []
    output.append("\n====DEBUG====")
    output.append("Saving home")
    data = pd.DataFrame(__get_locations(agentlist=model.agents, attr='home'), columns=["latitude","longitude"])
    data.to_csv(f"./debug/home_{foutname}.csv", index=False)
    
    output.append("Saving workplace")
    data = pd.DataFrame(__get_locations(agentlist=model.agents, attr='mainJob'), columns=["latitude","longitude"])
    data.to_csv(f"./debug/workplace_{foutname}.csv", index=False)
    output.append("============\n")
    
    print("\n".join(output))