import os
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
from io import BytesIO
from dotenv import load_dotenv
import openai

try:
    load_dotenv()
except Exception as e:
    print(f"⚠️  Aviso ao carregar .env: {str(e)}")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

openai_api_key = os.getenv('OPENAI_API_KEY')
try:
    if openai_api_key:
        client = openai.OpenAI(api_key=openai_api_key)
    else:
        client = None
        print("⚠️  OPENAI_API_KEY não configurada - funcionalidades de IA não estarão disponíveis")
except Exception as e:
    print(f"⚠️  Erro ao configurar OpenAI: {str(e)}")
    client = None

if not os.environ.get('VERCEL'):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_content):
    """Extrai texto de um arquivo PDF"""
    try:
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Erro ao processar PDF: {str(e)}")


def is_valid_text(text):
    """Valida se o texto contém palavras reais em português"""

    common_words = [
        'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das',
        'em', 'no', 'na', 'nos', 'nas', 'para', 'com', 'por', 'sobre',
        'que', 'qual', 'quais', 'quando', 'onde', 'como', 'porque',
        'é', 'são', 'foi', 'ser', 'estar', 'ter', 'ter', 'fazer',
        'você', 'vocês', 'eu', 'nós', 'eles', 'elas', 'meu', 'minha',
        'seu', 'sua', 'nosso', 'nossa', 'deles', 'delas',
        'prezado', 'prezada', 'senhor', 'senhora', 'obrigado', 'obrigada',
        'email', 'mensagem', 'contato', 'solicitação', 'pedido',
        'atenciosamente', 'abraço', 'abraços', 'beijos', 'beijo'
    ]
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    if len(words) == 0:
        return False
    
    known_words = sum(1 for word in words if word in common_words or len(word) > 3)
    
    if len(words) < 3:
        return False
    
    if len(words) >= 3 and known_words == 0:
        return False
    
    return True


def preprocess_text(text):
    """Pré-processa o texto removendo caracteres especiais e normalizando"""
    # Remove quebras de linha excessivas
    text = re.sub(r'\n+', ' ', text)
    # Remove espaços múltiplos
    text = re.sub(r'\s+', ' ', text)
    # Remove caracteres especiais mantendo acentos
    text = re.sub(r'[^\w\sáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ.,!?;:()\-]', '', text)
    return text.strip()


def classify_email_with_ai(email_text):
    """Classifica o email usando OpenAI API"""
    try:
        prompt = f"""Analise o seguinte email e classifique-o como "Produtivo" ou "Improdutivo".

Regras de classificação:
- PRODUTIVO: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, pedidos de informação, solicitações de serviço).
- IMPRODUTIVO: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos genéricos, mensagens informativas sem solicitação de ação).

Email:
{email_text}

Responda APENAS com uma das palavras: "Produtivo" ou "Improdutivo"."""

        if not client:
            raise Exception("OpenAI API key não configurada")
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em classificação de emails para empresas financeiras."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=20
        )
        
        classification = response.choices[0].message.content.strip()
        
        classification_lower = classification.lower()
        
        if "improdutivo" in classification_lower:
            return "Improdutivo"
        elif "produtivo" in classification_lower:
            return "Produtivo"
        else:
            print(f"⚠️  Resposta da API não reconhecida: '{classification}', usando fallback")
            return classify_email_fallback(email_text)
            
    except Exception as e:
        print(f"❌ Erro na classificação com AI: {str(e)}")
        import traceback
        traceback.print_exc()
        return classify_email_fallback(email_text)


def classify_email_fallback(email_text):
    """Classificação fallback baseada em palavras-chave"""
    email_lower = email_text.lower()
    
    if not is_valid_text(email_text):
        return "Improdutivo"
    
    # Palavras-chave produtivas
    productive_keywords = [
        'solicitação', 'solicito', 'pedido', 'preciso', 'necessito', 'requer',
        'suporte', 'ajuda', 'problema', 'erro', 'dúvida', 'questão', 'pergunta',
        'atualização', 'status', 'andamento', 'prazo', 'urgente', 'urgência',
        'informação', 'detalhes', 'documento', 'arquivo', 'anexo', 'protocolo',
        'serviço', 'contrato', 'proposta', 'orçamento', 'cobrança', 'fatura',
        'reclamação', 'reclamo', 'cancelamento', 'alteração', 'mudança'
    ]
    
    # Palavras-chave improdutivas
    unproductive_keywords = [
        'feliz natal', 'feliz ano novo', 'feliz páscoa', 'feliz aniversário',
        'parabéns', 'felicitações', 'cumprimentos', 'saudações',
        'obrigado', 'obrigada', 'agradeço', 'agradecimento', 'agradecimentos',
        'atenciosamente', 'abraço', 'abraços', 'beijos', 'beijo',
        'desejo', 'desejos', 'votos', 'voto', 'sucesso', 'prosperidade'
    ]
    
    productive_count = sum(1 for keyword in productive_keywords if keyword in email_lower)
    unproductive_count = sum(1 for keyword in unproductive_keywords if keyword in email_lower)
    
    has_greeting_pattern = any(phrase in email_lower for phrase in [
        'feliz natal', 'feliz ano novo', 'parabéns', 'felicitações'
    ])
    
    # Se tem padrão de felicitações, é improdutivo
    if has_greeting_pattern:
        return "Improdutivo"
    
    # Se tem muitas palavras de agradecimento e nenhuma solicitação, é improdutivo
    if unproductive_count >= 2 and productive_count == 0:
        return "Improdutivo"
    
    # Se tem palavras produtivas, é produtivo
    if productive_count > 0:
        return "Produtivo"
    
    # Se tem apenas agradecimentos genéricos, é improdutivo
    if unproductive_count > 0 and productive_count == 0:
        return "Improdutivo"
    
    # Se não houver palavras-chave claras, analisar o tamanho e estrutura
    # Emails muito curtos com apenas agradecimentos são improdutivos
    if len(email_text) < 200 and ('obrigado' in email_lower or 'agradeço' in email_lower):
        return "Improdutivo"
    
    # Se não conseguir determinar e não tem palavras-chave conhecidas, é improdutivo
    if productive_count == 0 and unproductive_count == 0:
        return "Improdutivo"
    
    # Por padrão, se não conseguir determinar, considerar improdutivo (mais seguro)
    return "Improdutivo"


def generate_response_with_ai(email_text, classification):
    """Gera uma resposta automática usando OpenAI API"""
    try:
        if classification == "Produtivo":
            prompt = f"""Com base no seguinte email classificado como PRODUTIVO, gere uma resposta profissional e adequada para uma empresa financeira.

O email deve receber uma resposta que:
- Seja profissional e cortês
- Reconheça a solicitação do cliente
- Indique que a solicitação está sendo processada
- Seja concisa e direta

Email recebido:
{email_text}

Gere uma resposta profissional em português brasileiro:"""

        else: 
            prompt = f"""Com base no seguinte email classificado como IMPRODUTIVO, gere uma resposta profissional e cordial para uma empresa financeira.

O email deve receber uma resposta que:
- Seja profissional e cortês
- Agradeça a mensagem
- Seja breve e amigável

Email recebido:
{email_text}

Gere uma resposta profissional em português brasileiro:"""

        if not client:
            raise Exception("OpenAI API key não configurada")
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em redação de respostas profissionais para empresas financeiras."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Erro na geração de resposta com AI: {str(e)}")
        return generate_response_fallback(classification)


def generate_response_fallback(classification):
    """Gera resposta fallback quando a API não está disponível"""
    if classification == "Produtivo":
        return """Prezado(a),

Agradecemos pelo seu contato. Recebemos sua solicitação e ela está sendo processada por nossa equipe.

Em breve entraremos em contato com mais informações.

Atenciosamente,
Equipe de Atendimento"""
    else:
        return """Prezado(a),

Agradecemos sua mensagem e os votos de felicitações.

Ficamos felizes em saber que está satisfeito(a) com nossos serviços.

Atenciosamente,
Equipe de Atendimento"""


@app.route('/')
def index():
    """Rota principal - serve a interface web"""
    return render_template('index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve arquivos estáticos"""
    return app.send_static_file(path)


@app.route('/api/analyze', methods=['POST'])
def analyze_email():
    """Endpoint para análise de email"""
    try:

        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Formato de arquivo não suportado. Use .txt ou .pdf'}), 400
            
            file_content = file.read()

            if file.filename.endswith('.pdf'):
                email_text = extract_text_from_pdf(file_content)
            else: 
                email_text = file_content.decode('utf-8')
        
        elif 'text' in request.json:
            email_text = request.json['text']
        
        else:
            return jsonify({'error': 'Envie um arquivo ou texto'}), 400
        
        if not email_text or len(email_text.strip()) == 0:
            return jsonify({'error': 'O conteúdo do email está vazio'}), 400
        
        processed_text = preprocess_text(email_text)
        
        if len(processed_text) < 10:
            return jsonify({'error': 'O texto do email é muito curto para análise'}), 400
        
        if not is_valid_text(processed_text):
            return jsonify({
                'success': True,
                'classification': 'Improdutivo',
                'suggested_response': 'O texto fornecido não parece ser um email válido. Por favor, verifique o conteúdo e tente novamente.',
                'original_text': email_text[:500] + '...' if len(email_text) > 500 else email_text,
                'warning': 'Texto não reconhecido como email válido'
            })
        
        classification = classify_email_with_ai(processed_text)
        
        suggested_response = generate_response_with_ai(processed_text, classification)
        
        return jsonify({
            'success': True,
            'classification': classification,
            'suggested_response': suggested_response,
            'original_text': email_text[:500] + '...' if len(email_text) > 500 else email_text
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao processar email: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'ok', 'message': 'API está funcionando'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)

