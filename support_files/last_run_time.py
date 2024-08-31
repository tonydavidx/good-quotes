import datetime


with open('D:/Documents/Python/Scrapping Projects/goodquotes/data/lastrun.txt', "w") as f:
    f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
