#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

WORKDIR         = "/tmp/syn/" # where to unpack & build
ARCHIVE_FS_ROOT = "syn"       # build stage folder
BUILD_FS_ROOT   = "build"     # build build folder

BIN_PKG         = "syn"       # pkg-1.0.BIN_PKG

DEFAULT_SYN   = "~/.syn/"
DEFAULT_SYNRC = DEFAULT_SYN + "synrc"

SYN_BUILDDIR        = "synd/"

SYN_BUILDDIR_SCRIPT = "build"      # build "rules" file
SYN_BUILDDIR_CONFIG = "buildrc"    # build config file (flags)
SYN_BUILDDIR_META   = "meta"       # metafile (control file)
SYN_BINARY_META     = ".meta-syn"  # binary metafile package location
#                                    (in the archive)

CONFIG_FLAGS = "CONFIG_FLAGS"
BUILD_FLAGS  = "BUILD_FLAGS"
STAGE_FLAGS  = "STAGE_FLAGS"
CONFIG       = "CONFIGURE"
BUILD        = "BUILD"
STAGE        = "STAGE"
DESTDIR      = "S_DESTDIR"
