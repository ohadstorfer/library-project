# Library Management System
The Library Management System is a user-friendly application designed to efficiently manage books and customers in a library setting. This README provides an overview of its functions and how to use them.


## Getting Started
To get started with the Library Management System, make sure you have the necessary dependencies and the Flask API server running. You can find the installation and setup instructions in the [Installation](#installation) section.


## Features


### Searching for Books and Customers
- **Select What to Search For:** You can search for either books or customers by selecting the respective option.
- **Type Your Search:** Enter the book or customer name you're looking for.
- **Start Your Search:** Click the "Search" button to initiate the search.
- **View the Results:** You'll see a list of matching books or customers. If no matches are found, you'll be informed.
- **Check Details:** Click on a result to access more information about the book or customer.


### Printing Books
Our Library Management System provides several functions for printing book listings:

- **Print All Books:** Fetches and displays all books from a Flask API.
- **Print Available Books:** Fetches and displays available books.
- **Print Loaned Books:** Fetches and displays loaned books.
- **Print Late Loans:** Fetches and displays late loaned books.
- **Print Books(books):** Handles the display of books in a card-style format.
- **Fetch Loan Details(bookId):** Retrieves loan details for a specific book.
- **Fetch Customer Loans(customerId):** Gathers details about a customer's loaned books.
- **Getting Return Date(bookId):** Retrieves the return date of a loaned book.


### Adding a Book
The `AddBook()` function allows you to add new books to the system. It provides a form where you can input book details, and upon submission, the data is sent to the Flask API to add a new book. Success or error messages are displayed accordingly.


### Deleting a Book
The `deleteBookById(bookId)` function allows you to delete books. It checks if a book is loaned, and if not, prompts for confirmation before sending a DELETE request to remove the book by its ID. It updates the UI after a successful deletion or displays error messages when needed.


### Printing Customers
- **Print All Customers:** Fetches all customers from the Flask API and displays their data, including name, city, age, and the ability to delete the customer. It also fetches loan details for each customer and highlights overdue book returns.
- **Print Active Customers:** Fetches customers with active loans and displays them similarly to `Print All Customers`, specifically for customers with loans.



### Loan a Book
The `handleLoanAction(bookId)` function allows you to loan a book to a customer. It prompts for the customer's name, checks if the customer exists by searching customers by name, calculates the return date based on the book's type, creates a loan object with the customer's ID, book ID, loan date, and return date, and sends a POST request to create the loan. It provides feedback on the success or failure of the loan creation.


### Return a Book
The `handleReturnAction(bookId)` function handles the return of a book. It attempts to find the loan ID associated with the provided bookId and then sends a DELETE request to the Flask API to delete the loan record. It provides appropriate feedback for success or failure and handles errors accordingly.


### Delete a Customer
The `deleteCustomerById(customerId)` function handles the deletion of a customer. It first checks if the customer has any active loans. If not, it prompts for confirmation before sending a DELETE request to the Flask API to delete the customer. Success or error messages are displayed.


### Add a Customer
The `AddCustomer()` function creates an "Add Customer" form, allowing users to input customer details. Upon submission, it sends a POST request to the Flask API to add the new customer and displays success or error messages.





## Installation
1. Clone this repository to your local machine. Use the "git clone" command to clone the project.
2. Navigate to the project directory.
3. Create a virtual environment (recommended).
4. Install the required dependencies using `pip install -r requirements.txt`.
5. Run the Flask API server. You can typically do this with `python app.py`.
6. Access the web application through your browser.


## Usage
The Library Management System provides a user-friendly interface to manage books and customers in a library setting. You can easily search, add, delete, loan, and return books. It also offers customer management functionalities.


## Contributing
Contributions to this project are welcome. Feel free to open issues or pull requests to improve the system.


## License
This project is licensed under the [MIT License](LICENSE).
