from .base_connector import BaseConnector


class HubSpotConnector(BaseConnector):
    """
    Placeholder implementation for a HubSpot connector.

    This class is intentionally left unimplemented. The application
    architecture allows any CRM connector that implements the
    BaseConnector interface and returns a pandas DataFrame.
    """

    def connect(self):
        raise NotImplementedError("HubSpot connector is not implemented.")

    def get_records(self):
        raise NotImplementedError("HubSpot connector is not implemented.")

    def disconnect(self):
        pass