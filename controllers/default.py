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
                                                                                 db.events.lbs,
                                                                                 db.events.duration,
                                                                                 db.events.note],
                             orderby=~db.events.event_time)
    return dict(form=form)


@auth.requires_login()
def new_event():
    db.events.systolic.show_if = (db.events.event_type == 1)
    db.events.diastolic.show_if = (db.events.event_type == 1)
    db.events.pulse.show_if = (db.events.event_type == 1)
    db.events.medicine.show_if = (db.events.event_type == 3)
    db.events.event_level.show_if = (db.events.event_type.belongs(4, 2, 5, 6))
    db.events.duration.show_if = (db.events.event_type.belongs(2, 4, 5, 6, 7))
    db.events.bristol_scale.show_if = (db.events.event_type == 8)
    db.events.lbs.show_if = (db.events.event_type == 9)
    form = SQLFORM(db.events, fields=["event_time",
                                      "event_type",
                                      "event_level",
                                      "bristol_scale",
                                      "systolic",
                                      "diastolic",
                                      "pulse",
                                      "medicine",
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
    db.events.systolic.show_if = (db.events.event_type == 1)
    db.events.diastolic.show_if = (db.events.event_type == 1)
    db.events.pulse.show_if = (db.events.event_type == 1)
    db.events.medicine.show_if = (db.events.event_type == 3)
    db.events.event_level.show_if = (db.events.event_type.belongs(4, 2, 5, 6))
    db.events.duration.show_if = (db.events.event_type.belongs(2, 4, 5, 6, 7))
    db.events.bristol_scale.show_if = (db.events.event_type == 8)
    db.events.lbs.show_if = (db.events.event_type == 9)
    form=SQLFORM(db.events, this_event, fields=["event_time",
                                                "event_type",
                                                "event_level",
                                                "bristol_scale",
                                                "systolic",
                                                "diastolic",
                                                "pulse",
                                                "medicine",
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
                             create=True, paginate=20, maxtextlength=60, fields=[db.medicines.medicine,
                                                                                 db.medicines.dosage],
                             orderby=db.medicines.medicine)
    return dict(form=form)


@auth.requires_login()
def new_medicine():
    form = SQLFORM(db.medicines, fields=["medicine",
                                         "dosage"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_medicines'))
    return dict(form=form)


@auth.requires_login()
def edit_medicine():
    this_medicine = db.medicines(db.medicines.id==request.args(0,cast=int))
    form=SQLFORM(db.medicines, this_medicine, fields=["medicine",
                                                      "dosage"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_medicines'))
    return dict(form=form)


@auth.requires_login()
def manage_bristol_scales():
    if 'new' in request.args:
        redirect(URL('new_bristol_scale'))
    elif 'edit' in request.args:
        redirect(URL('edit_bristol_scale', args=[request.args(2)]))
    form = SQLFORM.grid(db.bristol_scales, searchable=True, editable=True, deletable=True, details=False,
                             create=True, paginate=20, maxtextlength=60, fields=[db.bristol_scales.bristol_scale],
                             orderby=db.bristol_scales.bristol_scale)
    return dict(form=form)


@auth.requires_login()
def new_bristol_scale():
    form = SQLFORM(db.bristol_scales, fields=["bristol_scale"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_bristol_scales'))
    return dict(form=form)


@auth.requires_login()
def edit_bristol_scale():
    this_bristol_scale = db.bristol_scales(db.bristol_scales.id==request.args(0,cast=int))
    form=SQLFORM(db.bristol_scales, this_bristol_scale, fields=["bristol_scale"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_bristol_scales'))
    return dict(form=form)

@auth.requires_login()
def manage_event_types():
    if 'new' in request.args:
        redirect(URL('new_event_type'))
    elif 'edit' in request.args:
        redirect(URL('edit_event_type', args=[request.args(2)]))
    form = SQLFORM.grid(db.event_types, searchable=True, editable=True, deletable=True, details=False,
                             create=True, paginate=20, maxtextlength=60, fields=[db.event_types.event_type],
                             orderby=db.event_types.event_type)
    return dict(form=form)


@auth.requires_login()
def new_event_type():
    form = SQLFORM(db.event_types, fields=["event_type"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_event_types'))
    return dict(form=form)


@auth.requires_login()
def edit_event_type():
    this_event_type = db.event_types(db.event_types.id==request.args(0,cast=int))
    form=SQLFORM(db.event_types, this_event_type, fields=["event_type"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_event_types'))
    return dict(form=form)

@auth.requires_login()
def manage_event_levels():
    if 'new' in request.args:
        redirect(URL('new_event_level'))
    elif 'edit' in request.args:
        redirect(URL('edit_event_level', args=[request.args(2)]))
    form = SQLFORM.grid(db.event_levels, searchable=True, editable=True, deletable=True, details=False,
                             create=True, paginate=20, maxtextlength=60, fields=[db.event_levels.event_level],
                             orderby=db.event_levels.event_level)
    return dict(form=form)


@auth.requires_login()
def new_event_level():
    form = SQLFORM(db.event_levels, fields=["event_level"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_event_levels'))
    return dict(form=form)


@auth.requires_login()
def edit_event_level():
    this_event_level = db.event_levels(db.event_levels.id==request.args(0,cast=int))
    form=SQLFORM(db.event_levels, this_event_level, fields=["event_level"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_event_levels'))
    return dict(form=form)


@auth.requires_login()
def manage_durations():
    if 'new' in request.args:
        redirect(URL('new_duration'))
    elif 'edit' in request.args:
        redirect(URL('edit_duration', args=[request.args(2)]))
    form = SQLFORM.grid(db.durations, searchable=True, editable=True, deletable=True, details=False,
                             create=True, paginate=20, maxtextlength=60, fields=[db.durations.duration],
                             orderby=db.durations.duration)
    return dict(form=form)


@auth.requires_login()
def new_duration():
    form = SQLFORM(db.durations, fields=["duration"])
    if form.process().accepted:
        response.flash = 'Thanks for filling out the form'
        redirect(URL('manage_durations'))
    return dict(form=form)


@auth.requires_login()
def edit_duration():
    this_duration = db.durations(db.durations.id==request.args(0,cast=int))
    form=SQLFORM(db.durations, this_duration, fields=["duration"])
    if form.process().accepted:
        response.flash='Thanks for editing the form'
        redirect(URL('manage_durations'))
    return dict(form=form)