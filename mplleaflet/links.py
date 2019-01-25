#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest


class Link(object):
    def __init__(self, url, download=False):
        """Create a link object base on an url.
        Parameters
        ----------
            url : str
                The url to be linked
            download : bool, default False
                Whether the target document shall be loaded right now.
        """
        self.url = url
        self.code = None
        if download:
            # self.code = urllib.request.urlopen(self.url).read()
            self.code = urlrequest.urlopen(self.url).read()


class JavascriptLink(Link):
    def render(self, embedded=False):
        """Renders the object.
        
        Parameters
        ----------
            embedded : bool, default False
                Whether the code shall be embedded explicitely in the render.
        """
        if embedded:
            if self.code is None:
                # self.code = urllib.request.urlopen(self.url).read()
                self.code = urlrequest.urlopen(self.url).read()
            return '<script>{}</script>'.format(self.code)
        else:
            return '<script src="{}"></script>'.format(self.url)


class CssLink(Link):
    def render(self, embedded=False):
        """Renders the object.
        
        Parameters
        ----------
            embedded : bool, default False
                Whether the code shall be embedded explicitely in the render.
        """
        if embedded:
            if self.code is None:
                # self.code = urllib.request.urlopen(self.url).read()
                self.code = urlrequest.urlopen(self.url).read()
            return '<style>{}</style>'.format(self.code)
        else:
            return '<link rel="stylesheet" href="{}" />'.format(self.url)
