# Copyright (c) 2007, Simon Edwards <simon@simonzone.com>
# Copyright (c) 2014, Raphael Kubo da Costa <rakuco@FreeBSD.org>
# Copyright (c) 2014, Alexei Ardyakov <ardjakov@rambler.ru>
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.

import PyQt4.QtCore
import os
import sys


def get_default_sip_dir():
    # This is based on QScintilla's configure.py, and only works
    # for a few popular locations of PyQt SIP directory.
    if sys.platform == 'win32':
        import site
        default_sip_dirs = [
            os.path.join(p, 'PyQt4\\sip\\PyQt4')
            for p in site.getsitepackages()
            ]
    else:
        default_sip_dirs = [
            '/usr/share/sip/Py2-PyQt4',
            '/usr/share/sip/PyQt4',
            '/usr/local/share/sip/PyQt4',
            ]
    for sip_dir in default_sip_dirs:
        if os.path.exists(sip_dir) and os.path.exists(
                os.path.join(sip_dir, 'QtCore')):
            return sip_dir
    raise ValueError('Cannot find SIP directory in default locations')


def get_qt4_tag(sip_flags):
    in_t = False
    for item in sip_flags.split(' '):
        if item == '-t':
            in_t = True
        elif in_t:
            if item.startswith('Qt_4'):
                return item
        else:
            in_t = False
    raise ValueError('Cannot find Qt\'s tag in PyQt4\'s SIP flags.')


if __name__ == '__main__':
    
    try:
        import PyQt4.pyqtconfig
        pyqtcfg = PyQt4.pyqtconfig.Configuration()
        sip_dir = pyqtcfg.pyqt_sip_dir
        sip_flags = pyqtcfg.pyqt_sip_flags
    except ImportError:
        # PyQt4 >= 4.10.0 was built with configure-ng.py instead of
        # configure.py, so pyqtconfig.py is not installed.
        sip_dir = get_default_sip_dir()
        sip_flags = PyQt4.QtCore.PYQT_CONFIGURATION['sip_flags']

    print('pyqt_version:%06.x' % PyQt4.QtCore.PYQT_VERSION)
    print('pyqt_version_str:%s' % PyQt4.QtCore.PYQT_VERSION_STR)
    print('pyqt_version_tag:%s' % get_qt4_tag(sip_flags))
    print('pyqt_sip_dir:%s' % sip_dir)
    print('pyqt_sip_flags:%s' % sip_flags)
