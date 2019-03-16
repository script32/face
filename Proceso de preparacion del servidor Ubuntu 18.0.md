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


##Paso 4. Configuracion Nginx y Firewall

sudo apt install nginx

sudo ufw app list
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 22/tcp
sudo ufw allow 2222/tcp
sudo ufw allow 8000/tcp


systemctl status nginx

Referencia
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04


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
####sudo less /var/log/nginx/error.log: ver el log de errores de nginx.
####sudo less /var/log/nginx/access.log: ver los de acceso de nginx.
####sudo journalctl -u nginx: ver log en el proceso de nginx.
####sudo journalctl -u face: Chekea los logs de la aplicacion.
####sudo sudo systemctl status face: ve el status de la aplicacion
####sudo sudo systemctl start face: inicia la apliaccion
####sudo sudo systemctl stop face: para la aplicacion


