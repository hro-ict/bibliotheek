import sqlite3
from easygui import *


con= sqlite3.connect("biebsql5.db")
cursor= con.cursor()

def table_boeken():
    cursor.execute("CREATE TABLE IF NOT EXISTS boeken (Barcodenummer TEXT , Boek TEXT, Schrijver TEXT)")
    con.commit ()
def table_leden():
    cursor.execute("CREATE TABLE IF NOT EXISTS leden (Passnummer TEXT , Naam TEXT, Achternaam TEXT, Email TEXT)")
    con.commit ()
def table_lenen():
    cursor.execute("CREATE TABLE IF NOT EXISTS lenen (Barcodenummer TEXT , Boek TEXT, Schrijver TEXT, Lener TEXT, Lenerpassnummer TEXT,Leendatum TEXT,Inleverdatum TEXT, Status TEXT)")
    con.commit ()
def add_leden(passnummer,naam,achternaam,email):
    cursor.execute("INSERT INTO leden VALUES('{}','{}','{}', '{}')".format(passnummer,naam,achternaam,email))
    con.commit()
def add_boeken(barcodenummer,boek,schrijver):
    cursor.execute("INSERT INTO boeken VALUES('{}','{}','{}')".format(barcodenummer,boek,schrijver))
    con.commit()
def add_lenen(barcodenummer,boek,schrijver,lener,lenerpassnummer,leendatum,inleverdatum,status):
    cursor.execute("INSERT INTO lenen VALUES('{}','{}','{}','{}', '{}', '{}', '{}','{}')".format(barcodenummer,
                                                                                boek,
                                                                                schrijver,
                                                                                lener,lenerpassnummer,
                                                                                leendatum,inleverdatum,status))
    con.commit()

def update(date,barc):
    cursor.execute("UPDATE lenen SET Status= 'Ingeleverd in {}' WHERE Barcodenummer= '{}'".format(date,barc))
    con.commit()

def wijzigen():
    sql_update_query = """Update medewerker set naam = 'newnaam' where naam = 'tom'"""
    cursor.execute(sql_update_query)
    con.commit()


def delete(tabel,column, delet):
    sql_Delete_query = """Delete from {} where {}= '{}' """.format(tabel,column,delet)
    cursor.execute(sql_Delete_query)
    con.commit()

def zoeken_boek(woord):
        sql = cursor.execute("SELECT * FROM boeken WHERE  Boek = '{0}' OR Schrijver= '{0}' OR Barcodenummer= '{0}'".format(woord))
        result = cursor.fetchall()

        if result:

            for x in result:
                    msgbox("Er zijn {} reultaten gevonden:\n\nBarcodenummer: {}\
                    \nBoek: {}\
                    \nSchrijver : {}\n**********************".format(len(result),x[0],x[1],x[2]))
        else:
            msgbox("Niks gevonden")


def zoeken_lid(woord):
    sql = cursor.execute("SELECT * FROM leden WHERE  Naam = '{0}' OR Achternaam= '{0}' OR Passnummer= '{0}' OR Email= '{0}'".format(woord))
    result = cursor.fetchall()
    if result:
        for x in result:
            msgbox("Passnummer: {}\
            \nNaam: {}\
            \nAchternaam : {}\nEmail :{}\n**********************".format(x[0],x[1],x[2],x[3]))
    else:
        msgbox("Niks geonden")



def delete_alles(table):
    sql_Delete_query = """Delete  from {} """.format(table)
    cursor.execute(sql_Delete_query)
    con.commit()
