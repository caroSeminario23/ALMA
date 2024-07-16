import json
import requests
from dotenv import load_dotenv
import os
#import pathlib
import textwrap
import google.generativeai as genai
#from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

class GeminiChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_context = ("Soy una persona que desea saber si vive una situación de violencia intrafamiliar y cómo actuar ante ello. " 
                             "Ponte en el lugar de un asistente especializado en proporcionar apoyo y recursos a personas que pueden estar "
                             "experimentando violencia intrafamiliar. Realiza una evaluación de mi situación para determinar si vivo un "
                             "contexto de violencia intrafamiliar y si fuera así, bríndame apoyo emocional y consejos como también; "
                             "aliéntame a denunciar mi caso y oriéntame durante el proceso de denuncia, indicándome los servicios a "
                             "los que puedo acceder según el Estado Peruano y los pasos que debo seguir para salir de esa situación."
                             "Realiza preguntas durante el proceso de evaluación de la situación que te permitan comprender mi contexto,"
                             "luego, indícame si se trata de un caso de violencia intrafamiliar y especifica el tipo con detalle;"
                             "después, bríndame soporte emocional y aconséjame sobre la manera en que debería actuar; posteriormente, "
                             "bríndame instrucciones para denunciar mi caso considerando los servicios a los que puedo acceder."
                             "Ofrece ayuda con empatía, comprensión y confidencialidad.")
        
        with open("Backend/modulos_contexto.json", "r") as file:
            self.modules = json.load(file)

        '''self.modules = {
            "inicio": "Pregunta siempre por el bienestar del usuario.",
            "recursos": "Proporciona recursos y contactos de ayuda.",
            "empatía": "Muestra empatía y nunca juzgues.",
            # Agrega más módulos según sea necesario
        }'''
        
        self.current_context = self.base_context

    def add_module_to_context(self, module_name):
        if module_name in self.modules:
            self.current_context += f"\n{self.modules[module_name]}"

    def call_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7
        }
        response = model.generate_content("What is the meaning of life?")
        #response = requests.post("https://api.gemini.com/v1/complete", headers=headers, json=data)
        
        if response.status_code == 200:  # Verifica que la respuesta sea exitosa
            json_response = response.json()
            if "choices" in json_response and len(json_response["choices"]) > 0:  # Verifica que 'choices' esté presente y no esté vacío
                return json_response["choices"][0]["text"].strip()
            else:
                # Maneja el caso donde 'choices' no está presente o está vacío
                print("La respuesta de la API no contiene 'choices'.")
                return ""
        else:
            # Maneja respuestas no exitosas
            print(f"Error en la llamada a la API: Código de estado {response.status_code}")
            return ""
        #return response.json()["choices"][0]["text"].strip()

    def handle_input(self, user_input):
        # Actualizar el contexto con la entrada del usuario
        self.current_context += f"\nUsuario: {user_input}\nAsistente:"
        
        # Determinar el módulo relevante y agregarlo al contexto si es necesario
        if "recursos" in user_input.lower():
            self.add_module_to_context("recursos")
        elif "bienestar" in user_input.lower():
            self.add_module_to_context("inicio")
        elif "empatía" in user_input.lower():
            self.add_module_to_context("empatía")
        
        # Llamar a la API de Gemini
        response = self.call_api(self.current_context)
        
        # Actualizar el contexto con la respuesta del asistente
        self.current_context += f" {response}"
        
        return response


# Carga las variables de entorno desde .env
load_dotenv()

# Uso del chatbot
api_key = os.getenv('GEMINI_CHATBOT_API_KEY')
if not api_key:
    raise ValueError("No se encontró la clave API. Asegúrate de haber definido la variable de entorno 'GEMINI_CHATBOT_API_KEY' en el archivo .env.")
else:
    print("Clave API cargada exitosamente.")
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

chatbot = GeminiChatbot(api_key)

# Interacción con el chatbot
print("Chatbot iniciado. Escribe 'salir' para terminar.")

while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        print("Chatbot finalizado.")
        break
    response = chatbot.handle_input(user_input)
    print("Asistente:", response)

'''# Ejemplo de conversación
print(chatbot.handle_input("Hola"))
print(chatbot.handle_input("Me siento triste y ansioso"))
print(chatbot.handle_input("Sí, me gustaría recibir ayuda sobre recursos"))'''
