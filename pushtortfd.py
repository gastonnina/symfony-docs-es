#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import zipfile
import mechanize
import netrc

######## config ########
repo = 'test-sf-doc-es'

######## generar zip ########
print "Generando zip..."
target_dir = os.path.join(os.path.realpath('.'), '_build', 'html')

buildname = 'htmlbuild.zip'

buildzip = zipfile.ZipFile(buildname, 'w', zipfile.ZIP_DEFLATED)
rootlen = len(target_dir) + 1
for base, dirs, files in os.walk(target_dir):
    for file in files:
        fn = os.path.join(base, file)
        buildzip.write(fn, fn[rootlen:])
buildzip.close()

print "Zip generado, actualizando en el servidor..."
######## abrir navegador ########

b = mechanize.Browser()
b.open('http://readthedocs.org/accounts/login/')

######## login ########
# el form de login es el segundo
f = [i for i in b.forms()][1]

n = netrc.netrc()

f['username'] = n.hosts['readthedocs.org'][0]
f['password'] = n.hosts['readthedocs.org'][2]

b.form = f
b.submit()

######## submit zip file ########
b.open('http://readthedocs.org/dashboard/upload_html/' + repo)

f = [i for i in b.forms()][1]
b.form = f

b.form.add_file(open(buildname), filename=os.path.basename(buildname), name='content')
b.form['overwrite'] = ['on']
b.submit()

print "Envío completado, borrando zip..."
# borramos el zip generado
os.unlink(buildname)

print "Terminado."
