from easygui import *
from bibliotheek import *

versie = ("**************************WELKOM MEDIATHEK HOGESCHOOL ROTTERDAM****************")
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
    versie = ("**************************WELKOM MEDIATHEK HOGESCHOOL ROTTERDAM****************")
    keuze_menu = ["LIDMAATSCHAP OPZEGGEN",
                  "BOEK AFSCHRIJVEN", "BOEK ZEOEKEN", "LID ZOEKEN",
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
    else:
        exit()