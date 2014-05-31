#Central file for our caching methods.

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCached
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
from flask import abort
from sqlalchemy import exc, or_, and_
from database import db_session
from models import User, KeyingTask, Recipient

#Cache Functions
def cacheGetUserID(username):
    myid = cache.get(username+':id')
    if myid is None:        
        try:
            res = db_session.query(User.id).filter_by(name=username,active=1).one();
        except exc.SQLAlchemyError:
            abort(401, "You do not appear to be a valid user for this application")
        cache.set(username+':id',res.id,)
        myid = res.id
    return myid

def cacheGetAKeyingTask(userid):

        #get the keying task that user was working on last.
        res = cache.get(str(userid)+':current_task')

        #we don't need to check the db for in-process tasks.
        #if cache fails, we will warm load the cache with keying tasks.
        #check for warmload of cache here to prevent massive db problems.
        if res is None:    
            # we are going to remove the next line after enabling warm load of cache.
            res = db_session.query(KeyingTask).filter(or_(and_(KeyingTask.secondpass==1, KeyingTask.secondkeyer == userid),and_(KeyingTask.firstpass==1, KeyingTask.firstkeyer == userid))).first()
            #Find a second pass keying job first.
            if res is None:
                res = db_session.query(KeyingTask).with_lockmode('update').filter(or_(KeyingTask.secondkeyer == 0, KeyingTask.secondkeyer == None), KeyingTask.firstkeyer != userid).first()
        
            if res is None:
                 #Try to find something that hasn't been keyed yet
                 res = db_session.query(KeyingTask).with_lockmode('update').filter(or_(KeyingTask.firstkeyer == 0, KeyingTask.firstkeyer == None)).first()
        
            #no keying tasks left
            if res is None:
                return None
           
            # we found a keying task, now we need to update the db
            # so no one else works on the task.
            if res.firstkeyer == 0 or res.firstkeyer is None:
                res.firstpass = 1
                res.firstkeyer = userid
            elif (res.secondkeyer == 0 or res.secondkeyer is None) and res.firstkeyer != userid:
                res.secondpass = 1
                res.secondkeyer = userid
            
            db_session.commit()
            cache.set(str(userid)+':current_task',res,)
        return res
    
def cacheGetDict(resource):
    res = db_session.query(globals()[resource]).filter_by(active=1).all()
    mydict = {}
    for item in res:
        mydict[item.id] = item.lname + ', ' + item.fname
    return mydict



