import urllib.request
import json
from datetime import date
from datetime import datetime
from datetime import timedelta

#lastDate = lastDate + timedelta(days=1)

def getCurrOfDate(date):
    corrDate = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    currJson = json.loads(urllib.request.urlopen('https://exchangeratesapi.io/api/' + corrDate).read())
    return [datetime.strptime(currJson['date'], '%Y-%m-%d'), str(currJson['rates']['USD']).replace('.', ',')]

def getCurrOfToday():
    currJson = json.loads(urllib.request.urlopen('https://exchangeratesapi.io/api/latest?base=EUR').read())
    return [datetime.strptime(currJson['date'], '%Y-%m-%d'), str(currJson['rates']['USD']).replace('.', ',')]

def writeRowInCSV(date, rate):
    stringToWrite = str(date.year) + "-" + str(date.month) + ";" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + ";" + rate
    csv = open(csvLocation, 'a')
    csv.write('\n')
    csv.writelines(stringToWrite)
    csv.close()
    
def getCSVLocation():
    file = open('config.txt', 'r')
    configs = file.readlines()
    file.close()
    return configs[0]

def getLastCSVDate(csvLocation):
    file = open(csvLocation, 'r')
    lastLine = file.readlines()[-1]
    file.close()
    lastLine = lastLine.split(";")
    lastDate = datetime.strptime(lastLine[1], '%d-%m-%Y')
    return lastDate

csvLocation = getCSVLocation()
lastDate = getLastCSVDate(csvLocation)
today = datetime.today()

dateToGet = lastDate + timedelta(days=1)

if((today - dateToGet).days < 1):
    print("List was already updated")
else:
    while(not(today - dateToGet).days < 1):
        
        if(dateToGet.weekday() == 5 or dateToGet.weekday() == 6):
            print("skipped: " + str(dateToGet) + " because it is not a weekday")
        else:
            info = getCurrOfDate(dateToGet)
            writeRowInCSV(info[0], info[1])
            print("Added row with date: " + str(info[0]) + " and rate: " + str(info[1])) 
            
        dateToGet = dateToGet + timedelta(days=1)




    


