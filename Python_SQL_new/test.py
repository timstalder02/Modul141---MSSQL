

#Selects mit Python

import pyodbc
import os
import keyring

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=VMWS1\\M141;'
                      'Database=master;'
                      'Trusted_Connection=yes;'
                      'UID=vmadmin;' #Passwort sicher gespeichert
                      'PWD=' + str(keyring.get_password('Datenbank', 'vmadmin'))+";'")
cursor = conn.cursor()
cursor.execute("use M141;")

select = "select * from Systemuser;"

cursor.execute(select)

for row in cursor.fetchall():
    print(row)