from pickle import load
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pandas import isnull
import pandas as pd
import random
from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
import os

with open('data/participants_df.pickle', 'rb') as handle:
    df=load(handle)

def send_running_dinner_email(name):
    sender_email="mds.running.dinner@googlemail.com"
    receiver_email=df[df["Name"]==name]["Email"].iloc[0]
    message = MIMEMultipart("alternative")
    message["Subject"] = "MDS Running Dinner"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    team=df[df["Name"]==name]["Team"].iloc[0]
    partner=df[df["Team"]==team][df["Name"]!=name]["Name"].iloc[0] 
    course=df[df["Name"]==name]["course"].iloc[0]
    
    if course=="starters":
        guests=tuple(map(int, df[df["Team"]==team]['starters_group'].iloc[0].replace('(', '').replace(')', '').split(', ')))
    elif course=="main":
        guests=tuple(map(int, df[df["Team"]==team]['main_group'].iloc[0].replace('(', '').replace(')', '').split(', ')))
    elif course=='dessert':
        guests=tuple(map(int, df[df["Team"]==team]['dessert_group'].iloc[0].replace('(', '').replace(')', '').split(', ')))
    
    allergy_list = []
    [[allergy_list.append(allergy) for allergy in df[df["Team"]==guest]['allergies/preferences'].tolist()] for guest in guests]
    allergy_list = list(set([element for element in allergy_list if ~isnull(element) and isinstance(element, float) != True]))
    
    if len(allergy_list) > 1:
        allergies=f"For the MDS Running Dinner, we would like you to <b>prepare only vegetarian dishes</b>. Please also make sure to take into account these things your guests wished for: '{'; '.join(allergy_list)}'"
    else: allergies=f'While your guests do not have any special dietary requirements, please adhere to the guidelines of the MDS Running Dinner and <b>prepare a vegetarian dish</b>!'
    
    partner_email=df[df["Name"]==partner]["Email"].iloc[0]
        
    address_list=[]
    for course in ['starters', 'main', 'dessert']:
        teams=tuple(map(int, df[df["Team"]==team][course+"_group"].iloc[0].replace('(', '').replace(')', '').split(', ')))
        filter_df=pd.concat([df[df["Team"]==team][df["host"]=="yes"] for team in teams], axis=0) 
        address_list.append(random.choice(filter_df[filter_df["course"]==course]["address"].to_list()))
    
    n_meals=len(pd.concat([df[df["Team"]==guest] for guest in guests], axis=0))

    html_text="<html>"+"<body>"\
    f"<p>Hi {name},<br><br>"\
    f"Get your cooking spoon and lay the table, we have found you a team and assigned you a course to prepare!<br><br>"\
    f"You will be preparing a <b>{course}</b> course with <b>{partner}</b>! If you do not know eachother already, please contact your partner via his/her email address: {partner_email} <br><br>"\
    f"{allergies} <br>"\
    f"Please make sure that you (or your partner) can host at least <b>{n_meals} guests</b> and provide a dish for everyone.<br>"\
    f"<br>"\
    f"Please find below the addresses at which you will be having your respective courses:<br><br>"\
    f"Starters: {address_list[0]}<br>"\
    f"Main dish: {address_list[1]}<br>"\
    f"Dessert: {address_list[2]}<br><br>"\
    f"We wish you a great time preparing the dish, great company and a lot of fun!<br><br>"\
    f"Please don not hesitate to get in touch if there is anything unclear to you.<br><br>"\
    f"Best regards & guten Apetit, <br><br>"\
    f"Francesca, Hannah, Julian and Katalin <br>"\
    f"</p>"\
    f"</body>"\
    f"</html>"
    
    message.attach(MIMEText(html_text, "html"))
    return (sender_email, receiver_email, message)



port=465
password='mdsrunningdinner'
context=ssl.create_default_context()

names=["Francesca", "Hannah", "Katalin", "Julian"]

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("mds.running.dinner@googlemail.com", password)
    for name in names:
        email=send_running_dinner_email(name)
        server.sendmail(
            email[0], email[1], email[2].as_string()
        )
