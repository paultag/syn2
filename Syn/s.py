#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import Syn.tarball
import Syn.common as c
import Syn.Global as g
import Syn.build
import Syn.log

import tarfile
import os.path
import shutil
import json
import os

def targetTarball(tar):
	global _tb
	global _tb_dir
	_tb_dir = os.path.dirname(os.path.abspath(tar))
	_tb = Syn.tarball.us_tb()
	_tb.target(tar);

def getVersion():
	global _tb
	try:
		root = _tb.getRootFolder()
	except NameError as e:
		raise NameError("Package not set")

	package, version = Syn.common.processFullID(root)
	Syn.log.l(Syn.log.VERBOSE, "Processing package   `%s'" % package)
	Syn.log.l(Syn.log.VERBOSE, "Version processed as `%s'" % version)
	return [package, version]

def template():
	package, version = getVersion()
	Syn.common.cd(_tb_dir)
	if os.path.exists("synd"):
		raise IOError("Synd Exists!")
	else:
		Syn.common.mkdir("synd")

def putenv(key, value):
	Syn.log.l(Syn.log.VERBOSE, "%s = %s" % (key, value))
	# print "export " + key + "=\"" + value + "\""
	os.putenv(key, value)

def loadBuildConfigFile():
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_CONFIG)
	conf_file = f.read()
	return json.loads(conf_file)

def loadMetaConfigFile():
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_META)
	conf_file = f.read()
	return json.loads(conf_file)

def writeMetafile(frobernate):
	output = json.dumps(
		frobernate,
		sort_keys = True,
		indent    = 4
	)
	f = open(g.SYN_BUILDDIR + g.SYN_BUILDDIR_META, 'w')
	f.write(output)
	f.close()

def extractSource(pack_loc, path="."):
	global _tb
	c.cd(pack_loc)
	try:
		root = _tb.getRootFolder()		
		_tb.extractall(path)
	except NameError as e:
		raise NameError("Package not set")

def tarup( directory, outputname ):
	tarball_target = tarfile.open(outputname, "w|gz")
	tarball_target.add(directory)
	tarball_target.close()

def buildFromSource(pkg_path):
	Syn.build.buildFromSource(pkg_path)

def metadump(filezor):
	tarball_target = tarfile.open(filezor, "r")
	metafile = g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META
	tarinfo = tarball_target.getmember(metafile)
	if tarinfo.isfile():
		meta = tarball_target.extractfile(metafile)
		metadata = json.loads(meta.read())
	else:
		raise KeyError("Bum file")
	tarball_target.close()
	return metadata

def build(pack_loc):
	Syn.build.build(pack_loc)

def install(pathorig):
	path = os.path.abspath(pathorig)

	meta = metadump(path)
	pkg = meta['package']
	ver = meta['version']

	Syn.log.l(Syn.log.MESSAGE, "Installing version %s of %s" % ( ver, pkg ))
	c.cd(g.INSTALL_ROOT_PATH)

	archive = Syn.tarball.us_tb()
	archive.target(path)

	try:
		c.mkdir(pkg)
	except OSError:
		Syn.log.l(Syn.log.PEDANTIC, "we have a version of bash installed")
		pass # it's ok to have a pkg
		#      installed. just not ver
	c.cd(pkg)

	try:
		c.mkdir(ver)
	except OSError:
		Syn.log.l(Syn.log.CRITICAL, "Package exists in syn!")
		Syn.log.l(Syn.log.CRITICAL, "Can *NOT* continue!")
		return -1
	c.cd(ver)

	archive.extractall(".")

	shutil.move(
		g.ARCHIVE_FS_ROOT + "/" + g.SYN_BINARY_META,
		g.SYN_XTRACT_META,
	)

	return 0
