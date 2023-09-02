document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const addBookForm = document.getElementById('addBookForm');
    const bookList = document.getElementById('bookList');

    // Function to fetch and display books
    function displayBooks() {
        fetch('/books')
            .then((response) => response.json())
            .then((data) => {
                bookList.innerHTML = '';
                data.forEach((book) => {
                    const li = document.createElement('li');
                    li.innerHTML = `<strong>${book.title}</strong> by ${book.author}`;
                    bookList.appendChild(li);
                });
            });
    }

    // Event listener for adding a new book
    addBookForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const author = document.getElementById('author').value;

        fetch('/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, author }),
        })
            .then((response) => response.json())
            .then(() => {
                document.getElementById('title').value = '';
                document.getElementById('author').value = '';
                displayBooks();
            });
    });

    // Initial display of books
    displayBooks();
});
