from flask import Flask, render_template, redirect, request, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

#__name__ is the name of the application's module/package
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:oluwatobi@localhost/quotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FavQuotes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(50))
    quote = db.Column(db.String(2500))

#you use the route decorator to make a route. The function being decorated is triggered when someone visits that particular route in the args of the decorator
# you use a method called render_template() to render any template (html file) you have 
#to pass variables to your html, you pass the variable after the template name and use jinja to inject it into your html. This is done by interpolating the variable name in your html using {{}} 
@app.route('/')
def index() -> str:
    # fruits = ["apples", "oranges", "mangoes", "bananas", "kiwi", "pear"]
    # return render_template('index.html', quote = "Test ram", fruits = fruits)
    result: FavQuotes = FavQuotes.query.order_by(FavQuotes.id).all()# fetches everything in the table
    return render_template('index.html', result = result)
    

@app.route('/quotes')
def quotes() -> str:
    return render_template("quotes.html")

@app.route('/edit/<int:id>', methods = ['GET'])
def edit(id) -> str:
    try:
        quote: FavQuotes = FavQuotes.query.filter_by(id=id).first()
        if quote:
            return render_template('edit.html', fetchedQuote=quote)
        else:
            return 'Quote not found'

    except Exception as error:
        return f"An error occurred:{error}"    

@app.route('/process', methods = ['POST'])
def process() -> str:
    author: str = request.form['author']
    quote: str = request.form['quote']
    quoteData: FavQuotes = FavQuotes(author = author, quote = quote) # assign each inputs from users to variables named after the columns in the table. Next 2 lines is used to add the user inputs to database
    db.session.add(quoteData) 
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods = ['POST'])
def delete() -> str:
    id:int = request.form['id']
    quote: FavQuotes = FavQuotes.query.get_or_404(id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/makeedit/<int:id>', methods = ['POST'])
def makeedit(id) -> str:
    try:
        quote:FavQuotes = FavQuotes.query.filter_by(id=id).first()
        quote.author = request.form['author']
        quote.quote = request.form['quote']
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as error:
        return f'An error occured: {error}'



