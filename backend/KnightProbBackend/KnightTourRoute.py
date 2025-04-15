from flask import Blueprint, jsonify, request
import random
from .KnightTour import validate_player_path, solve_knights_tour

knight_blueprint = Blueprint('knight', __name__, url_prefix='/api')

@knight_blueprint.route('/start', methods=['GET'])
def start_game():
    start_x = random.randint(0, 7)
    start_y = random.randint(0, 7)
    return jsonify({"start": {"x": start_x, "y": start_y}})

@knight_blueprint.route('/validate', methods=['POST'])
def validate_path():
    data = request.get_json()
    path = data.get('path')

    if not path:
        return jsonify({"valid": False, "message": "Path not provided"}), 400

    try:
        path = [(int(p[0]), int(p[1])) for p in path]
        valid, message = validate_player_path(path)
        return jsonify({"valid": valid, "message": message})
    except Exception as e:
        return jsonify({"valid": False, "message": str(e)}), 500

@knight_blueprint.route('/solve', methods=['POST'])
def solve_from_start_position():
    data = request.get_json()
    path = data.get('path')

    # Validate input
    if not path or len(path) == 0 or not isinstance(path[0], list) or len(path[0]) != 2:
        return jsonify({"success": False, "message": "Invalid or missing start position"}), 400

    try:
        start_x, start_y = int(path[0][0]), int(path[0][1])
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Start position must contain integers"}), 400

    # Solve using backtracking
    solution = solve_knights_tour(start_x, start_y)

    if solution:
        return jsonify({"success": True, "path": solution})
    else:
        return jsonify({"success": False, "message": "No solution possible from this position"})
