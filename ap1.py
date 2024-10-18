from flask import Flask,render_template,request
import pickle
import numpy as np
popular_df = pickle.load(open('popular2.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html",
                           book_name=  list(popular_df['title'].values),
                           author =  list(popular_df['author'].values),
                           image =  list(popular_df['Image-URL-M'].values),
                           votes =  list(popular_df['number_of_rating'].values),
                           avg =  list(popular_df['avg_of_rating'].values),
                           )
    
@app.route('/recommend')                    
def recommend_ui():
    return render_template("new1.html")
 
 
@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    book_id = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity[book_id])),reverse = True,key = lambda x:x[1])[1:6]
    
    data=[]
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)   
    return render_template("new1.html",data=data)
    
if __name__ == '__main__':
     app.run(debug=True)
    
    
    