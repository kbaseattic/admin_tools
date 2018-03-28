#!/usr/bin/python

import os
import os.path
import time
import requests
import datetime
import rfc822

#requests.packages.urllib3.disable_warnings()

# suggested by https://bobrochel.blogspot.co.nz/2010/11/bad-servers-chunked-encoding-and.html
# to work around IncompleteRead issue
import httplib
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

# called recursively for each dir found at remote
def retrieve_dir(url,path):
    print 'retrieving directory ' + url + ' to path ' + path
    try:
        os.makedirs(path)
        print 'created dir ' + path
    except OSError as exc:
        if os.path.isdir(path):
            pass
        else:
	    raise
    
    remotereq=requests.get(url)
    remotels=remotereq.json()

    for remoteentry in remotels:
#        print remoteentry
        if remoteentry['type'] == 'directory':
	    retrieve_dir(url+'/'+remoteentry['name'],path+'/'+remoteentry['name'])
	if remoteentry['type'] == 'file' and remoteentry['name'] != '__READY__':
            remoteUrl=url + '/' + remoteentry['name']
#	    print remoteentry
	    mirrorDatestamp=time.mktime(rfc822.parsedate(remoteentry['mtime']))
            mirrorSize=remoteentry['size']
            localFile=path + '/' + remoteentry['name']
            if os.path.isfile(localFile):
	        fileDatestamp=os.path.getmtime(localFile)
                fileSize=os.stat(localFile).st_size
		print mirrorDatestamp
		print fileDatestamp
		print fileSize
		print mirrorSize
                if mirrorDatestamp < fileDatestamp and fileSize==mirrorSize:
                    print "mirror older than file and same size, skipping " + remoteUrl
#                if fileSize==mirrorSize:
#                    print "mirror same size (not checking datestamp), skipping " + remoteUrl
		    continue
	    print 'retrieving file ' + remoteUrl + ' (size ' + str(remoteentry['size']) + ') as ' + localFile
            filereq=requests.get(remoteUrl, timeout=5, stream=True)
	    with open (localFile, 'wb') as fd:
	        for chunk in filereq.iter_content(512*1024):
		    fd.write(chunk)

def mirror_refdata(refdataTopdir='https://kbase.us/refdata/', refdataDiskdir='refdata'):
    refdataReq = requests.get(refdataTopdir)
    modules = refdataReq.json()

    for module in modules:
        moduledir = refdataTopdir + module['name']
        moduleReq = requests.get(moduledir)
        versions = moduleReq.json()
        for version in versions:
            versiondir = moduledir + '/' + version['name']
            versionDiskPath= refdataDiskdir+'/'+module['name']+'/'+version['name']

# for retrieving dot files (requires building .dotfile manually at the source)
            remotedotfilesls=[]
            remotedotfilesreq=requests.get(versiondir+'/.dotfiles')
# for now just get the .dotfiles file
            try:
                remotedotfilesls=remotedotfilesreq.json()
            except:
                pass

            readyHeadReq = requests.head(versiondir+'/__READY__')
	    print readyHeadReq.headers['Last-Modified']
	    mirrorDatestamp=rfc822.mktime_tz(rfc822.parsedate_tz(readyHeadReq.headers['Last-Modified']))
            readyFile=versionDiskPath+'/__READY__'
            if os.path.isfile(readyFile):
                fileDatestamp=os.path.getmtime(readyFile)
                print mirrorDatestamp
		print fileDatestamp
                if mirrorDatestamp < fileDatestamp:
                    print "mirror __READY__ older than local file, skipping " + versiondir
		    continue
            try:
                os.makedirs(versionDiskPath)
                print 'created dir ' + versionDiskPath
            except OSError as exc:
	        if os.path.isdir(versionDiskPath):
	            pass
                else:
	            raise
            retrieve_dir(versiondir,versionDiskPath)

# hacky support for dot files
            for dotfile in remotedotfilesls:
# for now only support for dot dirs
# (need to break out the file retrieval into a separate method to do files here)
                retrieve_dir(versiondir+'/'+dotfile['name'],versionDiskPath+'/'+dotfile['name'])

            # if this works, retrieve __READY__ file
	    print 'retrieve ' + versiondir + ' succeeded, retrieving __READY__ file'
            filereq=requests.get(versiondir + '/__READY__', timeout=5, stream=True)
	    with open (versionDiskPath + '/__READY__', 'wb') as fd:
	        for chunk in filereq.iter_content(1024):
		    fd.write(chunk)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Mirror a KBase SDK reference data repository.', epilog='To do: add option to retrieve only one version of one data module')
    parser.add_argument('--url',default='https://kbase.us/refdata/', help='top-level URL where refdata is located (must use trailing /, must be JSON indexes like nginx can supply)')
    parser.add_argument('--dest',default='refdata', help='local directory where mirror will be copied to')
    args = parser.parse_args()

    mirror_refdata(refdataTopdir=args.url, refdataDiskdir=args.dest)
