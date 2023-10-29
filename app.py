from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libary.db'
db = SQLAlchemy()
CORS(app)  
migrate = Migrate(app, db)


# Define the book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    is_loaned = db.Column(db.Boolean, default=False)  
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, name, author, year_published,type, is_loaned=False):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = type
        self.is_loaned = is_loaned  
        



# Define the customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)  
    age = db.Column(db.Integer, nullable=False)        

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age



# Define the loans Model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)

    def __init__(self, customer_id, book_id, loan_date, return_date=None):
        self.customer_id = customer_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date



# Initialize the database with the app
db.init_app(app)





# ************************** CRUD for books ************************************





# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    name = data.get('name')
    author = data.get('author')
    year_published = data.get('year_published')
    book_type = data.get('type')  # Get the "type" field from the request

    if name and author and year_published:
        book = Book(name=name, author=author, year_published=year_published, type=book_type, is_loaned=False)
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': 'Book created successfully'}), 201
    else:
        return jsonify({'message': 'Invalid data'}), 400


# Retrieve a list of all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'type': book.type,  # Include the "type" field in the response
            'is_loaned': book.is_loaned
        })
    return jsonify(book_list)


# Retrieve a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'type': book.type  # Include the "type" field in the response
        })
    else:
        return jsonify({'message': 'Book not found'}), 404
    

#  Retrieve the availible books
@app.route('/books/available', methods=['GET'])
def get_available_books():
    available_books = []
    # Retrieve all books
    all_books = Book.query.all()
    # Filter out books that are not currently loaned
    for book in all_books:
        if not book.is_loaned:
            available_books.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published
            })

    return jsonify(available_books)



# Retrieve the loaned books
@app.route('/books/loaned', methods=['GET'])
def get_loaned_books():
    loaned_books = []
    # Retrieve all books
    all_books = Book.query.all()
    # Filter out books that are currently loaned
    for book in all_books:
        if book.is_loaned:
            # Include the 'is_loaned' property in the response
            loaned_books.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published,
                'is_loaned': book.is_loaned  # Include the is_loaned property
            })

    return jsonify(loaned_books)



# Retrieve if a specific book is loaned by ID
@app.route('/books/<int:book_id>/is-loaned', methods=['GET'])
def is_book_loaned(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'is_loaned': book.is_loaned})
    else:
        return jsonify({'message': 'Book not found'}), 404





@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    data = request.get_json()
    name = data.get('name')
    author = data.get('author')
    year_published = data.get('year_published')
    book_type = data.get('type')  # Get the "type" field from the request

    if name and author and year_published:
        book.name = name
        book.author = author
        book.year_published = year_published
        book.type = book_type  # Update the "type" field
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400



# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200









# ************************** CRUD for customers ************************************







# Create a new customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')  
    age = data.get('age')    

    if name and city and age:
        customer = Customer(name=name, city=city, age=age)
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully'}), 201
    else:
        return jsonify({'message': 'Invalid data'}), 400


# Retrieve a list of all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append({
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,  
            'age': customer.age     
        })
    return jsonify(customer_list)


# Retrieve a specific customer by ID
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,  
            'age': customer.age     
        })
    else:
        return jsonify({'message': 'Customer not found'}), 404
    


# Retrieve customers with active loans
@app.route('/customers/active-loans', methods=['GET'])
def get_customers_with_active_loans():
    active_customers = []
    # Retrieve all loans with non-null return dates
    active_loans = Loan.query.filter(Loan.return_date.isnot(None)).all()
    # Extract unique customer IDs from active loans
    customer_ids = set(loan.customer_id for loan in active_loans)
    # Retrieve customer information for each unique customer ID
    for customer_id in customer_ids:
        customer = Customer.query.get(customer_id)
        if customer:
            active_customers.append({
                'id': customer.id,
                'name': customer.name,
                'city': customer.city,
                'age': customer.age
            })

    return jsonify(active_customers)



# Check if a specific customer has active loans by ID
@app.route('/customers/<int:customer_id>/has-active-loans', methods=['GET'])
def has_active_loans(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        active_loans = Loan.query.filter(Loan.customer_id == customer_id, Loan.return_date != None).count()
        return jsonify({'has_active_loans': active_loans > 0})
    else:
        return jsonify({'message': 'Customer not found'}), 404



# Update an existing customer by ID
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    data = request.get_json()
    name = data.get('name')
    city = data.get('city')  
    age = data.get('age')    

    if name and city and age:
        customer.name = name
        customer.city = city    
        customer.age = age      
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'}), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400


# Delete a customer by ID
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200



@app.route('/customers/search', methods=['GET'])
def search_customers_by_name():
    customer_name = request.args.get('name')
    if customer_name:
        # Search for customers by name
        customers = Customer.query.filter(Customer.name.ilike(f"%{customer_name}%")).all()
        customer_list = []
        for customer in customers:
            customer_list.append({
                'id': customer.id,
                'name': customer.name,
                'city': customer.city,
                'age': customer.age
            })
        return jsonify(customer_list)
    else:
        return jsonify({'message': 'Invalid data'}), 400








# ************************** CRUD for loans ************************************






@app.route('/loans', methods=['POST'])
def create_loan():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        book_id = data.get('book_id')
        loan_date_str = data.get('loan_date')
        return_date_str = data.get('return_date')

        if customer_id and book_id and loan_date_str:
            # Parse loan_date and return_date strings into Python date objects
            loan_date = datetime.strptime(loan_date_str, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date() if return_date_str else None

            # Update is_loaned to True when adding the book to loans
            book = Book.query.get(book_id)
            if book:
                book.is_loaned = True
                loan = Loan(customer_id=customer_id, book_id=book_id, loan_date=loan_date, return_date=return_date)
                db.session.add(loan)
                db.session.commit()
                return jsonify({'message': 'Loan created successfully'}), 201
            else:
                return jsonify({'message': 'Book not found'}), 404
        else:
            return jsonify({'message': 'Invalid data'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400


# Retrieve a list of all loans
@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        loan_list.append({
            'id': loan.id,
            'customer_id': loan.customer_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d') if loan.return_date else None
        })
    return jsonify(loan_list)

# Retrieve a specific loan by ID
@app.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        return jsonify({
            'id': loan.id,
            'customer_id': loan.customer_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d') if loan.return_date else None
        })
    else:
        return jsonify({'message': 'Loan not found'}), 404



# Retrieve a specific loan by bookID
@app.route('/loans/book/<int:book_id>', methods=['GET'])
def get_loan_by_book_id(book_id):
    loans = Loan.query.filter_by(book_id=book_id).all()
    loan_list = []

    for loan in loans:
        loan_list.append({
            'id': loan.id,
            'customer_id': loan.customer_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d') if loan.return_date else None
        })

    return jsonify(loan_list)


# Retrieve a specific loan by customerID
@app.route('/loans/customer/<int:customer_id>', methods=['GET'])
def get_loan_by_customer_id(customer_id):
    loans = Loan.query.filter_by(customer_id=customer_id).all()
    loan_list = []

    for loan in loans:
        loan_list.append({
            'id': loan.id,
            'customer_id': loan.customer_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d') if loan.return_date else None
        })

    return jsonify(loan_list)



# Update an existing loan by ID
@app.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'message': 'Loan not found'}), 404

    data = request.get_json()
    customer_id = data.get('customer_id')
    book_id = data.get('book_id')
    loan_date = data.get('loan_date')
    return_date = data.get('return_date')

    if customer_id and book_id and loan_date:
        loan.customer_id = customer_id
        loan.book_id = book_id
        loan.loan_date = loan_date
        loan.return_date = return_date
        db.session.commit()
        return jsonify({'message': 'Loan updated successfully'}), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400



# Delete a loan by ID and update the book's is_loaned status
@app.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'message': 'Loan not found'}), 404

    # Retrieve the book associated with the loan
    book = Book.query.get(loan.book_id)

    if book:
        # Set is_loaned to False when a book is returned
        book.is_loaned = False

        db.session.delete(loan)
        db.session.commit()

        return jsonify({'message': 'Loan deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found for the loan'}), 404










if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)