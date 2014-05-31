#Central file for our caching methods.

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCached
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
from flask import abort, flash
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
    
def cacheGetDict(fieldtype, resource, attributes):
    '''Returns a dictionary object for use in auto_complete combobox on keying page.
       fieldtype == the field type of the keying task.
       resouce (case sensitive Model reference.  Ie, 'Recipient') == what table we're looking in.
       attributes (array of strings)== what columns from that table do we want?
       Since each field type might use a resource in a
       different way, we are going to cache by dict:<fieldtype>
       This ensure that if different field types use different
       attributes from a resource, we will not interfere with
       those objects.'''
    #First, try to get our auto_complete dict from cache
    mydict = cache.get('dict:'+str(fieldtype))
    #flash(mydict)
    if mydict is None:
        res = db_session.query(globals()[resource]).filter_by(active=1).all()
        if res is None:
            abort(401, "invalid resource type")
        mydict = {}
        for item in res:
            value = ''
            skip = 1
            for attr in attributes:
                if skip == 0:
                    value += str(getattr(item, attr, )) + ', '
                if skip == 1:
                     skip = 0
            
            #mydict[getattr(item, 'id',)] = getattr(item, 'lname', ) + ', ' + getattr(item, 'fname', ) + ', ' + getattr(item, 'mname', )
            mydict[getattr(item, 'id',)] = value
        cache.set('dict:'+str(fieldtype),mydict,)
    return mydict



