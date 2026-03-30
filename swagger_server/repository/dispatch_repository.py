from loguru import logger
from sqlalchemy import select

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db import Base
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.models.db.dispatch_images import DispatchImages
from swagger_server.models.db.dispatch_products import DispatchProducts
from swagger_server.models.db.dispatch_skus import DispatchSkus
from swagger_server.models.db.products_sku import ProductsSku
from swagger_server.models.db.vehicle_type import VehicleType
from swagger_server.models.db.dispatch_status import DispatchStatus
from swagger_server.models.request_dispatch_dispatch_data import RequestDispatchDispatchData
from swagger_server.resources.databases.postgresql import PostgreSQLClient


class DispatchRepository:
    
    def __init__(self):
        self.db = PostgreSQLClient("POSTGRESQL")
        # self.redis_client = RedisClient()

    
    def post_dispatch(self, data: RequestDispatchDispatchData, images, internal, external):
        saved_files = []

        with self.db.session_factory() as session:
            try:
                
                sku_saved = self.saveSku(session, data, internal, external)
                products = data.products_sku
                self.saveDispatch(session, data, sku_saved.id_sku, internal, external)

                for product in products:
                    self.saveProductSku(
                        session,
                        sku_saved.id_sku,
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


    def saveDispatch(self, session, data: RequestDispatchDispatchData, sku_id: int, internal, external):
        try:
            
            dispatch = Dispatch(
                vehicle_type_id=data.vehicle_type,
                destiny_id=data.destiny,
                driver=data.driver,
                observations=data.observations,
                weight=data.weight,
                truck_license=data.truck_license,
                created_by=data.user,
                updated_by=data.user,
                sku_id=sku_id,
                status_id=1
            )
            
            session.add(dispatch)

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)
        

    def saveSku(self, session, data: RequestDispatchDispatchData, internal, external) -> DispatchSkus:
        try:
            dispatch_skus = DispatchSkus(
                created_by=data.user,
                updated_by=data.user,
                type_sku=data.sku_type,
                code_sku='test'
            )
            
            session.add(dispatch_skus)
            session.flush()

            return dispatch_skus
            
        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            if isinstance(exception, CustomAPIException):
                raise exception
            
            raise CustomAPIException("Error al buscar en la base de datos", 500)
        

    def saveProductSku(self, session, sku_id: int, data, internal, external):
        try:
            
            product_sku = ProductsSku(
                product_id=data.id_product,
                quantity=data.quantity,
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
        
    def get_all_dispatch_products(self, internal, external):
        with self.db.session_factory() as session:
            try:
                result = session.execute(
                    select(DispatchProducts)
                )
                products = [
                    {
                        "id_product": c.id_product,
                        "name": c.name,
                        "price": c.price,
                        "stock": c.stock,
                        "presentation_type": c.presentation_type,
                        "created_at": c.created_at,
                        "updated_at": c.updated_at,
                        "created_by": c.created_by,
                        "updated_by": c.updated_by,
                    }
                    for c in result.scalars().all()
                ]
                return products
            except Exception as exception:
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al obtener en la base de datos", 500)
            
    def get_vehicle_types(self, internal, external):
        with self.db.session_factory() as session:
            try:
                result = session.execute(
                    select(VehicleType)
                )
                vehicle_types = [
                    {
                        "id_vehicle_type": c.id_vehicle_type,
                        "name": c.name,
                        "created_at": c.created_at,
                        "updated_at": c.updated_at,
                        "created_by": c.created_by,
                        "updated_by": c.updated_by,
                    }
                    for c in result.scalars().all()
                ]
                return vehicle_types
            except Exception as exception:
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al obtener en la base de datos", 500)