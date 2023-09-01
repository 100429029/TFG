# TFG
* Tener instalado Python 3.11. (Con Python 3.9.x no funciona).

* Tener instalado el juego Starcraft 2: [https://starcraft2.com/es-es/]

* Descargar este repositorio

* Mover el archivo “BerlingradAIE.SC2Map” del repositorio a la carpeta install-dir/Maps/, siendo install-dir la dirección de instalación del juego Starcraft2, por defecto Archivos De Programa (x86)/Starcraft 2.

* Tener instalada la librería de la API: 
```
        pip install --upgrade burnysc2
```    
* Ahora el proyecto debería estar listo para ejecutar.
```
        python main.py
```    
* Personalmente he encontrado un molesto problema con la librería ‘protobuf’ que he conseguido solucionar haciendo downgrade de la misma:
```
        pip install protobuf==3.20.*
```
