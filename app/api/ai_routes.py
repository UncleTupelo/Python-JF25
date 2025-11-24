"""AI Agent API routes."""
from flask import Blueprint, jsonify, request, current_app
from app.services.ai_service import AIAgentService

ai_bp = Blueprint('ai', __name__)

# Initialize AI service (singleton)
_ai_service = None

def get_ai_service():
    """Get or create AI service instance."""
    global _ai_service
    if _ai_service is None:
        api_key = current_app.config.get('OPENAI_API_KEY', '')
        model = current_app.config.get('AI_MODEL', 'gpt-4')
        _ai_service = AIAgentService(api_key=api_key, model=model)
    return _ai_service


@ai_bp.route('/chat', methods=['POST'])
def chat():
    """Send a message to the AI agent.

    Request body:
    {
        "message": "What's the TCO for an 8-GPU cluster?",
        "context": []  // Optional conversation history
    }
    """
    data = request.get_json()
    message = data.get('message', '')
    context = data.get('context', [])

    if not message:
        return jsonify({"error": "No message provided"}), 400

    service = get_ai_service()
    response = service.chat(message, context)

    return jsonify({
        "success": True,
        "response": response
    })


@ai_bp.route('/scenario', methods=['POST'])
def run_scenario():
    """Run an analysis scenario.

    Request body:
    {
        "type": "tco",
        "parameters": {
            "gpu_type": "H100",
            "num_gpus": 8,
            "power_rate": 0.08,
            "years": 3
        }
    }
    """
    data = request.get_json()
    scenario_type = data.get('type')
    parameters = data.get('parameters', {})

    if not scenario_type:
        return jsonify({"error": "No scenario type provided"}), 400

    service = get_ai_service()
    result = service.run_scenario(scenario_type, parameters)

    return jsonify({
        "success": True,
        "result": result
    })


@ai_bp.route('/knowledge', methods=['GET'])
def get_knowledge():
    """Get the AI agent's knowledge base."""
    service = get_ai_service()
    return jsonify({
        "success": True,
        "knowledge": service.knowledge_base
    })


@ai_bp.route('/gpu-comparison', methods=['GET'])
def gpu_comparison():
    """Get GPU comparison data."""
    service = get_ai_service()
    response = service._handle_gpu_comparison("")
    return jsonify({
        "success": True,
        "data": response["data"],
        "formatted": response["response"]
    })
