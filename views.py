from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from database import db_session


#from models import State, City

#Uncomment below for Memcached
#from werkzeug.contrib.cache import MemcachedCache
#cache = MemcachedCache(['127.0.0.1:11211'])
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()



#Cache Functions



def user(username):
    return "user view"

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

def index():  
    #Check username against cache
    
    #flash('New entry was successfully posted')
    return render_template('index.html')



