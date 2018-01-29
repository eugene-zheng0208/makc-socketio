from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.mixins import RoomsMixin
from makc_socketio.views.socketio_chat import ChatNamespace
from makc_socketio.views.CharacterCreate import CharCreateNamespace
import logging
import time
log = logging.getLogger(__name__)




def index(request):
    """ Base view to load our template """
    return {}




from pyramid.response import Response

def socketio_service(request):
    socketio_manage(request.environ,
                    {'/CharCreate': CharCreateNamespace},
                    request=request)

    return Response('')

