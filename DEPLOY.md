# 🚀 Guia de Deploy

Guia rápido para fazer deploy da aplicação na Vercel.

## 📋 Pré-requisitos

- Conta na OpenAI com API Key
- Repositório no GitHub
- Código commitado e enviado para o GitHub

## 🌐 Deploy na Vercel

### Passo a Passo

1. **Acesse a Vercel**
   - Vá em [vercel.com](https://vercel.com) e faça login (pode usar sua conta do GitHub)

2. **Crie um novo projeto**
   - Clique em "Add New Project"
   - Selecione seu repositório do GitHub
   - Clique em "Import"

3. **Configure o projeto**
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - Deixe as outras configurações padrão

4. **Adicione a variável de ambiente**
   - Na seção "Environment Variables", clique em "Add"
   - **Key**: `OPENAI_API_KEY`
   - **Value**: cole sua chave da OpenAI
   - Clique em "Save"

5. **Faça o deploy**
   - Clique em "Deploy"
   - Aguarde alguns minutos (geralmente 2-5 minutos)

Pronto! Sua aplicação estará online e você receberá uma URL tipo: `https://seu-projeto.vercel.app`

### Deploy Automático

A partir de agora, toda vez que você fizer push no GitHub, a Vercel fará o deploy automaticamente. Muito prático!

## 📝 Dicas Importantes

- **API Key**: Nunca commite sua chave da OpenAI no código. Sempre use variáveis de ambiente
- **Custos**: Monitore seu uso da API em [platform.openai.com/usage](https://platform.openai.com/usage)
- **Logs**: Você pode ver os logs da aplicação diretamente no dashboard da Vercel

## 🐛 Problemas?

Se algo der errado:
- Verifique se a variável `OPENAI_API_KEY` está configurada corretamente
- Confira os logs no dashboard da Vercel
- Certifique-se de que o arquivo `vercel.json` está no repositório

