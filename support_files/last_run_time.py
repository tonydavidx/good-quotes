import datetime


with open('D:/Documents/Python/Scrapping Projects/goodquotes/data/lastrun.txt', "r") as f:
    file_data = f.readlines()

new_data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

file_data.insert(0, new_data+"\n")


with open('D:/Documents/Python/Scrapping Projects/goodquotes/data/lastrun.txt', "w") as f:
    f.writelines(file_data)
