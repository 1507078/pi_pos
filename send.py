import os
import time
import datetime
import requests
import shutil
def upload_transaction(trans):
	url = 'https://antimind.000webhostapp.com/Raspberry/insert_transaction.php'
	str_Date = "'" + trans[0] + "'"
	str_Time = "'" + trans[1] + "'"
	str_Money = "'" + trans[2].strip('$') + "'"
#	print (str_Date)
#	print (str_Time)
#	print (str_Money)

	transaction = {'Date': str_Date, 'Time': str_Time, 'Money': str_Money}
	res = requests.get(url,params=transaction)
#	print(res.url)
#	print(res.text)
	return res.text

def check_today(fileDate):
    file_date = fileDate[0] + fileDate[1] + fileDate[2] + fileDate[3] +  fileDate[4] + fileDate[5] 
#    print file_date
    now_date = time.strftime("%Y%m%d%H%M%S")
#    print now_date
    d1 = datetime.datetime.strptime(file_date, "%Y%m%d%H%M%S")
    d2 = datetime.datetime.strptime(now_date, "%Y%m%d%H%M%S")
#    print d1
#    print d2
    if d1 <= d2:
        return 0
    elif d1 == d2:
	return 1
    return 2

def send(file):
    file_data = []
    loadFile = open(os.path.join("data/", file), 'rb')
    file_data.append(loadFile.read())
    loadFile.close()
#    print file_data
    for transaction in file_data:
#        print transaction
        trans = transaction.strip('\n').split(" ",3)
#	print trans
        ret = upload_transaction(trans)
	if ret[:6] == "con_ok":
	    moveFile(file)
    return 1

def moveFile(file):
    shutil.move("data/" + file, "backup/" + file)

def do_send():
    if os.system('ping -c 1 8.8.8.8') == 0:
        os.system('sync')
        print "send ..."
        for fileNames in os.walk("data/"):
#            print fileNames
            for file in fileNames[2]:
                fileName = os.path.splitext(file)[0]
	        if len(fileName) == 19:
#	            print fileName
	            fileDate =  fileName.split('-',5)	
	            if int(fileDate[0]) == 2017:
#		        print fileDate
		        ret = check_today(fileDate)
#		        print "check " +  str(ret)
		        if ret == 0:
  		            send(file)		    
        print "send ... end"
