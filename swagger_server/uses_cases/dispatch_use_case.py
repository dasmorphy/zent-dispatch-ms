



from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db.dispatch import Dispatch
from swagger_server.models.entry_control_data import EntryControlData
from swagger_server.models.reception_data import Receptiondata
from swagger_server.models.request_dispatch import RequestDispatch
from swagger_server.models.request_dispatch_dispatch_data import RequestDispatchDispatchData
from swagger_server.models.request_entry_control import RequestEntryControl
from swagger_server.models.request_reception import RequestReception
from swagger_server.repository.dispatch_repository import DispatchRepository


class DispatchUseCase:

    def __init__(self, dispatch_repository: DispatchRepository):
        self.dispatch_repository = dispatch_repository


    def post_dispatch(self, body: RequestDispatchDispatchData, images, internal_process: tuple) -> None:

        if len(images) > 10:
            raise CustomAPIException("Máximo 10 imagenes", 500)
        
        internal, external = internal_process
        
        self.dispatch_repository.post_dispatch(body, images, internal, external)

    def update_dispatch(self, data: RequestDispatchDispatchData, id_disp: int, images, internal_process: tuple) -> None:
        if len(images) > 10:
            raise CustomAPIException("Máximo 10 imagenes", 500)
        
        internal, external = internal_process
        self.dispatch_repository.update_dispatch(data, id_disp, images, internal, external)

    def get_all_dispatch_products(self, internal, external):
        return self.dispatch_repository.get_all_dispatch_products(internal, external)

    def get_vehicle_types(self, internal, external):
        return self.dispatch_repository.get_vehicle_types(internal, external)
    
    def get_status_dispatch(self, internal, external):
        return self.dispatch_repository.get_status_dispatch(internal, external)
    
    def get_all_dispatch(self, headers, params, internal, external):
        destiny = headers.get("destiny")
        filters = {
            "destiny": [int(x) for x in destiny.split(",")] if destiny else [],
            "user": headers.get("user"),
            "type_process": headers.get("type-process"),
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
                "type_process": dispatch.type_process,
                "created_at": dispatch.created_at,
                "updated_at": dispatch.updated_at,
                "created_by": dispatch.created_by,
                "updated_by": dispatch.updated_by,
                "order_number": dispatch.order_number,
                "skus": skus,
                "name_vehicle_type": name_vehicle_type,
                "name_destiny": name_destiny or dispatch.destiny_product,
                "status": dispatch_status.name,
                "reception": reception,
                "images": images
            }
            for dispatch, dispatch_status, name_destiny, name_vehicle_type, skus, images, reception in rows
        ]
    
    def post_reception(self, body: Receptiondata, images, internal_process: tuple) -> None:        
        internal, external = internal_process
        
        if len(images) > 10:
            raise CustomAPIException("Máximo 10 imagenes", 500)

        self.dispatch_repository.post_reception(body, images, internal, external)

    def post_entry_control(self, body: EntryControlData, images, internal_process: tuple) -> None:        
        internal, external = internal_process
        
        if len(images) > 10:
            raise CustomAPIException("Máximo 10 imagenes", 500)

        self.dispatch_repository.post_entry_control(body, images, internal, external)

    def get_materials(self, internal, external):
        return self.dispatch_repository.get_materials(internal, external)
    
    def get_areas(self, internal, external):
        return self.dispatch_repository.get_areas(internal, external)
    
    def get_staff_charge(self, internal, external):
        return self.dispatch_repository.get_staff_charge(internal, external)
    

    def get_history_dispatch(self, params, internal, external):
        return self.dispatch_repository.get_history_dispatch(params.get("id_dispatch"), internal, external)

    def get_entry_access(self, headers, params, internal, external):
        areas = headers.get("areas")
        filters = {
            "user": headers.get("user"),
            "start_date": params.get("start_date"),
            "end_date": params.get("end_date"),
            "areas": [int(x) for x in areas.split(",")] if areas else []
        }

        rows = self.dispatch_repository.get_entry_access(filters, internal, external)

        return [
            {
                "id_access_control": access_control.id_access_control,
                "dni": access_control.dni,
                "names_visit": access_control.names_visit,
                "reason_visit": access_control.reason_visit,
                "area_id": access_control.area_visit_id,
                "area_name": area.name,
                "staff_charge_id": access_control.staff_charge_id,
                "staff_charge_name": staff.name if staff else None,
                "other_staff": access_control.other_staff,
                "observations_entry": access_control.observations_entry,
                "observations_out": access_control.observations_out,
                "status": access_control.status,
                "created_at": access_control.created_at,
                "updated_at": access_control.updated_at,
                "created_by": access_control.created_by,
                "updated_by": access_control.updated_by,
                "images": images,
                "materials": materials
            }
            for access_control, area, staff, materials, images in rows
        ]
    
    def update_entry_access(self, data: EntryControlData, id_entry: int, images, internal_process: tuple) -> None:
        internal, external = internal_process
        self.dispatch_repository.update_entry_access(data, id_entry, images, internal, external)


    def get_resume_graphs(self, headers, params, internal, external):
        destiny = headers.get("destiny")
        product_term = []

        filters = {
            "type_process": headers.get("type-process"),
            "destiny": [int(x) for x in destiny.split(",")] if destiny else [],
            "user": headers.get("user"),
            "start_date": params.get("start_date"),
            "end_date": params.get("end_date"),
        }

        dispatch_by_status = self.dispatch_repository.get_dispatch_count_by_status(
            filters, internal, external
        )

        destiny_count = self.dispatch_repository.get_count_destiny(
            filters, internal, external
        )

        discrepancy = self.dispatch_repository.get_dispatch_count_discrepancy(
            filters, internal, external
        )

        entry_by_status = self.dispatch_repository.get_count_entry_status(
            filters, internal, external
        )

        count_type_access = self.dispatch_repository.get_count_type_access(
            filters, internal, external
        )

        discrepancy_last_7_days = self.dispatch_repository.get_dispatch_discrepancy_last_7_days(
            filters, internal, external
        )

        skus_store = self.dispatch_repository.get_skus_count_store(
            filters, internal, external
        )

        top_materials = self.dispatch_repository.get_top_materials_access(filters, internal, external)


        if filters.get("type_process") == "product":
            product_term = self.dispatch_repository.get_product_count_client(filters, internal, external)


        return {
            "product_term": product_term,
            "discrepancy_7_days": discrepancy_last_7_days,
            "dispatch_by_status": dispatch_by_status,
            "skus_store": skus_store,
            "destiny_count": destiny_count,
            "discrepancy": discrepancy["count_discrepancy"],
            "without_discrepancy": discrepancy["count_without_discrepancy"],
            "entry_biomar": {
                "entry_by_status": entry_by_status,
                "count_type_access": count_type_access,
                "top_materials": top_materials
            }
        }