# 🚀 Construindo com IA: Desafio de Monitoramento de Marca

Bem-vindo ao Desafio de Monitoramento de Marca do nosso workshop Construindo com IA! Neste exercício, você usará o ADK (e opcionalmente o MCP) para criar um agente de ponta a ponta que:

1. **Ingere** menções de uma marca de múltiplas fontes (Reddit, Twitter, APIs de notícias, web em geral).
2. **Analisa** o que as pessoas estão dizendo — sentimento, tópicos principais, detecção de problemas.
3. **Gera** um relatório consolidado destacando a percepção pública atual da marca e áreas de preocupação.

---


## 🛠 Ferramentas & Pré-requisitos do Workshop

- **Kit de Desenvolvimento de Agentes (ADK)**
  Ferramenta para definir seu agente, ferramentas e chamadas de função.

- **MCP (Model Context Protocol)** _(opcional)_
  Você receberá credenciais do MCP para se conectar. Se sua cota acabar, fique à vontade para criar seus próprios conectores ou usar chamadas diretas de função.

- **Gemini**
  O LLM que você usará para análise e geração de relatórios.

- **Dependências**
  Instale todos os pacotes necessários a partir do `requirements.txt` fornecido:

  ```bash
  pip install -r requirements.txt
  ```

---

## 🚦 Enunciado do Desafio

> **Dado** o nome de uma marca (entrada do usuário),
> **Construa** um agente de IA que:
> 1. Consulte **ao menos três** fontes de dados (ex.: Reddit, Twitter, API de Notícias, Web Scraper).
> 2. Realize **análise de sentimento**, **extração de tópicos** e **detecção de problemas** nas menções coletadas.
> 3. Produza um **Relatório de Monitoramento de Marca** estruturado (veja “Saída Esperada” abaixo).

---

## 📥 Entradas

- `company_name` (string)
  ex.: `"Acme Co."`


---

## 📈 Saída Esperada

Seu agente deve retornar um relatório Markdown contendo:

1. **Resumo Executivo**
   Uma visão geral em 2–3 frases sobre o sentimento geral e as principais preocupações.

2. **Distribuição de Sentimentos**
   Percentual de menções positivas / neutras / negativas, **por fonte**.

3. **Top 5 Tópicos & Problemas**
   Temas mais discutidos com frequência (ex.: “atrasos na entrega”, “suporte ao cliente”).

4. **Análise de Tendência**
   Resumo simples em série temporal (menções por dia), destacando os picos.

5. **Menções Exemplares**
   2–3 citações representativas (com nome da fonte e link) para cada categoria de sentimento.

6. **Recomendações**
   Com base nos problemas detectados, sugira 2–3 próximos passos acionáveis.

---

## 🏗 Suas Tarefas

1. **Configurar Conectores**
   - Use o MCP com as credenciais fornecidas, *ou* implemente seus próprios conectores via chamadas de função/web scraping.

2. **Definir Agente & Ferramentas no ADK**
   - Declare funções para ingestão de dados, análise e geração de relatório.

3. **Implementar Pipeline de Análise**
   - Ingerir menções brutas → limpar/filtrar/resumir → gerar report.

4. **Gerar Relatório**
   - Obter resultados na estrutura Markdown acima.

5. **Teste sua Solução**
   - Teste sua solução com pelo menos **duas** marcas diferentes.

---

## 📝 Submissão (Sugerido)

- **Repositório no GitHub** contendo:
  - `README.md`
  - Código-fonte do seu agente
  - `requirements.txt`
  - Exemplos de saída para pelo menos duas marcas

- **Critérios de Avaliação** (para sua referência):
  1. **Cobertura de Dados**: ≥3 fontes ingeridas.
  2. **Qualidade do Relatório**: Clareza, completude, estrutura.
  3. **Ferramentas**: Uso correto das funções do ADK (e do MCP, se utilizado).
  4. **Qualidade do Código**: Legível, modular, documentado.

# Setup

## Instruções de Configuração

- **Chave de API do Gemini**
  Acesse o Google: http://aistudio.google.com/
  Faça login com sua conta Google.
  Crie uma chave de API.
  Crie um arquivo chamado `.env`.
  Adicione a variável `GOOGLE_API_KEY` com o valor da chave de API do AI Studio.

## ADK

Abra a UI:

```
adk web
```

Execute o agente como serviço:

```
adk api_server
```

## MCP Local

Para executar o MCP local, certifique-se de ter as credenciais corretas no seu arquivo `.env`:

```
cd 06_challenge/mcp/
uvicorn src.api:app --host 0.0.0.0 --port 8001 --reload
```

## Credentials Websites

## 🛠️ Credenciais do Reddit
**Site:** [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
**O que você vai precisar:**
- **Client ID** (ou “App ID”)
- **Client Secret**
- **User Agent** (ex.: `my-app/0.1 by seu_usuario`)

---

## 🐦 Credenciais do Twitter
**Site:** [developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)
**O que você vai precisar:**
- **Bearer Token**

---

## 🗞️ News API (Tavily)
**Site:** [tavily.com](https://tavily.com/)
**O que você vai precisar:**
- **API Key**

---

Basta acessar cada link, seguir o fluxo de “Criar novo app” ou “Obter chave de API” e guardar esses valores com segurança — seu código vai agradecer! 🎉


---

Boa sorte e bom desenvolvimento! 🌟
