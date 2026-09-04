from flask import Flask, request, jsonify

app = Flask(__name__)

_couriers = {
    1: {
        "id": 1,
        "first_name": "Иван",
        "last_name": "Петров",
        "phone": "+79991234567",
    },
    2: {
        "id": 2,
        "first_name": "Ольга",
        "last_name": "Смирнова",
        "phone": "+79997654321",
    },
}

_next_id = 3


def _check_auth():
    auth = request.headers.get("Authorization")
    if auth != "Bearer test_token_123":
        return jsonify({"error": "Unauthorized"}), 401
    return None


@app.route("/api/couriers/<int:courier_id>", methods=["GET"])
def get_courier(courier_id):
    auth_error = _check_auth()
    if auth_error:
        return auth_error

    courier = _couriers.get(courier_id)

    if courier is None:
        return jsonify({"error": "Courier not found"}), 404

    return jsonify(courier), 200


@app.route("/api/couriers", methods=["POST"])
def create_courier():
    auth_error = _check_auth()
    if auth_error:
        return auth_error

    global _next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "Bad request"}), 400

    if "first_name" not in data:
        return jsonify({"error": "Bad request: first_name is required"}), 400

    new_courier = {
        "id": _next_id,
        "first_name": data["first_name"],
        "last_name": data.get("last_name", ""),
        "phone": data.get("phone", ""),
    }

    _couriers[_next_id] = new_courier
    _next_id += 1

    return jsonify(new_courier), 201


@app.route("/api/couriers/<int:courier_id>", methods=["PATCH"])
def update_courier(courier_id):
    auth_error = _check_auth()
    if auth_error:
        return auth_error

    courier = _couriers.get(courier_id)

    if courier is None:
        return jsonify({"error": "Courier not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Bad request"}), 400

    courier.update(data)

    return jsonify(courier), 200


@app.route("/api/couriers/<int:courier_id>", methods=["DELETE"])
def delete_courier(courier_id):
    auth_error = _check_auth()
    if auth_error:
        return auth_error

    if courier_id not in _couriers:
        return jsonify({"error": "Courier not found"}), 404

    del _couriers[courier_id]

    return "", 204


if __name__ == "__main__":
    app.run(port=5001, debug=False)