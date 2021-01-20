## IMPORTS ##

#Packages
import pyodbc
import os
import keyring


#Selber erstellte Module
from SQL_Commands import *
from Dict_Type import dictTypeID
from Dict_Systemuser import dictSystemuserID
from Dict_Usergroup import dictUsergroupID
from Dict_Digest import dictDigestID
from Constants import IMPORT_FILE, INSERT_LOG, PERM_APPEND, PERM_READ, DELEMITER

## VARIABLEN ##

lineCounter = 0

#Standardwerte
DEFAULT_FK_SYSTEMUSER = 1
DEFAULT_FK_USERGROUP  = 1

## LISTEN ##

createUsers            = [useDatabase, loginFriggapp, loginFriggrep, userFriggapp, userFriggrep, alterFriggapp, alterFriggrep]
createDatabaseTables   = [createDatabase, useDatabase, createType, createTag, createSystemuser, createUsergroup, createData, createMeta, createTag_Data, createImport]
simpleImportStatements = [useDatabase, importType, importSystemuser, importUsergroup]
alterTable             = [useDatabase, alterMetaNocheck, alterDataNocheck, alterMetaDataID, alterMetaSystemuserID, alterMetaUsergroupID, alterDataType]
filesDelete            = [INSERT_LOG]

## FUNKTIONEN ##

def execute_sql_statements(usedList):
    for command_to_execute in usedList:        
        cursor.execute(command_to_execute)
        cursor.commit()

def delete_files(usedList):
    for fileDelete in filesDelete:
        if os.path.exists(fileDelete):
            os.remove(fileDelete)


#Verbindung zum SQL-Server herstellen
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=VMWS1\\M141;'
                      'Database=master;'
                      'Trusted_Connection=yes;'
                      'UID=vmadmin;' #Passwort sicher gespeichert
                      'PWD=' + str(keyring.get_password('Datenbank', 'vmadmin'))+";'")

cursor = conn.cursor()
conn.autocommit = True 
#Löschen von Log-Files
delete_files(filesDelete)

# Datenbank und Tabellen erstellen
execute_sql_statements(createDatabaseTables)
print("Datenbank und Tabellen erstellt")
cursor.execute(setIdentityInsertOn) # Manuelle Einträge in Schlüsselfelder erlauben


#Importtable erstellen
with open(INSERT_LOG, PERM_APPEND) as insertLog:
    with open(IMPORT_FILE, PERM_READ) as importFile:
        for line in importFile:
            lineFormated = line.strip().split(DELEMITER)
            if lineCounter == 0:
                lineCounter += 1
                continue
            
            counter     = lineFormated[0]
            digest      = lineFormated[1]
            path        = lineFormated[2]
            size        = lineFormated[3]
            type_       = lineFormated[4] # type_ weil "type" ein Pythonausdruck ist
            mode        = lineFormated[5]
            uid         = lineFormated[6]
            user        = lineFormated[7]
            gid         = lineFormated[8]
            group       = lineFormated[9]
            time        = lineFormated[10]
            compression = lineFormated[11]
            data        = lineFormated[12]

            Values = [counter, digest, path, size, type_, mode, uid, user, gid, group, time, compression, data]
            insertLog.write(str(insertStatement + " " + str(Values) + "\n"))
            cursor.execute(insertStatement, Values)
print("Importtabelle erstellt")
lineCounter = 0

#Daten in Tabllen ohne FK importieren
execute_sql_statements(simpleImportStatements)
print("Tabellen ohne Fremdschlüssel (Type, Systemuser, Usergroup) erstellt")

#Daten in Tabelle Data importieren
with open(IMPORT_FILE, PERM_READ) as importFile:
    for line in importFile:
        lineFormated = line.strip().split(DELEMITER)
        if lineCounter == 0:
            lineCounter += 1
            continue

        digest      = lineFormated[0]
        size        = lineFormated[3]
        compression = lineFormated[11]
        data        = lineFormated[12]
        type_       = lineFormated[4]

        if type_ in dictTypeID:
            FK_Type = dictTypeID.get(type_)
        Values = [digest, data, size, compression, FK_Type]
        cursor.execute(DataSqlCommand, Values)
print("Tabelle Data erstellt")
lineCounter = 0


#Daten in Tabelle Meta importieren
with open(IMPORT_FILE, PERM_READ) as importFile:
    for line in importFile:
        lineFormated = line.strip().split(DELEMITER)
        if lineCounter == 0:
            lineCounter += 1
            continue

        digest = lineFormated[1]
        path   = lineFormated[2]
        mode   = lineFormated[5]
        user   = lineFormated[7]
        group  = lineFormated[9] 
        time   = lineFormated[10]

        if user in dictSystemuserID:
            FK_Systemuser = dictSystemuserID.get(user)
        else:
            FK_Systemuser = DEFAULT_FK_SYSTEMUSER
        if group in dictUsergroupID:
            FK_Usergroup = dictUsergroupID.get(group)
        else:
            FK_Usergroup = DEFAULT_FK_USERGROUP
        if digest in dictDigestID:
            FK_Digest = dictDigestID.get(digest)
        Values = [path, mode, time, FK_Digest, FK_Systemuser, FK_Usergroup]
        cursor.execute(MetaSqlCommand, Values)
print("Tabelle Meta erstellt")
lineCounter = 0


cursor.execute(setIdentityInsertOff)

execute_sql_statements(createUsers)
print("Benutzer wurden erstellt und entsprechen berechtigt")

execute_sql_statements(alterTable)
print("Die Beziehungen zwischen den Tabellen wurden erstellt")







