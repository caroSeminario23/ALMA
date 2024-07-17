from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv

app = Flask(__name__)
CORS(app) # Habilita CORS para permitir solicitudes desde cualquier origen

# Clase del Chatbot (sin cambios)
class GeminiChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_context = (
            "Soy una persona que desea saber si vive una situación de violencia intrafamiliar y cómo actuar ante ello. "
            "Ponte en el lugar de un asistente, de nombre ALMA, especializado en proporcionar apoyo y recursos a personas que pueden estar "
            "experimentando violencia intrafamiliar. Realiza una evaluación de mi situación para determinar si vivo un "
            "contexto de violencia intrafamiliar y si fuera así, bríndame apoyo emocional y consejos como también; "
            "aliéntame a denunciar mi caso y oriéntame durante el proceso de denuncia, indicándome los servicios a "
            "los que puedo acceder según el Estado Peruano y los pasos que debo seguir para salir de esa situación."
            "Realiza preguntas una a la vez durante el proceso de evaluación de la situación que te permitan comprender mi contexto,"
            "luego, indícame si se trata de un caso de violencia intrafamiliar y especifica el tipo con detalle;"
            "después, bríndame soporte emocional y aconséjame sobre la manera en que debería actuar; posteriormente, "
            "bríndame instrucciones para denunciar mi caso considerando los servicios a los que puedo acceder."
            "Ofrece ayuda con empatía, comprensión y confidencialidad."
        )
        
        # Carga los módulos de contexto desde un archivo JSON
        with open("/Users/carolinasv/Documents/VS_Code/ALMA/Backend/modulos_contexto.json", "r") as file:
            self.modules = json.load(file)
        
        # Inicializa el contexto actual
        self.current_context = self.base_context

    # Agrega un módulo al contexto actual
    def add_module_to_context(self, module_name):
        if module_name in self.modules:
            self.current_context += f"\n{self.modules[module_name]}"

    # Llama a la API de Google AI Platform
    def call_api(self, prompt):
        # Llama al modelo generativo de Google AI Platform
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        return response.text.strip()

    # Maneja la entrada del usuario y devuelve la respuesta del asistente
    def handle_input(self, user_input):
        # Actualiza el contexto con la entrada del usuario
        self.current_context += f"\nUsuario: {user_input}\nAsistente:"

        # Determina el módulo relevante y agrega al contexto si es necesario
        if "hola" in user_input.lower():
            self.add_module_to_context("inicio")
        elif "violencia intrafamiliar" in user_input.lower():
            self.add_module_to_context("definicion")
        elif "otros nombres" in user_input.lower():
            self.add_module_to_context("nombres")
        elif "objetivo" in user_input.lower():
            self.add_module_to_context("objetivo")
        elif "tipos" in user_input.lower():
            self.add_module_to_context("tipos")
        elif "recursos" in user_input.lower():
            self.add_module_to_context("recursos")
        elif "efectos en la victima" in user_input.lower():
            self.add_module_to_context("efectos_víctima")
        elif "efectos en la sociedad" in user_input.lower():
            self.add_module_to_context("efectos_sociedad")
        elif "causas" in user_input.lower():
            self.add_module_to_context("causas")
        elif "tipos" in user_input.lower():
            self.add_module_to_context("tipos")
        elif "violencia física" in user_input.lower():
            self.add_module_to_context("violencia_física")
        elif "violencia psicológica" in user_input.lower():
            self.add_module_to_context("violencia_psicológica")
        elif "violencia sexual" in user_input.lower():
            self.add_module_to_context("violencia_sexual")
        elif "violencia economica" in user_input.lower():
            self.add_module_to_context("violencia_económica")
        elif "factores" in user_input.lower():
            self.add_module_to_context("factores desenvolvimiento")
        elif "consecuencias fisicas" in user_input.lower():
            self.add_module_to_context("secuela_física")
        elif "consecuencias psicologicas" in user_input.lower():
            self.add_module_to_context("secuela_psicológica")
        elif "consecuencias sociales" in user_input.lower():
            self.add_module_to_context("secuela_social")
        elif "prevencion" in user_input.lower():
            self.add_module_to_context("prevención")
        elif "familia" in user_input.lower():
            self.add_module_to_context("familia")
        elif "tipos de victima" in user_input.lower():
            self.add_module_to_context("tipos_víctima")
        elif "maltrato infantil" in user_input.lower():
            self.add_module_to_context("maltrato_infantil")
        elif "consecuencias del maltrato infantil" in user_input.lower():
            self.add_module_to_context("consecuencia_maltrato")
        elif "abuso sexual" in user_input.lower():
            self.add_module_to_context("abuso_sexual")
        elif "manifestacion del abuso sexual" in user_input.lower():
            self.add_module_to_context("manifestación_abuso")
        elif "deteccion de abuso sexual" in user_input.lower():
            self.add_module_to_context("detectar_abuso")
        elif "accion ante abuso sexual" in user_input.lower():
            self.add_module_to_context("acción_abuso")
        elif "prevencion del abuso sexual" in user_input.lower():
            self.add_module_to_context("prevención_abuso")
        elif "violencia domestica" in user_input.lower():
            self.add_module_to_context("violencia_doméstica")
        elif "expresion de la violencia domestica" in user_input.lower():
            self.add_module_to_context("expresión_doméstica")
        elif "deteccion" in user_input.lower():
            self.add_module_to_context("detectar_doméstica")
        elif "involucrados" in user_input.lower():
            self.add_module_to_context("miembros_familia")
        elif "violencia a los padres" in user_input.lower():
            self.add_module_to_context("violencia_filoparental")
        elif "violencia de genero" in user_input.lower():
            self.add_module_to_context("violencia_género")
        elif "violencia en niños" in user_input.lower():
            self.add_module_to_context("violencia_niños")
        elif "normas" in user_input.lower():
            self.add_module_to_context("normativas")
        elif "objetivo de la ley 30364" in user_input.lower():
            self.add_module_to_context("ley_30364_objetivo")
        elif "principios de la ley 30364" in user_input.lower():
            self.add_module_to_context("ley_30364_principios")
        elif "servicios en peru" in user_input.lower():
            self.add_module_to_context("servicios_perú")
        elif "cai" in user_input.lower():
            self.add_module_to_context("cai")
        elif "ae" in user_input.lower():
            self.add_module_to_context("ae")
        elif "sar" in user_input.lower():
            self.add_module_to_context("sar")
        elif "sau" in user_input.lower():
            self.add_module_to_context("sau")
        elif "linea 100" in user_input.lower():
            self.add_module_to_context("línea_100")
        elif "cem" in user_input.lower():
            self.add_module_to_context("cem")
        elif "chat 100" in user_input.lower():
            self.add_module_to_context("chat_100")
        elif "hrt" in user_input.lower():
            self.add_module_to_context("hrt")
        elif "principios del cem" in user_input.lower():
            self.add_module_to_context("principios_cem")
        elif "derechos humanos" in user_input.lower():
            self.add_module_to_context("principio_ddhh")
        elif "desigualdad" in user_input.lower():
            self.add_module_to_context("principio_desigualdad")
        elif "salud publica" in user_input.lower():
            self.add_module_to_context("principio_salud_publica")
        elif "multicausalidad" in user_input.lower():
            self.add_module_to_context("principio_multicausalidad")
        elif "analisis interdisciplinarios" in user_input.lower():
            self.add_module_to_context("principio_interdisciplinario")
        elif "revictimizacion" in user_input.lower():
            self.add_module_to_context("principio_no_revictimización")
        elif "atencion" in user_input.lower():
            self.add_module_to_context("principio_atención_oportuna")
        elif "interculturalidad" in user_input.lower():
            self.add_module_to_context("principio_interculturalidad")
        elif "confidencialidad" in user_input.lower():
            self.add_module_to_context("principio_confidencialidad")
        elif "derechos de la victima" in user_input.lower():
            self.add_module_to_context("derechos_víctimas")
        elif "denuncia" in user_input.lower():
            self.add_module_to_context("quiénes_denuncian")
        elif "donde denunciar" in user_input.lower():
            self.add_module_to_context("dónde_denunciar")
        elif "derechos durante el proceso" in user_input.lower():
            self.add_module_to_context("derechos_proceso")
        elif "no aceptan mi denuncia" in user_input.lower():
            self.add_module_to_context("no_aceptan_denuncia")
        elif "considerar al denunciar" in user_input.lower():
            self.add_module_to_context("consideraciones_denuncia")
        elif "plan de accion" in user_input.lower():
            self.add_module_to_context("plan_acción_objetivo")
        elif "entidades" in user_input.lower():
            self.add_module_to_context("entidades_involucradas")
        elif "lineamientos" in user_input.lower():
            self.add_module_to_context("lineamientos_estrategicos")
        elif "medidas" in user_input.lower():
            self.add_module_to_context("medidas_protección")
        elif "impacto en niños" in user_input.lower():
            self.add_module_to_context("impacto_niños")
        elif "papel de las instituciones" in user_input.lower():
            self.add_module_to_context("papel_instituciones")
        elif "prevencion" in user_input.lower():
            self.add_module_to_context("legislación_prevención")
        elif "efectos a largo plazo" in user_input.lower():
            self.add_module_to_context("efectos_largo_plazo")
        elif "necesidades" in user_input.lower():
            self.add_module_to_context("necesidades_urgentes")
        elif "factores de riesgo" in user_input.lower():
            self.add_module_to_context("factores_riesgo")
        elif "señales de abuso" in user_input.lower():
            self.add_module_to_context("señales_abuso")
        elif "apoyo" in user_input.lower():
            self.add_module_to_context("estrategias_apoyo")
        elif "intervencion" in user_input.lower():
            self.add_module_to_context("intervenciones_afectivas")
        elif "abordar la violencia" in user_input.lower():
            self.add_module_to_context("abordaje_interdisciplinario")
        elif "educacion" in user_input.lower():
            self.add_module_to_context("educación_comunidad")
        elif "programas de prevecion" in user_input.lower():
            self.add_module_to_context("programas_prevención")
        elif "machismo" in user_input.lower():
            self.add_module_to_context("machismo")
        elif "mecanismos de denuncia" in user_input.lower():
            self.add_module_to_context("mecanismos_denuncia")
        elif "autocuidado" in user_input.lower():
            self.add_module_to_context("autocuidado_víctimas")
        elif "grupos de apoyo" in user_input.lower():
            self.add_module_to_context("grupos_apoyo")
        elif "terapia" in user_input.lower():
            self.add_module_to_context("terapia")
        elif "resiliencia" in user_input.lower():
            self.add_module_to_context("resiliencia")
        
        # Intenta llamar a la API y manejar cualquier error
        try:
            # Llama a la API de Gemini (Google AI Platform en este caso)
            response = self.call_api(self.current_context)

            # Actualiza el contexto con la respuesta del asistente
            self.current_context += f" {response}"

            return response
        
        except ValueError as ve:
            error = "Por favor reformula tu pregunta o respuesta, ya que contiene información sensible con la que no puedo tratar por políticas establecidas."
            return f"Advertencia: {error}"

# Carga las variables de entorno desde .env
load_dotenv()

# Verifica y carga la clave API
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("No se encontró la clave API. Asegúrate de haber definido la variable de entorno 'GEMINI_CHATBOT_API_KEY' en el archivo .env.")
else:
    print("Clave API cargada exitosamente.")

# Configura el API Key para Google AI Platform
genai.configure(api_key=api_key)

# Inicia el chatbot
chatbot = GeminiChatbot(api_key)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chatbot.handle_input(user_input)
    return jsonify({'response': response})

@app.route('/guardar_mensaje', methods=['POST'])
def guardar_mensaje():
    data = request.json
    email = data.get('email')
    mensaje = data.get('mensaje')

    if not email or not mensaje:
        return jsonify({"error": "Email y mensaje son requeridos"}), 400

    # Ruta del archivo CSV
    csv_file_path = 'Backend/mensajes_usuarios.csv'

    # Verificar si el archivo CSV existe
    file_exists = os.path.isfile(csv_file_path)

    # Escribir en el archivo CSV
    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Email', 'Mensaje']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escribir el encabezado solo si el archivo es nuevo
        if not file_exists:
            writer.writeheader()

        writer.writerow({'Email': email, 'Mensaje': mensaje})

    return jsonify({"message": "Mensaje guardado exitosamente"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
