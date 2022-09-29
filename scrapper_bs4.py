from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

class Scraper:
    def __init__(self, url):
        self.url = url


    def data_scraper_devgo(self):

        pagina = requests.get(self.url)
        soup = BeautifulSoup(pagina.content, "html.parser")

        titulos = soup.find_all("h1", class_="blog-article-card-title")
        link = [self.url + i.find("a").get("href") for i in titulos]
        titulos = [i.text for i in titulos]
        

        autor = soup.find_all("a", class_="blog-article-card-author-name")
        autor = [i.text for i in autor]

        t_leitura = soup.find_all("span")
        t_leitura = [i.text for i in t_leitura]
        t_leitura = [i for i in t_leitura if i]
        t_leitura.pop(0)
        t_leitura.pop(len(t_leitura) - 1)

        dados_post = {
                "Titulo": [i for i in titulos],
                "Autor": [i for i in autor],
                "T_Leitura": [i for i in t_leitura],
                "Link": [i for i in link]
        }

        return dados_post

    def data_scraper_stackoverflow(self, tag, n_pags):
        short_url = "https://pt.stackoverflow.com"
        new_url = self.url + tag
        
        dados = {
        "Titulo": [],
        "Autor": [],
        "Respostas": [],
        "Votos": [],
        "Visitas": [],
        "Link": [],
        }
        
        for i in range(1, int(n_pags) + 1):
            newer_url = new_url + f"?tab=newest&page={i}&pagesize=15"
            pagina = requests.get(newer_url)
            soup = BeautifulSoup(pagina.content, "html.parser")


            titulos = soup.find_all("h3", class_="s-post-summary--content-title")
            link = [short_url + i.find("a").get("href") for i in titulos]
            titulos = [i.text for i in titulos]
            titulos = [i.strip("\n") for i in titulos]

            autor = soup.find_all("div", class_="s-user-card--link d-flex gs4")
            autor = [i.text for i in autor]
            autor = [i.strip("\n") for i in autor]
            autor = [i.title() for i in autor]

            votos_resposta_visitas = soup.find_all("div", class_="s-post-summary--stats-item")
            votos_resposta_visitas = [i.text for i in votos_resposta_visitas]
            c = 0
            votos = []
            respostas = []
            visitas = []

            for i in votos_resposta_visitas:
                if c == 0:
                    votos.append(i)
                    c += 1
                elif c == 1:
                    respostas.append(i)
                    c += 1
                else:
                    visitas.append(i)
                    c = 0
            votos = [i.replace("\n", " ") for i in votos]
            respostas = [i.replace("\n", " ") for i in respostas]
            visitas = [i.replace("\n", " ") for i in visitas]

            [dados["Titulo"].append(i) for i in titulos]
            [dados["Autor"].append(i) for i in autor]
            [dados["Respostas"].append(i) for i in respostas]
            [dados["Votos"].append(i) for i in votos]
            [dados["Visitas"].append(i) for i in visitas]
            [dados["Link"].append(i) for i in link]

        return dados

    def data_scraper_acmods(self):
        short_url = "https://www.racedepartment.com"
        pagina = requests.get(self.url)
        soup = BeautifulSoup(pagina.content, "html.parser")

        versao = soup.find_all("span", class_="u-muted")
        versao = [i.text for i in versao]
        versao = [re.sub("[v,V]", "", r) for r in versao]

        modelo = soup.find_all("div", class_="structItem-title")
        link = [short_url + i.find("a").get("href") for i in modelo]
        modelo = [i.find("a") for i in modelo]
        modelo = [i.text for i in modelo]

        rating = soup.find_all("span", class_="u-srOnly")
        rating = [i.text for i in rating]
        rating = [re.sub("[^0-9]", "", i) for i in rating]
        rating = [i for i in rating if i]
        rating = [int(i)/100 for i in rating]

        data = {  
                "Modelo": [i for i in modelo],
                "Versao": [i for i in versao],
                "Nota": [i for i in rating],
                "Link": [i for i in link]
                }
        return data

