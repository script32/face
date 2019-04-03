#Proceso de preparacion del servidor Ubuntu 18.04

##Paso 1. Actualizacion e instalacion

sudo apt-get update
sudo apt-get install git

sudo apt-get install python3.6
sudo apt-get install python-dev python-pip python3-dev python3-pip

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libx11-dev libatlas-base-dev
sudo apt-get install libgtk-3-dev libboost-python-dev

sudo apt-get install nginx

sudo -H pip2 install -U pip numpy
sudo -H pip3 install -U pip numpy

pip2 install virtualenv virtualenvwrapper
pip3 install virtualenv virtualenvwrapper

##Paso 1.1 Instalar virtual environment
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

##Paso 2: Compilar DLib
###Paso 2.1: Compilar binario de C ++

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

###Paso 2.2: Compilar el módulo de Python
####Para Python 2
workon facecourse-py2
 
####Para Python 3
workon facecourse-py3

#####mover al directorio raíz de dlib
cd dlib-19.6
python setup.py install
#####limpiar (este paso es necesario si desea compilar dlib para Python2 y Python3)
rm -rf dist
rm -rf tools/python/build
rm python_examples/dlib.so

###Comprobar la instlacion blib Python3
pip3 install dlib

###Instalar face_recognition Python3
pip3 install face_recognition

###Instalar buscador de archivo bien util
apt-get install apt-file



##Paso 3. Clonar Github Face
git clone https://github.com/script32/face


##Paso 4. Configuracion Apache y Firewall

sudo ufw app list
sudo ufw allow 'Apache2 HTTP'
sudo ufw allow 22/tcp
sudo ufw allow 2222/tcp
sudo ufw allow 5000/tcp


###Archivos Apache2 Config:
####defual-ssl.conf
***
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

####000-defualt.conf
***
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

###Configuracion para SSL (Example.com = Dominio) 
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
	sudo nano /etc/apache2/sites-available/defual-ssl.conf

	sudo apache2ctl configtest

Si recibe un error, vuelva a abrir el archivo del host virtual y verifique si hay errores tipográficos o caracteres faltantes. Una vez que la sintaxis de su archivo de configuración sea correcta, vuelva a cargar Apache para cargar la nueva configuración:

***
	sudo systemctl reload apache2

Certbot ahora puede encontrar el bloque de VirtualHost correcto y actualizarlo.

Permitir HTTPS a través del Firewall
sudo ufw status
sudo ufw allow 'Apache Full'
sudo ufw delete allow 'Apache'
sudo ufw status

Obtención de un certificado SSL
sudo certbot --apache -d example.com -d www.example.com
sudo certbot renew --dry-run



##Paso 5, Instalacion y Activacion de Flask
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv

###buscar la carpeta que genero la descarga del git clone, face
cd path/face

python3.6 -m venv face

source faceenv/bin/activate
sudo pip install wheel

pip3 install gunicorn flask

###comprobar que no tenga error y generar gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app

CTRL-C

deactivate

sudo nano /etc/systemd/system/face.service

	[Unit]
	Description=Gunicorn instance to serve face
	After=network.target

	[Service]
	User=root
	Group=www-data
	WorkingDirectory=/root/work/face
	Environment="PATH=/root/work/face/bin"
	ExecStart=/root/work/face/bin/gunicorn --workers 3 --bind unix:face.sock -m 007 wsgi:app

	[Install]
	WantedBy=multi-user.target
	

sudo systemctl start face
sudo systemctl enable face

sudo systemctl status face
	
	face.service - Gunicorn instance to serve face
 	Loaded: loaded (/etc/systemd/system/face.service; enabled; vendor preset: enabled)
   	Active: active (running) since Sat 2019-03-16 11:41:23 CDT; 31min ago
 	Main PID: 4259 (gunicorn)
    Tasks: 4 (limit: 4915)
   	CGroup: /system.slice/face.service
           |-4259 /root/work/face/bin/python3.6 /root/work/face/bin/gunicorn --workers 3 --bind unix:face.sock -m 007 wsgi:app
           |-4261 /root/work/face/bin/python3.6 /root/work/face/bin/gunicorn --workers 3 --bind unix:face.sock -m 007 wsgi:app
           |-4269 /root/work/face/bin/python3.6 /root/work/face/bin/gunicorn --workers 3 --bind unix:face.sock -m 007 wsgi:app
           `-4270 /root/work/face/bin/python3.6 /root/work/face/bin/gunicorn --workers 3 --bind unix:face.sock -m 007 wsgi:app

	Mar 16 11:41:23 baremetal01 systemd[1]: Started Gunicorn instance to serve face.
	Mar 16 11:41:23 baremetal01 gunicorn[4259]: [2019-03-16 11:41:23 -0500] [4259] [INFO] Starting gunicorn 19.9.0
	Mar 16 11:41:23 baremetal01 gunicorn[4259]: [2019-03-16 11:41:23 -0500] [4259] [INFO] Listening at: unix:face.sock (4259)
	Mar 16 11:41:23 baremetal01 gunicorn[4259]: [2019-03-16 11:41:23 -0500] [4259] [INFO] Using worker: sync
	Mar 16 11:41:23 baremetal01 gunicorn[4259]: [2019-03-16 11:41:23 -0500] [4261] [INFO] Booting worker with pid: 4261
	Mar 16 11:41:23 baremetal01 gunicorn[4259]: [2019-03-16 11:41:23 -0500] [4269] [INFO] Booting worker with pid: 4269
	Mar 16 11:41:23 baremetal01 gunicorn[4259]: [2019-03-16 11:41:23 -0500] [4270] [INFO] Booting worker with pid: 4270
	

sudo nano /etc/nginx/sites-available/face
	
	server {
    	listen 8000;
    	listen [::]:8000;

   	location / {
        	include proxy_params;
        	proxy_pass http://unix:/root/work/face/face.sock;

    	}
	}
	

sudo ln -s /etc/nginx/sites-available/face /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl restart nginx

sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'

###Comandos mas usados
####sudo journalctl -u face: Chekea los logs de la aplicacion.
####sudo systemctl status face: ve el status de la aplicacion
####sudo systemctl start face: inicia la apliaccion
####sudo systemctl stop face: para la aplicacion


