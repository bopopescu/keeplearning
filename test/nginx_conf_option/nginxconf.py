#!/usr/bin/env python
# -*- coding: utf-8 -*-



from optparse import OptionParser
import sys, os
import json

ident_char = "    "

components = ['krosa', 'tembin', 'omais', "higos", "etau",
    "hato", "hagibis", "bailu", "choi_wan", "atsani"
]

ssl =  [
    ('ssl', 'on'),
    ('ssl_certificate', '/opt/disk2/var/serverconfig/server.cert'),
    ('ssl_certificate_key', '/opt/disk2/var/serverconfig/server.key'),
]



class Upstream(object):

    def __init__(self, **kwargs):
        self.servers = kwargs['servers']
        self.name = kwargs['name']
        # load balance options, currentlly empty
        self.balance_opts = ''

    def dumps(self, indent=''):
        string = ""
        idt = indent + ident_char
        for server in self.servers:
            string += "%sserver %s%s;\n" % (idt, server, self.balance_opts)
        data = "%supstream %s {\n%s%s}\n\n" % (indent, self.name, string, indent)
        return data


    def __str__(self):
        return self.dumps()


class Location(object):

    def __init__(self, location, **kwargs):
        self.location = location
        self.parameters = kwargs.get('parameters')

    def dumps(self, indent=''):
        string = ""
        idt = indent + ident_char
        for k, v in self.parameters:
            string += "%s%s %s;\n" % (idt, k, v)
        data = "%slocation %s {\n%s%s}\n\n" % (indent, self.location, string, indent)
        return data
        

class Server(object):
    def __init__(self, **kwargs):
        self.parameters = kwargs.get('parameters')
        self.directives = []

    def add_directive(self, dir):
        self.directives.append(dir)

    def dumps(self, ident=''):
        string = ''
        # parameters
        idt = ident + ident_char
        for k, v in self.parameters:
            string += "%s%s %s;\n" % (idt, k, v)
        # directive
        for directvie in self.directives:
            string += directvie.dumps(idt)
        data = "server {\n%s}\n\n" % (string)
        return data


class UpstreamCollection(object):

    def __init__(self, basefile='/opt/disk2/var/serverconfig/upstream.conf', 
            extentfolder='/opt/disk2/var/serverconfig/upstream.d/',
            **kwargs):
        self.base = []
        self.extention = {}
        self.basefile = basefile
        self.extentfolder = extentfolder
        os.system("mkdir -p %s" % '/opt/disk2/var/serverconfig/')
        os.system("mkdir -p %s" % extentfolder)
        

    def add_base(self, upstream):
        self.base.append(upstream)

    def add_extention(self, upstream, dep_id):
        self.extention.setdefault(dep_id, [])
        self.extention[dep_id].append(upstream)

    def dumps(self, indent=''):
        string = ''
        idt = indent + ident_char
        for up in self.base:
            string += up.dumps(idt)
        return string

    def dumps_ex(self, indent='',):
        idt = indent + ident_char
        for dep_id, exs in self.extention.items():
            string = ''
            for each in exs:
                string += each.dumps()
            # write to extention file
            path = "%s%s.conf" % (self.extentfolder,  dep_id)
            f = open(path, "w+")
            f.write(string)
            f.close()

    def dumps_file(self, indent=''):
        string = self.dumps()
        if string:
            f = open(self.basefile, "w+")
            f.write(string)
            f.close()
        # dump extentions
        self.dumps_ex()

class Proxy(object):

    def __init__(self, project, basefile='/opt/disk2/var/serverconfig/%s.conf',
            extension_path='/opt/disk2/var/serverconfig/%s_api/', **kwargs):
        self.project = project
        self.servers = []
        self.location_ex = {}
        self.basefile = basefile % project
        self.extentfolder = extension_path % project 
        os.system("mkdir -p %s" % '/opt/disk2/var/serverconfig/')
        os.system("mkdir -p %s" % self.extentfolder)
        

    def add_server(self, server):
        self.servers.append(server)

    def add_extention(self, dep_id, location):
        self.location_ex.setdefault(dep_id, [])
        self.location_ex[dep_id].append(location)

    def dumps(self, intent=''):
        string = ''
        for server in self.servers:
            string += server.dumps()
        return string

    def dumps_file(self, intent=''):
        string = ''
        # import pdb
        # pdb.set_trace()
        for server in self.servers:
            string += server.dumps()
        if string:
            basic = self.basefile
            f = open(basic, "w")
            f.write(string)
            f.close()
        # it is not that easy to dump all the exs. relationship is complicated 
        for dep_id, ex in self.location_ex.items():
            string = ''
            for each in ex:
                string += each.dumps()
                # write to extention file
            path = "%s%s.conf" % (self.extentfolder, dep_id)
            f = open(path, "w")
            f.write(string)
            f.close()


# -b --basic  portal.com pamc.com api.com  "a;b"  "c;d" "e;f" "g;h" "i;j"

#  cmd  upstream   -u --upstream "a;b" -d --did "rcm_saas"

#  cmd  server -l --location "/api/krosa/rcm_saas;/web/manager" -u --upstream "rcm_saas"

# if __name__ == '__main__':
#     optparser = OptionParser()
#     optparser.add_option('-p', '--path', dest='path', help='path of yaml file', default='config.yaml')
#     optparser.add_option('-s', '--set', dest='set_config', default=None, help='set config, example: redis.host=127.0.0.1;')
#     optparser.add_option('-d', '--delete', dest='del_config', default=None, help='del config, example: redis.host;')
#     optparser.add_option('-r', '--reset', dest='reset_config', default=None, help='reset config, json, example: {"redis":{"host":"127.0.0.1", "port":6379}}')

#     options, args = optparser.parse_args()

def basic_upstream_setup(ip_list):
    # ours components, the order is important
    if len(ip_list) != len(components):
        print "upstreams count not correct"
        sys.exit(1)

    upc = UpstreamCollection()
    for component in components:
        index = components.index(component)
        servers = ip_list[index].split(";")
        up = Upstream(name="%s_api" % component, servers=servers)
        upc.add_base(up)
    # dump it to config files
    print upc.dumps()
    upc.dumps_file()

def create_server(project='krosa', server_name='example.com', listen=443, basic=False):
    server_param = [
        ('listen', listen),
        ('server_name', server_name),
        ('charset', 'utf-8'),
        ('root', '/opt/disk2/var/www/%s/' % project),
        ('error_page 500', '/%s/views/initcdr/500.html' % project),
        ('error_page 400', '/%s/views/initcdr/404.html' % project),
        ('include', "%s_api/*.conf" % project)
    ]
    if listen == 443:
        server_param.extend(ssl)
    server = Server(parameters=server_param)
    # add root localtions
    loc_param = [
        ('expires', '5d'),
        ('root', '/opt/disk2/var/www/%s' % project),
    ]
    root = Location("/", parameters=loc_param)
    favicon = Location(r"^(.*)\.favicon.ico$", parameters=[('log_not_found', 'off')])
    svn = Location(r"^~ /\.svn(.*)$", parameters=[('return', '404')])
    server.add_directive(root)
    server.add_directive(favicon)
    server.add_directive(svn)
    # add basic locations
    for component in components:
        loc_param = [
            ('proxy_pass', "http://%s_api" % component),
            ('proxy_set_header', 'Host $host'),
            ('proxy_set_header', 'X-Real-IP $remote_addr'),
            ('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
            ('proxy_redirect', 'off'),
        ]
        l = Location("^~ /api/%s/%s" % (project, component), parameters=loc_param)
        server.add_directive(l)
    return server




def basic_proxy_setup(krosa_name, tembin_name, nuri_name, ip_list):

    # create krosa proxy    
    krosa = Proxy('krosa')
    https = create_server(project='krosa', server_name=krosa_name, listen=443)
    krosa.add_server(https)
    # http server rewrite to https
    # krosa special 
    http = Server()
    # create tembin proxy
    tembin = Proxy('tembin')
    https = create_server(project='tembin', server_name=tembin_name, listen=443)
    tembin.add_server(https)
    # create nuri proxty
    nuri = Proxy('nuri')
    https = create_server(project='nuri', server_name=nuri_name, listen=80)
    nuri.add_server(https)
    # create www-nginx.conf file
    krosa.dumps_file()
    tembin.dumps_file()
    nuri.dumps_file()

    # extra rcm_server setup
    rcm_saas_krosa =  Proxy(project='krosa')
    loc_param = [
        ('proxy_pass', "http://rcm_saas_api"),
        ('proxy_set_header', 'Host $host'),
        ('proxy_set_header', 'X-Real-IP $remote_addr'),
        ('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
        ('proxy_redirect', 'off'),
    ]   
    loc = Location("^~ /api/krosa/rcm_saas", parameters=loc_param)
    rcm_saas_krosa.add_extention(loc, "rcm_saas")

    rcm_saas_nuri =  Proxy(project='nuri')
    loc_param = [
        ('proxy_pass', "http://rcm_saas_api"),
        ('proxy_set_header', 'Host $host'),
        ('proxy_set_header', 'X-Real-IP $remote_addr'),
        ('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
        ('proxy_redirect', 'off'),
    ]   
    loc = Location("^~ /api/nuri/rcm_saas", parameters=loc_param)
    rcm_saas_nuri.add_extention(loc, "rcm_saas")

    rcm_saas_krosa.dumps_file()
    rcm_saas_nuri.dumps_file()


def ex_up_setup(dep_id, upstream_conf):
    # upstream_conf must be json format
    upc = UpstreamCollection()
    for k, v in upstream_conf.items():
        up = Upstream(name=k, servers=v)
        upc.add_extention(up, dep_id)
    upc.dumps_file()

def ex_server_setup(dep_id, api_location, krosa_location):
    krosa = Proxy(project='krosa')
    nuri = Proxy(project='nuri')
    for k, v in api_location.items():
        loc = Location(k, parameters=v)
        krosa.add_extention(dep_id, loc)
        nuri.add_extention(dep_id, loc)

    for k, v in krosa_location.items():
        loc = Location(k, parameters=v)
        krosa.add_extention(dep_id, loc)   

    krosa.dumps_file()
    nuri.dumps_file()

 


def main(options):
    options.config = json.loads(options.config)
    options.web = json.loads(options.web)
    if options.upstream:
        ex_up_setup(options.dep_id, options.config)

    if options.proxy:
        ex_server_setup(options.dep_id, options.config, options.web)


if __name__ == '__main__':
    optparser = OptionParser()
    optparser.add_option('-d', "--dep_id", dest='dep_id', help='deploy id', default=None)
    optparser.add_option('-u', '--upstream', action="store_true", dest='upstream', help='add upstream', default=False)
    optparser.add_option('-p', '--proxy', action="store_true", dest='proxy', default=False, help='add proxy')
    optparser.add_option('-c', '--config', dest='config', default="{}", help='del config')
    optparser.add_option('-w', '--web', dest='web', default="{}", help='web config, json')

    options, args = optparser.parse_args()

    main(options)

    # config = {"rcm_saas_api":["1.1.1.1","2.2.2.2"], "dmanager":["10.6.0.16"]}
    # config = {"^~ /api/krosa/rcm_saas":[["proxy_pass","http://rcm_saas_api"],["proxy_set_header","Host $host"],["proxy_set_header","X-Real-IP $remote_addr"],["proxy_set_header","X-Forwarded-For $proxy_add_x_forwarded_for"],["proxy_redirect","off"]]}
    # config = {"^~ /web/dmanager":[["proxy_pass","http://dmanager"],["proxy_set_header","Host $host"],["proxy_set_header","X-Real-IP $remote_addr"],["proxy_set_header","X-Forwarded-For $proxy_add_x_forwarded_for"],["proxy_redirect","http:// https://"]]}


    # loc_param = [
    #     ('proxy_pass', "http://rcm_saas_api"),
    #     ('proxy_set_header', 'Host $host'),
    #     ('proxy_set_header', 'X-Real-IP $remote_addr'),
    #     ('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
    #     ('proxy_redirect', 'off'),
    # ]   
    # loc = Location("^~ /api/krosa/rcm_saas", parameters=loc_param)
    # rcm_saas_krosa.add_extention(loc, "rcm_saas")

   
    # loc_param = [
    #     ('proxy_pass', "http://rcm_saas_api"),
    #     ('proxy_set_header', 'Host $host'),
    #     ('proxy_set_header', 'X-Real-IP $remote_addr'),
    #     ('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
    #     ('proxy_redirect', 'off'),
    # ]   
    # loc = Location("^~ /api/nuri/rcm_saas", parameters=loc_param)
    # rcm_saas_nuri.add_extention(loc, "rcm_saas")
