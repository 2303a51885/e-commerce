from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import uuid


app = Flask(__name__)
CORS(app)


# in-memory store for demo
PRODUCTS = {
1: {"id":1, "name":"Red T-Shirt", "price":19.99, "stock":10},
2: {"id":2, "name":"Blue Jeans", "price":49.99, "stock":5},
}
ORDERS = {}


@app.route('/products', methods=['GET'])
def list_products():
return jsonify(list(PRODUCTS.values()))


@app.route('/orders', methods=['POST'])
def place_order():
body = request.get_json()
if not body or 'items' not in body:
abort(400)
order_id = str(uuid.uuid4())
items = body['items']
total = 0.0
# simple inventory check
for it in items:
pid = int(it['productId'])
qty = int(it['quantity'])
if pid not in PRODUCTS or PRODUCTS[pid]['stock'] < qty:
return jsonify({'error':'product out of stock','productId':pid}), 400
total += PRODUCTS[pid]['price'] * qty
# deduct stock
for it in items:
PRODUCTS[int(it['productId'])]['stock'] -= int(it['quantity'])
ORDERS[order_id] = {'id': order_id, 'items': items, 'status':'processing', 'total': total}
# simulate payment + shipment creation (would call external APIs)
return jsonify(ORDERS[order_id]), 201


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
if order_id not in ORDERS:
abort(404)
return jsonify(ORDERS[order_id])


if __name__ == '__main__':
app.run(debug=True, port=5000)
