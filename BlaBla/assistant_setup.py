from app.postgresqldb.tables import Assistant, AssistantConfig, Connection


class AssistantSetup:
    """
    This class encapsulates all of the necessary components to make a call to an assistant.
    """

    def __init__(self, connection: Connection, assistant: Assistant, assistant_config: AssistantConfig) -> None:
        self.connection = connection
        self.assistant = assistant
        self.assistant_config = assistant_config

    