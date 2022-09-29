from flask import Flask, render_template, request
from scrapper_bs4 import Scraper
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def devgo_page():
    data = Scraper("https://devgo.com.br")
    datahtml = pd.DataFrame(data=data.data_scraper_devgo())
    return render_template("devgo.html", devgo_data=data.data_scraper_devgo(), tables=[datahtml.to_html(classes="data")], titles=datahtml.columns.values)

@app.route('/stackoverflow', methods=("POST", "GET"))
def stackoverflow_page():
    data = Scraper("https://pt.stackoverflow.com/questions/tagged/")
    datahtml = pd.DataFrame(data=data.data_scraper_stackoverflow("javascript", 1))
    return render_template("stackoverflow.html", stack_data=data.data_scraper_stackoverflow("javascript", 1), tables=[datahtml.to_html(classes="data")], titles=datahtml.columns.values)

@app.route('/assetto', methods=("POST", "GET"))
def assetto_page():
    data = Scraper("https://www.racedepartment.com/downloads/categories/ac-cars.6/?order=rating_weighted&direction=desc")
    datahtml = pd.DataFrame(data=data.data_scraper_acmods())
    return render_template("assetto.html", assetto_data=data.data_scraper_acmods(), tables=[datahtml.to_html(classes="data")], titles=datahtml.columns.values)


@app.route('/custom',  methods=("POST", "GET"))
def custom_page():
    tag = request.form.get("tag")
    n_pags = request.form.get("n_pags")
    data = Scraper("https://pt.stackoverflow.com/questions/tagged/")
    data = data.data_scraper_stackoverflow(tag=tag, n_pags=n_pags)
    datahtml = pd.DataFrame(data=data)
    return render_template("/custom.html", stack_data=data, tag=tag, n_pags=n_pags, tables=[datahtml.to_html(classes="data")], titles=datahtml.columns.values)





if __name__ == ("__main__"): 
    app.run(debug=True)