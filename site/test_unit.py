from scrapper_bs4 import Scraper

data = Scraper("https://pt.stackoverflow.com/questions/tagged/")

data = data.data_scraper_stackoverflow("python")

for c in range(len(data)):
    print("pocapica")
    for coluna, valor in data.items():
        print(valor[c])
        print("C") 
    
# for i in data:
#     for x in data[i]:
#         print(data.i[x])
