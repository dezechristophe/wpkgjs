import glob
import os
import shutil
from lxml import etree

#class packages():
def get_packages():
	"""
	initialise la liste des applications disponibles
	"""
	apps=[]
	lspackages = glob.glob(u'/home/wpkg/packages/*.xml')
	for fic in lspackages:
        #print fic
		if os.path.isfile(fic):
			try:
				xml = etree.parse(fic)
			except:
				#si erreur on tente de corriger le fichier
				oput = open("output.txt","w")
				data = open(fic).read()
				oput.write( re.sub('&(?!amp;|quot;|nbsp;|gt;|lt;|laquo;|raquo;|copy;|reg;|bul;|rsquo;)', '&amp;', data) )
				oput.close()
				shutil.move("output.txt", fic)

			finally:
				parser = etree.XMLParser(remove_comments=False)
				xml = etree.parse(fic,parser)
				strxml = etree.tostring(xml.getroot())
				for group in xml.getiterator(u'package'):
					uid = group.get(u'id')
					name = group.get(u'name')
					dvars = dict()
					for vars in xml.getiterator('variable'):
						dvars[vars.get('name').lower()] = vars.get('value').lower()

				#on remplit le dico des appli dispo
				#print fic,uid,name
				apps.append((fic,uid,name))

	return apps

def get_content(filename):
    print filename
    if os.path.isfile(filename):
        return open(filename,'r').read().decode('utf-8')
    else:
        print 'rien'
        return 'rien'



