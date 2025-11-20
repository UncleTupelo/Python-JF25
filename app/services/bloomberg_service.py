"""Bloomberg API integration service for Desktop API and Server API connections."""
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class BloombergService:
    """Service for Bloomberg Terminal API integration.

    Supports both Desktop API (DAPI) and Server API (SAPI/B-PIPE) connections.
    Requires valid Bloomberg Terminal subscription and active session.
    """

    def __init__(self, host: str = 'localhost', port: int = 8194):
        """Initialize Bloomberg service.

        Args:
            host: Bloomberg API host (localhost for Desktop API)
            port: Bloomberg API port (default 8194)
        """
        self.host = host
        self.port = port
        self.session = None
        self._connected = False
        self._blpapi_available = False

        # Try to import blpapi
        try:
            import blpapi
            self._blpapi = blpapi
            self._blpapi_available = True
        except ImportError:
            logger.warning("blpapi not installed. Bloomberg features will use mock data.")
            self._blpapi = None

    def connect(self) -> bool:
        """Establish connection to Bloomberg Terminal.

        Returns:
            True if connection successful, False otherwise
        """
        if not self._blpapi_available:
            logger.info("Using mock Bloomberg connection (blpapi not installed)")
            self._connected = True
            return True

        try:
            session_options = self._blpapi.SessionOptions()
            session_options.setServerHost(self.host)
            session_options.setServerPort(self.port)

            self.session = self._blpapi.Session(session_options)

            if not self.session.start():
                logger.error("Failed to start Bloomberg session")
                return False

            if not self.session.openService("//blp/refdata"):
                logger.error("Failed to open //blp/refdata service")
                return False

            self._connected = True
            logger.info(f"Connected to Bloomberg at {self.host}:{self.port}")
            return True

        except Exception as e:
            logger.error(f"Bloomberg connection error: {e}")
            return False

    def disconnect(self):
        """Close Bloomberg connection."""
        if self.session:
            self.session.stop()
        self._connected = False
        logger.info("Disconnected from Bloomberg")

    def is_connected(self) -> bool:
        """Check if connected to Bloomberg."""
        return self._connected

    def get_reference_data(self, securities: List[str], fields: List[str]) -> Dict[str, Any]:
        """Get reference data for securities.

        Args:
            securities: List of Bloomberg security identifiers (e.g., ['NVDA US Equity'])
            fields: List of Bloomberg fields (e.g., ['PX_LAST', 'NAME'])

        Returns:
            Dictionary with security data
        """
        if not self._connected:
            raise ConnectionError("Not connected to Bloomberg")

        if not self._blpapi_available:
            # Return mock data for development/testing
            return self._get_mock_reference_data(securities, fields)

        try:
            ref_data_service = self.session.getService("//blp/refdata")
            request = ref_data_service.createRequest("ReferenceDataRequest")

            for security in securities:
                request.append("securities", security)
            for field in fields:
                request.append("fields", field)

            self.session.sendRequest(request)

            results = {}
            while True:
                event = self.session.nextEvent(30000)
                for msg in event:
                    if msg.hasElement("securityData"):
                        security_data = msg.getElement("securityData")
                        for i in range(security_data.numValues()):
                            security = security_data.getValueAsElement(i)
                            sec_name = security.getElementAsString("security")
                            field_data = security.getElement("fieldData")

                            results[sec_name] = {}
                            for field in fields:
                                if field_data.hasElement(field):
                                    results[sec_name][field] = field_data.getElementAsString(field)

                if event.eventType() == self._blpapi.Event.RESPONSE:
                    break

            return results

        except Exception as e:
            logger.error(f"Error fetching reference data: {e}")
            raise

    def get_historical_data(self, security: str, fields: List[str],
                           start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get historical data for a security.

        Args:
            security: Bloomberg security identifier
            fields: List of Bloomberg fields
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            List of dictionaries with historical data
        """
        if not self._connected:
            raise ConnectionError("Not connected to Bloomberg")

        if not self._blpapi_available:
            return self._get_mock_historical_data(security, fields, start_date, end_date)

        try:
            ref_data_service = self.session.getService("//blp/refdata")
            request = ref_data_service.createRequest("HistoricalDataRequest")

            request.append("securities", security)
            for field in fields:
                request.append("fields", field)

            request.set("startDate", start_date)
            request.set("endDate", end_date)
            request.set("periodicitySelection", "DAILY")

            self.session.sendRequest(request)

            results = []
            while True:
                event = self.session.nextEvent(30000)
                for msg in event:
                    if msg.hasElement("securityData"):
                        security_data = msg.getElement("securityData")
                        field_data = security_data.getElement("fieldDataArray")

                        for i in range(field_data.numValues()):
                            data_point = field_data.getValueAsElement(i)
                            point = {"date": data_point.getElementAsString("date")}
                            for field in fields:
                                if data_point.hasElement(field):
                                    point[field] = data_point.getElementAsFloat(field)
                            results.append(point)

                if event.eventType() == self._blpapi.Event.RESPONSE:
                    break

            return results

        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            raise

    def get_gpu_market_data(self) -> Dict[str, Any]:
        """Get GPU-related market data for AI infrastructure analysis.

        Returns data for major GPU/AI chip companies and related metrics.
        """
        securities = [
            "NVDA US Equity",   # NVIDIA
            "AMD US Equity",    # AMD
            "INTC US Equity",   # Intel
            "TSM US Equity",    # TSMC
            "AVGO US Equity",   # Broadcom
        ]

        fields = [
            "PX_LAST",          # Last price
            "CHG_PCT_1D",       # 1-day change %
            "CUR_MKT_CAP",      # Market cap
            "PE_RATIO",         # P/E ratio
            "BEST_EPS_1YR",     # Forward EPS
        ]

        return self.get_reference_data(securities, fields)

    def get_datacenter_reit_data(self) -> Dict[str, Any]:
        """Get datacenter REIT data for TCO modeling.

        Returns data for major datacenter operators.
        """
        securities = [
            "EQIX US Equity",   # Equinix
            "DLR US Equity",    # Digital Realty
            "AMT US Equity",    # American Tower
            "CCI US Equity",    # Crown Castle
        ]

        fields = [
            "PX_LAST",
            "DVD_YLD",          # Dividend yield
            "FUNDS_FROM_OPS",   # FFO
            "CUR_MKT_CAP",
        ]

        return self.get_reference_data(securities, fields)

    def _get_mock_reference_data(self, securities: List[str], fields: List[str]) -> Dict[str, Any]:
        """Return mock data for development without Bloomberg Terminal."""
        mock_data = {
            "NVDA US Equity": {
                "PX_LAST": "875.28", "CHG_PCT_1D": "2.34",
                "CUR_MKT_CAP": "2150000000000", "PE_RATIO": "65.2", "BEST_EPS_1YR": "13.42",
                "NAME": "NVIDIA Corp"
            },
            "AMD US Equity": {
                "PX_LAST": "178.45", "CHG_PCT_1D": "1.82",
                "CUR_MKT_CAP": "288000000000", "PE_RATIO": "48.7", "BEST_EPS_1YR": "3.66",
                "NAME": "Advanced Micro Devices Inc"
            },
            "INTC US Equity": {
                "PX_LAST": "31.24", "CHG_PCT_1D": "-0.45",
                "CUR_MKT_CAP": "132000000000", "PE_RATIO": "32.1", "BEST_EPS_1YR": "0.97",
                "NAME": "Intel Corp"
            },
            "TSM US Equity": {
                "PX_LAST": "142.67", "CHG_PCT_1D": "1.12",
                "CUR_MKT_CAP": "740000000000", "PE_RATIO": "24.8", "BEST_EPS_1YR": "5.75",
                "NAME": "Taiwan Semiconductor Manufacturing Co Ltd"
            },
            "AVGO US Equity": {
                "PX_LAST": "1324.56", "CHG_PCT_1D": "0.89",
                "CUR_MKT_CAP": "615000000000", "PE_RATIO": "35.6", "BEST_EPS_1YR": "37.21",
                "NAME": "Broadcom Inc"
            },
            "EQIX US Equity": {
                "PX_LAST": "812.34", "DVD_YLD": "2.1",
                "FUNDS_FROM_OPS": "32.45", "CUR_MKT_CAP": "76000000000",
                "NAME": "Equinix Inc"
            },
            "DLR US Equity": {
                "PX_LAST": "142.89", "DVD_YLD": "3.4",
                "FUNDS_FROM_OPS": "6.78", "CUR_MKT_CAP": "44000000000",
                "NAME": "Digital Realty Trust Inc"
            },
        }

        results = {}
        for security in securities:
            if security in mock_data:
                results[security] = {
                    field: mock_data[security].get(field, "N/A")
                    for field in fields
                }

        return results

    def _get_mock_historical_data(self, security: str, fields: List[str],
                                  start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Return mock historical data for development."""
        import random
        from datetime import datetime, timedelta

        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")

        results = []
        current = start
        base_price = 100.0

        while current <= end:
            if current.weekday() < 5:  # Exclude weekends
                base_price *= (1 + random.uniform(-0.03, 0.035))
                point = {"date": current.strftime("%Y-%m-%d")}
                for field in fields:
                    if field == "PX_LAST":
                        point[field] = round(base_price, 2)
                    elif field == "PX_VOLUME":
                        point[field] = random.randint(1000000, 50000000)
                results.append(point)
            current += timedelta(days=1)

        return results
