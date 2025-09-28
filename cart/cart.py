from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    """
    Manages the shopping cart stored in the user's session.
    """
    def __init__(self, request):
        """
        Initializes the cart, getting it from the session or creating a new one.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session if one doesn't exist
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Adds a product to the cart or updates its quantity.
        The price is stored as a string to ensure it is JSON serializable.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # THE FIX (Part 1): Convert the Decimal to a string before saving to session.
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Marks the session as "modified" to ensure it gets saved on the next response.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Removes a product completely from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterates over the items in the cart, yielding a new dictionary
        for each item with the product object and calculated totals.
        This method is now SAFE and has NO SIDE EFFECTS on the session.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        # Create a mapping of product_id -> product_object for efficient lookup
        product_map = {str(p.id): p for p in products}

        # Iterate over a copy of the original session data to prevent modification
        for product_id, item_data in self.cart.items():
            product = product_map.get(product_id)

            # Ensure the product still exists in the database
            if product:
                # THE FIX (Part 2): Create a new, temporary dictionary to yield.
                # This prevents any changes to the original self.cart dictionary.
                # The 'price' is converted back to a Decimal for calculations here.
                yield {
                    'quantity': item_data['quantity'],
                    'price': Decimal(item_data['price']),
                    'product': product,
                    'total_price': Decimal(item_data['price']) * item_data['quantity']
                }

    def __len__(self):
        """
        Counts the total number of items in the cart (sum of all quantities).
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculates the total cost of all items in the cart.
        This method is safe as it reads string prices and converts them
        to Decimals for calculation without modifying the session.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_item_quantity(self, product_id):
        """
        Returns the current quantity of a specific product in the cart.
        """
        product_id = str(product_id)
        return self.cart.get(product_id, {}).get('quantity', 0)

    def clear(self):
        """
        Removes the cart completely from the session.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()