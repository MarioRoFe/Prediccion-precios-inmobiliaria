import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json
import pandas as pd
import joblib
import time

# ----------------------------- CONFIGURACIÓN INICIAL -----------------------------
st.set_page_config(page_title="Predicción de precios", page_icon="🏡")

# Elementos que se usarán en la sección main
main_text = """
    <style>
    .centered-text-subtitle {
        text-align: justify;
        font-size: 16px;
    }
    </style>
    <div class="centered-text-subtitle">
    Este proyecto está pensado para ayudar a un agente
    inmobiliario cuya operación se lleve a cabo en 
    en la ciudad de Oaxaca de Juárez.<br><br>

    Con la ayuda de un modelo de Machine Learning entrenado
    con datos de cientos de casas de la zona, se puede calcular 
    el precio de mercado de una casa cuyo valor se desconozca.<br>

    También se puede comparar el precio ya conocido de una
    casa con el precio de mercado, calculado por el modelo.<br>

    Si te interesa conocer con más detalle el funcionamiento del
    modelo puedes encontrarlo en mi repositorio o bien, contactarme
    en mis redes sociales o vía email.<br>
    </div>
"""

with open("./streamlit_dev/visuales/main_animation.json") as source_main_animation:
    main_animation = json.load(source_main_animation)


# Titulo de la página
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
        font-size: 35px;
        font-weight: bold
    }
    </style>
    <div class="centered-text">ESTIMACIÓN DE PRECIOS DE VIVIENDAS EN OAXACA DE JUAREZ</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


# ----------------------------- BARRA DE PAGINACIÓN -----------------------------
selected = option_menu(
    menu_title=None,
    options=["Home", "Predecir", "Comparar"],
    icons=["house", "coin", "arrow-left-right"],
    default_index=0,
    menu_icon="list",
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#262730"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {
            "font-size": "25px",
            "text-aling": "left",
            "margin": "0px",
            "--hover-color": "#053C5E",
        },
        "nav-link-selected": {"background-color": "#b21e35"},
    },
)


# ----------------------------- SECCIÓN HOME -----------------------------
if selected == "Home":
    # ----- Side bar -----
    with st.sidebar:
        st.header("Bienvenido!!!")
        st.markdown(main_text, unsafe_allow_html=True)

        col_bar1, col_bar2, col_bar3 = st.columns([0.10, 0.10, 0.70])
        with col_bar1:
            st.markdown(
                """
                <a href='https://github.com/MarioRoFe/Prediccion-precios-inmobiliaria' target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#b21e35" class="bi bi-github" viewBox="0 0 16 16">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                </a>
                """,
                unsafe_allow_html=True,
            )
        with col_bar2:
            st.markdown(
                """
                <a href='https://www.linkedin.com/in/mario-rodriguez-felix-921a297a/' target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#b21e35" class="bi bi-linkedin" viewBox="0 0 16 16">
                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                </svg>
                </a>
                """,
                unsafe_allow_html=True,
            )
        with col_bar3:
            st.markdown(
                """
                <div style="display: flex; align-items: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="#b21e35" class="bi bi-envelope" viewBox="0 0 16 16" style="margin-top: -13px;">
                        <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
                    </svg>
                    <p style="margin-left: 10px;">mario.r.felix19@gmail.com</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    left_col_home, center_col_home, right_col_home = st.columns([0.20, 0.60, 0.20])
    with center_col_home:
        st_lottie(
            main_animation,
            width=400,
            height=400,
            loop=True,
            speed=1,
        )


# ----------------------------- SECCIÓN PREDICCIÓN -----------------------------
if selected == "Predecir":
    left_col_predecir, right_col_predecir = st.columns((2, 1))

    #                        ----- Formularios -----
    with left_col_predecir:
        # Subtítulo del formulario
        st.markdown(
            """
            <style>
            .centered-text-subtitle {
                text-align: center;
                font-size: 25px;
                font-weight: bold
            }
            </style>
            <div class="centered-text-subtitle">Ingresa los datos de la propiedad</div>
            """,
            unsafe_allow_html=True,
        )

        # Se crea un campo formulario que contendrá los campos para
        # recibir los inputs del ususario
        with st.form(key="Form1", clear_on_submit=True):
            bedrooms = st.number_input("Número de Recámaras", value=1)
            bathrooms = st.number_input("Número de Baños", value=1.0)
            built_area = st.number_input("Tamaño de Construcción (M2)", value=1.0)
            land_area = st.number_input("Tamaño de Terreno (M2)", value=1.0)
            location = st.selectbox(
                label="""Selecciona la ubicación""",
                help="Tomando como referencia al zócalo de la ciudad",
                options=("Nor-Oeste", "Nor-Este", "Sur-Oeste", "Sur-Este"),
            )
            enter = st.form_submit_button("Enter")

    #                        ----- Resultado -----
    with right_col_predecir:
        # Cargando el modelo entrenado previamente
        model_loaded = joblib.load("./notebooks/best_model.pkl")

        # Se cambia el nombre de los imputs de location
        # Esto para que puedan ser usados por el modelo
        if location == "Nor-Oeste":
            location = "nw"
        elif location == "Nor-Este":
            location = "ne"
        elif location == "Sur-Oeste":
            location = "sw"
        else:
            location = "se"

        data = pd.DataFrame(
            data={
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "built_area": built_area,
                "land_area": land_area,
                "location": location,
            },
            index=[0],
        )

        # En esta sección se muestra la estimació del modelo
        st.markdown(
            """
            <style>
            .centered-text_final {
                text-align: center;
                font-size: 25px;
                font-weight: bold
            }
            </style>
            <div class="centered-text_final">Resultado</div>
            """,
            unsafe_allow_html=True,
        )

        #                        ----- Resultado -----
        with st.form("Form2", clear_on_submit=True):
            if enter:
                try:
                    st.markdown(
                        """
                        <style>
                        .centered-text_predict {
                            text-align: center;
                            font-size: 25px;
                            font-weight: bold
                        }
                        </style>
                        <div class="centered-text_predict">Precio Estimado</div>
                        """,
                        unsafe_allow_html=True,
                    )
                    with st.spinner("Calculando..."):
                        time.sleep(1)
                    prediction = model_loaded.predict(data)[0]
                    prediction_format = "${:,.0f}".format(prediction)
                    st.markdown(
                        f'<div style="font-size: 34px; margin-top: 20px; text-align: center;">{prediction_format}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("---")

                    with open(
                        "./streamlit_dev/visuales/animation_house.json"
                    ) as source_house:
                        animation_house = json.load(source_house)
                    # se ejecuta la animación
                    st_lottie(
                        animation_house, width=200, height=232, loop=False, speed=3
                    )
                except:
                    st.error("Ups, un error ha ocurrido, intenta de nuevo")

            back = st.form_submit_button("Back")

    st.markdown("---")


# ----------------------------- SECCIÓN COMPARACIÓN -----------------------------
if selected == "Comparar":
    left_col_comparar, right_col_comparar = st.columns((2, 1))

    #                        ----- Formularios -----
    with left_col_comparar:
        # Subtítulo del formulario
        st.markdown(
            """
            <style>
            .centered-text-subtitle {
                text-align: center;
                font-size: 25px;
                font-weight: bold
            }
            </style>
            <div class="centered-text-subtitle">Ingresa los datos de la propiedad</div>
            """,
            unsafe_allow_html=True,
        )

        # Se crea un campo formulario que contendrá los campos para
        # recibir los inputs del ususario
        with st.form(key="Form3", clear_on_submit=True):
            price = st.number_input("Precio de la casa", value=1.0)
            bedrooms = st.number_input("Número de Recámaras", value=1)
            bathrooms = st.number_input("Número de Baños", value=1.0)
            built_area = st.number_input("Tamaño de Construcción (M2)", value=1.0)
            land_area = st.number_input("Tamaño de Terreno (M2)", value=1.0)
            location = st.selectbox(
                label="""Selecciona la ubicación""",
                help="Tomando como referencia al zócalo de la ciudad",
                options=("Nor-Oeste", "Nor-Este", "Sur-Oeste", "Sur-Este"),
            )
            enter = st.form_submit_button("Enter")

    #                        ----- Resultado -----
    with right_col_comparar:
        # Cargando el modelo entrenado previamente
        model_loaded = joblib.load("./notebooks/best_model.pkl")

        # Se cambia el nombre de los imputs de location
        # Esto para que puedan ser usados por el modelo
        if location == "Nor-Oeste":
            location = "nw"
        elif location == "Nor-Este":
            location = "ne"
        elif location == "Sur-Oeste":
            location = "sw"
        else:
            location = "se"

        data = pd.DataFrame(
            data={
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "built_area": built_area,
                "land_area": land_area,
                "location": location,
            },
            index=[0],
        )

        # En esta sección se muestra la estimación del modelo
        st.markdown(
            """
            <style>
            .centered-text_final {
                text-align: center;
                font-size: 25px;
                font-weight: bold
            }
            </style>
            <div class="centered-text_final">Resultado</div>
            """,
            unsafe_allow_html=True,
        )

        #                        ----- Animación Resultado -----
        with st.form("Form4", clear_on_submit=True):
            if enter:
                try:
                    with st.spinner("Calculando..."):
                        time.sleep(1)
                    prediction = model_loaded.predict(data)[0]
                    prediction_format = "${:,.0f}".format(prediction)
                    price_format = "${:,.0f}".format(price)
                    st.markdown(
                        """
                        <style>
                        .centered-text_p_real {
                            text-align: center;
                            font-size: 25px;
                            font-weight: bold
                        }
                        </style>
                        <div class="centered-text_p_real">Precio Actual</div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if prediction > price:
                        st.markdown(
                            f'<div style="font-size: 34px; margin-top: 0px; text-align: center; color: #38b000;">{price_format}</div>',
                            unsafe_allow_html=True,
                        )
                        st.write("---")
                    else:
                        st.markdown(
                            f'<div style="font-size: 34px; margin-top: 0px; text-align: center; color: #b21e35;">{price_format}</div>',
                            unsafe_allow_html=True,
                        )
                        st.write("---")

                    st.markdown(
                        """
                        <style>
                        .centered-text_p_estimado {
                            text-align: center;
                            font-size: 25px;
                            font-weight: bold;
                            margin-top: -10px;
                        }
                        </style>
                        <div class="centered-text_p_estimado">Precio Estimado</div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<div style="font-size: 34px; margin-top: 0px; text-align: center;">{prediction_format}</div>',
                        unsafe_allow_html=True,
                    )
                    st.write("---")

                    if prediction > price:
                        sub_precio = "Se encuentra por debajo del precio de mercado"
                        st.write(
                            f'<div style="font-size: 18px; margin-top: -10px; text-align: center;">{sub_precio}</div>',
                            unsafe_allow_html=True,
                        )
                        with open(
                            "./streamlit_dev/visuales/green_animation.json"
                        ) as source_house:
                            animation_house = json.load(source_house)
                        # se ejecuta la animación
                        st_lottie(
                            animation_house, width=200, height=143, loop=False, speed=1
                        )
                    else:
                        sobre_precio = "Se encuentra por encima del precio de mercado"
                        st.write(
                            f'<div style="font-size: 18px; margin-top: -10px; text-align: center;">{sobre_precio}</div>',
                            unsafe_allow_html=True,
                        )
                        with open(
                            "./streamlit_dev/visuales/red_animation.json"
                        ) as source_house:
                            animation_house = json.load(source_house)
                        # se ejecuta la animación
                        st_lottie(
                            animation_house, width=200, height=143, loop=False, speed=1
                        )
                except:
                    st.error("Ups, un error ha ocurrido, intenta de nuevo")

            back = st.form_submit_button("Back")

    st.markdown("---")
