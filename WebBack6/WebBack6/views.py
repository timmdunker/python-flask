"""
Routes and views for the flask application.

Timm Dunker AE8678

"""

from flask import render_template, request, jsonify
import json
from WebBack6 import app

@app.route('/')
def main():
    return render_template('index.html')

def createArticles(article):
    f = open("articles.json")
    data = json.load(f)
    data["articles"].append(article)
    f.close()

    file = open('articles.json', 'w')
    file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',',': ')))
    file.close()

@app.route('/done', methods=['POST'])
def submitArticles():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    data_dict = {
        "title":title,
        "author":author,
        "content":content
    }
    createArticles(data_dict)
    return render_template('done.html', title=title, author=author)

@app.route('/articles', methods=['GET'])
def getArticles():
  with open('articles.json', 'r') as f:
     return render_template('article_list.html', articles=json.loads(f.read())['articles'])

@app.route('/api/articles', methods=['GET'])
def getJSON():
  with open('articles.json', 'r') as f:
      articles = json.load(f)
      return jsonify(articles)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

@app.route('/api/articles/<title>', methods=['GET'])
def profile(title):
      with open('articles.json', 'r') as f:
        articles = json.load(f)
        for key, value in articles.items():
            for form in value:
                if(form['title']== title):
                    data_dict = {
                        "title":form['title'],
                        "author":form['author'],
                        "content":form['content'],
                        }
                    return jsonify(data_dict)

@app.route('/articles/<title>/', methods=['GET'])
def getSpecificArticle(title):
      with open('articles.json', 'r') as f:
        articles = json.load(f)
        for key, value in articles.items():
            for form in value:
                if(form['title']== title):
                    title = form['title']
                    author = form['author']
                    content = form['content']
                    return render_template('article_specific.html', title=title, author=author, content=content)

@app.route('/articles/<title>/edit', methods=['GET'])
def editSpecificArticle(title):
    with open('articles.json', 'r') as f:
        articles = json.load(f)
        for key, value in articles.items():
            for form in value:
                if(form['title']== title):
                    title = form['title']
                    author = form['author']
                    content = form['content']
                    data_dict = {
                        "title":title,
                        "author":author,
                        "content":content
                        }
                    return render_template('article_edit.html', title=title, author=author, content=content)

@app.route('/articles/<title>/edit/done', methods=['POST'])
def saveEditedArticle(title):
    with open('articles.json', 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            for form in value:
                if(form['title']== title):
                    data_dict = {
                    "title": request.form['title'],
                    "author": request.form['author'],
                    "content": request.form['content'],
                    }
                    data["articles"].append(data_dict)

                    for i in range(len(data["articles"])):
                        if data["articles"][i]["title"] == title:
                            data["articles"].pop(i)
                            break

    file = open('articles.json', 'w')
    file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    file.close()
    return render_template('article_update.html')