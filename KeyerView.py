from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from models import User,KeyingTask
import cache_methods
cache = cache_methods.cache

from database import db_session

class KeyerView(MethodView):
    #get is the default method for entering the keying page.
    #we do not submit form data across get, only post.
    def get(self, user_id):
        #this would be for /key/<user_id>
        #which is not defined right now.
        
        #testing
        myid = cache.get('mgugino:id')
        
        #this will load cache with user_id; if
        #there is no active user_id, app
        #will fail to 401 unauthorized.
        if myid is None:
            myid = cache_methods.cacheGetUserID(username='mgugino')
            cache.set('mgugino:id',myid,)
        
        #Check permissions here
        
        #check to see if we already have a task we should be keying
        #otherwise, we need to fetch a task from the db.
        my_current_task = cache.get(str(myid)+':current_task')
        
        if my_current_task is None:
            #we don't have a task defined (ie, we didn't refresh, or memcached died)
            #This should only be called once when the keyer enters for the day
            #or after a logout.
            my_current_task = cache_methods.cacheGetAKeyingTask(userid=myid)
            
            #if there's no task to get, then we will error.
            if my_current_task is None:
                flash('There are no valid keying tasks at this time, please check back later')
                return render_template('index.html')
            cache.set(str(myid)+':current_task',my_current_task,)
            
        my_current_task = db_session.merge(my_current_task)
        
        #testing area
        my_current_task.png = '/static/images/demo3.png'
        db_session.commit()
        cache.set(str(myid)+':current_task',my_current_task,)
        flash("Resuming Previous keying task, id: " + str(my_current_task.png))
        #testing area.
        
        return render_template('key.html', kt=my_current_task)

    def post(self):
        return render_template('index.html')

    def delete(self, user_id):
        if user_id is None:
            pass

        else:
            flash(user_id)
        return render_template('index.html')

    def put(self, user_id):
        return render_template('index.html')
    
