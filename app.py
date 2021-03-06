from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mezadigi_dbtest:4nonimouS@mx46.hostgator.mx:3306/mezadigi_sportcenter'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cmeza:4nonimouS@192.168.64.3:3306/SportCenter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


app.secret_key = 'mysecretkey'
###Models####


class Article(db.Model):
    __tablename__ = "articles"
    sku = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(70))
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    def __init__(self, article, description, price, stock):
        self.article = article
        self.description = description
        self.price = price
        self.stock = stock


db.create_all()

# Schemas


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('sku', 'article', 'description', 'price', 'stock')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/articles', methods=['Post'])
def create_article():
    article = request.json['article']
    description = request.json['description']
    price = request.json['price']
    stock = request.json['stock']

    new_article = Article(article, description, price, stock)

    db.session.add(new_article)
    db.session.commit()

    return article_schema.jsonify(new_article)


@app.route('/articles', methods=['GET'])
def get_articles():
    all_articles = Article.query.all()
    artlists = articles_schema.dump(all_articles)
    print(artlists)
    return jsonify(artlists)


@app.route('/article/<sku>', methods=['GET'])
def get_article(sku):
    article = Article.query.get(sku)
    return article_schema.jsonify(article)


@app.route('/article/<sku>', methods=['PUT'])
def update_article(sku):
    updArticles = Article.query.get(sku)
    print(updArticles)
    article = request.json['article']
    description = request.json['description']
    price = request.json['price']
    stock = request.json['stock']

    updArticles.article = article
    updArticles.description = description
    updArticles.price = price
    updArticles.stock = stock

    db.session.commit()

    return article_schema.jsonify(updArticles)


@app.route('/article/<sku>', methods=['DELETE'])
def delete_article(sku):
    article = Article.query.get(sku)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Sport Center API... Wellcome'})


if __name__ == "__main__":
    app.run(port=6000, debug=False)
