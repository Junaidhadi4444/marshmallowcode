import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, ValidationError, fields, pre_load

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/quotes_db'
db = SQLAlchemy(app)

##### MODELS #####


class Author(db.Model):  # Represents an author
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80))
    last = db.Column(db.String(80))


class Quote(db.Model):  # Represents a quote
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)  # Added length for content
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref=db.backref("quotes", lazy="dynamic"))
    posted_at = db.Column(db.DateTime)


##### SCHEMAS #####


class AuthorSchema(Schema):  # Serializer for Author model
    id = fields.Int(dump_only=True)
    first = fields.Str()
    last = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, author):
        return f"{author.last}, {author.first}"


# Custom validator to ensure data is not blank
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


class QuoteSchema(Schema):  # Serializer for Quote model
    id = fields.Int(dump_only=True)
    author = fields.Nested(AuthorSchema, validate=must_not_be_blank)
    content = fields.Str(required=True, validate=must_not_be_blank)
    posted_at = fields.DateTime(dump_only=True)

    # Process input to extract author's full name
    @pre_load
    def process_author(self, data, **kwargs):
        author_name = data.get("author")
        if author_name:
            first, last = author_name.split(" ")
            author_dict = dict(first=first, last=last)
        else:
            author_dict = {}
        data["author"] = author_dict
        return data


# Initialize schemas
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True, only=("id", "content"))


##### API #####


@app.route("/authors", methods=["GET"])  # Get all authors
def get_authors():
    authors = Author.query.all()
    result = authors_schema.dump(authors)
    return {"authors": result}


@app.route("/authors/<int:pk>", methods=["GET"])  # Get author by ID
def get_author(pk):
    try:
        author = Author.query.filter(Author.id == pk).one()
    except NoResultFound:
        return {"message": "Author could not be found."}, 400
    author_result = author_schema.dump(author)
    quotes_result = quotes_schema.dump(author.quotes.all())
    return {"author": author_result, "quotes": quotes_result}


@app.route("/quotes/", methods=["GET"])  # Get all quotes
def get_quotes():
    quotes = Quote.query.all()
    result = quotes_schema.dump(quotes)
    return {"quotes": result}


@app.route("/quotes/<int:pk>", methods=["GET"])  # Get quote by ID
def get_quote(pk):
    try:
        quote = Quote.query.filter(Quote.id == pk).one()
    except NoResultFound:
        return {"message": "Quote could not be found."}, 400
    result = quote_schema.dump(quote)
    return {"quote": result}


@app.route("/quotes/", methods=["POST"])  # Create a new quote
def new_quote():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        data = quote_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    first, last = data["author"]["first"], data["author"]["last"]
    author = Author.query.filter_by(first=first, last=last).first()
    if author is None:
        # Create a new author if they don't exist
        author = Author(first=first, last=last)
        db.session.add(author)
    # Create a new quote
    quote = Quote(
        content=data["content"],
        author=author,
        posted_at=datetime.datetime.now(datetime.UTC),
    )
    db.session.add(quote)
    db.session.commit()
    result = quote_schema.dump(Quote.query.get(quote.id))
    return {"message": "Created new quote.", "quote": result}


if __name__ == "__main__":
    with app.app_context():  # Set up the application context
        db.create_all()  # Create the tables in the database
    app.run(debug=True)
