from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from models import User,KeyingTask, KeyingAnswer
import cache_methods
cache = cache_methods.cache

from database import db_session

class KeyerView(MethodView):
    '''
        This class displays and controls
        keying mode.
    '''
    def get(self, user_id):
        '''
       "get" is the default method for entering the keying page.
       We do not submit form data across get, only "post."
       Here, we resume a previously started keying task
       by checking cache.  This is in case the user closed
       their browser or navigated away during a task.
       If no task is found in cache, then we select a new task.
       First, we select something that is on second pass not
       keyed by the user.
       If nothing, we select something that is on first pass.
        '''
        #this would be for /key/<user_id>
        #which is not defined right now.
        
        #testing
        username='mgugino'
        
        #this will load cache with user_id; if
        #there is no active user_id, app
        #will fail to 401 unauthorized.
        myid = cache_methods.cacheGetUserID(username=username)
        
        #Check permissions here
        
        #check to see if we already have a task we should be keying
        #otherwise, we need to fetch a task from the db.
        my_current_task = cache_methods.cacheGetAKeyingTask(userid=myid)
        
        #if we still don't have a task, that means there's nothing to key
        #at the moment.
        if my_current_task is None:
            flash('There are no valid keying tasks at this time, please check back later')
            return render_template('index.html')
            
        #Turn task into a session object so we can update it, etc.
        #For testing only at this point.    
        my_current_task = db_session.merge(my_current_task)
        
        #testing area
        #my_current_task.png = '/static/images/demo3.png'
        #db_session.commit()
        #cache.set(str(myid)+':current_task',my_current_task,)
        
        #determine field type goes here
        #This information should go in fielddefs table.
        resource='Recipient'
        
        #This information should go in res_ourcedefs table.
        attributes=['id', 'lname', 'fname', 'mname']
        
        #retrieve field resources
        my_dict = cache_methods.cacheGetDict(fieldtype=my_current_task.fieldtype_id, resource=resource, attributes=attributes)
        #flash(my_dict[1])
        #return render_template('index.html')
        return render_template('key.html', kt=my_current_task, auto_dict=my_dict)

    def post(self, user_id):
        '''
            This method is used for submission of keying data.
            First, the submitted task id is check against the cache.
            If the cache contains a keying task with the user's id,
            then the form is submitted.  Otherwise, the user will
            be redirected to the index page to log in again.  This
            is to prevent stale data from being submitted.            
        '''
        
        #testing
        username='mgugino'
        
        #this will load cache with user_id; if
        #there is no active user_id, app
        #will fail to 401 unauthorized.
        myid = cache_methods.cacheGetUserID(username=username)
        
        # Make sure our answer fields are all present from the form.
        if (request.form.get('kt_id') is None or request.form.get('pass_number') is None or request.form.get('answer') is None):
            abort(500, "Invalid form submitted.  If you continue to see this error, contact your administrator")
            
        # check cache for 'keyingtask:<kt_id>:<pass_number>' = <myid>
        # This ensure's we're not keying a stale task, as well as preventing spoofing.
        if (cache.get('keyingtask:'+str(request.form['kt_id'])+':'+str(request.form['pass_number'])) != myid):
            # if no task / user_id match found in cache, exit to index.
            cache.delete(str(myid)+':current_task')
            flash("Invalid Keying Task Submitteda")
            return render_template('index.html')
        
        
        # if task was found, submit task to rabbitmq, unset user cache and task cache.
        #in testing, all that happens here.
        
        #Ensure we have a current task in cache.
        my_current_task = cache.get(str(myid)+':current_task')
        if (my_current_task is None):
            #No current task means we cannot procedure further.  Fall back to index.
            cache.delete(str(myid)+':current_task')
            flash("Invalid Keying Task Submitted")
            return render_template('index.html')
        #Task is valid, submit message to process results.
        #-------------RabbitMQ part-----------------
        #Testing: Make sure warm cache is implemented before offloading db update to rabbit.
        my_current_task = db_session.merge(my_current_task)
        if (request.form['pass_number'] == str(1)):
            my_current_task.firstpass = 2
            my_current_answer = KeyingAnswer(kt_id=request.form['kt_id'], firstanswer=request.form['answer'])
            db_session.add(my_current_answer)
        else:
            my_current_task.secondpass = 2
            my_current_answer =  db_session.query(KeyingAnswer).with_lockmode('update').filter(KeyingAnswer.kt_id == int(request.form['kt_id'])).first()
            my_current_answer.secondanswer = request.form['answer']
        db_session.commit()
        
        #-------------End RabbitMQ part-----------------
        cache.delete(str(myid)+':current_task')
        cache.delete('keyingtask:'+str(request.form['kt_id'])+':'+str(request.form['pass_number']))
        #get new task
        my_current_task = cache_methods.cacheGetAKeyingTask(userid=myid)
        if my_current_task is None:
            flash('There are no valid keying tasks at this time, please check back later')
            return render_template('index.html')
        #testing area
        #my_current_task.png = '/static/images/demo.png'
        #db_session.commit()
        #cache.set(str(myid)+':current_task',my_current_task,)
        
        #determine field type goes here
        #This information should go in fielddefs table.
        resource='Recipient'
        
        #This information should go in res_ourcedefs table.
        attributes=['id', 'lname', 'fname', 'mname']
        
        #retrieve field resources
        my_dict = cache_methods.cacheGetDict(fieldtype=my_current_task.fieldtype_id, resource=resource, attributes=attributes)
        #flash(my_dict[1])
        #return render_template('index.html')
        
        return render_template('key.html', kt=my_current_task, auto_dict=my_dict)

    def delete(self, user_id):
        if user_id is None:
            pass

        else:
            flash(user_id)
        return render_template('index.html')

    def put(self, user_id):
        return render_template('index.html')
    
