import os
from lxml import etree

def get_profile(grp):
    """
    lit la liste des appli affectes au groupe de  machines
    si elle n'existe pas on cree une vide
    """
    profiles=[]
    filename = u'/home/wpkg/profiles/' + grp + '.xml'
    if os.path.exists(filename):
        xml = etree.parse(filename)
        for group in xml.getiterator('package'):
            profiles.append(group.get('package-id'))
    else:
        set_profile(grp, True)
    return profiles

def set_profile(grp, noapp=False):
    """
    creation fichiers contenant les applis pour un group
    """
    if not os.path.exists('/home/wpkg/profiles/'):
        os.makedirs('/home/wpkg/profiles/')
    filename = u'/home/wpkg/profiles/' + grp + '.xml'
    xmlfp = open(filename, "w")
    xmlfp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    xmlfp.write('<profiles>\n')
    xmlfp.write('<profile id="' + grp + '">\n')
    if noapp == False:
        #for uid in self.checklistboxapp.GetCheckedStrings():
        for uid in self.dgrps[grp].packages:
            xmlfp.write('<package package-id="' + uid + '" />\n')
            #on ajoute les raccourcis
            """
            if createshortcuts:
                for shortcut in self.dapps[uid].shortcuts:
                    self.addshortcut(uid,shortcut,'R:\\' + grp + '\\_Machine\Bureau\\' + os.path.basename(shortcut) + '.lnk')
                print self.dapps[uid].xmlshortcuts
                for shortcut in self.dapps[uid].xmlshortcuts:
                    for d in shortcut['dest']:
                        self.addshortcut(uid,shortcut['exe'],d )
            """
    xmlfp.write('</profile>\n')
    xmlfp.write('</profiles>\n')
    xmlfp.close()



