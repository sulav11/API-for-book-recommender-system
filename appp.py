
import uvicorn 
from fastapi import FastAPI



import numpy as np
import pickle 
import pandas as pd
import json
from sklearn.neighbors import NearestNeighbors

pivot_table = pickle.load(open('pivot_table.pkl','rb'))
ratings = pickle.load(open('ratings.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))
dataset = pd.read_csv('dataset.csv')

with open('Book-Lists.json') as d:
    Book_list = json.load(d)
   


app = FastAPI()

app.get('/')
def ask_():
    return f'What would you like to read'


@app.get("/BookLists/")
def function_1():
    return ratings['Book-Title']


@app.post("/Recommend/")
def recommend(book):
    a = book
    b =  list(Book_list.keys())[list(Book_list.values()).index(a)]
    c = int(b)
    recommended_books= []
    distances, suggestions = model.kneighbors(pivot_table.iloc[c, :].values.reshape(1, -1))
    for i in range(6):
        if i != 0:
            recommended_books.append(pivot_table.index[suggestions[0,i]])
    return recommended_books
  

@app.post("/Details/")
def details(book):
    Book_Title = recommend(book)
    book_name = []
    author = []
    isbn = []
    imgurl = []
    price=[]
    rating=[]
    total_votes = []
    for ele in Book_Title:
        indexes = dataset[dataset['Book_Title'] == ele]['Book_Author'].index[0]
        book_name.append(ele)
        isbn.append(dataset[dataset['Book_Title'] == ele]['ISBN'][indexes])
        imgurl.append(dataset[dataset['Book_Title'] == ele]['Image_URL_L'][indexes])
        author.append(dataset[dataset['Book_Title'] == ele]['Book_Author'][indexes])
        price.append(dataset[dataset['Book_Title'] == ele]['Price'][indexes])
        rating.append(dataset[dataset['Book_Title'] == ele]['Avg_rating'][indexes])
        total_votes.append(dataset[dataset['Book_Title'] == ele]['Total_Votes'][indexes])

    return book_name,isbn,imgurl,author,price,rating
    
@app.post("/Manipulate/")
def book_details(book):
    list_1 = details(book)
    list_b = []
    for j in range(5):
        list_a = []
        for i in range(6):
            list_a.append(list_1[i][j])
        list_b.append(list_a)    
    return list_b        

@app.post("/Finally don't mess up this time ,Inderrrrr")
def book_obj(book):
    list_nu = book_details(book)
    list_nn =['name','isbn','imgurl','author','price','rating']
    list_mo = []
    for ele in list_nu:
        dd = dict(zip(list_nn,ele))
        list_mo.append(dd)
    return list_mo    


        


    
    


