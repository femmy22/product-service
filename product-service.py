from flask import Flask, jsonify, request

app = Flask("Product Service")

# In-memory storage for products (for simplicity, using a dict to store products)
products = {
    1: {'name': 'broccoli', 'price': 1.0, 'quantity': 50},
    2: {'name': 'salmon', 'price': 0.5, 'quantity': 100},
    3: {'name': 'avocados', 'price': 3.0, 'quantity': 10}
}

# Endpoint to retrieve the list of all products
@app.route('/products', methods=['GET'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def get_products():
    return jsonify(products)

# Endpoint to get details of a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# Endpoint to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.json
    product_id = len(products) + 1
    products[product_id] = {
        'name': new_product['name'],
        'price': new_product['price'],
        'quantity': new_product['quantity']
    }
    return jsonify({"message": "Product added", "product": products[product_id]}), 201

if __name__ == '__main__':
    app.run(port=5001)
