from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from models import User
import cache_methods
cache = cache_methods.cache





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

def add_user():
    #Check username against cache
    
    # Check permissions
    return render_template('index.html')




