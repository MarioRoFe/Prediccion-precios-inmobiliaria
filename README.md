# Acerca del proyecto
![alt text](https://github.com/MarioRoFe/Prediccion-precios-inmobiliaria/blob/main/streamlit_dev/visuales/visual_home_app.png?raw=true)

En este proyecto se puede predecir el precio de una casa ubicada en la ciudad de Oaxaca de Juárez México. 

También se puede tomar una casa cuyo precio ya se conozca y compararlo con el precio de mercado predicho por el modelo para saber si se encuentra sobre o debajo del precio de mercado.

Este proyecto se realizó con el propósito de ayudar a una inmobiliaria local a analizar sus precios y ajustar sus estrategias de ventas.

# Desarrollado con 
* Python 3.9

# Pasos en el desarrollo del proyecto
Para la elaboración de este proyecto se llevaron a cabo los sigientes pasos:
* Extracción de datos mediante webscraping con Scrapy y Selenium
* Limpieza y análisis exploratorio de datos con Numpy y Pandas
* Entrenamiento, evaluación y selección del modelo con Scikit-Learn
* Desarrollo de aplicación web con Streamlit

# Probar el proyecto
Puedes probar el proyecto en el siguiente enlace

[https://prediccion-precios-inmobiliaria-oaxaca.streamlit.app/](https://prediccion-precios-inmobiliaria-oaxaca.streamlit.app/)
### Correrlo de manera local
Si prefieres correrlo de manera local tienes que ejecutar

```pip install -r .\requirements.txt```

luego

```streamlit run streamlit_dev/main.py```

y visitar

[http://localhost:8501](http://localhost:8501)
