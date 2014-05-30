#Central file for our caching methods.

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCached
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
from flask import abort
from sqlalchemy import exc, or_, and_
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
        #res = db_session.query(KeyingTask).with_lockmode('update').filter(KeyingTask.firstkeyer != userid).first()
       
        res = db_session.query(KeyingTask).filter(or_(and_(KeyingTask.secondpass==1, KeyingTask.secondkeyer == userid),and_(KeyingTask.firstpass==1, KeyingTask.firstkeyer == userid))).first()
        #Find a second pass keying job first.
        if res is None:
            res = db_session.query(KeyingTask).filter(or_(KeyingTask.secondkeyer == 0, KeyingTask.secondkeyer == None), KeyingTask.firstkeyer != userid).first()
        
        if res is None:
            #Try to find something that hasn't been keyed yet
            res = db_session.query(KeyingTask).filter(or_(KeyingTask.firstkeyer == 0, KeyingTask.firstkeyer == None)).first()
        
        #no keying tasks left
        if res is None:
           abort(401, "No keying task could be found")
           
        if res.firstkeyer == 0 or res.firstkeyer is None:
            res.firstpass = 1
            res.firstkeyer = userid
        elif (res.secondkeyer == 0 or res.secondkeyer) and res.firstkeyer != userid is None:
            res.secondpass = 1
            res.secondkeyer = userid
            
        db_session.commit()

        return res