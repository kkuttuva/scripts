#!/usr/bin/env python

import argparse
import datetime
import ftplib
import getpass
import os 
import subprocess

def upload_ftp(input_f, output_d, host, username, password):
    from ftplib import FTP
    ftp = FTP(host)
    ftp.login(username, password)
    ftp.cwd(output_d)
    ftp.storlines('STOR ' + input_f, open(input_f, 'r'))
    ftp.quit()
    print 'Upload done.'

def backup_ws(output_d, host, username, password):
    path = os.getcwd()
    prefix = path.split('/', 5)[4] + "_"
    from datetime import datetime
    fname = prefix + datetime.now().strftime("%m_%d_%H_%M_%S") + '.txt'
    with open(fname, 'w') as output_f:
        p1 = subprocess.Popen(['git', 'diff'], stdout = output_f)
    p1.wait()
    output_f.close()
    upload_ftp(fname, output_d, host, username, password)

def main():
    parser = argparse.ArgumentParser(description='Upload git workspace.')
    parser.add_argument('host', metavar='IP', nargs=1, help='host IP')
    parser.add_argument('username', metavar='username', nargs=1, help='username')
    parser.add_argument('rdir', metavar='remotedir', nargs=1, help='remote directory')
    args = parser.parse_args()
    password=getpass.getpass()
    backup_ws(args.rdir[0], args.host[0], args.username[0], password)

main()
