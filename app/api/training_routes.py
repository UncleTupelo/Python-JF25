"""Training module API routes."""
from flask import Blueprint, jsonify, request
from app.services.training_service import TrainingService

training_bp = Blueprint('training', __name__)

# Initialize training service (singleton)
_training_service = None

def get_training_service():
    """Get or create training service instance."""
    global _training_service
    if _training_service is None:
        _training_service = TrainingService()
    return _training_service


@training_bp.route('/modules', methods=['GET'])
def list_modules():
    """Get list of available training modules."""
    service = get_training_service()
    modules = service.get_modules()
    return jsonify({
        "success": True,
        "modules": modules
    })


@training_bp.route('/modules/<module_id>', methods=['GET'])
def get_module(module_id):
    """Get a specific training module."""
    service = get_training_service()
    module = service.get_module(module_id)

    if not module:
        return jsonify({"error": "Module not found"}), 404

    return jsonify({
        "success": True,
        "module": module
    })


@training_bp.route('/modules/<module_id>/lessons/<lesson_id>', methods=['GET'])
def get_lesson(module_id, lesson_id):
    """Get a specific lesson from a module."""
    service = get_training_service()
    lesson = service.get_lesson(module_id, lesson_id)

    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404

    return jsonify({
        "success": True,
        "lesson": lesson
    })


@training_bp.route('/modules/<module_id>/lessons/<lesson_id>/quiz', methods=['POST'])
def submit_quiz(module_id, lesson_id):
    """Submit quiz answers for a lesson.

    Request body:
    {
        "answers": [1, 2, 0],  // Array of answer indices
        "user_id": "user123"   // Optional user ID
    }
    """
    data = request.get_json()
    answers = data.get('answers', [])
    user_id = data.get('user_id', 'default')

    service = get_training_service()
    result = service.submit_quiz(module_id, lesson_id, answers, user_id)

    if "error" in result:
        return jsonify(result), 400

    return jsonify({
        "success": True,
        "result": result
    })


@training_bp.route('/progress', methods=['GET'])
def get_progress():
    """Get user's learning progress."""
    user_id = request.args.get('user_id', 'default')

    service = get_training_service()
    progress = service.get_user_progress(user_id)

    return jsonify({
        "success": True,
        "progress": progress
    })
