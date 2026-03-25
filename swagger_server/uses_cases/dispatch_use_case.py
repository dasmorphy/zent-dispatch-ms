



from swagger_server.models.db.dispatch import Dispatch
from swagger_server.repository.dispatch_repository import DispatchRepository


class DispatchUseCase:

    def __init__(self, logbook_repository: DispatchRepository):
        self.logbook_repository = logbook_repository


    def post_dispatch(self, body, images, internal_process: tuple) -> None:
        internal, external = internal_process

        dispatch = Dispatch(
            unity_id=body['id_unity'],
            category_id=body['id_category'],
            group_business_id=body['id_group_business'],
            shipping_guide=body['shipping_guide'],
            description=body['description'],
            quantity=body['quantity'],
            weight=body['weight'],
            provider=body['provider'],
            truck_license=body['truck_license'],
            name_driver=body['name_driver'],
            destiny_intern=body['destiny_intern'],
            authorized_by=body['authorized_by'],
            observations=body['observations'],
            created_by=body['created_by'],
            updated_by=body['created_by'],
            name_user=body['name_user'],
            workday=body['workday'],
            lat=body.get('lat'),
            long=body.get('long')
        )

        self.logbook_repository.post_dispatch(dispatch, images, internal, external)