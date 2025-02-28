from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data storage
data_store = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data_store)


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data_store if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request"}), 400
    new_item = {"id": len(data_store) + 1, "name": data["name"]}
    data_store.append(new_item)
    return jsonify(new_item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in data_store if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if "name" in data:
        item["name"] = data["name"]
    return jsonify(item)


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data_store
    data_store = [item for item in data_store if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
