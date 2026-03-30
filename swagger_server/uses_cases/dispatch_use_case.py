



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

    def get_all_dispatch_products(self, internal, external):
        return self.dispatch_repository.get_all_dispatch_products(internal, external)

    def get_vehicle_types(self, internal, external):
        return self.dispatch_repository.get_vehicle_types(internal, external)