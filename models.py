import logging

from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Authenticated, Everyone, Allow, Deny
from pyramid.security import authenticated_userid
log = logging.getLogger(__name__)


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DBMetadata = MetaData()



from pyramid.security import unauthenticated_userid

def get_user(request):
    # the below line is just an example, use your own method of
    # accessing a database connection here (this could even be another
    # request property such as request.db, implemented using this same
    # pattern).
    
    userid = unauthenticated_userid(request)
    if userid is not None:
        # this should return None if the user doesn't exist
        # in the database
        return DBSession.query(Users).filter(Users.UserID == userid ).first()
        
          
          
## default authentication ##
class Root(object):
    __acl__ = [
        (Allow, Everyone, 'anonymous'),
        (Allow, Authenticated, 'logged_in'),
    ]

    def __init__(self, request):
        self.request = request

        
        

class ReflectedTable(object):
    """Base class for database objects that are mapped to tables by reflection.
    """
    __tablename__ = None




class Users(ReflectedTable):
    __tablename__ = 'users'
    
def map_tables(to_reflect):
    for _class in to_reflect:
        log.info('Reflecting {0} from table {1}'
                 .format(_class, _class.__tablename__))
        table = Table(_class.__tablename__, DBMetadata, autoload=True)
        mapper(_class, table)


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    DBMetadata.bind = engine
    to_reflect = (
    
        Users,
    )
    map_tables(to_reflect)
