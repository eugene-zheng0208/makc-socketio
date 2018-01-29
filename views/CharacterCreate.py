from socketio.namespace import BaseNamespace
from makc_socketio.data_files.skills import SkillList
from makc_socketio.data_files.archtypes import archtypes
import logging
import time
import json
import random
import redis
log = logging.getLogger(__name__)


def generate_values(valcount):
        result=[]
        for i in range(0,valcount):
          rng=random.randint(1,6)
          result.append(rng)
        result.sort()
        
        return result
    
class CharCreateNamespace(BaseNamespace):

    def on_getarchtypelist(self,race_id,class_id,identifier):
        log.debug("Race"+race_id)  
        log.debug("Class"+class_id)
        race_id = int(race_id)
        class_id = int(class_id)
        archtypelist = []
        

        for k, v in enumerate(archtypes.archtype):

          if v["class"] == class_id:
            log.debug(v["class"])  
            if v["race"] == -1:
              
              archtypelist.append({"raceSpecific": 0, "name": v["name"], "index": k})
              log.debug("not race specific: "+v['name'])
            if v["race"] == race_id:
              archtypelist.append({"raceSpecific": 1, "name": v["name"], "index": k})
              log.debug("race specific: "+v['name'])
        
        
        log.debug(json.dumps(archtypelist))
        self.emit("sendarchtypelist",json.dumps(archtypelist))
      
      
      
    def on_rollabilitydice(self,variety,identifier):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        #pkt = dict(type="event",name="ForceDisconnect",args="",endpoint=self.ns_name)
        #Are they supposed to be connecting? If not, don't let them!
        log.debug(r.get("allowed:"+identifier))
        log.debug(r.get("rolls:"+identifier))
        if r.get("allowed:"+identifier) is None:
          self.emit("ForceDisconnect")
          return
        
        ##Have they rolled in the last 24 hours?
        if r.get("rolls:"+identifier) is not None:
          
          self.emit("generatedroll",r.get("rolls:"+identifier))
          return
          
        if variety == 0:       
          ## Generate First Value
          result = generate_values(4)
          diceroll1 = " + ".join(map(str, result))
          ## delete lowest # for variety 0
          del result[0]
          dicetotal1 = sum(result,0)
          
          ## Generate Second Value
          result = generate_values(4)
          diceroll2 = " + ".join(map(str, result))
          ## delete lowest # for variety 0
          del result[0]
          dicetotal2 = sum(result,0)

          ## Generate Third Value
          result = generate_values(4)
          diceroll3 = " + ".join(map(str, result))
          ## delete lowest # for variety 0
          del result[0]
          dicetotal3 = sum(result,0)

          ## Generate Fourth Value
          result = generate_values(4)
          diceroll4 = " + ".join(map(str, result))
          ## delete lowest # for variety 0
          del result[0]
          dicetotal4 = sum(result,0)

          ## Generate Fifth Value
          result = generate_values(4)
          diceroll5 = " + ".join(map(str, result))
          ## delete lowest # for variety 0
          del result[0]
          dicetotal5 = sum(result,0)

          ## Generate Six Value
          result = generate_values(4)
          diceroll6 = " + ".join(map(str, result))
          ## delete lowest # for variety 0
          del result[0]
          dicetotal6 = sum(result,0)


        rolls = {
          "variety": variety,
          "diceroll1": diceroll1,
          "dicetotal1": dicetotal1,
          "diceroll2": diceroll2,
          "dicetotal2": dicetotal2,
          "diceroll3": diceroll3,
          "dicetotal3": dicetotal3,
          "diceroll4": diceroll4,
          "dicetotal4": dicetotal4,
          "diceroll5": diceroll5,
          "dicetotal5": dicetotal5,
          "diceroll6": diceroll6,
          "dicetotal6": dicetotal6,

          }
        r.set("rolls:"+identifier,json.dumps(rolls))
        r.expire("rolls:"+identifier,86400)
        log.debug(r.get("rolls:"+identifier))
        self.emit("generatedroll",json.dumps(rolls))

             
    def on_chat(self, msg, room=""):
        #log.debug(room)
        if room == "":
          self.broadcast_event('chat', msg)
        else:
          self.emit_to_room(room, 'roomchat', self.session['nickname'], room, msg)

    #def recv_connect(self):
    #    self.broadcast_event('user_connect')

    #def recv_disconnect(self):
    #    self.broadcast_event('user_disconnect')
    #    self.disconnect(silent=True)

    #def on_join(self, nickname, channel):
    #    self.check_dupe(channel,nickname);
        
    #    self.join(channel, nickname)