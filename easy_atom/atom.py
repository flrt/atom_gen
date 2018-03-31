#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Production d'un fichier ATOM XML

    Definition : https://tools.ietf.org/html/rfc4287

    Outil de validation : https://validator.w3.org/feed/

"""
__author__ = 'Frederic Laurent'
__version__ = "1.0"
__copyright__ = 'Copyright 2017, Frederic Laurent'
__license__ = "MIT"

import codecs
import datetime
import logging
import os.path

import lxml.etree
from lxml.etree import SubElement

from easy_atom import helpers, content


class Feed:
    """
        Création d'un fichier de flux RSS au format ATOM

    """
    ATOM_FEED_DIR = "feeds"
    ATOM_CONFIG_DIR = "conf"
    FEED_ENCODING = 'utf-8'

    def __init__(self, ref, selfhref=''):
        """
        Constructeur du générateur

        Lien vers l'auto référence du flux : https://www.feedvalidator.org/docs/warning/MissingAtomSelfLink.html

        :param ref: référentiel concerné
        :param selfhref: HREF du flux XML une fois déployé pour son auto référence
        """
        self.logger = logging.getLogger('feed')
        self.ref = ref
        self.selhref = selfhref
        self.feed_config = {}
        self.load_config()

        output = self.feed_config["output_dir"] if "output_dir" in self.feed_config else Feed.ATOM_FEED_DIR
        self.feed_filename = os.path.join(output, self.feed_config["header"]["atom_feedname"])
        self.rss2_filename = os.path.join(output, self.feed_config["header"]["rss2_feedname"])
        self.update_date = datetime.datetime.now(datetime.timezone.utc).isoformat(sep='T')
        self.logger.debug("Feed : %s (RSS2 %s)" % (self.feed_filename, self.rss2_filename))

    def load_config(self):
        """
        Chargement de la configuration du flux
        :return:
        """
        filename = os.path.join(Feed.ATOM_CONFIG_DIR, "feed_config_{}.json".format(self.ref))
        self.logger.debug("Load config file : {}".format(filename))
        self.feed_config = helpers.load_json(filename)

    def make_entry_id(self, id):
        return "{}{}".format(self.feed_config["entry"]["urn_mask"], id)

    def generate(self, entries):
        """
        Génération du fichier XML Atom
        :param entries: listes des entrées du fichier
        :return: noeud XML du document Atom XML
        """
        self.logger.debug("Feed to XML : {} entries".format(len(entries)))

        root = content.xmlelt(None, "feed", None, {"xmlns": "http://www.w3.org/2005/Atom"})

        content.xmlelt(root, "id", self.feed_config["header"]["id"])
        content.xmlelt(root, "title", self.feed_config["header"]["title"])
        content.xmlelt(root, "subtitle", self.feed_config["header"]["subtitle"])
        content.xmlelt(root, "link", None,
                       {"href": self.feed_config["header"]["link"],
                        "rel": "related"})
        content.xmlelt(root, "link", None,
                       {"href": '{}{}'.format(self.selhref,
                                              self.feed_config["header"]["atom_feedname"]),
                        "rel": "self"})

        content.xmlelt(root, "updated", self.update_date)
        author = SubElement(root, "author")
        content.xmlelt(author, "name", self.feed_config["header"]["author"]["name"])
        content.xmlelt(author, "email", self.feed_config["header"]["author"]["email"])

        content.xmlelt(root, "category", None,
                       {"term": self.feed_config["header"]["category"]})

        content.xmlelt(root, "generator", "python program - atom.py",
                       {"uri": "https://github.com/flrt/atom_gen",
                        "version": "1.0"})
        content.xmlelt(root, "rights", "CC BY-SA 3.0 FR")

        for entry in entries:
            self.logger.debug("current entry : %s" % entry)

            xml_entry = content.xmlelt(root, "entry")
            content.xmlelt(xml_entry, "title", entry["title"])

            if 'files' in entry and entry['files']:
                for fi in entry['files']:
                    content.xmlelt(xml_entry, "link", None,
                                   {"href": fi,
                                    "rel": "related",
                                    "type": self.mimetype(fi)})

            content.xmlelt(xml_entry, "id", entry["id"])
            # fabrication du contenu
            content.make_xhtml(xml_entry, entry)
            content.xmlelt(xml_entry, "updated", entry["date"])
            content.xmlelt(xml_entry, "summary", entry["summary"])

        return root

    @staticmethod
    def mimetype(link):
        """
        Detection du type mime en fonction de l'extension de l'URL
        :param link: URL du fichier
        :return: type mime associé. Type: str
        """
        mimetypes = {".zip": "application/zip",
                     ".dbf": "application/dbase",
                     ".csv": "text/plain"}
        ext = link[link.rfind('.'):]
        if ext in mimetypes:
            return mimetypes[ext]
        else:
            return "application/octet-stream"

    def save(self, root):
        """
        Sauvegarde locale des données
        :param root: noeud XML
        :return: -
        """
        self.logger.info("Save Atom {0}".format(self.feed_filename))
        with codecs.open(self.feed_filename, "w", Feed.FEED_ENCODING) as fout:
            fout.write(content.xml2text(root, Feed.FEED_ENCODING))

    def rss2(self, feed=None):
        """
        Conversion du document atom en ficher rss2

        :param feed: arbre XML du flux Atom
        :return: -
        """
        try:
            import atomtorss2
            import atomtorss2.xslt_ext

            self.logger.info("Save RSS2 {0}".format(self.rss2_filename))

            # XSL
            filedir = os.path.dirname(os.path.abspath(atomtorss2.__file__))
            xslt_filename = os.path.join(filedir, atomtorss2.DEFAULT_XSLT_FILE)

            proc = atomtorss2.xslt_ext.DateFormatterProcessor()
            proc.load_xslt(xslt_filename)

            # conversion RSS2
            if feed is not None:
                result_xml = proc.transform(feed)
            else:
                result_xml = proc.transform(lxml.etree.parse(self.feed_filename))

            with codecs.open(self.rss2_filename, "w", Feed.FEED_ENCODING) as fout:
                fout.write(content.xml2text(result_xml, Feed.FEED_ENCODING))

        except ImportError:
            self.logger.warn("No transformation library found : atom -> rss2")
