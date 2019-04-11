### Proceso de preparacion del servidor Ubuntu 18.04

#### Paso 1. Actualizacion e instalacion
***
	sudo apt-get update
	sudo apt-get install git

	sudo apt-get install python3.6
	sudo apt-get install python-dev python-pip python3-dev python3-pip

	sudo apt-get install build-essential cmake pkg-config
	sudo apt-get install libx11-dev libatlas-base-dev
	sudo apt-get install libgtk-3-dev libboost-python-dev

	sudo -H pip2 install -U pip numpy
	sudo -H pip3 install -U pip numpy

	pip2 install virtualenv virtualenvwrapper
	pip3 install virtualenv virtualenvwrapper

#### Paso 1.1 Instalar virtual environment
	sudo pip2 install virtualenv virtualenvwrapper
	sudo pip3 install virtualenv virtualenvwrapper

	echo "# Virtual Environment Wrapper" >> ~/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
	source ~/.bashrc

### Para Python 2

#### crear virtual environment
	mkvirtualenv facecourse-py2 -p python2
	workon facecourse-py2
  
#### Ahora instala bibliotecas de Python dentro de este virtual environment
	pip install numpy scipy matplotlib scikit-image scikit-learn ipython
  
#### salir virtual environment
	deactivate
  
### Para Python 3
#### create virtual environment
	mkvirtualenv facecourse-py3 -p python3
	workon facecourse-py3

#### ahora instala bibliotecas de Python dentro de este entorno virtual
	pip install numpy scipy matplotlib scikit-image scikit-learn ipython

## Paso 2: Compilar DLib
### Paso 2.1: Compilar binario de C ++

	wget http://dlib.net/files/dlib-19.6.tar.bz2
	
	tar xvf dlib-19.6.tar.bz2
	
	cd dlib-19.6/
	
	mkdir build
	
	cd build
	
	cmake ..
	
	cmake --build . --config Release
	
	sudo make install
	
	sudo ldconfig
	
	cd ..

	pkg-config --libs --cflags dlib-1

### Paso 2.2: Compilar el módulo de Python
#### Para Python 2
	workon facecourse-py2
 
#### Para Python 3
	workon facecourse-py3

##### mover al directorio raíz de dlib
	cd dlib-19.6
	
	python setup.py install
##### limpiar (este paso es necesario si desea compilar dlib para Python2 y Python3)
	rm -rf dist
	
	rm -rf tools/python/build
	
	rm python_examples/dlib.so

### Comprobar la instlacion blib Python3
	pip3 install dlib

### Instalar face_recognition Python3
	pip3 install face_recognition

### Instalar buscador de archivo bien util
	apt-get install apt-file

## Paso 3. Clonar Github Face
### Crear carpeta de la aplicacion
	mkdir /var/www/flask/
### Posicionarse en la carpeta
	cd /var/www/flask
### Clonar proyecto
	git clone https://github.com/script32/face
### Mover archivo app.wsgi
	cd /var/www/flask/face
	mv app.wsgi /var/www/flask/app.wsgi


## Paso 4. Configuracion Apache y Firewall

#### Instalar Apache
	sudo apt-get install apache2

#### Activar ssl
	sudo a2enmod ssl

	sudo service apache2 restart	

	sudo mkdir /etc/apache2/ssl


### Archivos Apache2 Config:
#### defualt-ssl.conf
***
	sudo nano /etc/apache2/sites-available/default-ssl.conf

	<IfModule mod_ssl.c>
	 <VirtualHost _default_:443>
                ServerAdmin cristianrodr@gmail.com
                ServerName kycface.mooo.com

                DocumentRoot /var/www/html
		WSGIPassAuthorization On		
                WSGIScriptAlias / /var/www/flask/app.wsgi

		 <Directory /var/www/flask/face>
			WSGIProcessGroup face
		        WSGIApplicationGroup %{GLOBAL}
		        Order deny,allow
		        Allow from all
		</Directory>
		
		ProxyRequests off
		ProxyPreserveHost on

                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/access.log combined

                SSLEngine on


                <FilesMatch "\.(cgi|shtml|phtml|php)$">
                                SSLOptions +StdEnvVars
                </FilesMatch>
                <Directory /usr/lib/cgi-bin>
                                SSLOptions +StdEnvVars
                </Directory>


                SSLCertificateFile      /etc/letsencrypt/live/kycface.mooo.com/fullchain.pem
				SSLCertificateKeyFile /etc/letsencrypt/live/kycface.mooo.com/privkey.pem
				Include /etc/letsencrypt/options-ssl-apache.conf
	</VirtualHost>
	</IfModule>

#### 000-defualt.conf
***
	sudo nano /etc/apache2/sites-available/000-default.conf

	<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	 WSGIDaemonProcess face user=www-data  group=www-data  threads=5 home=/var/www/flask/face
	 WSGIScriptAlias / /var/www/flask/app.wsgi

	<Directory /var/www/flask/face>
	 WSGIProcessGroup face
         WSGIApplicationGroup %{GLOBAL}
         WSGIScriptReloading On
         Order deny,allow
         Allow from all
       </Directory>

	</VirtualHost>


### Configuracion para SSL (Example.com = Dominio) 
Importante  tener el dominio direccionado al servidor.

El primer paso para usar Let's Encrypt para obtener un certificado SSL es instalar el software Certbot en su servidor.

Certbot está en desarrollo muy activo, por lo que los paquetes de Certbot proporcionados por Ubuntu tienden a estar desactualizados. 

***
	sudo add-apt-repository ppa:certbot/certbot

Instale el paquete Apache de Certbot con apt:

***
	sudo apt install python-certbot-apache

Certbot debe poder encontrar el host virtual correcto en su configuración de Apache para que pueda configurar automáticamente SSL. Específicamente, lo hace buscando una ServerNamedirectiva que coincida con el dominio para el que solicita un certificado.

***
	sudo nano /etc/apache2/sites-available/defualt-ssl.conf

	sudo apache2ctl configtest

Si recibe un error, vuelva a abrir el archivo del host virtual y verifique si hay errores tipográficos o caracteres faltantes. Una vez que la sintaxis de su archivo de configuración sea correcta, vuelva a cargar Apache para cargar la nueva configuración:

***
	sudo systemctl reload apache2

Certbot ahora puede encontrar el bloque de VirtualHost correcto y actualizarlo.

#### Permitir HTTPS a través del Firewall
	sudo ufw status
	sudo ufw allow 'Apache Full'
	sudo ufw delete allow 'Apache'
	sudo ufw status

#### Obtención de un certificado SSL
	sudo certbot --apache -d example.com -d www.example.com
	sudo certbot renew --dry-run



## Paso 5, Instalacion y Activacion de Flask
	sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
	sudo apt install python3-venv

### buscar la carpeta que genero la descarga del git clone, face
	cd /var/www/flask/face

	python3.6 -m venv face

	source face/bin/activate
	
	sudo pip install wheel

### Paso 6 Configuracion WSGI
Dado a que el servidor web esta en apache se debe configurar wsgi para generar la conexion y la ejecion de los servicios.

#### Instalacion
	apt-get install libapache2-mod-wsgi

#### Crear archivo app.wsgi

Si no existe el archivo en app.wsgi en la carpeta /var/www/flask/ se debe crear, este archivo es el que ejecuta las llamdas de apache y conecta el python
	
	#!/usr/bin/python3
	import sys

	sys.path.insert(0,"/var/www/flask/face/")

	from face.app import app as application


Reiniciar Apache

	sudo service apache2 restart
