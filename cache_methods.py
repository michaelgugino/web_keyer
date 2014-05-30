#Central file for our caching methods.

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCached
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
from flask import abort
from sqlalchemy import exc, or_
from database import db_session
from models import User, KeyingTask

#Cache Functions
def cacheGetUserID(username):
    try:
        res = db_session.query(User.id).filter_by(name=username,active=1).one();
    except exc.SQLAlchemyError:
        abort(401)
    return res.id

def cacheGetAKeyingTask(userid):
        #res = db_session.query(KeyingTask).with_lockmode('update').filter(KeyingTask.firstkeyer != userid,KeyingTask.secondkeyer != userid).filter((KeyingTask.firstpass==0) | (KeyingTask.firstpass==1, KeyingTask.secondpass==0)).first();
        res = db_session.query(KeyingTask).with_lockmode('update').filter(KeyingTask.firstkeyer != userid).first()
        if res is None:
            abort(401)
        if res.firstpass == 0:
            res.firstpass = 1
        else:
            res.secondpass = 1
        db_session.commit()

        return res