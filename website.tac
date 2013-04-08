# _*_ coding: UTF8 _*_
# Copyright (C) 2010-2012 Team Gaspacho (see README for all contributors)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


#/usr/bin/twistd -noy website.tac

from sys import exit
from twisted.application import internet, service
from twisted.web import server, resource, static, server
from twisted.internet import ssl #, reactor
from twisted.web.error import NoResource, Error
from twisted.python import components

from zope.interface import Interface
#from elixir import *
#from sqlalchemy.exc import OperationalError

import pwd, grp
from fnmatch import fnmatch

from socket import gethostbyaddr, herror
from os.path import join, isfile
import os
#from wpkgjs.util import is_object, get_object_by_id
#from wpkgjs.valid import valid

#from wpkgjs import (get_groups, get_templates, add_group, 
#        get_users, get_user, del_group, del_template, add_template, 
#        add_user, del_user, get_categories, get_choices, 
#        get_softwares, get_oses, load, commit_database, initialize_database,
#        rollback_database)

from wpkgjs.config import (store_dir_apply, serv_port, serv_tls, serv_crt, 
        serv_key, serv_static_path, admin_pam_user, auth_type, wpkgjs_login,
        wpkgjs_password, default_serv_lang, default_separator,
        force_resolve_dns_name)

import wpkgjs.packages
import wpkgjs.machines
import wpkgjs.profiles

try:
    import json
except:
    #for python 2.5
    import simplejson as json

if auth_type == 'PAM':
    import PAM

    


class IPreferences(Interface):
    pass

class Preferences(components.Adapter):
    __implements__ = IPreferences

    def __init__(self, original):
        self.authentified = 'no'
        self.bad_auth = '0'
        self.user = ""
        self.level = ''
        components.Adapter.__init__(self,original)

components.registerAdapter(Preferences, server.Session, IPreferences)

class Page(resource.Resource):
    """
        abstract page
    """
    isLeaf = True
    allowed_for_manager = False
    def __init__(self, save_database=False):
        #when simply query, don't save database
        self.save_database = save_database

    ## authentification
    def close_session(self, request):
        prefs = request.getSession(IPreferences)
        prefs.authentified = 'no'
#        prefs.bad_auth = '0'
        prefs.user = ''
        prefs.lang = ''
        prefs.level = ''

    def require_auth(self, request):
        prefs = request.getSession(IPreferences)
        return self.send_json(auth=False)

    def render(self, request):
        # is the session authentified ? authentified = yes or no
        prefs = request.getSession(IPreferences)
        if hasattr(prefs, 'authentified'):
            if prefs.authentified != 'yes':
                print "NON authentified", prefs.authentified , request.getSession().uid
                return self.require_auth(request)
            else:
                print "authentified", prefs.authentified , request.getSession().uid
                try:
                    #if prefs.level == 'manager' and \
                    #                self.allowed_for_manager == False:
                    #    return self.send_json(error='Not allowed for a manager')
                    return self.render_page(request)
                except Exception, e:
                    import traceback
                    traceback.print_exc()
                    return self.send_json(error=str(e))
        return self.require_auth(request)

    ## getters
    def get_data_from_request(self, request, arg, load_json=False, 
                    checkbox=False, object_type=None, required=True):
        """
        Return arg from request. If object_type specified, return object
        request is return by twister
        arg: name of argument return by user
        load_json: if value is a json type
        checkbox: if value is a checkbox boolean
        object_type: if value is an id of an object, specify the object type
                     to return directly the object
        required: if True, return a ValueError if argument is not specify by
                  user or is no object has this id
        """
        if checkbox and object_type != None:
            raise Exception('If checkbox, object_type must not be set')
        #if arg is in the request
        if request.args.has_key(arg):
            try:
                #return value
                if object_type == None:
                    ret = request.args[arg][0]
                    if load_json:
                        #load json value
                        return json.loads(ret)
                    elif checkbox:
                        #if checkbox, return 'on' for True
                        if ret == 'on':
                            return True
                        else:
                            raise Exception('Are you should %s is a checkbox type ?' % arg)
                    else:
                        return ret
                #return object
                else:
                    obj = get_object_by_id(request.args[arg][0], object_type)
                    if required and obj == None:
                        raise ValueError("value %s required"% str(arg))
                    return obj
            except Exception, e:
                raise ValueError(str(e))
        else:
            if checkbox:
                #if checkbox, not value is return for False
                return False
            elif required:
                raise ValueError("value %s required"% str(arg))
            else:
                return None

 
    def send_json(self, ret=None, error=None, message=None, auth=True, treenode=False):
        """
        Convert answer to json for extjs
        error: if return an error, error must be the error message
        message: if a message must be display (not an error message)
        """
        #print ret
        #if authentified session
        if auth == True:
            buf = {'success': True, 'data': '', 'authentification': True}
            if error == None:
                if self.save_database:
                    try:
                        commit_database()
                    except Exception, e:
                        # FIXME traceback is bad in production mode
                        import traceback
                        traceback.print_exc()
                        error = "error while saving database"
                if ret != None:
                    if treenode == True:
                        #if treenode
                        buf = ret
                    else:
                        buf['data'] = ret
                if message != None:
                    buf['message'] = message
            if error != None:
                if self.save_database:
                    rollback_database()
                buf = {'success': False, 'data': '', 'message': error}
        #if session is not authentified
        else:
            buf = {'success': True, 'data': '', 'authentification': False}
            if error != None:
                buf['success'] = False
                buf['message'] = error
        #print buf        
        return json.dumps(buf)

class Login(Page):
    def render(self, request):
        try:
            user = self.get_data_from_request(request=request, arg='login')
            password = self.get_data_from_request(request=request, arg='password')
            #lang = self.get_data_from_request(request=request, arg='countryCode')
            #FIXME: default langage!
            lang = 'fr'#default_serv_lang
        except Exception, e:
            return self.send_json(error=str(e))

        #if auth_type == 'PAM':
        #    if admin_pam_user != None and user in admin_pam_user:
        #        luser = user
        #        level = 'admin'
        #    else:
        #        luser = get_user(unicode(user))
        #        if luser != None:
        #            level = 'manager'
        #        else:
        #            return self.send_json(error='User not allowed', auth=False)

        prefs = request.getSession(IPreferences)

        if auth_type == 'PAM':
            # PAM stuff
            def pam_conv(auth, query_list, userData):
                #pam password authentification utility
                resp = []
                for i in range(len(query_list)):
                    query, type = query_list[i]
                    #print query, type
                    if type == PAM.PAM_PROMPT_ECHO_ON or type == PAM.PAM_PROMPT_ECHO_OFF:
                        resp.append((password, 0))
                    elif type == PAM.PAM_PROMPT_ERROR_MSG or type == PAM.PAM_PROMPT_TEXT_INFO:
                        resp.append(('', 0))
                    else:
                        return None
                return resp

            auth = PAM.pam()
            auth.start('WPKGjs')
            auth.set_item(PAM.PAM_USER, user)
            auth.set_item(PAM.PAM_CONV, pam_conv)
            try:
                #print "auth.authenticate()"
                auth.authenticate()
                auth.acct_mgmt()
                prefs.user = user
                #prefs.level = level
                prefs.authentified = 'yes'
                prefs.lang = lang
                prefs.display_platforms = False
                return self.send_json(ret={'level': 'admin'}, auth=True,message='ok')
            except PAM.error, resp:
                #print 'Go away! (%s)' % resp
                prefs.authentified = 'no'
                return self.send_json(error='Login failed', auth=False)
            except:
                prefs.authentified = 'no'
                return self.send_json(error='Login failed', auth=False)
                #print 'Internal error'
				
        else:
            #internal
            if wpkgjs_login == None or password == None:
                return self.send_json(error='Login failed', auth=False)

            if user == wpkgjs_login and password == wpkgjs_password:
                #request.getSession().touch()
                prefs.user = user
                prefs.level = 'admin'
                prefs.authentified = 'yes'
                prefs.lang = lang
                prefs.display_platforms = False
                return self.send_json(ret={'level': prefs.level}, message='Successful login', auth=True)
            else:
                prefs.authentified = 'no'
                return self.send_json(error='Login failed', auth=False)


class Logout(Page):
    allowed_for_manager = True
    def render_page(self, request):
        self.close_session(request)
        return self.send_json(message="session closed", auth=False)

class GetPackages(Page):
    def render_page(self, request):
        ret = None
        #groupe= request.postpath[0]

        #grp, user = self.get_object_by_webid(request, required=False)
        ret = []
        print "getpackages"
        #if is_object(grp, 'group'):
        if len(request.postpath) ==0:
            for filename, uid, name in wpkgjs.packages.get_packages():
                #print   filename, uid, name 
                ret.append({"filename": filename, "uid": uid, 'name': name,'checked':False})
        else:
            prof = wpkgjs.profiles.get_profile(request.postpath[0]) 
            packages = wpkgjs.packages.get_packages()
            print prof
            print request.postpath[0]
            for filename, uid, name in packages:
                #print   filename, uid, name 
                if uid in prof:
                    print uid
                    ret.append({"filename": filename, "uid": uid, 'name': name,'checked':True})
                else:
                    ret.append({"filename": filename, "uid": uid, 'name': name,'checked':False})
        return self.send_json(ret)


class GetGroupesESU(Page):
    def render_page(self, request):
        print "GetGroupesESU"
    	ret = None
        #grp, user = self.get_object_by_webid(request, required=False)
        ret = []
        #if is_object(grp, 'group'):
        for group in wpkgjs.machines.get_machines():
            ret.append({"grp": group})
        return self.send_json(ret)

class GetProfile(Page):
    def render_page(self, request):
        print "GetProfile" 
        print request.postpath
    	ret = None
        #grp, user = self.get_object_by_webid(request, required=False)
        ret = []
        #if is_object(grp, 'group'):
        for group in wpkgjs.machines.get_machines():
            ret.append({"grp": group})
        return self.send_json(ret)

class GetXml(Page):
    def render_page(self, request):
        print "GetXML" 
        print request.postpath
    	ret = None
        #grp, user = self.get_object_by_webid(request, required=False)
        ret = []
        #if is_object(grp, 'group'):
        if len(request.postpath) ==0:
            ret=[{'data':'rien'}]
        else:
            ret =[{'data' : wpkgjs.packages.get_content('/' + os.path.join(*request.postpath))}]
        return self.send_json(ret)
        
        
class MainPage(Page):
    def render_page(self, request):
        print "mainpage"
        mainpagehtml="""<html><head>
            <title>WPKGjs Bienvenue</title>
            <link rel="stylesheet" type="text/css" href="extjs/resources/css/ext-all.css" />
            <link rel="stylesheet" type="text/css" href="extjs/examples/ux/css/CheckHeader.css">
            <script src="extjs/ext-all.js" type="text/javascript"></script>
            <script src="app.js" type="text/javascript"></script>            
            </head><body></body></html>
        """
        prefs = request.getSession(IPreferences)
        if prefs.authentified == 'yes':
            return mainpagehtml
        else:
            return "<html>caramba!</html>"
		
#----------------------------------- ADD -----------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------

class MainPages(resource.Resource):
    def getChild(self, name, request):
        pages = { 
            main: MainPage()
                }


        if static.isDangerous(name):
            return static.dangerousPathError
        if name in pages.keys():
            return pages[name]
        # unauthorized request
        return NoResource()

class SetPages(resource.Resource):
    def getChild(self, name, request):
        pages = { 
                }

        if static.isDangerous(name):
            return static.dangerousPathError
        if name in pages.keys():
            return pages[name]
        # unauthorized request
        return NoResource()

class GetPages(resource.Resource):
    def getChild(self, name, request):
        pages = {
		    'packages': GetPackages(),
		    'groupesesu': GetGroupesESU(),
            'profile': GetProfile(),
            'xmlcontent': GetXml()
                
                }
        if static.isDangerous(name):
            return static.dangerousPathError
        if name in pages.keys():
            return pages[name]
        # unauthorized request
        return NoResource()

class LogPage(resource.Resource):
    def getChild(self, name, request):
        pages = {'in': Login(),
                'out': Logout(),
        }
        if static.isDangerous(name):
            return static.dangerousPathError
        if name in pages.keys():
            return pages[name]
        # unauthorized request
        return NoResource()




index_file = join(serv_static_path, 'index.html')
if not isfile(index_file):
    print 'Unable to find %s, please configure serv_static_path in wpkgjs.conf' % index_file
    exit(1)
root = static.File(serv_static_path)
root.putChild("get", GetPages())
root.putChild("set", SetPages())
root.putChild("log", LogPage())
root.putChild("main", MainPage())

site = server.Site(root)

application = service.Application("WPKGjs")

if serv_tls == "disabled":
    serv = internet.TCPServer(serv_port, site)
else:
    sslContext = ssl.DefaultOpenSSLContextFactory(
        serv_key,
        serv_crt,
    )
    serv = internet.SSLServer(serv_port, site, contextFactory = sslContext)
serv.setServiceParent(application)
# vim: ts=4 sw=4 expandtab
