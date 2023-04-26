from .models import Order, Product


class CartForAuthenticatedUser:
    def __init__(self, request, product_slug=None, product_color=None, action=None):
        self.user = request.user

        if product_slug and product_color and action:
            self.add_or_delete(product_slug=product_slug, product_color=product_color, action=action)
        elif product_slug and product_color:
            self.delete_product(product_slug=product_slug, product_color=product_color)

    def get_cart_info(self):
        order = Order.objects.get(user=self.user, is_completed=False)
        products = order.orderproduct_set.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order_products': products,
            'order': order
        }

    def add_or_delete(self, product_slug, product_color, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(slug=product_slug)
        order_product, created = order.orderproduct_set.get_or_create(product=product, color_title=product_color)

        if action == 'add' and product.quantity_in_storage > 0:
            product.quantity_in_storage -= 1
            order_product.quantity += 1
        else:
            product.quantity_in_storage += 1
            order_product.quantity -= 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.save()

    def delete_product(self, product_slug, product_color):
        order = self.get_cart_info()['order']
        order_product = order.orderproduct_set.get(product__slug=product_slug, color_title=product_color)
        order_product.delete()
        order.save()
