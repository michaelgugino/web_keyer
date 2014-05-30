from flask import Flask, render_template
import views, config


app = Flask(__name__)
app.config.from_object('config.Config')
app.add_url_rule('/', view_func=views.index)

app.add_url_rule('/users/<user_id>/', view_func=views.users)
#app.add_url_rule('/key', view_func=views.key)
#app.add_url_rule('/audit', view_func=views.audit)
#app.add_url_rule('/admin', view_func=views.admin)


app.add_url_rule('/test', view_func=views.test)
app.add_url_rule('/test2', view_func=views.test2)
app.add_url_rule('/testdoc', view_func=views.testdoc)
app.add_url_rule('/testkt', view_func=views.testkt)
app.add_url_rule('/testdoctype', view_func=views.testdoctype)
app.add_url_rule('/testfieldtype', view_func=views.testfieldtype)
 

from KeyerView import KeyerView
from AuditView import AuditView
from AdminView import AdminView

keyerview = KeyerView.as_view('key')
app.add_url_rule('/key', view_func=keyerview, methods=['GET',], defaults={'user_id': None})
auditview = AuditView.as_view('audit')
app.add_url_rule('/audit', view_func=auditview, methods=['GET',], defaults={'user_id': None})
adminview = AdminView.as_view('admin')
app.add_url_rule('/admin', view_func=adminview, methods=['GET',], defaults={'user_id': None})




from database import db_session
from database import init_db

#init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()