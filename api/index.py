from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import json
import os
import random
import copy

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração da API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"ERRO ao inicializar o cliente Gemini: {e}")

# Lista de modelos
MODELS_TO_TRY = [
    "gemini-1.5-flash-8b", 
    "gemini-1.5-flash", 
    "gemini-2.0-flash-exp", 
    "gemini-2.0-flash"
]

# Banco de questões local categorizado
LOCAL_QUESTIONS = [
    {"enunciado": "O que significa 'JS' no desenvolvimento web?", "opcoes": ["JavaSource", "JavaScript", "JustScript", "J-Style"], "certa": "JavaScript", "tags": ["javascript", "js", "programação", "tecnologia"]},
    {"enunciado": "Qual dessas é uma palavra-chave para declarar variáveis no JavaScript?", "opcoes": ["var", "define", "dim", "string"], "certa": "var", "tags": ["javascript", "js", "programação"]},
    {"enunciado": "Python é uma linguagem...", "opcoes": ["Compilada", "Interpretada", "Apenas para Mobile", "De baixo nível"], "certa": "Interpretada", "tags": ["python", "programação"]},
    {"enunciado": "Qual é a capital da França?", "opcoes": ["Londres", "Berlim", "Madri", "Paris"], "certa": "Paris", "tags": ["história", "geografia", "geral"]},
    {"enunciado": "Quem pintou a Mona Lisa?", "opcoes": ["Van Gogh", "Leonardo da Vinci", "Picasso", "Michelangelo"], "certa": "Leonardo da Vinci", "tags": ["arte", "geral"]},
    {"enunciado": "Qual o maior oceano do planeta?", "opcoes": ["Atlântico", "Índico", "Glacial Ártico", "Pacífico"], "certa": "Pacífico", "tags": ["geografia", "geral"]},
    {"enunciado": "Qual o rio mais longo do mundo?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Yangtzé"], "certa": "Amazonas", "tags": ["geografia", "geral"]},
    {"enunciado": "Qual o animal terrestre mais rápido?", "opcoes": ["Leão", "Guepardo", "Cavalo", "Antílope"], "certa": "Guepardo", "tags": ["natureza", "geral"]}
]

perguntas_vistas = []

@app.route('/')
def index():
    global perguntas_vistas
    perguntas_vistas = []
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_question():
    global perguntas_vistas
    data = request.json
    topico = data.get('topico', 'Conhecimentos Gerais').lower()
    
    prompt_texto = f"""
    Crie uma pergunta de múltipla escolha sobre o tema "{topico}" em PORTUGUÊS DO BRASIL.
    A pergunta deve ser criativa e DIFERENTE.
    Retorne APENAS o objeto JSON.
    
    Formato:
    {{
        "enunciado": "Pergunta...",
        "opcoes": ["A", "B", "C", "D"],
        "certa": "Resposta exata"
    }}
    """

    for model_name in MODELS_TO_TRY:
        try:
            local_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
            resposta = local_client.models.generate_content(
                model=model_name,
                contents=prompt_texto,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 1.0,
                    "top_p": 0.95
                },
            )
            
            pergunta_data = json.loads(resposta.text)
            enunciado = pergunta_data.get("enunciado")
            
            if enunciado in perguntas_vistas:
                continue 
                
            perguntas_vistas.append(enunciado)
            return jsonify(pergunta_data)
        except Exception:
            continue 
            
    # Fallback inteligente
    disponiveis = [
        q for q in LOCAL_QUESTIONS 
        if q["enunciado"] not in perguntas_vistas and 
        any(tag in topico for tag in q.get("tags", []))
    ]
    
    if not disponiveis:
        disponiveis = [q for q in LOCAL_QUESTIONS if q["enunciado"] not in perguntas_vistas]
    
    if not disponiveis:
        disponiveis = LOCAL_QUESTIONS
        
    fallback_q = copy.deepcopy(random.choice(disponiveis))
    perguntas_vistas.append(fallback_q["enunciado"])
    return jsonify(fallback_q)

# Handler para Vercel
app = app
