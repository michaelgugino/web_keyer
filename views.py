from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from models import User
import cache_methods
cache = cache_methods.cache


from database import db_session




def users(user_id):
    
    return "user view"


def index():  
    #Check username against cache
    myid = cache.get('mgugino:id')
    if myid is None:
        myid = cache_methods.cacheGetUserID(username='mgugino')
        cache.set('mgugino:id',myid,)
    #flash('New entry was successfully posted')
    return render_template('index.html')


def key():
    #Check username against cache
    
    # Check permissions
    
    #check for existing tasks
    
    return render_template('index.html')

def audit():
    #Check username against cache
    
    # Check permissions
    
    #check for existing tasks
    
    return render_template('index.html')

def admin():
    #Check username against cache
    
    # Check permissions
    
    return render_template('index.html')

def test():
    #Check username against cache
    my_new_user = User(name='m3', active=0)
    db_session.add(my_new_user)
    db_session.commit()
    # Check permissions
    return render_template('index.html')

def test2():
    #Check username against cache
    my_new_user = db_session.query(User).filter_by(name='m2').first()
    #my_new_user.update({"active": 5})
    my_new_user.active = 3
    db_session.commit()
    # Check permissions
    return render_template('index.html')


