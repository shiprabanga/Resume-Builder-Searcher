# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    c=auth.user_id
    response.flash = T("Welcome to web2py!")
    return locals()
    #return dict(message=T('Hello World'))

def resume_display():
	c=request.args[0]
	cont=db(db.auth_user.id==c).select(db.auth_user.ALL)
	pers=db(db.Personal.pid==c).select(db.Personal.ALL)
	edu=db(db.Education.eid==c).select(db.Education.ALL)
	mer=db(db.Merit.mid==c).select(db.Merit.ALL)
	exp=db(db.Experience.exid==c).select(db.Experience.ALL)
	return locals()

import re
def resume_search():
	c=[]
	i_n=[]
	flag=0
	form=SQLFORM.factory(
		Field('search_by',requires = IS_IN_SET(['Firstname','Lastname','Email'])),
		Field('search_item'))
	acc=db(db.auth_user.id>0).select(db.auth_user.ALL)

	if form.process().accepted:
		search_by=form.vars.search_by
		search_item=form.vars.search_item

		if search_by=="Firstname":
			for j in acc:
				if re.search(search_item,j['first_name'],re.IGNORECASE)!=None:
					flag=1
					c.append(j['first_name'])
					i_n.append(j['id'])
			if flag!=1:
				c.append("Not Found")
				i_n.append("")
		if search_by=="Lastname":
			for j in acc:
				if re.search(search_item,j['last_name'],re.IGNORECASE)!=None:
					flag=1
					c.append(j['last_name'])
					i_n.append(j['id'])
			if flag!=1:
				c.append("Not Found")
				i_n.append("")
		if search_by=="Email":
			for j in acc:
				if re.search(search_item,j['email'],re.IGNORECASE)!=None:
					flag=1
					c.append(j['email'])
					i_n.append(j['id'])
			if flag!=1:
				c.append("Not Found")
				i_n.append("")

	return locals()

@auth.requires_login()
def Personal():
	c=auth.user_id
	db.Personal.pid.default=c
	db.Personal.pid.readable=True
	db.Personal.pid.writable=False
	form=SQLFORM(db.Personal)
	if form.process().accepted:
		response.flash='form accepted'
	elif form.errors:
		response.flash = 'form has errors'
	return dict(form=form)
def Education():
	c=auth.user_id
	db.Education.eid.default=c
	db.Education.eid.readable=True
	db.Education.eid.writable=False
	form=SQLFORM(db.Education)
	if form.process().accepted:
		response.flash='form accepted'
	elif form.errors:
		response.flash='form has errors'
	return dict(form=form)
def Merit():	
	c=auth.user_id
	db.Merit.mid.default=c
	db.Merit.mid.readable=True
	db.Merit.mid.writable=False
	form=SQLFORM(db.Merit)
	if form.process().accepted:
		response.flash='form accepted'
	elif form.errors:
		response.flash='form has errors'
	return dict(form=form)

def Experience():
	c=auth.user_id
	db.Experience.exid.default=c
	db.Experience.exid.readable=True
	db.Experience.exid.writable=False
	form=SQLFORM(db.Experience)
	if form.process().accepted:
		response.flash='form accepted'
	elif form.errors:
		response.flash='form has errors'
	return dict(form=form)

def create():
	return locals()

def prin():
	c=auth.user_id
	cont=db(db.auth_user.id==c).select(db.auth_user.ALL)
	pers=db(db.Personal.pid==c).select(db.Personal.ALL)
	edu=db(db.Education.eid==c).select(db.Education.ALL)
	mer=db(db.Merit.mid==c).select(db.Merit.ALL)
	exp=db(db.Experience.exid==c).select(db.Experience.ALL)
	return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


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


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
