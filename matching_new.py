import pandas as pd
import random

df=pd.read_csv("data/example_file.csv", sep=";")

rest=len(df)%6
df=df[:len(df)-rest]

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
    df['Team'].loc[df.Name.isin(team)]=int(count)
    count+=1

while len(hosts) > 0:
    team=random.sample(hosts, 2)
    hosts.remove(team[0])
    hosts.remove(team[1])
    df['Team'].loc[df.Name.isin(team)]=int(count)
    count+=1
    
df['course']=''
courses=['starters', 'main', 'dessert']
teams=list(set(df['Team']))
for course in courses:
    dish=teams[0:5]
    [teams.remove(team) for team in dish]
    df['course'].loc[df.Team.isin(dish)]=f'{course}'

starters_df=pd.concat([df['Team'][df['course']=='starters'].drop_duplicates().sort_values().reset_index()['Team'].rename('starters'), 
                df['Team'][df['course']=='main'].drop_duplicates().sort_values().reset_index()['Team'].rename('guest_main'), 
                df['Team'][df['course']=='dessert'].drop_duplicates().sort_values().reset_index()['Team'].rename('guest_dessert')], 
               axis=1)

main=[starters_df['guest_main'].to_list()[-1]] + starters_df['guest_main'].to_list()[:-1]
guest_starters=starters_df['starters'].tolist()
guest_dessert=starters_df['guest_dessert'].to_list()[-2:] + starters_df['guest_dessert'].to_list()[:-2]

main_df=pd.DataFrame(list(zip(guest_starters, main, guest_dessert)),
                         columns=['guest_starters', 'main', 'guest_dessert'])

guest_main=[main_df['main'].to_list()[-1]] + main_df['main'].to_list()[:-1]
guest_starters=main_df['guest_starters'].tolist()
dessert=main_df['guest_dessert'].to_list()[-2:] + main_df['guest_dessert'].to_list()[:-2]

dessert_df=pd.DataFrame(list(zip(guest_starters, guest_main, dessert)),
                         columns=['guest_starters', 'guest_main', 'dessert'])
dessert_df

