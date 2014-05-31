from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger, Text, DateTime
from database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False, nullable=False)
    active = Column(SmallInteger)

    
    def __init__(self, name=None, active=None):
        self.name = name
        self.active = active


    def __repr__(self):
        return '<User %r>' % (self.name)

class UserPermission(Base):
    __tablename__ = 'userpermission'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    permission = Column(Integer)

    
    def __init__(self, user_id=None, permission=None):
        self.user_id = user_id
        self.permission = permission


    def __repr__(self):
        return '<User %r>' % (self.user_id)

class Recipient(Base):
    __tablename__ = 'recipient'
    id = Column(Integer, primary_key=True)
    lname = Column(String(50), unique=False, nullable=False)
    fname = Column(String(50), unique=False)
    mname = Column(String(50), unique=False)
    address = Column(String(50), unique=False)
    active = Column(SmallInteger)
    
    def __init__(self, lname=None, fname=None, mname=None, address=None, active=None):
        self.lname = lname
        self.fname = fname 
        self.mname = mname
        self.address = address
        self.active = active

    def __repr__(self):
        return '<Recipient %r>' % (self.lname + ", " + self.fname)
    
class Document(Base):
    __tablename__ = 'document'
    doc_id = Column(Integer, primary_key=True)
    barcode = Column(String(50))
    image = Column(Text())
    doc_type = Column(Integer)
    
    def __init__(self, barcode=None, image=None, doc_type=None):
        self.barcode = barcode
        self.image = image
        self.doc_type = doc_type

    def __repr__(self):
        return '<Image %r>' % (self.image)
    
class DocumentAnswer(Base):
    __tablename__ = 'documentanswer'
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey('document.doc_id'))
    field_id = Column(Integer, ForeignKey('fieldtype.fieldtype_id'))
    answer = Column(Text)
    
    def __init__(self, doc_id=None, field_id=None, answer=None):
        self.doc_id = doc_id
        self.field_id = field_id
        self.answer = answer

    def __repr__(self):
        return '<Answer %r>' % (self.answer)
    
class Barcode(Base):
    __tablename__ = 'barcode'
    id = Column(Integer, primary_key=True)
    barcode = Column(String(50), unique=True)
    doc_id = Column(Integer)
    datetime = Column(DateTime)
    deleted = Column(SmallInteger)
    exported = Column(SmallInteger)
    
    # We will most likely not initialize barcodes via web app directly.
    # More likely, we'll call a stored procedure.
    def __init__(self, barcode=None, doc_id=None, datetime=None, deleted=None, exported=None):
        self.barcode = barcode
        self.doc_id = doc_id
        self.datetime = datetime
        self.deleted = deleted
        self.exported = exported

    def __repr__(self):
        return '<Barcode: %r>' % (self.barcode)
    
class Doctype(Base):
    __tablename__ = 'doctype'
    doctype_id = Column(Integer, primary_key=True)
    description = Column(String(200))
    active = Column(SmallInteger)
    
    def __init__(self, description=None, active=None):
        self.description = description
    
    def __repr__(self):
        return '<Description %r>' % (self.description)
    
class Fieldtype(Base):
    __tablename__ = 'fieldtype'
    fieldtype_id = Column(Integer, primary_key=True)
    doctype_id = Column(Integer, ForeignKey('doctype.doctype_id'))
    description = Column(String(200))
    active = Column(SmallInteger)

    
    def __init__(self, doctype_id=None, description=None, active=None):
        self.doctype_id = doctype_id
        self.description = description
        self.active = active
    
    def __repr__(self):
        return '<Description %r>' % (self.description)

class KeyingTask(Base):
    __tablename__ = 'keyingtask'
    kt_id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey('doctype.doctype_id'))
    fieldtype_id = Column(Integer, ForeignKey('fieldtype.fieldtype_id'))
    png = Column(Text)
    firstpass = Column(SmallInteger)
    secondpass = Column(SmallInteger)
    audit = Column(SmallInteger)
    firstkeyer = Column(Integer, ForeignKey('user.id'))
    secondkeyer = Column(Integer, ForeignKey('user.id'))
    auditor = Column(Integer, ForeignKey('user.id'))

    
    def __init__(self, doc_id=None, fieldtype_id=None, png=None, firstpass=None, secondpass=None,
                    audit=None, firstkeyer=None, secondkeyer=None, auditor=None):
        self.doc_id = doc_id
        self.fieldtype_id = fieldtype_id
        self.png = png
        self.firstpass = firstpass
        self.secondpass = secondpass
        self.audit = audit
        self.firstkeyer = firstkeyer
        self.secondkeyer = secondkeyer
        self.auditor = auditor
    
    def __repr__(self):
        return '<Task ID %r>' % (self.kt_id)
