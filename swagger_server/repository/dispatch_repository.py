from loguru import logger
from sqlalchemy import and_, exists, func, select

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db import Base
from swagger_server.models.db.destiny_intern import DestinyIntern
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.models.db.dispatch_images import DispatchImages
from swagger_server.models.db.dispatch_products import DispatchProducts
from swagger_server.models.db.dispatch_reception import DispatchReception
from swagger_server.models.db.dispatch_reception_detail import DispatchReceptionDetail
from swagger_server.models.db.dispatch_skus import DispatchSkus
from swagger_server.models.db.products_sku import ProductsSku
from swagger_server.models.db.vehicle_type import VehicleType
from swagger_server.models.db.dispatch_status import DispatchStatus
from swagger_server.models.reception_data import Receptiondata
from swagger_server.models.request_dispatch_dispatch_data import RequestDispatchDispatchData
from swagger_server.models.request_reception import RequestReception
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


    def update_dispatch(self, data: RequestDispatchDispatchData, id_disp: int, internal, external):
        with self.db.session_factory() as session:
            try:
                
                dispatch_exist = session.get(Dispatch, id_disp)

                if not dispatch_exist:
                    raise CustomAPIException("Despacho no encontrado", 404)
                
                update_fields = {
                    "vehicle_type_id": data.vehicle_type,
                    "destiny_id": data.destiny,
                    "driver": data.driver,
                    "observations": data.observations,
                    "weight": data.weight,
                    "truck_license": data.truck_license,
                    "status_id": data.status_id,
                }

                for field, value in update_fields.items():
                    if value is not None:
                        setattr(dispatch_exist, field, value)

                dispatch_exist.updated_by = data.user
                dispatch_exist.updated_at = func.now()
                
                session.add(dispatch_exist)
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

            vehicle_exists = session.execute(
                select(
                    exists().where(
                        VehicleType.id_vehicle_type == data.vehicle_type
                    )
                )
            ).scalar()

            if not vehicle_exists:
                raise CustomAPIException("El tipo de vehículo no existe", 404)
            
            destiny_exists = session.execute(
                select(
                    exists().where(
                        DestinyIntern.id_destiny == data.destiny
                    )
                )
            ).scalar()

            if not destiny_exists:
                raise CustomAPIException("El destino no existe", 404)
            
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
            
            raise CustomAPIException("Error al guardar el despacho en la base de datos", 500)
        

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
            
            raise CustomAPIException("Error al guardar el sku en la base de datos", 500)
        

    def saveProductSku(self, session, sku_id: int, data, internal, external):
        try:
            product_exists = session.execute(
                select(
                    exists().where(
                        DispatchProducts.id_product == data.id_product
                    )
                )
            ).scalar()

            if not product_exists:
                raise CustomAPIException("El producto no existe", 404)
            
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
            
            raise CustomAPIException("Error al guardar el producto sku en la base de datos", 500)


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
            
    def get_status_dispatch(self, internal, external):
        with self.db.session_factory() as session:
            try:
                result = session.execute(
                    select(DispatchStatus)
                )
                status = [
                    {
                        "id_status": c.id_status,
                        "name": c.name,
                        "created_at": c.created_at
                    }
                    for c in result.scalars().all()
                ]
                return status
            except Exception as exception:
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al obtener en la base de datos", 500)
            
    def get_all_dispatch(self, filtersBase, internal, external):
        with self.db.session_factory() as session:
            try:

                products_sku_subq = (
                    select(
                        ProductsSku.sku_id,
                        func.json_agg(
                            func.json_build_object(
                                "id_product", ProductsSku.product_id,
                                "name", DispatchProducts.name,
                                "quantity", ProductsSku.quantity
                            )
                        ).label("products_sku")
                    )
                    .join(
                        DispatchProducts,
                        DispatchProducts.id_product == ProductsSku.product_id
                    )
                    .group_by(ProductsSku.sku_id)
                    .subquery()
                )

                stmt = (
                    select(
                        Dispatch,
                        DispatchSkus,
                        DispatchStatus,
                        DestinyIntern.name.label("name_destiny"),
                        VehicleType.name.label("name_vehicle_type"),
                        func.coalesce(products_sku_subq.c.products_sku, '[]').label("products_sku")
                    )
                    .join(
                        DispatchSkus,
                        DispatchSkus.id_sku == Dispatch.sku_id
                    )
                    .join(
                        DestinyIntern,
                        DestinyIntern.id_destiny == Dispatch.destiny_id
                    )
                    .join(
                        DispatchStatus,
                        DispatchStatus.id_status == Dispatch.status_id
                    )
                    .join(
                        VehicleType,
                        VehicleType.id_vehicle_type == Dispatch.vehicle_type_id
                    )
                    .outerjoin(
                        products_sku_subq,
                        products_sku_subq.c.sku_id == DispatchSkus.id_sku
                    )
                )

                filters = []

                if filtersBase.get("user"):
                    filters.append(Dispatch.created_by == filtersBase.get("user"))

                if filtersBase.get("start_date"):
                    filters.append(Dispatch.created_at >= filtersBase.get("start_date"))

                if filtersBase.get("end_date"):
                    filters.append(Dispatch.created_at <= filtersBase.get("end_date"))

                if filters:
                    stmt = stmt.where(and_(*filters))

                result = session.execute(stmt).all()
                return result

            except Exception as exception:
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al obtener en la base de datos", 500)
            
    def post_reception(self, body: Receptiondata, internal, external) -> None:
        with self.db.session_factory() as session:
            try:
                dispatch_exists = session.execute(
                    select(
                        exists().where(
                            Dispatch.id_dispatch == body.dispatch_id
                        )
                    )
                ).scalar()

                if not dispatch_exists:
                    raise CustomAPIException("Despacho no encontrado", 404)
                
                reception_data = DispatchReception(
                    dispatch_id=body.dispatch_id,
                    is_correct=body.is_correct,
                    observations=body.observations,
                    created_by=body.user
                )

                session.add(reception_data)

                if (body.is_correct and body.reception_details):
                    for detail in body.reception_details:
                        product_exists = session.execute(
                            select(
                                exists().where(
                                    DispatchProducts.id_product == detail.product_id
                                )
                            )
                        ).scalar()

                        if not product_exists:
                            raise CustomAPIException("Un producto no existe", 404)
                        
                        reception_detail = DispatchReceptionDetail(
                            reception_id=reception_data.id_reception,
                            expected_quantity=detail.expected_quantity,
                            received_quantity=detail.received_quantity,
                            product_id=detail.product_id,
                            observations=detail.observations
                        )
                        session.add(reception_detail)

                elif body.is_correct and (body.reception_details is None or len(body.reception_details) == 0):
                    raise CustomAPIException("El detalle de recepción no puede ser vacío", 400)


                session.flush()
                session.commit()
            
            except Exception as exception:
                session.rollback()
                logger.error('Error: {}', str(exception), internal=internal, external=external)
                if isinstance(exception, CustomAPIException):
                    raise exception
                
                raise CustomAPIException("Error al obtener en la base de datos", 500)

