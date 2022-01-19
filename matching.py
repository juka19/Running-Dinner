import pandas as pd
import random

df=pd.read_csv("data/example_file.csv", sep=";")

n_participants=len(df)
n_teams=n_participants//2
hosts=df[df['host']=='yes']['Name'].to_list()
no_hosts=df[df['host']=='no']['Name'].to_list()

df['Team']=''
count=1
while len(no_hosts)>0:
    team=(random.sample(hosts, 1)[0], random.sample(no_hosts, 1)[0])
    hosts.remove(team[0])
    no_hosts.remove(team[1])
    df['Team'].loc[df.Name.isin(team)]=f'team#{count}'
    count+=1

while len(hosts) > 0:
    team=random.sample(hosts, 2)
    hosts.remove(team[0])
    hosts.remove(team[1])
    df['Team'].loc[df.Name.isin(team)]=f'team#{count}'
    count+=1
    
# assign course
 # draw random sample of a third of total teams for each course 
 # assign the course to the team

# match with other-course teams
 # filter on course 
 # assign non-preparing teams to dining_group
 # repeat draw if teams matched before
 # assign course_host for each participant for each course