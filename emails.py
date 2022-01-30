from pickle import load
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open('data/participants_df.pickle', 'rb') as handle:
    df = load(handle)
    

name=df[df["Name"]=="random1"]["Name"].iloc[0]
def send_running_dinner_email(name):
    sender_email="mds.running.dinner@googlemail.com"
    receiver_email=df[df["Name"]==name]["Email"]
    message = MIMEMultipart("alternative")
    message["Subject"] = "MDS Running Dinner"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    team=df[df["Name"]==name]["Team"].iloc[0]
    partner=df[df["Team"]==team][df["Name"]!=name]["Name"].iloc[0] # make sure to adapt this to teams with more than 2 peeps with a tuple
    course=df[df["Name"]==name]["course"].iloc[0]
    
    # A few variables for adapting the text. Essentially these should be logical tests, wheter certain conditions are met
    
    dinner_prep='' # I would already create a whole text block here rather than just extracting just the allergy, and then piece the whole text together
    address1='' # Same for this. Notice that the address will obviously not always be the same one!
    address2=''
    hosting_7='' # Variable for hosting more than 6 people. Also we should probably somehow write a test for whether there are dinners with even more people

    html_text = f"""\
    <html>
    <body>
        <p>Hi {name},<br>
        How are you?<br>
        You will be preparing a {course} with {partner[0]}
        
        </p>
    </body>
    </html>
    """
    message.attach(MIMEText(html_text, "html"))
    
    return (sender_email, receiver_email, message)



port=465
password='mdsrunningdinner'
context=ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("mds.running.dinner@googlemail.com", password)
    for name in names:
        email=send_running_dinner_email(name)
        server.sendmail(
            email[0], email[1], email[2].as_string()
        )