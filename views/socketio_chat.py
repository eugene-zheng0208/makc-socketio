from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.mixins import RoomsMixin
import logging
import time
log = logging.getLogger(__name__)


class ChatRoomsMixin(object):
    def __init__(self, *args, **kwargs):
        super(ChatRoomsMixin, self).__init__(*args, **kwargs)
        if 'rooms' not in self.session:
            self.session['rooms'] = set()  # a set of simple strings
            self.session['nickname'] = ""
    def join(self, room, nickname):
        """Lets a user join a room on a specific Namespace."""
        self.session['rooms'].add(self._get_room_name(room))
        self.session['nickname'] = nickname
        log.debug("Joined a channel"+room)

    def leave(self, room):
        """Lets a user leave a room on a specific Namespace."""
        self.session['rooms'].remove(self._get_room_name(room))

    def _get_room_name(self, room):
        return self.ns_name + '_' + room
    
    def check_dupe(self, room, nick):
        log.debug("dupecheck");
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'nickname' not in socket.session:
                continue
            
            if nick in socket.session['nickname']:
                log.debug("dupe found, disconnecting old")
                pkt = dict(type="event",name="ForceDisconnect",args="",endpoint=self.ns_name)
                socket.send_packet(pkt)
                break

        
    def emit_to_room(self, room, event, *args):
        """This is sent to all in the room (in this particular Namespace)"""
        #log.debug(args)
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        t0 = time.clock()
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'rooms' not in socket.session:
                continue
            
            if room_name in socket.session['rooms']:
                socket.send_packet(pkt)
            #if room_name in socket.session['rooms'] and self.socket != socket:
            #    socket.send_packet(pkt)
        log.debug(time.clock() - t0)

class ChatNamespace(BaseNamespace, ChatRoomsMixin, BroadcastMixin):
             
    def on_chat(self, msg, room=""):
        #log.debug(room)
        if room == "":
          self.broadcast_event('chat', msg)
        else:
          self.emit_to_room(room, 'roomchat', self.session['nickname'], room, msg)

    def recv_connect(self):
        self.broadcast_event('user_connect')

    def recv_disconnect(self):
        self.broadcast_event('user_disconnect')
        self.disconnect(silent=True)

    def on_join(self, nickname, channel):
        self.check_dupe(channel,nickname);
        
        self.join(channel, nickname)

