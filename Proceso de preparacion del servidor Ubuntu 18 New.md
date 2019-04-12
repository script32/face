### Proceso de preparacion del servidor Ubuntu 18.04
#### Paso 1. Actualizacion e Instalacion
***
	sudo apt-get update
	sudo apt-get update
	sudo apt-get install git

	sudo apt-get install python3.6
	sudo apt-get install python-dev python-pip python3-dev python3-pip

	sudo apt-get install build-essential cmake pkg-config
	sudo apt-get install libx11-dev libatlas-base-dev
	sudo apt-get install libgtk-3-dev libboost-python-dev


#### Paso 2. Compilar DLib
Esta libreria se puede instalar en cualquier carpeta del servidor, en el servidor de prueba se creo una carpeta de la siguiente manera:

	mkdir /work

	cd /work

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

#### Paso 3. Compilar el módulo de Python 
Se sigue estando en la direccion /work

	workon facecourse-py3

	cd dlib-19.6

	python setup.py install


##### Paso 4. limpiar 

	rm -rf dist
	
	rm -rf tools/python/build
	
	rm python_examples/dlib.so
***

#### Paso 5. Librerias Python

	sudo -H pip3 install -U pip numpy

	pip3 install setuptools
	pip3 install wheel
	pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython
	pip3 install Flask
	pip3 install Flask-Cors
	pip3 install Flask-JWT
	pip3 install Flask-JWT-Extended
	pip3 install Flask-RESTful
	pip3 install Flask-SocketIO
	pip3 install jsonify
	pip3 install Pillow 
	pip3 install psycopg2
	pip3 install psycopg2-binary
	pip3 install dlib
	pip3 install face-recognition
	pip3 install opencv-python

## Paso 6. Clonar Github Face
### Crear carpeta de la aplicacion
	mkdir /var/www/flask/
### Posicionarse en la carpeta
	cd /var/www/flask
### Clonar proyecto
	git clone https://github.com/script32/face
### Mover archivo app.wsgi
	cd /var/www/flask/face
	mv app.wsgi /var/www/flask/app.wsgi

### Probar microservicio.
Hasta aqui ya podemo probar localmente el microservicio flask, para eso tenemos que ir a la carpeta face y ejecutar app.py

	cd /var/www/flask/face
	python3 app.py

debe retornar que la aplicacion esta operativa en el puerto 5000, con ctrl + c se cierra la aplicacion

	CTRL + C


## Paso6. Instalacion de Apache2
Ahora necesitamos exponer el microservico a la red, para esto utilizaremos apache, si no esta instalado, comenzamos con lo basico:

	sudo apt install apache2

Verificamos el Firewall

	sudo ufw app list

	Output
	Available applications
	Apache
	Apache Full
	Apache Secure
	OpenSSH

Habilitamos apache en el ufw

	sudo ufw allow 'Apache'

Verificar el cambio:
	
	sudo ufw status

Output
	
	Status: active

	To                         Action      From
	--                         ------      ----
	OpenSSH                    ALLOW       Anywhere                  
	Apache                     ALLOW       Anywhere                  
	OpenSSH (v6)               ALLOW       Anywhere (v6)             
	Apache (v6)                ALLOW       Anywhere (v6)


	sudo systemctl status apache2

Output

	apache2.service - The Apache HTTP Server
  
	Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
	Drop-In: /lib/systemd/system/apache2.service.d
           └─apache2-systemd.conf
	Active: active (running) since Tue 2018-04-24 20:14:39 UTC; 9min ago
	Main PID: 2583 (apache2)
    Tasks: 55 (limit: 1153)
	CGroup: /system.slice/apache2.service
           ├─2583 /usr/sbin/apache2 -k start
           ├─2585 /usr/sbin/apache2 -k start
           └─2586 /usr/sbin/apache2 -k start

hasta aqui deberias poder acceder al puerto 80, pero no hemos configurado que apache se conecte a nuestro microservicio. Ahora continuaremos con la confiracion ssl, con cerbot y un dns dinamico generado en https://freedns.afraid.org/


Primero agregamos el repositorio de Cerbot
	
	sudo add-apt-repository ppa:certbot/certbot

Instalamos Cerbot

	sudo apt install python-certbot-apache

el subdominio de la prueba es kycface.mooo.com, es importante que esta referencia de aqui en adelante la modifique con el subdominio que registro:

	sudo nano /etc/apache2/sites-available/kycface.mooo.com.conf

ingresar la siguiente linea:

	ServerName example.com;

guardar y salir.

verifique la sintaxis de sus ediciones de configuración:

	sudo apache2ctl configtest

Debe devolver un OK

Una vez que la sintaxis de su archivo de configuración sea correcta, vuelva a cargar Apache para cargar la nueva configuración:

	sudo systemctl reload apache2


Verificamos el ufw

	sudo ufw status

Output
	
	Status: active

	To                         Action      From
	--                         ------      ----
	OpenSSH                    ALLOW       Anywhere                  
	Apache                     ALLOW       Anywhere                  
	OpenSSH (v6)               ALLOW       Anywhere (v6)             
	Apache (v6)                ALLOW       Anywhere (v6)


Para permitir además que entre el tráfico HTTPS, permita el perfil completo de Apache y elimine la asignación de perfil de Apache redundante:

	sudo ufw allow 'Apache Full'
	sudo ufw delete allow 'Apache'


	sudo ufw status


Output
	
	Status: active

	To                         Action      From
	--                         ------      ----
	OpenSSH                    ALLOW       Anywhere                  
	Apache Full                ALLOW       Anywhere                  
	OpenSSH (v6)               ALLOW       Anywhere (v6)             
	Apache Full (v6)           ALLOW       Anywhere (v6)    



A continuación, ejecutemos Certbot y obtengamos nuestros certificados.


Certbot proporciona una variedad de formas de obtener certificados SSL a través de complementos. El complemento de Apache se encargará de reconfigurar Apache y volver a cargar la configuración cuando sea necesario. Para usar este plugin, escriba lo siguiente:


	sudo certbot --apache -d kycface.mooo.com -d kycface.mooo.com

Esto se ejecuta certbotcon el --apachecomplemento, y se usa -dpara especificar los nombres para los que desea que el certificado sea válido.

Si es la primera vez que se ejecuta certbot, se le solicitará que ingrese una dirección de correo electrónico y acepte los términos del servicio. Después de hacerlo, certbotse comunicará con el servidor de Let's Encrypt, luego ejecutará un desafío para verificar que usted controla el dominio para el que solicita un certificado.

Si tiene éxito, certbotle preguntará cómo desea configurar sus ajustes de HTTPS:

Output
	
	Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
	-------------------------------------------------------------------------------
	1: No redirect - Make no further changes to the webserver configuration.
	2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
	new sites, or if you're confident your site works on HTTPS. You can undo this
	change by editing your web server's configuration.
	-------------------------------------------------------------------------------
	Select the appropriate number [1-2] then [enter] (press 'c' to cancel):


Seleccione su elección y luego pulsa ENTER. La configuración se actualizará, y Apache se volverá a cargar para recoger la nueva configuración. certbotfinalizará con un mensaje que le informará que el proceso se realizó correctamente y dónde se almacenan sus certificados:


Output

	IMPORTANT NOTES:
	- Congratulations! Your certificate and chain have been saved at:
	/etc/letsencrypt/live/example.com/fullchain.pem
	Your key file has been saved at:
	/etc/letsencrypt/live/example.com/privkey.pem
	Your cert will expire on 2018-07-23. To obtain a new or tweaked
	version of this certificate in the future, simply run certbot again
	with the "certonly" option. To non-interactively renew *all* of
	your certificates, run "certbot renew"
	- Your account credentials have been saved in your Certbot
	configuration directory at /etc/letsencrypt. You should make a
	secure backup of this folder now. This configuration directory will
	also contain certificates and private keys obtained by Certbot so
	making regular backups of this folder is ideal.
	- If you like Certbot, please consider supporting our work by:

	Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
	Donating to EFF:                    https://eff.org/donate-le


Los certificados de Let's Encrypt solo son válidos por noventa días. Esto es para animar a los usuarios a automatizar su proceso de renovación de certificados. El certbotpaquete que instalamos se encarga de esto al agregar un script de renovación a /etc/cron.d. Este script se ejecuta dos veces al día y renovará automáticamente cualquier certificado que esté dentro de los treinta días de vencimiento.


	sudo certbot renew --dry-run


Ahora enlazaremos el python con el apache, con mod-wsgi


### Configuracion WSGI
Dado a que el servidor web esta en apache se debe configurar wsgi para generar la conexion y la ejecion de los servicios.

#### Instalacion
	apt-get install libapache2-mod-wsgi
	


### Archivos Apache2 Config:
Hay que verificar que solo existan 2 conf 000-default.conf y default-ssl.conf, si existe otro se tiene que eliminar y realziar un reload del apache



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


Verificamos que este todo Ok con los archivos conf

	sudo apache2ctl configtest

Si recibe un error, vuelva a abrir el archivo del host virtual y verifique si hay errores tipográficos o caracteres faltantes. Una vez que la sintaxis de su archivo de configuración sea correcta, vuelva a cargar Apache para cargar la nueva configuración:

***
	sudo systemctl reload apache2


Con esto ya podemos iniciar la api, si por algun motivo no inicia verificar el archivo app.wsgi

	nano /var/www/flask/app.wsgi

debe tener el siguiente formato, sino modificar.
	
	#!/usr/bin/python3
	import sys

	sys.path.insert(0,"/var/www/flask/face/")

	from face.app import app as application


Reiniciar Apache

	sudo service apache2 restart
