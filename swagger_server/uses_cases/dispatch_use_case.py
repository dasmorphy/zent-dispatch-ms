



from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.repository.dispatch_repository import DispatchRepository


class DispatchUseCase:

    def __init__(self, logbook_repository: DispatchRepository):
        self.logbook_repository = logbook_repository


    def post_dispatch(self, body, images, internal_process: tuple) -> None:

        if len(images) > 10:
            raise CustomAPIException("Máximo 10 imagenes", 500)
        
        internal, external = internal_process
        self.logbook_repository.post_dispatch(body, images, internal, external)