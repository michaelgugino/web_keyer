from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from models import User
import cache_methods
cache = cache_methods.cache

class KeyerView(MethodView):
    def get(self, user_id):
        #this would be for /key/<user_id>
        #which is not defined right now.
        if user_id is None:
            pass

        else:
            flash(user_id)
        
        return render_template('key.html')

    def post(self):
        return render_template('index.html')

    def delete(self, user_id):
        return render_template('index.html')

    def put(self, user_id):
        return render_template('index.html')
    
