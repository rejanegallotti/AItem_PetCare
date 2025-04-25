# 🚀 Build with AI: Desafio de Monitoramento de Marca

Bem-vindo ao Desafio de Monitoramento de Marca do nosso workshop Build with AI!
Neste exercício você usará o ADK (e opcionalmente o MCP) para construir um agente de ponta a ponta que:

1. **Coleta** menções de uma marca a partir de múltiplas fontes (Reddit, Twitter, APIs de notícias, web em geral).
2. **Analisa** o que as pessoas estão dizendo — sentimento, tópicos-chave, identificação de problemas.
3. **Gera** um relatório consolidado destacando a percepção pública atual da marca e áreas de preocupação.

---

## 🛠 Ferramentas & Pré-requisitos

- **Agent Development Kit (ADK)**
  Ferramenta para definir seu agente, ferramentas e chamadas de função.

- **MCP (Model Context Protocol)** _(opcional)_
  Você receberá credenciais MCP para conectar. Se o seu limite estourar, sinta-se livre para criar seus próprios conectores ou usar chamadas de função “cruas”.

- **Gemini**
  O LLM que você usará para análise e geração de relatório.

- **Dependências**
  Instale todos os pacotes necessários a partir do `requirements.txt` fornecido:

  ```bash
  pip install -r requirements.txt
  ```

---

## 🚦 Declaração do Desafio

> **Dado** o nome de uma marca (entrada do usuário),
> **Construa** um agente de IA que:
> 1. Consulte **pelo menos três** fontes de dados (por exemplo, Reddit, Twitter, News API, Web Scraper).
> 2. Realize **análise de sentimento**, **extração de tópicos** e **detecção de problemas** sobre as menções coletadas.
> 3. Produza um **Relatório de Monitoramento de Marca** estruturado (veja “Saída Esperada” abaixo).

---

## 📥 Entradas

- `brand_name` (string)
  Ex.: `"Acme Co."`

- *(Opcional)* `start_date` / `end_date` para definir o período de monitoramento.

---

## 📈 Saída Esperada

Seu agente deve retornar um relatório em **JSON** (ou Markdown) contendo:

1. **Resumo Executivo**
   Visão geral de 2–3 frases sobre o sentimento geral e principais preocupações.

2. **Distribuição de Sentimentos**
   Percentual de menções positivas / neutras / negativas, **por fonte**.

3. **Top 5 Tópicos & Problemas**
   Temas mais frequentes (por exemplo, “atrasos de entrega”, “suporte ao cliente”).

4. **Análise de Tendência**
   Resumo simples em série temporal (menções por dia), destacando picos.

5. **Exemplos de Menções**
   2–3 trechos representativos (com fonte e link) para cada categoria de sentimento.

6. **Recomendações**
   Com base nos problemas identificados, sugira 2–3 próximos passos acionáveis.

---

## 🏗 Suas Tarefas

1. **Configurar Conectores**
   - Use o MCP com as credenciais fornecidas,
     _ou_ implemente seus próprios via chamadas de função/web scraping.

2. **Definir Agente & Ferramentas no ADK**
   - Declare funções para ingestão de dados, análise e geração de relatório.

3. **Implementar Pipeline de Análise**
   - Ingerir menções brutas → limpar/filtrar → chamar funções Gemini para sentimento e tópicos.

4. **Gerar Relatório**
   - Agregar resultados na estrutura JSON/Markdown descrita acima.

5. **Demonstração**
   - Execute uma apresentação ao vivo para **duas** marcas diferentes.

---

## 📝 Submissão (Sugerida)

- **Repositório GitHub** contendo:
  - `README.md`
  - Código-fonte do agente
  - `requirements.txt`
  - Exemplos de saída para pelo menos duas marcas

- **Critérios de Avaliação**:
  1. **Cobertura de Dados**: ≥3 fontes ingeridas.
  2. **Qualidade do Relatório**: Clareza, completude e organização.
  3. **Ferramentas**: Uso correto das funções do ADK (e do MCP, se usado).
  4. **Qualidade do Código**: Legibilidade, modularidade e documentação.

Boa sorte, e bom desenvolvimento! 🌟
