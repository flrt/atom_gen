#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test simple de la generation de contenu
"""

import os.path
import unittest
from xmlunittest import XmlTestCase

import logging
import content
import atom
import helpers

class TestContent(XmlTestCase):

    def setUp(self):
        self.logger = logging.getLogger('tests')
        self.infos_in = {
            "available": True,
            "date": "2018-05-07T21:17:45.849391+00:00",
            "files": [
                "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_total_00407_20180504.dbf",
                "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_maj_00407_20180504.dbf",
                "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_histo_prix_00407_20180504.dbf",
                "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_taux_00407_20180504.dbf",
                "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_cout_sup_00407_20180504.dbf"
            ],
            "files_props": [
                           {
                    "http_status": 200,
                    "size": "2827330",
                    "type": "data",
                    "url": "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_total_00407_20180504.dbf"
                },
                {
                    "http_status": 200,
                    "size": "33858",
                    "type": "data",
                    "url": "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_maj_00407_20180504.dbf"
                },
                {
                    "http_status": 200,
                    "size": "1728448",
                    "type": "data",
                    "url": "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_histo_prix_00407_20180504.dbf"
                },
                {
                    "http_status": 200,
                    "size": "444757",
                    "type": "data",
                    "url": "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_taux_00407_20180504.dbf"
                },
                {
                    "http_status": 200,
                    "size": "233686",
                    "type": "data",
                    "url": "http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_cout_sup_00407_20180504.dbf"
                },
                {
                    "http_status": 301,
                    "size": "0",
                    "type": "link",
                    "url": "https://www.twitter.com/frlrtdev/status/995218408013692928"
                }
            ],
            "html": "<div>\n    <h1>Informations sur la version 407</h1>\n    <p>23 lignes mises \u00e0 jour.</p>\n    \n    <p>Les m\u00e9dicaments concern\u00e9s par la mise \u00e0 jour sont les suivants :</p>\n    <p>KOVALTRY, CASPOFUNGINE, NEVIRAPINE, VESANOID, ABACAVIR, EPOPROSTENOL, PANZYGA</p>\n\n    <p></p>\n</div>",
            "id": "urn:ameli:ucd:v407",
            "summary": "Version 407 disponible",
            "title": "Nomenclature UCD Version 407",
            "type": "UCD",
            "url": None,
            "version": "407"
        }
        self.feed_config={"header":{
    "title": "Versions du référentiel AMELI - CCAM",
    "subtitle": "Referentiel - Le codage des actes médicaux - CCAM",
    "link" : "https://www.ameli.fr/medecin/exercice-liberal/facturation-remuneration/nomenclatures-codage/codage-actes-medicaux-ccam",
    "author": {"name":"Frederic LAURENT", "email":"frederic.laurent@gmail.com"},
    "id":"http://www.opikanoba.org/feeds/ameli/ccam",
    "category":"referentiel,ameli,CCAM",
    "atom_feedname": "ameli_ccam.xml",
    "rss2_feedname": "ameli_ccam.rss2"
  },
  "entry" : {
    "link_mask":"http://",
    "urn_mask":"urn:ameli:ccam:v",
    "title_mask" : "Version",
    "content_mask": "Version"
  }
}

    def test_entry(self):
        expected_out="""<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <content type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <article>
          <div>
            <h1>5 Fichiers à télécharger : </h1>
            <ul>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_total_00407_20180504.dbf">ucd_total_00407_20180504.dbf (2.7 Mo)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_maj_00407_20180504.dbf">ucd_maj_00407_20180504.dbf (33.06 Ko)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_histo_prix_00407_20180504.dbf">ucd_histo_prix_00407_20180504.dbf (1.65 Mo)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_taux_00407_20180504.dbf">retro_histo_taux_00407_20180504.dbf (434.33 Ko)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_cout_sup_00407_20180504.dbf">retro_histo_cout_sup_00407_20180504.dbf (228.21 Ko)</a>
              </li>
            </ul>
          </div>
          <div>
    <h1>Informations sur la version 407</h1>
    <p>23 lignes mises à jour.</p>

    <p>Les médicaments concernés par la mise à jour sont les suivants :</p>
    <p>KOVALTRY, CASPOFUNGINE, NEVIRAPINE, VESANOID, ABACAVIR, EPOPROSTENOL, PANZYGA</p>

    <p/>
</div>
        </article>
      </div>
    </content>
  </entry>
</feed>
"""
        f = atom.Feed('ccam')
        f.feed_config = self.feed_config

        root = content.xmlelt(None, "feed", None, {"xmlns": "http://www.w3.org/2005/Atom"})

        f.make_entry(root, self.infos_in)

        print(content.xml2text(root))
        #self.assertEqual(content.xml2text(root), expected_out)
        #root = self.assertXmlDocument(expected_out)


    def test_entry_content(self):
        expected_out="""<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <content type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <article>
          <div>
            <h1>5 Fichiers à télécharger : </h1>
            <ul>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_total_00407_20180504.dbf">ucd_total_00407_20180504.dbf (2.7 Mo)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_maj_00407_20180504.dbf">ucd_maj_00407_20180504.dbf (33.06 Ko)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/ucd_histo_prix_00407_20180504.dbf">ucd_histo_prix_00407_20180504.dbf (1.65 Mo)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_taux_00407_20180504.dbf">retro_histo_taux_00407_20180504.dbf (434.33 Ko)</a>
              </li>
              <li>
                <a href="http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm_it/retro_histo_cout_sup_00407_20180504.dbf">retro_histo_cout_sup_00407_20180504.dbf (228.21 Ko)</a>
              </li>
            </ul>
          </div>
          <div>
    <h1>Informations sur la version 407</h1>
    <p>23 lignes mises à jour.</p>

    <p>Les médicaments concernés par la mise à jour sont les suivants :</p>
    <p>KOVALTRY, CASPOFUNGINE, NEVIRAPINE, VESANOID, ABACAVIR, EPOPROSTENOL, PANZYGA</p>

    <p/>
</div>
        </article>
      </div>
    </content>
  </entry>
</feed>
"""

        root = content.xmlelt(None, "feed", None, {"xmlns": "http://www.w3.org/2005/Atom"})
        xml_entry = content.xmlelt(root, "entry")
        content.make_xhtml(xml_entry, self.infos_in)

        print(content.xml2text(root))
        #self.assertEqual(content.xml2text(root), expected_out)
        root = self.assertXmlDocument(expected_out)


if __name__ == '__main__':
    loggers = helpers.stdout_logger(['tests','content'], logging.DEBUG)
    unittest.main()
