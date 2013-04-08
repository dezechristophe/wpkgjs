import os
from xml.etree import ElementTree as ET

def get_machines():
    print "coin"
    grps=[]
    print '/home/esu/Base/ListeGM.xml'
    if os.path.exists(u'/home/esu/Base/ListeGM.xml'):
        filename = u'/home/esu/Base/ListeGM.xml'
        xml = ET.parse(filename)
        i = 0
        for group in xml.getiterator('GM'):
            grp = group.get('nom')
            print grp
            grps.append(grp)
    else:
        grp = 'grp_eole'
        grps=[grp]
    return grps
