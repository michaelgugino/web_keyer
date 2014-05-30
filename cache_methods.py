#Central file for our caching methods.

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCached
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from sqlalchemy import exc
from database import db_session
from models import User

#Cache Functions
def cacheGetUserID(username):
    try:
        res = db_session.query(User.id).filter_by(name=username,active=1).one();
    except exc.SQLAlchemyError:
        abort(401)
    return res.id