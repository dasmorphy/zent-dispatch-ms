import json
from timeit import default_timer
from flask import request

import connexion
from flask.views import MethodView
from loguru import logger

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.entry_control_data import EntryControlData
from swagger_server.models.reception_data import Receptiondata
from swagger_server.models.request_dispatch import RequestDispatch  # noqa: E501
from swagger_server.models.request_dispatch_dispatch_data import RequestDispatchDispatchData
from swagger_server.models.request_entry_control import RequestEntryControl
from swagger_server.models.request_reception import RequestReception
from swagger_server.repository.dispatch_repository import DispatchRepository
from swagger_server.uses_cases.dispatch_use_case import DispatchUseCase
from swagger_server.utils.transactions.transaction import generate_internal_transaction_id

class DispatchView(MethodView):
    def __init__(self):
        self.logger = logger
        dispatch_repository = DispatchRepository()
        self.dispatch_use_case = DispatchUseCase(dispatch_repository)


    def post_dispatch(self):  # noqa: E501
        """Guarda el despacho en la base de datos.

        Guardado de despacho # noqa: E501

        :param body: 
        :type body: dict | bytes

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "post_dispatch"
        response = {}
        status_code = 500
        try:
            if request.content_type.startswith("multipart/form-data"):
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())

                dispatch_file = request.files.get("dispatch_data")
                if not dispatch_file:
                    raise CustomAPIException("Campo dispatch_data no enviado", 400)

                dispatch_raw = dispatch_file.read().decode("utf-8")
                dispatch_dict = json.loads(dispatch_raw)
                dispatch_data = RequestDispatchDispatchData.from_json(dispatch_dict)
                
                external_transaction_id = dispatch_dict['external_transaction_id']
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {dispatch_dict['channel']}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                files = request.files.getlist("images")
                self.dispatch_use_case.post_dispatch(dispatch_data, files, internal_process)
                response["error_code"] = 0
                response["message"] = "Despacho creado correctamente"
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=dispatch_dict['external_transaction_id'])
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code


    def update_dispatch(self, dispatch_id):  # noqa: E501
        """Actualiza el despacho en la base de datos.

        Actualiza de despacho # noqa: E501

        :param body: 
        :type body: dict | bytes

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "update_dispatch"
        response = {}
        status_code = 500
        try:
            if connexion.request.is_json:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                body = RequestDispatch.from_dict(connexion.request.get_json())  # noqa: E501
                external_transaction_id = body.external_transaction_id
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {body.channel}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                self.dispatch_use_case.update_dispatch(body, dispatch_id, internal_process)
                response["error_code"] = 0
                response["message"] = "Despacho actualizado correctamente"
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=body.external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def get_status_dispatch(self):  # noqa: E501
        """Obtiene todos los estados de despacho

        Devuelve todos los estados de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_status_dispatch"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                results = self.dispatch_use_case.get_status_dispatch(internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Estados de despacho obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def get_dispatch(self):  # noqa: E501
        """Obtiene todos los despachos

        Devuelve todos los despachos de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_dispatch"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                headers = {k.lower(): v for k, v in request.headers.items()}
                results = self.dispatch_use_case.get_all_dispatch(headers, request.args, internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Despachos obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def get_dispatch_products(self):  # noqa: E501
        """Obtiene todos los productos de despacho

        Devuelve todos los productos de despacho de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_all_unities"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                results = self.dispatch_use_case.get_all_dispatch_products(internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Productos de despacho obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    

    def get_vehicle_types(self):  # noqa: E501
        """Obtiene todos los tipos de vehículo

        Devuelve todos los tipos de vehículo de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_vehicle_types"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                results = self.dispatch_use_case.get_vehicle_types(internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Tipos de vehículo obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def post_reception(self):  # noqa: E501
        internal_process = (None, None)
        function_name = "post_reception"
        response = {}
        status_code = 500
        try:
            if request.content_type.startswith("multipart/form-data"):
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())

                reception_file = request.files.get("reception_data")
                if not reception_file:
                    raise CustomAPIException("Campo reception_data no enviado", 400)
                
                reception_raw = reception_file.read().decode("utf-8")
                reception_dict = json.loads(reception_raw)
                reception_data = Receptiondata.from_json(reception_dict)

                external_transaction_id = reception_dict['external_transaction_id']
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {reception_dict['channel']}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                files = request.files.getlist("images")
                self.dispatch_use_case.post_reception(reception_data, files, internal_process)
                response["error_code"] = 0
                response["message"] = "Recepción creada correctamente"
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    

    def post_entry_control(self):  # noqa: E501
        internal_process = (None, None)
        function_name = "post_dispatch"
        response = {}
        status_code = 500
        try:
            if request.content_type.startswith("multipart/form-data"):
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())

                entry_file = request.files.get("entry_data")
                if not entry_file:
                    raise CustomAPIException("Campo entry_data no enviado", 400)

                entry_raw = entry_file.read().decode("utf-8")
                entry_dict = json.loads(entry_raw)
                entry_data = EntryControlData.from_json(entry_dict)
                
                external_transaction_id = entry_dict['external_transaction_id']
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {entry_dict['channel']}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                files = request.files.getlist("images")
                self.dispatch_use_case.post_entry_control(entry_data, files, internal_process)
                response["error_code"] = 0
                response["message"] = "Despacho creado correctamente"
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=entry_dict['external_transaction_id'])
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def get_materials(self):  # noqa: E501
        """Obtiene todos los materiales para ingresos de biomar

        Devuelve todos los materiales de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_materials"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                results = self.dispatch_use_case.get_materials(internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Materiales obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def get_areas(self):  # noqa: E501
        """Obtiene todos los áreas de visita para ingresos de biomar

        Devuelve todos las áreas de visitas de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_areas"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                results = self.dispatch_use_case.get_areas(internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Áreas de visitas obtenidas correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    

    def get_staff_charge(self):  # noqa: E501
        """Obtiene todos el personal para ingresos de biomar

        Devuelve todos el personal de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        internal_process = (None, None)
        function_name = "get_staff_charge"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                results = self.dispatch_use_case.get_staff_charge(internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Personal a cargo obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code

    def get_entry_access(self):
        internal_process = (None, None)
        function_name = "get_entry_access"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                external_transaction_id = request.headers.get('externalTransactionId')
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {request.headers.get('channel')}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                headers = {k.lower(): v for k, v in request.headers.items()}
                results = self.dispatch_use_case.get_entry_access(headers, request.args, internal_transaction_id, external_transaction_id)
                response["error_code"] = 0
                response["message"] = "Ingresos obtenidos correctamente"
                response["data"] = results
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=external_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code
    
    def update_entry_access(self, entry_id):  # noqa: E501
        internal_process = (None, None)
        function_name = "update_entry_access"
        response = {}
        status_code = 500
        try:
            if request.content_type.startswith("multipart/form-data"):
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                
                entry_file = request.files.get("entry_data")
                if not entry_file:
                    raise CustomAPIException("Campo entry_data no enviado", 400)

                entry_raw = entry_file.read().decode("utf-8")
                entry_dict = json.loads(entry_raw)
                entry_data = EntryControlData.from_json(entry_dict)

                external_transaction_id = entry_dict['external_transaction_id']
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {entry_dict['channel']}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                files = request.files.getlist("images")
                self.dispatch_use_case.update_entry_access(entry_data, entry_id, files, internal_process)
                response["error_code"] = 0
                response["message"] = "Ingreso actualizado correctamente"
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=entry_dict['external_transaction_id'])
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code