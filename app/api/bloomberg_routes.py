"""Bloomberg API routes for market data access."""
from flask import Blueprint, jsonify, request, current_app
from app.services.bloomberg_service import BloombergService

bloomberg_bp = Blueprint('bloomberg', __name__)

# Initialize Bloomberg service (singleton)
_bloomberg_service = None

def get_bloomberg_service():
    """Get or create Bloomberg service instance."""
    global _bloomberg_service
    if _bloomberg_service is None:
        host = current_app.config.get('BLOOMBERG_HOST', 'localhost')
        port = current_app.config.get('BLOOMBERG_PORT', 8194)
        _bloomberg_service = BloombergService(host=host, port=port)
    return _bloomberg_service


@bloomberg_bp.route('/connect', methods=['POST'])
def connect():
    """Connect to Bloomberg Terminal."""
    service = get_bloomberg_service()
    success = service.connect()
    return jsonify({
        "success": success,
        "message": "Connected to Bloomberg" if success else "Connection failed"
    })


@bloomberg_bp.route('/disconnect', methods=['POST'])
def disconnect():
    """Disconnect from Bloomberg Terminal."""
    service = get_bloomberg_service()
    service.disconnect()
    return jsonify({
        "success": True,
        "message": "Disconnected from Bloomberg"
    })


@bloomberg_bp.route('/status', methods=['GET'])
def status():
    """Get Bloomberg connection status."""
    service = get_bloomberg_service()
    return jsonify({
        "connected": service.is_connected(),
        "host": service.host,
        "port": service.port
    })


@bloomberg_bp.route('/reference-data', methods=['POST'])
def reference_data():
    """Get reference data for securities.

    Request body:
    {
        "securities": ["NVDA US Equity", "AMD US Equity"],
        "fields": ["PX_LAST", "NAME", "CUR_MKT_CAP"]
    }
    """
    service = get_bloomberg_service()

    if not service.is_connected():
        return jsonify({"error": "Not connected to Bloomberg"}), 400

    data = request.get_json()
    securities = data.get('securities', [])
    fields = data.get('fields', ['PX_LAST'])

    if not securities:
        return jsonify({"error": "No securities provided"}), 400

    try:
        result = service.get_reference_data(securities, fields)
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bloomberg_bp.route('/historical-data', methods=['POST'])
def historical_data():
    """Get historical data for a security.

    Request body:
    {
        "security": "NVDA US Equity",
        "fields": ["PX_LAST"],
        "start_date": "20240101",
        "end_date": "20240301"
    }
    """
    service = get_bloomberg_service()

    if not service.is_connected():
        return jsonify({"error": "Not connected to Bloomberg"}), 400

    data = request.get_json()
    security = data.get('security')
    fields = data.get('fields', ['PX_LAST'])
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not all([security, start_date, end_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        result = service.get_historical_data(security, fields, start_date, end_date)
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bloomberg_bp.route('/gpu-market', methods=['GET'])
def gpu_market():
    """Get GPU-related market data."""
    service = get_bloomberg_service()

    if not service.is_connected():
        # Auto-connect for convenience
        service.connect()

    try:
        result = service.get_gpu_market_data()
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bloomberg_bp.route('/datacenter-reits', methods=['GET'])
def datacenter_reits():
    """Get datacenter REIT data."""
    service = get_bloomberg_service()

    if not service.is_connected():
        service.connect()

    try:
        result = service.get_datacenter_reit_data()
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
