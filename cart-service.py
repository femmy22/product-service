from flask import Flask, jsonify, request
import requests

app = Flask("Cart Service")

# In-memory storage for carts
user_carts = {}

# Helper function to get product details from Product Service
def get_product_from_product_service(product_id):
    product_service_url = f"http://127.0.0.1:5001/products"
    response = requests.get(product_service_url)
    if response.status_code == 200:
        return response.json()
    return None

# Endpoint to get the cart contents of a specific user
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = user_carts.get(user_id, {})
    
    if not cart:
        return jsonify({"message": "Cart is empty", "cart": [], "total_price": 0.0})

    cart_contents = []
    total_price = 0.0

    for product_id, item in cart.items():
        product_total_price = item['quantity'] * item['price']
        total_price += product_total_price
        cart_contents.append({
            'product_id': product_id,
            'product_name': item['name'],
            'quantity': item['quantity'],
            'unit_price': item['price'],
            'total_price': product_total_price
        })

    return jsonify({"cart": cart_contents, "total_price": total_price})

# Endpoint to add a product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    product = get_product_from_product_service(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    quantity = request.json.get('quantity', 1)
    
    if user_id not in user_carts:
        user_carts[user_id] = {}

    cart = user_carts[user_id]
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity
        }

    return jsonify({"message": "Product added to cart", "cart": cart})

# Endpoint to remove a product from a user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    if user_id not in user_carts or product_id not in user_carts[user_id]:
        return jsonify({"error": "Product not found in cart"}), 404

    quantity_to_remove = request.json.get('quantity', 1)
    cart = user_carts[user_id]
    
    cart[product_id]['quantity'] -= quantity_to_remove
    
    if cart[product_id]['quantity'] <= 0:
        del cart[product_id]
    
    return jsonify({"message": "Product removed from cart", "cart": cart})

if __name__ == '__main__':
    app.run(port=5002)
