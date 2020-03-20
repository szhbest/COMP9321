import requests


# type(book) = dict
def print_book(book):
    print("Book {")
    for key in book.keys():
        attr = str(key)
        val = str(book[key])
        print("\t" + attr + ":" + val)
    print("}")


def get_book(id):
    r = requests.get("http://127.0.0.1:5000/book/" + str(id))
    # get only one book, type(book) = dict
    book = r.json()
    print("Get status Code:" + str(r.status_code))
    if r.ok:
        print_book(book)
        return book
    else:
        print('Error: ' + book['message'])


def remove_book(id):
    r = requests.delete("http://127.0.0.1:5000/book/" + str(id))
    print("Delete status Code:" + str(r.status_code))
    print(r.json()['message'])


if __name__ == '__main__':

    '''
    GET: Programmatically get and print top-5 books ordered by 'Date_of_Publication' in an ascending order.
    '''
    r = requests.get("http://127.0.0.1:5000/books",
                     params={'order': 'Date_of_Publication', 'ascending': True})
    print("Status Code:" + str(r.status_code))
    # type(books) = list, type(books[i]) = dict
    books = r.json()
    for i in range(5):
        print_book(books[i])

    '''
    POST: Programmatically add a new book to the dataset
    '''
    new_book = {
        "Date_of_Publication": 2018,
        "Publisher": "UNSW",
        "Author": "Nobody",
        "Title": "Nothing",
        "Flickr_URL": "http://somewhere",
        "Identifier": 2,
        "Place_of_Publication": "Sydney"
    }

    r = requests.post("http://127.0.0.1:5000/books", json=new_book)

    print("Status Code:" + str(r.status_code))
    resp = r.json()
    print(resp['message'])

    '''
    PUT: Programmatically update the book which its ID is 206 by changing the author name to 'Nobody'
    '''
    print("***** Book information before update *****")
    book = get_book(206)

    # update the book information
    print("***** Updating Book Information *****")
    book['Author'] = 'Nobody'
    r = requests.put("http://127.0.0.1:5000/book/206", json=book)
    print("Put status Code:" + str(r.status_code))
    print(r.json()['message'])

    print("***** Book information after update *****")
    book = get_book(206)

    '''
    DELETE: Programmatically delete the book which its ID is 206
    '''
    print("***** Book information before update *****")
    get_book(206)

    # update the book information
    print("***** Deleting Book *****")
    remove_book(206)

    print("***** Book information after Delete *****")
    get_book(206)
