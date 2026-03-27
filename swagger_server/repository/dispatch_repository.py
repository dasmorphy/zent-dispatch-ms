from loguru import logger

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.models.db.dispatch_images import DispatchImages
from swagger_server.models.db.dispatch_skus import DispatchSkus
from swagger_server.models.db.products_sku import ProductsSku
from swagger_server.resources.databases.postgresql import PostgreSQLClient


class DispatchRepository:
    
    def __init__(self):
        self.db = PostgreSQLClient("POSTGRESQL")
        # self.redis_client = RedisClient()

    
    def post_dispatch(self, body, images, internal, external):
        saved_files = []

        with self.db.session_factory() as session:
            try:
                
                sku_saved = self.saveSku(session, body, internal, external)
                products = body.get("products_sku")
                self.saveDispatch(session, body, internal, external)

                for product in products:
                    self.saveProductSku(
                        session,
                        sku_saved['id_sku'],
                        product,
                        internal,
                        external
                    )

                # self.saveImages(session, images, internal, external)
                session.commit()

            except Exception as exception:
                session.rollback()
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al insertar en la base de datos", 500)

            finally:
                session.close()


    def saveDispatch(self, session, data, internal, external):
        try:
            
            dispatch = Dispatch(
                vehicle_type_id=data.get('vehicle_type'),
                destiny_id=data.get('destiny'),
                driver=data.get('driver'),
                observations=data.get('observations'),
                quantity=data.get('quantity'),
                weight=data.get('weight'),
                provider=data.get('provider'),
                truck_license=data.get('truck_license'),
                created_by=data.get('user'),
                updated_by=data.get('user'),
                # sku=
            )
            
            session.add(dispatch)

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)
        

    def saveSku(self, session, data, internal, external):
        try:
            dispatch_skus = DispatchSkus(
                created_by=data.get('user'),
                updated_by=data.get('user'),
                type_sku=data.get('type_sku'),
                code_sku=data.get('code_sku')
            )
            
            session.add(dispatch_skus)
            session.flush()

            return dispatch_skus
            
        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)
        

    def saveProductSku(self, session, sku_id, data, internal, external):
        try:
            
            product_sku = ProductsSku(
                product_id=data.get('id_product'),
                quantiy=data.get('quantiy'),
                sku_id=sku_id
            )
            
            session.add(product_sku)

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)


    def saveImages(self, session, data, internal, external):
        try:
            
            images = DispatchImages(

            )
            
            session.add(images)

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)