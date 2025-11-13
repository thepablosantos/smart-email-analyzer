# 📧 Smart Email Analyzer

Solução inteligente para classificação automática de emails e geração de respostas usando Inteligência Artificial.

## 🎯 Sobre o Projeto

O **Smart Email Analyzer** é uma aplicação web desenvolvida para automatizar a leitura e classificação de emails em empresas do setor financeiro. A solução utiliza IA para:

- **Classificar emails** em categorias: **Produtivo** ou **Improdutivo**
- **Gerar respostas automáticas** personalizadas baseadas na classificação
- **Processar arquivos** em formato .txt ou .pdf
- **Interface moderna e intuitiva** para fácil utilização

## ✨ Funcionalidades

- 📁 **Upload de Arquivos**: Suporte para arquivos .txt e .pdf (até 5MB)
- ✍️ **Entrada de Texto**: Possibilidade de inserir texto diretamente
- 🤖 **Classificação Inteligente**: Utiliza OpenAI GPT para classificar emails
- 💬 **Geração de Respostas**: Cria respostas profissionais automaticamente
- 🎨 **Interface Moderna**: Design responsivo e intuitivo
- 📋 **Copiar Resposta**: Botão para copiar a resposta sugerida

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.9+ com Flask
- **IA**: OpenAI GPT-3.5-turbo
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Processamento**: PyPDF2 para leitura de PDFs
- **Deploy**: Vercel (recomendado)

## 📋 Pré-requisitos

- Python 3.9 ou superior
- Conta na OpenAI com API Key
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/smart-email-analyzer.git
cd smart-email-analyzer
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key da OpenAI

Crie um arquivo `.env` na raiz do projeto:

```bash
OPENAI_API_KEY=sua_chave_api_aqui
```

Você pode obter uma API Key em: https://platform.openai.com/api-keys

### 5. Execute a aplicação

```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5001`

## 📁 Estrutura do Projeto

```
smart-email-analyzer/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências
├── vercel.json           # Configuração para Vercel
├── templates/
│   └── index.html        # Interface web
└── examples/             # Emails de exemplo
```

## 🌐 Deploy na Nuvem

### Vercel (Recomendado)

1. Faça push do código para o GitHub
2. Acesse [vercel.com](https://vercel.com) e crie uma conta
3. Clique em "Add New Project"
4. Conecte seu repositório GitHub
5. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
6. Adicione a variável de ambiente:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: sua chave da OpenAI
7. Clique em "Deploy"

Pronto! Sua aplicação estará online em poucos minutos.

Para mais detalhes, veja o [guia completo de deploy](DEPLOY.md).

## 📖 Como Usar

1. **Acesse a aplicação** (local ou hospedada)
2. **Escolha o método de entrada**:
   - **Upload de Arquivo**: Clique na área de upload ou arraste um arquivo .txt ou .pdf
   - **Inserir Texto**: Cole ou digite o conteúdo do email diretamente
3. **Clique em "Analisar Email"**
4. **Aguarde a análise** (pode levar alguns segundos)
5. **Visualize os resultados**:
   - Classificação (Produtivo ou Improdutivo)
   - Resposta sugerida
6. **Copie a resposta** se necessário

## 🎨 Categorias de Classificação

### Produtivo
Emails que requerem uma ação ou resposta específica:
- Solicitações de suporte técnico
- Atualizações sobre casos em aberto
- Dúvidas sobre o sistema
- Pedidos de informação
- Solicitações de serviço

### Improdutivo
Emails que não necessitam de uma ação imediata:
- Mensagens de felicitações
- Agradecimentos genéricos
- Mensagens informativas sem solicitação de ação

## 🔧 Configurações Avançadas

### Alterar Modelo da OpenAI

No arquivo `app.py`, você pode alterar o modelo usado:

```python
# Linha ~80
response = openai.chat.completions.create(
    model="gpt-4",  # Altere para gpt-4 se tiver acesso
    ...
)
```

### Ajustar Temperatura

A temperatura controla a criatividade das respostas (0.0 = mais determinístico, 1.0 = mais criativo):

```python
# Linha ~82
temperature=0.3,  # Ajuste conforme necessário
```

## 📝 Teste

Na pasta `examples/` você encontra emails de exemplo para testar:
- `email_produtivo.txt` - Exemplo de email produtivo
- `email_improdutivo.txt` - Exemplo de email improdutivo

