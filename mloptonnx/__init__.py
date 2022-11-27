# -*- coding: utf-8 -*-
"""
@file
@brief Module *mloptonnx*.
:epkg:`Python` + C + :epkg:`ONNX`.
"""

__version__ = "0.1.1"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/mloptonnx"
__url__ = "http://www.xavierdupre.fr/app/mloptonnx/helpsphinx/index.html"
__license__ = "MIT License"
__blog__ = """
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>blog</title>
    </head>
    <body>
        <outline text="mloptonnx"
            title="mloptonnx"
            type="rss"
            xmlUrl="http://www.xavierdupre.fr/app/mloptonnx/helpsphinx/_downloads/rss.xml"
            htmlUrl="http://www.xavierdupre.fr/app/mloptonnx/helpsphinx/blog/main_0000.html" />
    </body>
</opml>
"""


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.
    If you want to disable the logs:

    :param log: if True, display information, otherwise
    :return: 0 or exception
    """
    return True
