# Copyright (C) 2009-2012 Team Gaspacho (see README fr all contributors)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from configobj import ConfigObj
from formencode.validators import StringBoolean
from os.path import isfile

if isfile("wpkgjs.conf"):
    conffile = "wpkgjs.conf"
else:
    conffile = "/etc/eole/wpkgjs.conf"
    if not isfile(conffile):
        raise Exception("Unable to find configuration file")
try:
    config = ConfigObj(conffile)
except Exception, err:
    print "ERROR: --- unable to load configuration file ---"
    print err
    sys.exit(1)

def string_to_bool(value):
    return StringBoolean().to_python(value)

default_serv_lang = config.get('default_serv_lang', 'fr')

### Language order if not translate in selected language
ordered_lang = config.get('ordered_lang', ['en', 'fr'])

### Directories
store_dir_apply = config.get('store_dir_apply', '/var/lib/wpkgjs/apply')
serv_static_path = config.get('serv_static_path', '/var/www/html/wpkgjs/')

serv_port = int(config.get('serv_port', '8181'))
serv_tls = config.get('serv_tls', 'disabled')
serv_crt = config.get('serv_crt', '')
serv_key = config.get('serv_key', '')
multi_site = string_to_bool(config.get('multi_site', False))
force_resolve_dns_name = string_to_bool(config.get('force_resolve_dns_name',
            True))


admin_pam_user = config.get('admin_pam_user', ['root', 'wpkgjs'])

auth_type = config.get('auth_type', 'internal')

wpkgjs_login = config.get('wpkgjs_login', 'admin')
wpkgjs_password = config.get('wpkgjs_password', 'admin')

#loglevel must be in 'critical', 'error', 'warning', 'info' or 'debug'
log_level = config.get('log_level', 'error')
log_file = config.get('log_file', '/var/log/wpkgjs/error.log')

database_version = u'0.91'

default_separator = '-'

required_descr = ['name', 'version', 'database', 'os', 'software', 'packages',
                    'categories']
required_os = ['name', 'version']
required_software = ['name', 'version']
required_category = ['names', 'tags']
required_names = ['lang', 'label']
required_tag = ['names', 'rules']
#FIXME: name ou names ???
required_rule = ["names", "type", "variables"]
optional_rule = ['defaultstate', 'display', 'defaultvalue', 'options',
                         'comments']
required_variable = ["name", "level", "type", "extension", "value_off", "path"]
optional_variable = ["value_on", "info", "comment"]
required_group = ['name', 'comment', 'level', 'installpkg', 'lang', 'computers']
required_template = ['name', 'comment']
required_user = ['name', 'type', 'comment']
required_site = ['name', 'comment', 'cn']
required_choice = ['state', 'value']
required_path = ['name', 'extension', 'info']
# vim: ts=4 sw=4 expandtab
