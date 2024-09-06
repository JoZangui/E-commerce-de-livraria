""" Cart """
from books.models import Books
from users.models import Profile


class Cart():
    def __init__(self, request) -> None:
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no cart session! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def add(self, book, quantity):
        book_id = str(book)
        book_quantity = str(quantity)

        if book_id in self.cart:
            pass
        else:
            self.cart[book_id] = int(book_quantity)
        
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4} Dict to String
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(user_Cart=str(carty))

    def cart_total(self):
        # Get book IDS
        book_ids = self.cart.keys()
        # lookup those keys in our books database model
        books = Books.objects.filter(id__in=book_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key, value in quantities.items():
            # Convert key string into string so we can do match
            key = int(key)
            for book in books:
                if book.id == key:
                    if book.is_sale:
                        total = total + (book.sale_price * value)
                    else:
                        total = total + (book.price * value)
        return total
    
    def __len__(self):
        return len(self.cart)

    def get_books(self):
        # Get ids from cart
        book_ids = self.cart.keys()
        # Use ids to lookup books in database model
        books = Books.objects.filter(id__in=book_ids)

        # return those looked up books
        return books
    
    def get_quantities(self):
        quantities = self.cart

        return quantities
    
    def update(self, book, quantity):
        book_id = str(book)
        book_quantity = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dicitonary/cart
        ourcart[book_id] = book_quantity

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4} Dict to String
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(user_cart=str(carty))

        updated_cart = self.cart
        return updated_cart
    
    def delete(self, book):
        book_id = str(book)
        # Delete from dictionary/cart
        if book_id in self.cart:
            del self.cart[book_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4} Dict to String
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(user_cart=str(carty))
