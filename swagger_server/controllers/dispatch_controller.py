import connexion
from flask.views import MethodView
import six

from swagger_server.models.generic_response import GenericResponse  # noqa: E501
from swagger_server.models.request_dispatch import RequestDispatch  # noqa: E501
from swagger_server.models.response_error import ResponseError  # noqa: E501
from swagger_server import util

class DispatchView(MethodView):
    def post_dispatch(body=None):  # noqa: E501
        """Guarda el despacho en la base de datos.

        Guardado de despacho # noqa: E501

        :param body: 
        :type body: dict | bytes

        :rtype: GenericResponse
        """
        if connexion.request.is_json:
            body = RequestDispatch.from_dict(connexion.request.get_json())  # noqa: E501
        return 'do some magic!'


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
