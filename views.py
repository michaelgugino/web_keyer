from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from models import User, Document, Doctype, Fieldtype, KeyingTask
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

def testdoc():
    #Check username against cache
    my_new_user = Document()
    my_new_user.barcode = '123'
    my_new_user.image = '/static/images/demo.png'
    my_new_user.doc_type = 1
    db_session.add(my_new_user)
    db_session.commit()
    # Check permissions
    flash('new document added')
    return render_template('index.html')

def testdoctype():
    new = Doctype()
    new.description = "A test document"
    new.active = 1
    db_session.add(new)
    db_session.commit()
    return render_template('index.html')
 
def testfieldtype():
    new = Fieldtype()
    new.doctype_id = 1
    new.description = "A test field"
    new.active = 1
    db_session.add(new)
    db_session.commit()
    return render_template('index.html')

def testkt():
    new = KeyingTask()
    new.doc_id = 1
    new.fieldtype_id = 1
    new.png = '/static/images/demo.png'
    db_session.add(new)
    db_session.commit()
    new = KeyingTask()
    new.doc_id = 1
    new.fieldtype_id = 1
    new.png = '/static/images/demo3.png'
    db_session.add(new)
    db_session.commit()
    return render_template('index.html')