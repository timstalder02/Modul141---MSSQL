createDatabase         =   'CREATE DATABASE M141'

useDatabase            =   'USE M141' 

createType             = '''CREATE TABLE Type (
	                        TypeID INT IDENTITY(1,1) PRIMARY KEY,
	                        name varchar(50),
                            );'''

createTag              ='''CREATE TABLE Tag (
	                       TagID INT IDENTITY(1,1) PRIMARY KEY,
	                       name varchar(50)
                           );'''

createSystemuser       ='''CREATE TABLE Systemuser(
	                       SystemuserID INT IDENTITY(1,1) PRIMARY KEY,
	                       uid int,
	                       name varchar(50)
                           );'''

createUsergroup        ='''CREATE TABLE Usergroup(
	                       UsergroupID INT IDENTITY(1,1) PRIMARY KEY,
	                       gid int,
	                       name varchar(50)
                           );'''

createData             ='''CREATE TABLE Data(
	                       DataID INT IDENTITY(1,1) PRIMARY KEY,
                           digest varchar(50),
                           content varchar(MAX),
                           size int,
                           compression int,
                           TypeID int
                           );'''

createMeta             ='''CREATE TABLE Meta(
                           MetaID INT IDENTITY(1,1) PRIMARY KEY,
                           path varchar(250),
                           perm int,
                           time int,
                           DataID int,
                           SystemuserID int,
                           UsergroupID int,
                           );'''

createTag_Data         ='''CREATE TABLE Tag_Data(
                           Tag_DataID INT IDENTITY(1,1) PRIMARY KEY,
                           DataID INT FOREIGN KEY REFERENCES Data(DataID),
                           TagID INT FOREIGN KEY REFERENCES Tag(TagID)
                           );'''

createImport           ='''CREATE TABLE import (count INT IDENTITY(1,1) PRIMARY KEY, 
                           digest nvarchar(50), path nvarchar(250), size int, type nvarchar(50),
                           mode int, uid int, [user] nvarchar(50), gid int, [group] nvarchar(50), time int, 
                           compression int, data nvarchar(MAX));'''


#SQL-Alter-Table

alterMetaNocheck       =  'ALTER TABLE Meta NOCHECK CONSTRAINT all;'
alterDataNocheck       =  'ALTER TABLE Data NOCHECK CONSTRAINT all;'
alterMetaDataID        =  'ALTER TABLE Meta ADD CONSTRAINT DataID FOREIGN KEY (DataID) REFERENCES Data(DataID);'
alterMetaSystemuserID  =  'ALTER TABLE Meta ADD CONSTRAINT SystemuserID FOREIGN KEY (SystemuserID) REFERENCES Systemuser(SystemuserID);'
alterMetaUsergroupID   =  'ALTER TABLE Meta ADD CONSTRAINT UsergroupID FOREIGN KEY (UsergroupID) REFERENCES Usergroup(UsergroupID);'
alterDataType          =  'ALTER TABLE Data ADD CONSTRAINT TypeID FOREIGN KEY (TypeID) REFERENCES [Type](TypeID);'

#Change IdentityInsert
setIdentityInsertOn  = 'SET IDENTITY_INSERT import ON'
setIdentityInsertOff = 'SET IDENTITY_INSERT import OFF'

#Insert 2 Import
insertStatement      = 'INSERT INTO import (count, digest, path, size, type, mode, uid, [user], gid, [group], time, compression, data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'

#Simple import-statements in variables (No FK)
importType =        'INSERT INTO Type (name) SELECT DISTINCT type FROM import;'
importSystemuser =  'INSERT INTO Systemuser (uid, name) SELECT DISTINCT [uid], [user] FROM import;'
importUsergroup =   'INSERT INTO Usergroup (gid, name) SELECT DISTINCT [gid], [group] FROM import;'

#SQL-Import-Statements
DataSqlCommand       = "INSERT INTO Data (digest, content, size, compression, TypeID) VALUES (?,?,?,?,?)"
MetaSqlCommand       = "INSERT INTO Meta (path, perm, time, DataID, SystemuserID, UsergroupID) VALUES (?,?,?,?,?,?)"

#Drop-User funktioniert nicht per ODBC
# #Drop-Users
# dropFriggapp         = 'DROP USER IF EXISTS friggapp'
# dropFriggrep         = 'DROP USER IF EXISTS friggrep'

#Create-Login 
loginFriggapp        = "CREATE LOGIN friggapp WITH PASSWORD = 'sml12345';"
loginFriggrep        = "CREATE LOGIN friggrep WITH PASSWORD = 'sml12345';"

#Create-User
userFriggapp         = 'CREATE USER friggapp for login friggapp;'
userFriggrep         = 'CREATE USER friggrep for login friggrep;'

#Alter-User
alterFriggapp        = 'ALTER ROLE [db_owner] ADD MEMBER friggapp;'
alterFriggrep        = 'ALTER ROLE [db_datareader] ADD MEMBER friggrep;'