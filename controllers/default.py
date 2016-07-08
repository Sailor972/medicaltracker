from plugin_timezone import fast_tz_detector

# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def detect_timezone():
    tz = fast_tz_detector()
    return dict(tz=tz)

@auth.requires_login()
def manage_events():
    if 'new' in request.args:
        redirect(URL('new_event'))
    elif 'edit' in request.args:
        redirect(URL('edit_event', args=[request.args(2)]))
    form = SQLFORM.grid(db.events, searchable=True, editable=True, deletable=True, details=False,
                             create=True, paginate=20, maxtextlength=60, fields=[db.events.event_time,
                                                                                 db.events.event_type,
                                                                                 db.events.event_level,
                                                                                 db.events.bristol_scale,
                                                                                 db.events.systolic,
                                                                                 db.events.diastolic,
                                                                                 db.events.pulse,
                                                                                 db.events.medicine,
                                                                                 db.events.dosage,
                                                                                 db.events.lbs,
                                                                                 db.events.duration,
                                                                                 db.events.note],
                             orderby=~db.events.event_time)
    return dict(form=form)


@auth.requires_login()
def new_event():
    db.events.systolic.show_if = (db.events.event_type == "Blood Pressure")
    db.events.diastolic.show_if = (db.events.event_type == "Blood Pressure")
    db.events.pulse.show_if = (db.events.event_type == "Blood Pressure")
    db.events.medicine.show_if = (db.events.event_type == "Medicine")
    db.events.dosage.show_if = (db.events.event_type == "Medicine")
    db.events.event_level.show_if = (db.events.event_type.belongs("Mood", "Headache", "Nausea", "Pain"))
    db.events.duration.show_if = (db.events.event_type.belongs("Headache", "Mood", "Nausea", "Pain", "Sleep Duration"))
    db.events.bristol_scale.show_if = (db.events.event_type == "Stool")
    db.events.lbs.show_if = (db.events.event_type == "Weight")
    form = SQLFORM(db.events, fields=["event_time",
                                      "event_type",
                                      "event_level",
                                      "bristol_scale",
                                      "systolic",
                                      "diastolic",
                                      "pulse",
                                      "medicine",
                                      "dosage",
                                      "lbs",
                                      "duration",
                                      "note"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_events'))
    return dict(form=form)


@auth.requires_login()
def edit_event():
    this_event = db.events(db.events.id==request.args(0,cast=int))
    db.events.systolic.show_if = (db.events.event_type == "Blood Pressure")
    db.events.diastolic.show_if = (db.events.event_type == "Blood Pressure")
    db.events.pulse.show_if = (db.events.event_type == "Blood Pressure")
    db.events.medicine.show_if = (db.events.event_type == "Medicine")
    db.events.dosage.show_if = (db.events.event_type == "Medicine")
    db.events.event_level.show_if = (db.events.event_type.belongs("Mood", "Headache", "Nausea", "Pain"))
    db.events.duration.show_if = (db.events.event_type.belongs("Headache", "Mood", "Nausea", "Pain", "Sleep Duration"))
    db.events.bristol_scale.show_if = (db.events.event_type == "Stool")
    db.events.lbs.show_if = (db.events.event_type == "Weight")
    form=SQLFORM(db.events, this_event, fields=["event_time",
                                                "event_type",
                                                "event_level",
                                                "bristol_scale",
                                                "systolic",
                                                "diastolic",
                                                "pulse",
                                                "medicine",
                                                "dosage",
                                                "lbs",
                                                "duration",
                                                "note"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_events'))
    return dict(form=form)


@auth.requires_login()
def manage_medicines():
    if 'new' in request.args:
        redirect(URL('new_medicine'))
    elif 'edit' in request.args:
        redirect(URL('edit_medicine', args=[request.args(2)]))
    form = SQLFORM.grid(db.medicines, searchable=True, editable=True, deletable=True, details=False,
                             create=True, paginate=20, maxtextlength=60, fields=[db.medicines.medicine_name],
                             orderby=db.medicines.medicine_name)
    return dict(form=form)


@auth.requires_login()
def new_medicine():
    form = SQLFORM(db.medicines, fields=["medicine_name"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_medicines'))
    return dict(form=form)


@auth.requires_login()
def edit_medicine():
    this_medicine = db.medicines(db.medicines.id==request.args(0,cast=int))
    form=SQLFORM(db.medicines, this_medicine, fields=["medicine_name"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_medicines'))
    return dict(form=form)