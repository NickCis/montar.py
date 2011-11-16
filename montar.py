#! /usr/bin/env python

import os
import sys
import shlex
import subprocess
try:
    import cPickle as pickle
except:
    import pickle


DEFAULTPATH = "~/ip_%%ip%%"
DEFAULTREMOTEPATH = '/'
DEFAULTUSER = "root"
DEFAULTIP =  "192.168.1.1".split('.')
EXESTRING = "sshfs %s@%s:%s %s"
#UMOUNTSTRING = "sudo umount %s"
UMOUNTSTRING = "fusermount -u %s"
CONFIGPATH = os.path.expanduser("~/.montadorsshfs")

def parseArgString(argstring):
    '''Parses the syntax of the ips (see montar.py -h for further details) '''
    user = argstring.split('@')[0] if (argstring.find('@') != -1) else \
                                                                DEFAULTUSER
    ipString = argstring[0 if (argstring.find('@') == -1) else argstring.find('@'): \
                   len(argstring) if (argstring.find(':') == -1) else \
                   argstring.find(':')]
    ip = ipString.split('.')
    if (len(ip) == 4 ):
        ip =  "%s.%s.%s.%s" % tuple(ip)
    elif (len(ip) == 3 ):
        ip.insert(0, DEFAULTIP[0])
        ip =  "%s.%s.%s.%s" % tuple(ip)
    elif (len(ip) == 2 ):
        ip.insert(0, DEFAULTIP[1])
        ip.insert(0, DEFAULTIP[0])
        ip =  "%s.%s.%s.%s" % tuple(ip)
    elif (len(ip) == 1 ):
        ip.insert(0, DEFAULTIP[2])
        ip.insert(0, DEFAULTIP[1])
        ip.insert(0, DEFAULTIP[0])
        ip =  "%s.%s.%s.%s" % tuple(ip)
    else:
        ip =  "%s.%s.%s.%s" % tuple(DEFAULTIP)
    remotePath = DEFAULTREMOTEPATH if (argstring.find(':') == -1) else \
            argstring[argstring.find(':'): argstring.find('|') if \
                      (argstring.find('|') != -1) else len(argstring)]
    path = DEFAULTPATH  if (argstring.find('|') == -1 ) else \
            argstring[argstring.find('|'):]
    path =os.path.expanduser(path.replace('%%ip%%', ipString.replace('.','_')))
    return (user, ip, remotePath, path)
def mountList(mlist):
    '''Mounts the specified ips (mlists ir an array of the ips to mount)'''
    for i in range(0, len(mlist)):
        #print sys.argv[i]
        user, ip, remotepath, path = parseArgString(mlist[i])
        #print path
        #print os.path.exists(path)
        if not os.path.exists(path):
            os.mkdir(path)
        #args = shlex.split(EXESTRING % (DEFAULTUSER, ip, remotepath, path))
        args = shlex.split(EXESTRING % (user, ip, remotepath, path))
        #print args
        subprocess.call(args)
def umountList(mlist):
    '''Unmounts the specifieds ips'''
    for ind in range(0, len(mlist)):
        args = shlex.split(UMOUNTSTRING % (mlist[ind]))
        subprocess.call(args)

def loadList():
    '''Reads the saved ip list from the config file and returns it.'''
    if not os.path.isfile(CONFIGPATH):
        return []
    configFile = open(CONFIGPATH)
    lst = pickle.load(configFile)
    configFile.close()
    return lst

def saveList(lst, replace=False):
    '''Saves lst in the config file. If replace is true, the current saved list
    is override. If not, the lists are mixed. The new one gets priority'''
    if not replace:
        oldlst = loadList()
        for val in oldlst:
            if lst.count(val) == 0:
                lst.append(val)
    saveFile = open(CONFIGPATH, 'w')
    pickle.dump(lst, saveFile)
    saveFile.close()

def printList():
    '''Prints saved ip list '''
    lst = loadList()
    formatString = "{0:2} | {1:10} | {2:16} | {3:40} | {4:40}"
    print formatString.format("ID","USER","IP", "REMOTE PATH", "LOCAL PATH")
    for ind in range(0, len(lst)):
        user, ip, remotepath, localpath = parseArgString(lst[ind])
        print formatString.format(ind, user, ip, remotepath, localpath)

if __name__ == '__main__':
    if sys.argv.count('-h') > 0 or sys.argv.count('-help') > 0:
        print """Usage: montar.py [options] [ips]
        If the script is run without arguments, the saved ips will be mounted.
        By default, all ips mounted by the script are saved.
        Options:
            -l: lists saved ips and exits
            -n: mount but don't save ips
            -e: edit saved configuration
            -lm: list saved ips and ask what ip to mount
            -u:  lists ips and ask what ip to unmount.
        Valid ip sintaxis:
            <user>@<ip>:<remote mount point>|<local mount point>
            where:
                <user> is the user (default is root)
                <ip> ip, 192.168.1.1 will be used as default.
                    Instead of passing the full ip, only the lasts digits can be passed.
                    Eg: if 69 is passed, 192.168.1.69 will be used
                        if 4.67 is passed, 192.168.4.67 will be used
                        if 160.3.45 is passed, 192.160.3.45 will be used
                        if 200.40.32.4 is passed 200.40.32.4 will be used
            <remove mount point> like in sshfs, / will be used as default
            <local mount point> local folder where to mount.
                %%ip%%  will be replaced by the ip.
                Default local mount point:  ~/ip_%%ip%%
            All [options] are optional.
        Examples:
            python montar.py 69 (192.168.1.69 will mounted in ~/ip_69 as root)
            python montar.py 69 89 (192.168.1.69 and 192.168.1.89 will be mounted in ~/ip_69 ~/ip_89 as root)
            python montar.py (saved ips will be mounted)
            python montar.py 69 -n (192.168.1.69 will be mounted in ~/ip_69 as root without saving the ip)
            python montar.py pepe@4.69 (192.168.4.69 will be mounted in ~/ip_69 as pepe)
            python montar.py 4.69:/asd|~/miFolder/%%ip%% (/asd folder from 192.168.4.69 will be mounted in  ~/miFolder/4_69 as root)
            python montar.py -l (will list saved ips)
            python mountar.py -e (will list saved ips for erasing)
        Config file: ~/.montadorsshfs
        """
        exit(0)
    if sys.argv.count('-l') > 0:
        printList()
        exit(0)
    if sys.argv.count('-e') > 0:
        printList()
        rta = raw_input('Ingrese id a borrar:')
        lst = loadList()
        lst.pop(int(rta))
        saveList(lst, True)
        exit(0)
    if sys.argv.count('-lm') > 0:
        printList()
        rta = raw_input('Ingrese id a montar:')
        lst = loadList()[int(rta)]
        mountList([lst])
        exit(0)
    if sys.argv.count('-u') > 0:
        printList()
        rta = raw_input('Ingrese id a desmontar:')
        lst = loadList()[int(rta)]
        user, ip, remotepath, localpath = parseArgString(lst)
        umountList([localpath])
        exit(0)
    if len(sys.argv) > 1:
        save = True if (sys.argv.count('-n') == 0) else False
        lst = [x for x in sys.argv][1:]
        if lst.count('-n') > 0:
            lst.remove('-n')
        mountList(lst)
        if save:
            saveList(lst)
    else:
        mountList(loadList())
    exit(0)
