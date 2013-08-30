#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.dom.pulldom as pulldom
from xml.dom.pulldom import START_ELEMENT, parse
from trwiktionaryParser import make_parser
from mediawiki_parser.text import toolset
import sys, pdb, codecs, locale, codecs

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

diller = {}

def anlamlarCb(node, kelime):
    ret = ""
    dil = node.value[0].value[1].value
    tur = node.value[1].value[1].value
    for anlam in node.value[2].value:
        sira = anlam.value[0].value
        deger = anlam.value[1].value
        ret += u"%s\t%s\t%s\t%s\t%s\n" % (dil, kelime, tur, sira, deger)
    try:
        diller[dil] = u''.join([diller[dil], ret])
    except KeyError as e:
        diller[dil] = ret
    print ret
    
if __name__ == "__main__":
    outfile = codecs.open(sys.argv[2], "w", "UTF-8")
    doc = parse(sys.argv[1])
    for event, node in doc:
        if event == START_ELEMENT and node.localName == "page":
            doc.expandNode(node)
            title = node.getElementsByTagName("title")[0].firstChild.data
            if ':' in title:
                continue
            text = u"".join([node.data for node in node.getElementsByTagName("text")[0].childNodes])
            #print text
            actions = toolset({}, {})
            def anlamlarCbWrap(node):
                anlamlarCb(node, title)
            actions["anlamlarCb"] = anlamlarCbWrap
            make_parser(actions).parse( (text+"\n") )
    # print the results we got
    for dil in diller.keys():
        outfile.write(diller[dil])
    outfile.flush()
    outfile.close()
