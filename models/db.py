import pytz

user_timezone = session.plugin_timezone_tx or 'UTC'

# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_user_timezonehttps()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

db.define_table('medicines',
                Field('medicine_name', 'string', length=40, required=True),
                format = '%(medicine_name)s',
                )

db.define_table('events',
                Field('event_time', 'datetime', default = request.now, update = request.now,
                    requires=IS_DATETIME(format=('%m-%d-%Y %H:%M'), timezone=pytz.timezone(user_timezone))),
                Field('event_type', 'string', requires=IS_IN_SET(['', 'Blood Pressure', 'Headache', 'Medicine', 'Mood', 'Nausea',
                                                        'Pain', 'Sleep Duration', 'Stool', 'Weight']), default=''),
                Field('event_level', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['', '0 - Pain Free', '1 - Minor Annoyance', '2 - Moderate Annoyance', '3 - Distracting',
                                                                                   '4- Can Be Ignored', '5 - Unable To Ignore', '6 - Difficult To Focus', '7 - Unable To Sleep',
                                                                                   '8 - Physical Activity Severely Limited', '9 - Almost Unbearable', '10 - Unbearable'])),
                                                                                   default='', represent=lambda v, r: '' if v is None else v),
                Field('bristol_scale', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['', 'Type 1 - Separate hard lumps', 'Type 2 - Lumpy and sausage like',
                                                                     'Type 3 - A sausage shape with cracks in the surface', 'Type 4 - Like a smooth, soft sausage',
                                                                     'Type 5 - Soft blobs with clear-cut edges', 'Type 6 - Mushy consistency with ragged edges',
                                                                     'Type 7 - Liquid consistency with no solid pieces'])), default='', represent=lambda v, r: '' if v is None else v),
                Field('systolic', 'integer', length=3, required=False, represent=lambda v, r: '' if v is 0 else v),
                Field('diastolic', 'integer', length=3, required=False, represent=lambda v, r: '' if v is 0 else v),
                Field('pulse', 'integer', length=3, required=False, represent=lambda v, r: '' if v is 0 else v),
                Field('medicine', 'reference medicines', requires = IS_EMPTY_OR(IS_IN_DB(db, db.medicines.id, '%(medicine_name)s')),  represent=lambda v, r: '' if v is None else v),
                Field('dosage', 'string', length=10, required=False, default='', represent=lambda v, r: '' if v is None else v),
                Field('lbs', 'double', required=False, represent=lambda v, r: '' if v is 0.00 else v),
                Field('duration', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['', ':15', ':30', ':45', '1:00', '1:15', '1:30', '1:45', '2:00', '2:15', '2:30', '2:45', '3:00',
                                                                            '3:15', '3:30', '3:45', '4:00', '4:15', '4:30', '4:45', '5:00', '5:15', '5:30', '5:45', '6:00',
                                                                            '6:15', '6:30', '6:45', '7:00', '7:15', '7:30', '7:45', '8:00', 'All Day'])), default='',
                                                                            represent=lambda v, r: '' if v is None else v),
                Field('note', 'text', required=False, default='', represent=lambda v, r: '' if v is None else v)
               )

db.medicines.id.readable = False
db.events.id.readable = False