from flask import Flask, render_template
from flask.views import MethodView
#from models import State, City
import views, config
from KeyerView import KeyerView
#from AdminView import AdminView
#from AuditView import AuditView

app = Flask(__name__)
app.config.from_object('config.Config')
app.add_url_rule('/', view_func=views.index)
#app.add_url_rule('/key', view_func=views.key)
#app.add_url_rule('/audit', view_func=views.audit)
#app.add_url_rule('/admin', view_func=views.admin)

keyerview = KeyerView.as_view('key')
app.add_url_rule('/key', view_func=keyerview, methods=['GET',], defaults={'user_id': None})
auditview = KeyerView.as_view('audit')
app.add_url_rule('/audit', view_func=auditview, methods=['GET',], defaults={'user_id': None})
adminview = KeyerView.as_view('admin')
app.add_url_rule('/admin', view_func=adminview, methods=['GET',], defaults={'user_id': None})

from database import db_session
from database import init_db

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()