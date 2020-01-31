from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url):
    #This is fuction for scrapping
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    table = soup.find_all('div', attrs={'class':'lister-item-content'}) 
    

    temp = [] #initiating a tuple

    for i in range(0, len(table)):

      judul = table[i].find('h3',attrs={'class':'lister-item-header'})
      judul2 = judul.find('a').text

      votes1 = table[i].find('p', attrs={'class':'sort-num_votes-visible'})
      votes2 = votes1.find('span', attrs={'name':'nv'}).text

      if(table[i].find('span', attrs={'class':'metascore favorable'}) is None): 
         meta = 0 
      else : 
         meta = table[i].find('span', attrs={'class':'metascore favorable'}).text.strip()

      rating = table[i].find('div', attrs={'class':'inline-block ratings-imdb-rating'})
      rating = rating.find('strong', attrs={'':''}).text

      temp.append((judul2,votes2,meta,rating)) 



    df = pd.DataFrame(temp, columns = ('Title','Votes','Metascore','Rating' ))
    df['Rating']=df['Rating'].astype('float64')
    df['Votes']=df['Votes'].str.replace(",","").astype('int64')
    df['Metascore']=df['Metascore'].astype('float64')

   #data wranggling -  try to change the data type to right data type

   #end of data wranggling

    return df

@app.route("/")
def index():
    df = scrap("https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31") #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
