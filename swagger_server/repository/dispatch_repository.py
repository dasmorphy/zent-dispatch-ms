from swagger_server.resources.databases.postgresql import PostgreSQLClient


class DispatchRepository:
    
    def __init__(self):
        self.db = PostgreSQLClient("POSTGRESQL")
        # self.redis_client = RedisClient()