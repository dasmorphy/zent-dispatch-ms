import json
from timeit import default_timer
from flask import request
from venv import logger

import connexion
from flask.views import MethodView

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.request_dispatch import RequestDispatch  # noqa: E501
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

                external_transaction_id = dispatch_dict['external_transaction_id']
                internal_process = (internal_transaction_id, external_transaction_id)
                response["internal_transaction_id"] = internal_transaction_id
                response["external_transaction_id"] = external_transaction_id
                message = f"start request: {function_name}, channel: {dispatch_dict['channel']}"
                logger.info(message, internal=internal_transaction_id, external=external_transaction_id)
                files = request.files.getlist("images")
                self.dispatch_use_case.post_dispatch(dispatch_dict, files, internal_process)
                response["error_code"] = 0
                response["message"] = "Despacho creado correctamente"
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=dispatch_dict['external_transaction_id'])
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_process)
            
        return response, status_code


    def update_dispatch(body=None):  # noqa: E501
        """Actualiza el despacho en la base de datos.

        Actualiza de despacho # noqa: E501

        :param body: 
        :type body: dict | bytes

        :rtype: GenericResponse
        """
        if connexion.request.is_json:
            body = RequestDispatch.from_dict(connexion.request.get_json())  # noqa: E501
        return 'do some magic!'
    
    def get_status_dispatch(external_transaction_id, channel):  # noqa: E501
        """Obtiene todos los estados de despacho

        Devuelve todos los estados de la base # noqa: E501

        :param external_transaction_id: 
        :type external_transaction_id: str
        :param channel: 
        :type channel: str

        :rtype: GenericResponse
        """
        return 'do some magic!'
