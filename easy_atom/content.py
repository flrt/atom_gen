#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Fonctions de production de contenu


"""
__author__ = 'Frederic Laurent'
__version__ = "1.0"
__copyright__ = 'Copyright 2017, Frederic Laurent'
__license__ = "MIT"

import lxml.etree
from lxml.etree import Element, SubElement


def make_xhtml(root, entry):
    """
    Creation d'un contenu XHTML pour une entree ATOM
    content > div > article > blabla

    si files fait partie des informations dans l'entree, une section telechargement est inseree
    contenu : text

    :param root: noeud XML du père du contenu
    :param entry: données de l'entrée ATOM
    :return: noeud XML produit
    """
    content_elt = xmlelt(root, "content", None, {"type": "xhtml"})
    main_div_elt = xmlelt(content_elt, "div", None, {"xmlns": "http://www.w3.org/1999/xhtml"})
    article_elt = xmlelt(main_div_elt, "article", None, None)
    div_elt = xmlelt(article_elt, "div", None, None)

    if 'files' in entry and entry['files']:
        xmlelt(div_elt, "h1", u"Fichier%s à télécharger : " %
               "" if len(entry["files"]) == 1 else "s")

        ul = xmlelt(div_elt, "ul")
        for fi in entry['files']:
            xmlelt(xmlelt(ul, "li"), "a", fi, {"href": fi})

    # raw text in a div html
    if "text" in entry and entry["text"]:
        elt = lxml.etree.fromstring("<div>{}</div>".format(entry["text"]))
        article_elt.append(elt)
    # insert html content
    if "html" in entry and entry["html"]:
        elt = lxml.etree.fromstring(entry["html"])
        article_elt.append(elt)

    return content_elt


def make_xhtml_(root, entry):
    """
    Creation d'un contenu XHTML pour une entree ATOM
    content > div > article > blabla

    si files fait partie des informations dans l'entree, une section telechargement est inseree
    contenu : text

    :param root: noeud XML du père du contenu
    :param entry: données de l'entrée ATOM
    :return: noeud XML produit
    """
    content_elt = xmlelt(root, "content", None, {"type": "xhtml"})
    main_div_elt = xmlelt(content_elt, "div", None, {"xmlns": "http://www.w3.org/1999/xhtml"})
    article_elt = xmlelt(main_div_elt, "article", None, None)
    div_elt = xmlelt(article_elt, "div", None, None)

    if 'files' in entry and entry['files']:
        xmlelt(div_elt, "h1",
               u"Fichier{} à télécharger : ".format(
               "" if len(entry["files"]) == 1 else "s"))

        ul = xmlelt(div_elt, "ul")
        for fi in entry['files']:
            xmlelt(xmlelt(ul, "li"), "a", fi, {"href": fi})

    if "text" in entry and entry["text"]:
        # elt = xml.etree.ElementTree.fromstring(entry["text"])
        elt = lxml.etree.fromstring(entry["text"])
        article_elt.append(elt)

    return content_elt


def xml2text(elem, encoding='utf-8', xml_decl=True):
    """
        Retourne une version indentée de l'arbre XML
    :param encoding:
    :param elem: noeud de l'arbre XML
    :return: Texte avec XML indenté
    """
    # rough_string = xml.etree.ElementTree.tostring(elem, encoding=encoding)
    # reparsed = minidom.parseString(rough_string)
    # return reparsed.toprettyxml(indent="  ")

    data = lxml.etree.tostring(elem, encoding=encoding,
                               pretty_print=True,
                               xml_declaration=xml_decl)
    return data.decode(encoding)


def xmlelt(root, tag, text=None, attrs=None):
    """
    Production d'un noeud XML avec positionnement des attributs

    :param attrs:
    :param text:
    :param root: root de l'arbre XML
    :param tag: balise
    :return: element cree
    """
    if root is None:
        elem = Element(tag)
    else:
        elem = SubElement(root, tag)

    if text:
        elem.text = text

    if attrs:
        for (k, v) in attrs.items():
            elem.attrib[k] = v

    return elem
