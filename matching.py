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

df['course']=''
courses=['starters', 'main', 'dessert']
teams=list(set(df['Team']))
for course in courses:
    dish=random.sample(teams, int(len(df)/2/len(courses)))
    [teams.remove(team) for team in dish]
    df['course'].loc[df.Team.isin(dish)]=f'{course}'

starter_guests_main=list(set(df['Team'][df['course']=='main']))
starter_guests_dessert=list(set(df['Team'][df['course']=='dessert']))
df['starters_id']=''
count=1
for hoster in list(set(df['Team'][df['course']=='starters'])):
    guests=(starter_guests_main.pop(0), 
            starter_guests_dessert.pop(0), 
            hoster)
    df['starters_id'].loc[df.Team.isin(guests)]=f'starter#{count}'
    count+=1
    
main_guests_starter=list(set(df['Team'][df['course']=='starters']))
main_guests_dessert=list(set(df['Team'][df['course']=='dessert']))
df['main_id']=''
count=1
for hoster in list(set(df['Team'][df['course']=='main'])):
    hoster_id=df['starters_id'][df['Team']==hoster].iloc[0]
    fmgs=[guest for guest in list(set(df['Team'][df['starters_id']!=hoster_id].loc[df.Team.isin(main_guests_starter)]))]
    fmgd=[guest for guest in list(set(df['Team'][df['starters_id']!=hoster_id].loc[df.Team.isin(main_guests_dessert)]))]
    guests=(fmgs.pop(0), fmgd.pop(0), hoster)
    main_guests_starter.remove(guests[0])
    main_guests_dessert.remove(guests[1])
    df['main_id'].loc[df.Team.isin(guests)]=f'main#{count}'
    count+=1
    
dessert_guests_starter=list(set(df['Team'][df['course']=='starters']))
dessert_guests_main=list(set(df['Team'][df['course']=='main']))
df['dessert_id']=''
count=1
for hoster in list(set(df['Team'][df['course']=='dessert'])):
    hoster_id1=df['starters_id'][df['Team']==hoster].iloc[0]
    hoster_id2=df['main_id'][df['Team']==hoster].iloc[0]
    fdgm=[guest for guest in 
          list(set(df['Team'][df['starters_id']!=hoster_id1][df['main_id']!=hoster_id2].loc[df.Team.isin(dessert_guests_main)]))]
    fdgs=[guest for guest in 
          list(set(df['Team'][df['starters_id']!=hoster_id1][df['main_id']!=hoster_id2].loc[df.Team.isin(dessert_guests_starter)]))]
    print(fdgm)
    print('--------')
    print(fdgs)
    print('_________________')
    guests=(fdgs.pop(0), fdgm.pop(0), hoster)
    dessert_guests_starter.remove(guests[0])
    dessert_guests_main.remove(guests[1])
    df['dessert_id'].loc[df.Team.isin(guests)]=f'dessert#{count}'
    count+=1
    

# match with other-course teams
 # filter on course 
 # assign non-preparing teams to dining_group
 # repeat draw if teams matched before
 # assign course_host for each participant for each course