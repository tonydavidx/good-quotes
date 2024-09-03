import unidecode

text = "The gospel has done its work in us when we crave God more than we crave everything else in life and when seeing His kingdom advance in the lives of others gives us more joy than anything we could own. When we see Jesus as greater than anything the world can offer, we\u2019ll gladly let everything else go to possess Him.\n"

text = unidecode.unidecode(text)

print(text)

with open("D:/Documents/Python/Scrapping Projects/goodquotes/data/lastrun.txt", "w") as f:
    f.write(text)
