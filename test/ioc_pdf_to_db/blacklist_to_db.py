#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : blacklist_to_db.py
# Author    : wuqingfeng@

import os
import fnmatch
import mysql.connector
from mysql.connector import errorcode
from iocp import Parser
from iocp.Output import OutputHandler

mysql_config = {
    'user': 'ant',
    'password': '123456',
    'host': '10.5.0.144',
    'database': 'thinkcmf'
} 

cnx = cur = None
try:
    cnx = mysql.connector.connect(**mysql_config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cur = cnx.cursor()

def ip2int(x):
    try:
        intip = 0
        for j,i in enumerate(x.split('.')[::-1]):
            intip = intip + 256**j*int(i)
        return intip
    except Exception,e:
        return 0


class CParser(Parser.Parser):
    def __init__(self, *args, **kwargs):
        super(CParser, self).__init__(*args, **kwargs)

    def parse(self, path):
        try:
            if path.startswith('http://') or path.startswith('https://'):
                if 'requests' not in IMPORTS:
                    e = 'HTTP library not found: requests'
                    raise ImportError(e)
                headers = { 'User-Agent': 'Mozilla/5.0 Gecko Firefox' }
                r = requests.get(path, headers=headers)
                r.raise_for_status()
                f = StringIO(r.content)
                self.parser_func(f, path)
                return
            elif os.path.isfile(path):
                with open(path, 'rb') as f:
                    self.parser_func(f, path)
                return
            elif os.path.isdir(path):
                for walk_root, walk_dirs, walk_files in os.walk(path):
                    for walk_file in fnmatch.filter(walk_files, self.ext_filter):
                        fpath = os.path.join(walk_root, walk_file)
                        try:
                            with open(fpath, 'rb') as f:
                                self.parser_func(f, fpath)
                        except:
                            print fpath
                            continue
                return

            e = 'File path is not a file, directory or URL: %s' % (path)
            raise IOError(e)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.handler.print_error(path, e)

class OutputHandler_custom(OutputHandler):
    def print_match(self, fpath, page, name, match):
        # print fpath
        # if name in ['Host', 'IP']:
        #     print name, match
        if name == 'Host':
            host_list = match.split('.')
            if len(host_list) > 2:
                match = '.'.join(host_list[-2:])
            domain = (match,)
            stmt_select = 'SELECT EXISTS(SELECT * FROM cmf_black_domainlist WHERE domain = %s)'
            cur.execute(stmt_select, domain)
            isexists = cur.fetchone()[0]
            if not isexists:
                stmt_insert = 'INSERT INTO cmf_black_domainlist (domain) VALUES (%s)'
                # print stmt_insert, domain
                cur.execute(stmt_insert, domain)
                cnx.commit()
        elif name == 'IP':
            ipint = ip2int(match)
            ip = (match, ipint)
            stmt_select = 'SELECT EXISTS(SELECT * FROM cmf_black_iplist WHERE ip = %s and ip_raw = %s)'
            cur.execute(stmt_select, ip)
            isexists = cur.fetchone()[0]
            if not isexists:
                stmt_insert = 'INSERT INTO cmf_black_iplist (ip, ip_raw) VALUES (%s, %s)'
                # print stmt_insert, ip
                cur.execute(stmt_insert, ip)
                cnx.commit()


if __name__ == '__main__':
    parser = CParser(output_handler=OutputHandler_custom())
    # print 2008
    # parser.parse('/opt/workplace/APTnotes/2008/')
    # print 2009
    # parser.parse('/opt/workplace/APTnotes/2009/')
    # print 2010
    # parser.parse('/opt/workplace/APTnotes/2010/')
    print 2011
    parser.parse('/opt/workplace/APTnotes/2011/')
    print 2012
    parser.parse('/opt/workplace/APTnotes/2012/')
    print 2013
    parser.parse('/opt/workplace/APTnotes/2013/')
    print 2014
    parser.parse('/opt/workplace/APTnotes/2014/')
    print 2015
    parser.parse('/opt/workplace/APTnotes/2015/')
    if cur:
        cur.close()
    if cnx:
        cnx.close()

                
