



from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.models.request_dispatch import RequestDispatch
from swagger_server.repository.dispatch_repository import DispatchRepository


class DispatchUseCase:

    def __init__(self, dispatch_repository: DispatchRepository):
        self.dispatch_repository = dispatch_repository


    def post_dispatch(self, body: RequestDispatch, images, internal_process: tuple) -> None:

        if len(images) > 10:
            raise CustomAPIException("Máximo 10 imagenes", 500)
        
        internal, external = internal_process
        self.dispatch_repository.post_dispatch(body.dispatch_data, images, internal, external)

    def update_dispatch(self, body: RequestDispatch, id_disp: int, internal_process: tuple) -> None:
        internal, external = internal_process
        self.dispatch_repository.update_dispatch(body.dispatch_data, id_disp, internal, external)

    def get_all_dispatch_products(self, internal, external):
        return self.dispatch_repository.get_all_dispatch_products(internal, external)

    def get_vehicle_types(self, internal, external):
        return self.dispatch_repository.get_vehicle_types(internal, external)
    
    def get_status_dispatch(self, internal, external):
        return self.dispatch_repository.get_status_dispatch(internal, external)
    
    def get_all_dispatch(self, headers, params, internal, external):
        filters = {
            "user": headers.get("user"),
            "start_date": params.get("start_date"),
            "end_date": params.get("end_date"),
        }

        rows = self.dispatch_repository.get_all_dispatch(filters, internal, external)

        return [
            {
                "id_dispatch": dispatch.id_dispatch,
                "driver": dispatch.driver,
                "truck_license": dispatch.truck_license,
                "weight": dispatch.weight,
                "observations": dispatch.observations,
                "created_at": dispatch.created_at,
                "updated_at": dispatch.updated_at,
                "created_by": dispatch.created_by,
                "updated_by": dispatch.updated_by,
                "type_sku": dispatch_sku.type_sku,
                "code_sku": dispatch_sku.code_sku,
                "products_sku": products_sku,
                "name_vehicle_type": name_vehicle_type,
                "name_destiny": name_destiny,
                "sku_id": dispatch.sku_id,
                "status": dispatch_status.name,
            }
            for dispatch, dispatch_sku, dispatch_status, name_destiny, name_vehicle_type, products_sku in rows
        ]
    