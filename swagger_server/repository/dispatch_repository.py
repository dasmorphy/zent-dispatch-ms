from loguru import logger

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.resources.databases.postgresql import PostgreSQLClient


class DispatchRepository:
    
    def __init__(self):
        self.db = PostgreSQLClient("POSTGRESQL")
        # self.redis_client = RedisClient()

    
    def post_dispatch(self, body, images, internal, external):
        saved_files = []

        with self.db.session_factory() as session:
            try:
                dispatch = Dispatch(
                    vehicle_type_id=body.get('vehicle_type'),
                    destiny_id=body.get('destiny'),
                    driver=body.get('driver'),
                    observations=body.get('observations'),
                    truck_license=body.get('truck_license'),
                    quantity=body.get('quantity'),
                    weight=body.get('weight'),
                    provider=body.get('provider'),
                    truck_license=body.get('truck_license'),
                    weight=body.get('name_driver'),
                    created_by=body.get('user'),
                    updated_by=body.get('user'),
                )

                self.saveImages(session)
                session.commit()

            except Exception as exception:
                session.rollback()
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al insertar en la base de datos", 500)

            finally:
                session.close()


    def saveImages(self, session, data: RequestIdempotency, internal, external):
        try:
            
            uuid_request_exist = session.execute(
                select(
                    exists().where(
                        RequestIdempotency.uuid == data.uuid
                    )
                )
            ).scalar()

            if uuid_request_exist:
                raise CustomAPIException(
                    message="Duplicación de registro, el external transaction ya existe",
                    status_code=409
                )

            session.add(data)
            # session.commit()

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)