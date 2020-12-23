from easygui import *
import json
import datetime
from datetime import date
from datetime import timedelta
import time
import random as ran
from hashlib import *

from sql_module import *
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



data_lenen = {}
data_leden = {}
data_boeken = {}


table_boeken()
table_leden()
table_lenen()

#Uncomment to database delete

#delete_alles("lenen")
#delete_alles("leden")
#delete_alles("boeken")

with open("files\data_leden.txt", "r+") as login_file:
    data_leden = json.load(login_file)
with open("files\data_boeken.txt", "r+") as login_file:
    data_boeken = json.load(login_file)
with open("files\data_lenen.txt", "r+") as file:
    data_lenen = json.load(file)




def nieuwe_lid():
    while True:
        msg = "NIEUWE LID REGISTRATIE"
        titel = "DE BIBILIOTHEEK"
        fieldNames = ["Voornaam", "Achternaam", "Email"]
        fieldValues = []
        fieldValues = multenterbox(msg, titel, fieldNames)
        sql = cursor.execute("SELECT * FROM leden  WHERE Email= '{}'".format(fieldValues[2]))
        result = cursor.fetchall()
        while 1:
            if fieldValues  == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is niet ingevuld.\n\n' % fieldNames[i])
            if errmsg == "": break  # no problems found
            fieldValues = multenterbox(errmsg, titel, fieldNames, fieldValues)

        if "@" not in fieldValues[2] or  not fieldValues[2].endswith(".nl") and not fieldValues[2].endswith(".com"):
            msgbox("Voer een geldige email adres in\nexample= name@service.com OR name@service.nl")
        elif result:
            msgbox("Email adress bestaat al")

        else:
            willekeurig = ran.randrange(100000, 999999)
            passnummer = fieldValues[1][:2] + str(willekeurig)
            data_leden[passnummer] = fieldValues[0], fieldValues[1], fieldValues[2]
            msgbox("PASSNUMMER: {}\
    \nNAAM: {}\
    \nACHTERNAAM: {}\
    \nEMAIL: {}\
    \nVERGEET UW PASSNUMMER NIET. WE WERKEN MET PASSNUMMERS".format(passnummer, fieldValues[0], fieldValues[1],fieldValues[2]),
                   image="images\welkom.gif")
            with open("files\data_leden.txt", "w") as login_file:
                json.dump(data_leden, login_file)
            add_leden(passnummer, fieldValues[0], fieldValues[1],fieldValues[2])
            home_menu()




def nieuwe_boek():
    while True:
        msg = "NIEUWE BOEK REGISTRATIE"
        titel = "DE BIBLIOTHEEK"
        fieldNames = ["Boek", "Schrijver"]
        fieldValues = ([])
        fieldValues = multenterbox(msg, titel, fieldNames)
        while 1:
            if fieldValues  == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is niet ingevuld.\n\n' % fieldNames[i])
            if errmsg == "": break  # no problems found
            fieldValues = multenterbox(errmsg, titel, fieldNames, fieldValues)

        willekeurig = ran.randrange(100000, 999999)
        barcodenummer = fieldValues[1][:2] + str(willekeurig)
        data_boeken[barcodenummer] = fieldValues[0], fieldValues[1]
        yn= ynbox("BARCODENUMMER: {}\nBOEK: {}\nSCHRIJVER: {}".format(barcodenummer, fieldValues[0], fieldValues[1]),
               image="images\\nieuweboek.gif")
        with open("files\data_boeken.txt", "w") as login_file:
            json.dump(data_boeken, login_file)
        print(data_boeken)
        add_boeken(barcodenummer,fieldValues[0],fieldValues[1])
        if yn== True:
            nieuwe_boek()
        else:
            home_menu()
 

def home_menu():
    versie = ("**************************WELKOM DE BIBLIOTHEEK****************")
    keuze_menu = ["LENEN",
                  "INLEVEREN",
                  "NIEUWE LID REGISTRATIE",
                  "NIEUWE BOEK TOEVOEGEN","ANDERE ZAKEN"
                ]
    button = buttonbox("{:>15}".format("KIES EEN MENU?"), title=versie, choices=keuze_menu, image="images\mediath.GIF")
    if button == keuze_menu[0]:
        lenen()
    if button == keuze_menu[1]:
        inleveren()
    if button == keuze_menu[2]:
        nieuwe_lid()

    if button == keuze_menu[3]:
        nieuwe_boek()
    if button == keuze_menu[4]:
        versie = ("**************************WELKOM DE BIBLIOTHEEK****************")
        keuze_menu = ["LIDMAATSCHAP OPZEGGEN",
                      "BOEK AFSCHRIJVEN", "BOEK ZEOEKEN", "LID ZOEKEN","TERUG",
                      "EXIT"]
        button = buttonbox("{:>15}".format("KIES EEN MENU?"), title=versie, choices=keuze_menu, image="images\mediath.GIF")
        if button== keuze_menu[0]:
            lid_verwijderen()
            home_menu()
        elif button== keuze_menu[1]:
            boek_afschrijven()
            home_menu()
        elif button== keuze_menu[2]:
            boek_zoeken()
            home_menu()
        elif button == keuze_menu[3]:
            lid_zoeken()
            home_menu()
        elif button == keuze_menu[4]:
            home_menu()
        else:
            exit()


def lenen():
    while True:
        msg = "LENEN"
        titel = "DE BIBLIOTHEEK"
        fieldNames = ["BARCODENUMMER", "PASNUMMER"]
        fieldValues = []
        fieldValues = multenterbox(msg, titel, fieldNames)
        leendatum = datetime.datetime.now()
        inleverdatum = leendatum + datetime.timedelta(days=21)
        while 1:
            if fieldValues  == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is niet ingevuld.\n\n' % fieldNames[i])
            if errmsg == "": break  # no problems found
            fieldValues = multenterbox(errmsg, titel, fieldNames, fieldValues)


        if fieldValues[1] not in data_leden.keys():
            msgbox("De lid bestaat niet")


        elif fieldValues[0] not in data_boeken.keys():
            msgbox("Het item is niet gevonden")
        else:
            passnummer = fieldValues[1]
            email = data_leden[fieldValues[1]][2]
            barcodenummer = fieldValues[0]
            boek = data_boeken[fieldValues[0]][0]
            schrijver = data_boeken[fieldValues[0]][1]
            lenersnaam = data_leden[fieldValues[1]][0]
            lenersachternaam = data_leden[fieldValues[1]][1]
            data_lenen[fieldValues[0]] = boek, schrijver, passnummer, lenersnaam, lenersachternaam, str(
                datetime.datetime.today().replace(microsecond=0))
            text= "BOEK GEGEVENS\
\nBARCODENUMMER: {}\
\nBOEK         : {}\
\nSCHRIJVER    : {}\
\n\nLENERGEGEVENS\
\nPASSNUMMER   : {}\
\nLENER        : {} {}\
\nLEENDATUM    : {}\
\nINLEVERDATUM : {}".format(barcodenummer,
                            boek,
                            schrijver,
                            passnummer,
                            lenersnaam,
                            lenersachternaam,
                            leendatum.replace(microsecond=0),
                            inleverdatum.replace(microsecond=0))

            msgbox(text, image="images\lenen.gif")
            with open("files\data_lenen.txt", "w+") as login_file:
                json.dump(data_lenen, login_file)
            add_lenen(barcodenummer,
                      boek,schrijver,
                      lenersnaam+" "+lenersachternaam,passnummer,
                      leendatum.replace(microsecond=0),inleverdatum.replace(microsecond=0), "nog niet ingeleverd")
            mail(email,text, lenersachternaam)
            if email.endswith("hr.nl"):
                webbrowser.open("https://webmail.hro.nl/")
                home_menu()
            elif email.endswith("gmail.com"):
                webbrowser.open("www.gmail.com")
                home_menu()
            elif email.endswith("hotmail.com"):
                webbrowser.open("www.hotmail.com")
                home_menu()
            home_menu()


def inleveren():
    while True:
        msg = "INLEVEREN"
        title = "DE BIBLIOTHEEK"
        fieldNames = ["BARCODENUMMER"]
        fieldValues = []
        fieldValues = multenterbox(msg, title, fieldNames)
        vandaag = datetime.datetime.today().replace(microsecond=0)
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "": break  # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
        if fieldValues[0] not in data_lenen.keys():
            msgbox(data_lenen.get(fieldValues[0], "Barcode nummer is niet gevonden"))
            continue
        else:
            barcodenummer = fieldValues[0]
            boek = data_lenen[fieldValues[0]][0]
            schrijver = data_lenen[fieldValues[0]][1]
            lenerpass = data_lenen[fieldValues[0]][2]
            lenersnaam = data_lenen[fieldValues[0]][3]
            lenersachternaam = data_lenen[fieldValues[0]][4]
            leendatum = data_lenen[fieldValues[0]][5]
            leendatum = datetime.datetime.strptime(data_lenen[fieldValues[0]][5], '%Y-%m-%d %H:%M:%S').replace(
                microsecond=0)
            behouden = vandaag - leendatum
            msgbox("GEGEVENS\
\nBarcodenummer   : {}\
\nBoek            : {}\
\nSchrijver       : {}\
\nLenerpassnummer : {}\
\nLenersnaam      : {}\
\nLenersachternaam: {}\
\nLeendatum       : {}\
\nInleverdatum    : {}\
\nU hebt het boek {} minuten en {} seconden behouden".format(barcodenummer,
                                                             boek,
                                                             schrijver,
                                                             lenerpass,
                                                             lenersnaam,
                                                             lenersachternaam,
                                                             leendatum,
                                                             vandaag,
                                                             round(behouden.seconds / 60),
                                                             behouden.seconds % 60), image="images\inleveren.gif")
            with open("files\data_lenen.txt", "w+") as file:
                json.dump(data_lenen, file)
        update(str(vandaag),fieldValues[0])

        home_menu()


def lid_verwijderen():
    while True:
        msg = ("LIDMAATSCHAP OPZEGGEN")
        title = "DE BIBLIOTHEEK"
        fieldNames = ["PASSNUMMER"]
        fieldValues = []
        fieldValues = multenterbox(msg, title, fieldNames)
        while 1:
            if fieldValues  == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is niet ingevuld.\n\n' % fieldNames[i])
            if errmsg == "": break  # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        if fieldValues[0] in data_leden.keys():
            del data_leden[fieldValues[0]]
            msgbox("Het lidmaatschap is opgezegd\
\nWij vinden jammer dat u niet meer lid bent van onze bibliotheek\
\nAls u opnieuw lid wil  worden,\
\nbent u altijd welkom", image="images\\bye.gif")
            with open("files\data_leden.txt", "w+") as file:
                json.dump(data_leden, file)
            delete("leden", "Passnummer", fieldValues[0])
            home_menu()
        else:
            msgbox("Passnummer is niet gevonden")



def boek_afschrijven():
    while True:
        msg = ("BOEK VERWIJDEREN")
        title = "DE BIBLIOTHEEK"
        fieldNames = ["BARCODENUMMER"]
        fieldValues = []
        fieldValues = multenterbox(msg, title, fieldNames)
        while 1:
            if fieldValues  == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is niet ingevuld.\n\n' % fieldNames[i])
            if errmsg == "": break  # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        if fieldValues[0] in data_boeken.keys():
            del data_boeken[fieldValues[0]]
            msgbox("Het boek is afgeschreven", image="images\\nieuweboek.gif")
            with open("files\data_boeken.txt", "w+") as file:
                json.dump(data_boeken, file)
            delete("boeken", "Barcodenummer", fieldValues[0])
            home_menu()
        else:
            msgbox("Het boek is niet gevonden")



def boek_zoeken():
    while True:
        msg = ("BOEK ZOEKEN")
        title = "DE BIBLIOTHEEK"
        fieldNames = ["ZOEK"]
        fieldValues = []
        fieldValues = multenterbox(msg, title, fieldNames)
        zoeken_boek(fieldValues[0])
        home_menu()


def lid_zoeken():
    msg = ("LID ZOEKEN")
    title = "DE BIBLIOTHEEK"
    fieldNames = ["ZOEK"]
    fieldValues = []
    fieldValues = multenterbox(msg, title, fieldNames)
    zoeken_lid(fieldValues[0])

def mail(mailaddress, tekst,lener):
    message = MIMEMultipart()  

    message["From"] =  "ict1crac@gmail.com" 

    message["To"] = mailaddress

    message["Subject"] = "No-reply" # subject of mail


    text = "Goededag meneer/mevrouw {}\nU hebt volgende boek geleend:\n\n{}".format(lener,tekst)


    message_body=  MIMEText(text,"plain") 

    mesaj.attach(message_body) 



    try:
        mail =  smtplib.SMTP("smtp.gmail.com",587)

        mail.ehlo() # SMTP server starting

        mail.starttls() 

        mail.login("maildadress@domanin.com","password") # Login on SMTP server

        mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())  # mail sending
        msgbox("Gegevens zijn  verstuurd naar ( {} )".format(mailadress))
        mail.close()  # SMTP server closed

    except:
        msgbox("Mail sturen is niet succesvol")
home_menu()
