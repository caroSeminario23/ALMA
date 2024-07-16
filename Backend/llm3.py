import json
import textwrap
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Clase del Chatbot
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
        
        with open("/Users/carolinasv/Documents/VS_Code/ALMA/Backend/modulos_contexto.json", "r") as file:
            self.modules = json.load(file)
        
        self.current_context = self.base_context

    def add_module_to_context(self, module_name):
        if module_name in self.modules:
            self.current_context += f"\n{self.modules[module_name]}"

    def call_api(self, prompt):
        # Llama al modelo generativo de Google AI Platform
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()

    def handle_input(self, user_input):
        # Actualiza el contexto con la entrada del usuario
        self.current_context += f"\nUsuario: {user_input}\nAsistente:"

        # Determina el módulo relevante y agrega al contexto si es necesario
        if "recursos" in user_input.lower():
            self.add_module_to_context("recursos")
        elif "bienestar" in user_input.lower():
            self.add_module_to_context("inicio")
        elif "empatía" in user_input.lower():
            self.add_module_to_context("empatía")
        elif "definicion_violencia intrafamiliar" in user_input.lower():
            self.add_module_to_context("definicion de violencia intrafamiliar")

        # Llama a la API de Gemini (Google AI Platform en este caso)
        response = self.call_api(self.current_context)

        # Actualiza el contexto con la respuesta del asistente
        self.current_context += f" {response}"

        return response


# Carga las variables de entorno desde .env
load_dotenv()

# Verifica y carga la clave API
api_key = os.environ["API_KEY"]
if not api_key:
    raise ValueError("No se encontró la clave API. Asegúrate de haber definido la variable de entorno 'GEMINI_CHATBOT_API_KEY' en el archivo .env.")
else:
    print("Clave API cargada exitosamente.")

# Configura el API Key para Google AI Platform
genai.configure(api_key=api_key)

# Inicia el chatbot
chatbot = GeminiChatbot(api_key)

# Interacción con el chatbot
print("Chatbot iniciado. Escribe 'salir' para terminar.")
while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        print("Chatbot finalizado.")
        break
    response = chatbot.handle_input(user_input)
    print("Asistente:", response)  # Mostrar la respuesta directamente
