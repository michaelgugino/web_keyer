from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView


class AuditView(MethodView):
    def get(self, user_id):
        if user_id is None:
            flash('user id is none')
            return render_template('index.html')

        else:
            return render_template('index.html')

    def post(self):
        return render_template('index.html')

    def delete(self, user_id):
        return render_template('index.html')

    def put(self, user_id):
        return render_template('index.html')