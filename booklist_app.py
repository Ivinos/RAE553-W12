from flask import Flask, request # Importing the relevant packages
from flask_restful import Resource, Api
import json

app = Flask(__name__) # Create our Application
api = Api(app)

# JSON with initial data
# In general is better to use a proper DBMS like MySQL or something like pandas
# But here we just want to try the HTTP methods with flask, so we will use simple data
Books =  '[{"Title":"Book 1", "Author":"someone", "City":"New York"}, {"Title":"Book 2", "Author":"someone else", "City":"Paris"}]'

# Parse JSON data into python data
Books = json.loads(Books)


class Book(Resource): # Class Book inherits from the clase "Resource"
    """
    Class Book is useful for all request where the user provides the title of a
    book. So we use this class for request on a single book (to view it, update
    it or delete it).
    """

    def get(self, title):
        """
        Return the selected book
        """

        for book in Books:
            if book['Title'] == title:

                return {'Book' : book}, 200 # 200 = http status code => "The request is OK."

        # If no book is find with the title provided, we inform the user
        return {'message' : 'There is no book with this title.'}, 200

    def delete(self, title):
        """
        Delete a selected book
        """

        for book in Books:
            if book['Title'] == title:
                Books.remove(book)

                return {'message' : 'Book deleted successfully.'}, 200

        # If no book is find with the title provided, we can't delet it and we need to inform the user
        return {'message' : 'There is no book with this title.'}, 200


    def put(self, title):
        """
        Edits a selected book
        """

        edit_book = request.get_json() # We take information sent by user

        for book in Books:
            if book['Title'] == title:
                book['Title'] = edit_book['Title']
                book['Author'] = edit_book['Author']
                book['City'] = edit_book['City']

                return {'message' : 'Book updated succesfully.'}

        # If no book is find with the title provided, we can't update it and we need to inform the user
        return {'message' : 'There is no book with this title.'}, 200

# We add our resource with a path
api.add_resource(Book, '/Books/<string:title>') # for example : http://127.0.0.1:5000/Books/Book 1



class Booklist(Resource): # Class Booklist inherits from the clase "Resource"
    """
    Class Booklist is useful when we want to interact with the all library. We
    can see all the books at the same time or add books on the booklist.
    """

    def get(self):
        """
        Return a list of books
        """

        return {"Books": Books}, 200

    def post(self):
        """
        Add a new book
        """

        new_book = request.get_json() # We take information sent by user

        if new_book:
            Books.append(new_book)
            return new_book, 201 # 201 = http status code => "The request is complete, and a new resource is created."
        else: # If we have nothing in the request
            new_book = {"response": "error"}
            return new_book, 404

# Again we add our resource to the API with a path
api.add_resource(Booklist, '/Books') # http://127.0.0.1:5000/Books

# Class below isn't finish and is only here to show what else we can do
# (ie add a graphical interface for the requests)
class Booklist_graphical(Resource): # Same feature as before but with an graphical interface
        """
        Class Booklist_graphical will do everything than both class Book and
        Booklist, but for the moment it can only add book. This class was to try
        the API with a graphical interface.
        """

        # Allow both GET and POST requests via http://127.0.0.1:5000/Books/add_book
        @app.route('/Books/add_book', methods=['GET', 'POST'])
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
                      </form>''', 201


app.run(port=5000) # we use the port 5000 for the connection (default)
