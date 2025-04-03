<div align="center">
  <img src="https://github.com/marcmarant/reparto-habitaciones-sc/raw/master/icon.ico" alt="Logo del Colegio Mayor Santa Cruz" width="100"/>
</div>

# Programa de Asignación de Habitaciones para el *Colegio Mayor de Santa Cruz*

En este repositorio esta el código en python del programa usado para el reparto de habitaciones en el *[Colegio Mayor de Santa Cruz](https://es.wikipedia.org/wiki/Colegio_Mayor_Santa_Cruz)*.
De forma que cualquier colegial pueda acceder tanto al algoritmo que determina la habitación que se le será asignada para el siguiente curso como descargarse el código para poder probarlo el mismo. 

## Instalación ⬇️​

### Descarga el ejecutable para Windows:
<p align="center">
  <a href="https://github.com/TU_USUARIO/TU_REPO/releases/download/v1.0.0/reparto_habitaciones_sc.exe" target="_blank">
    <img src="https://img.shields.io/badge/Descargar-main.exe-blue?style=for-the-badge&logo=windows" style="border-radius: 10px; background: #222; padding: 10px;">
  </a>
</p>

Para ejecutar el programa en python clona el repo y ejecuta:
```bash
python main.py
```
Adicionalmente si tienes un sistema Linux y no tienes tkinter instalado deberas ejecutar:
```bash
sudo apt-get install python3-tk
```

## Algoritmo 📜

El algoritmo de reparto de habitaciones funciona de la siguiente manera:

1.  Se toman los datos de cada colegial, incluyendo:
    - **Habitación actual**
    - **Años en el colegio**
    - **Creditos obtenidos en el año**
    - **Lista de habitaciones solicitadas en orden de preferencia**

2. Si un colegial no ha solicitado ninguna habitación, se mantiene en su habitación actual.

3. Si un colegial ha solicitado habitaciones, se le ira intentado asignar la primera habitación disponible en el orden de preferencia indicado por el colegial.

4. Al intentar asignar una habitación a varios colegiales esta será asignada al colegial que:
    - Haya obtenido más creditos durante el actual curso académico contando hasta un **máximo de 60 creditos**.
    - En caso de empate a creditos la habitación será asignada por veterania al colegial que lleve más años en el colegio.
    - En caso de un nuevo empate se asignará la habitación de forma trivial por orden alfabético.

5. Si un que colegial ha solicitado habitaciones no obtiene el cambio a ninguna de ellas se mantendrá en la misma habitación.
