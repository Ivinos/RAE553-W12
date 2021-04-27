from flask import Flask, request # importing the relevant packages
from flask_restful import Resource, Api
import json

app = Flask(__name__) # Create our Application
api = Api(app)

# JSON with initial data
Books =  '[{"Title":"Book 1", "Author":"someone", "City":"New York"}, {"Title":"Book 2", "Author":"someone else", "City":"Paris"}]'

# Parse JSON data into python data
Books = json.loads(Books)


class Booklist(Resource): # Class Booklist inherits from the clase "Resource"
    def get(self):
        """
        return a list of books
        """

        return {"response": Books}

    def post(self):
        """
        Add a new book
        """

        new_book = request.get_json()
        if new_book:
            Books.append(new_book)
            return new_book, 200
        else: # If we have nothing in the request
            new_book = {"response": "error"}
            return new_book, 404

    # Allow both GET and POST requests via http://127.0.0.1:5000/add-book
    @app.route('/add-book', methods=['GET', 'POST'])
    def add_book():
        """
        Add a new book with a form
        """

        # Handle the POST request
        if request.method == 'POST':
            title = request.form.get('title')
            author = request.form.get('author')
            city = request.form.get('city')

            # Add the new book in the data
            new_book = {"Title":title, "Author":author, "City":city}
            Books.append(new_book)

            return '''
                      <h1>The title value is: {}</h1>
                      <h1>The author value is: {}</h1>
                      <h1>The city value is: {}</h1>'''.format(title, author, city)

        # Simple form for the post request
        return '''
                  <form method="POST">
                      <div><label>Title: <input type="text" name="title"></label></div>
                      <div><label>Author: <input type="text" name="author"></label></div>
                      <div><label>City: <input type="text" name="city"></label></div>
                      <input type="submit" value="Submit">
                  </form>'''

    def put(self): # We need to have put(self, title), then we can change the title of a book
        """
        Edits a selected book
        """

        # Here we have a problem !! We can't modify the name of a book...

        edit_book = request.get_json()

        for book in Books:
            if book['Title'] == edit_book['Title']:
                print(edit_book['City'])
                book['Title'] = edit_book['Title']
                book['Author'] = edit_book['Author']
                book['City'] = edit_book['City']

    def delete(self, title):
        """
        Delete a selected book
        """

        for book in Books:
            if book['Title'] == title:
                Books.remove(book)



api.add_resource(Booklist, '/Books') # http://127.0.0.1:5000/Books
# api.add_resource(Booklist, '/Books/<string:name>') # http://127.0.0.1:5000/Books/Book 1

app.run(port=5000)
