from services.models import Product
CART_ID_SESSION = 'cart'


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_ID_SESSION)
        if not cart:
            cart = self.session[CART_ID_SESSION] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            yield item

    def all_total_price(self):
        i = 0
        for item in self.cart.values():
            i += int(item['price'])
        return i

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price_whit_discount())}
        self.cart[product_id] = {'price': str(product.price_whit_discount())}
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        del self.cart[product_id]
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_ID_SESSION]
        self.save()

