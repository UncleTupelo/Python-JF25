"""Dashboard API routes for unified data access."""
from flask import Blueprint, jsonify
from app.services.bloomberg_service import BloombergService
from app.services.ai_service import AIAgentService
from app.services.training_service import TrainingService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/overview', methods=['GET'])
def overview():
    """Get dashboard overview data."""
    # Initialize services
    bloomberg = BloombergService()
    ai_service = AIAgentService()
    training = TrainingService()

    # Connect to Bloomberg (will use mock if unavailable)
    bloomberg.connect()

    # Get GPU market data
    gpu_data = bloomberg.get_gpu_market_data()

    # Get training progress
    progress = training.get_user_progress()

    # Get knowledge base summary
    knowledge = ai_service.knowledge_base

    return jsonify({
        "success": True,
        "data": {
            "market_data": gpu_data,
            "training_progress": progress,
            "gpu_architectures": list(knowledge["gpu_architectures"].keys()),
            "tco_factors": knowledge["tco_factors"]
        }
    })


@dashboard_bp.route('/tco-calculator', methods=['POST'])
def tco_calculator():
    """Calculate TCO based on parameters.

    Request body:
    {
        "gpu_type": "H100",
        "num_gpus": 8,
        "power_rate": 0.08,
        "pue": 1.3,
        "years": 3
    }
    """
    from flask import request
    data = request.get_json()

    ai_service = AIAgentService()
    result = ai_service.run_scenario("tco", data)

    return jsonify({
        "success": True,
        "result": result
    })


@dashboard_bp.route('/roi-calculator', methods=['POST'])
def roi_calculator():
    """Calculate ROI for GPU investment.

    Request body:
    {
        "investment": 240000,
        "hourly_rate": 3.5,
        "utilization": 0.85,
        "num_gpus": 8
    }
    """
    from flask import request
    data = request.get_json()

    ai_service = AIAgentService()
    result = ai_service.run_scenario("roi", data)

    return jsonify({
        "success": True,
        "result": result
    })
