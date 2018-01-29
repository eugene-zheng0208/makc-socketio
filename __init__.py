from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config
from makc_socketio.views.socketio_loader import socketio_service
##from makc_socketio.views.CharacterCreate import index
#from makc_socketio.views.index_unloggedin import NotLoggedInView

import logging
import os

here = os.path.dirname(os.path.abspath(__file__))

from makc_socketio.models import (
    DBSession,
    DBMetadata,
    Root,
    get_user
    )
    
def simple_route(config, name, url, fn):
    """
    Function to simplify creating routes in pyramid
    Takes the pyramid configuration, name of the route, url, and view
    function.
    """
    config.add_route(name, url)
    config.add_view(fn, route_name=name,
            renderer="makc:templates/%s.mako" % name)


def main(global_config, **settings):
   """ This function returns a Pyramid WSGI application.
    """
   engine = engine_from_config(settings, 'sqlalchemy.')

   authn_policy = AuthTktAuthenticationPolicy(settings['authentication_key'], hashalg='sha512', timeout=1200, reissue_time=300)
   authz_policy = ACLAuthorizationPolicy()
    
   models.initialize_sql(engine)
   settings['mako.directories'] = os.path.join(here, 'templates') 
   DBSession.configure(bind=engine)
   DBMetadata.bind = engine
   config = Configurator(settings=settings,root_factory=Root)
   config.add_request_method(get_user, 'user', reify=True)    
   config.set_authentication_policy(authn_policy)
   config.set_authorization_policy(authz_policy)

  # simple_route(config, 'index', '/indeee', index)
 #  config.add_route('home','/')
 #  config.add_route('about','/about')
 #  config.add_route('signup','/signup')
 #  config.add_route('login','/login')
 #  config.add_route('validate','/validate/{validation_code}')
    
   # The socketio view configuration
   simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service)

  # config.add_static_view('static', 'static', cache_max_age=3600)
   config.scan()
   app = config.make_wsgi_app()

   return app
