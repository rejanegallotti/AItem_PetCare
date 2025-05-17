# 🐾 AI tem PetCare? 🐾

## Sistema de Agentes de IA para Cuidados com Pets

[![GitHub license](https://img.shields.io/github/license/rejanegallotti/AItem_PetCare)](https://github.com/rejanegallotti/AItem_PetCare/blob/main/LICENSE)
[![Python version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Pro%2FFlash-yellow)](https://ai.google.dev/models)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-v0.1.0%2B-green)](https://google.github.io/adk-docs/)

Este projeto implementa um sistema interativo de agentes de inteligência artificial focado em auxiliar tutores de pets com cuidados básicos. Utilizando o **Google Gemini** como modelo de linguagem e o **Google Agent Development Kit (ADK)** para orquestração dos agentes, o sistema oferece orientações preliminares em áreas essenciais do bem-estar animal.

## ✨ Funcionalidades

O sistema "AI tem PetCare?" é composto por agentes especializados que podem ajudar com:

1.  **Diagnóstico de Saúde Primária:** Avaliação de sintomas comuns, identificação de sinais de alerta e recomendações sobre quando procurar um veterinário.
2.  **Adestramento em Casa:** Dicas práticas e passo a passo para ensinar comandos básicos e lidar com comportamentos comuns, com foco em reforço positivo.
3.  **Orientações sobre Dieta Natural:** Informações sobre alimentos seguros e perigosos, e princípios gerais para uma alimentação natural e balanceada (sempre com o aviso da necessidade de um nutricionista veterinário).

## 🧠 Arquitetura

O projeto utiliza a arquitetura de agentes do Google ADK, onde diferentes agentes com papéis e instruções específicas colaboram (indiretamente, neste caso, através do fluxo principal) para processar as requisições do usuário. A ferramenta `google_search` é integrada a alguns agentes para permitir a busca de informações externas quando necessário.

-   `agente_saude`: Especialista em sintomas e triagem veterinária.
-   `agente_dieta`: Consultor em nutrição e segurança alimentar.
-   `agente_treinamento`: Focado em técnicas de adestramento positivo.
-   `agente_revisor`: Garante a segurança e clareza das respostas geradas pelos outros agentes.
-   `root_agent`: Ponto de entrada para interfaces que esperam um agente raiz.

## 🚀 Como Executar

Para rodar o sistema "AI tem PetCare?" localmente, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/rejanegallotti/AItem_PetCare.git](https://github.com/rejanegallotti/AItem_PetCare.git)
    cd AItem_PetCare
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows (Git Bash/CMD):
    source venv/Scripts/activate
    # No Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    # Ou manualmente:
    # pip install google-genai google-adk python-dotenv
    ```

4.  **Configure sua Chave API do Google Gemini:**
    Obtenha sua chave API no [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key). Crie um arquivo na raiz do projeto chamado `.env` e adicione sua chave:
    ```dotenv
    GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"
    ```
    **Não compartilhe este arquivo e adicione-o ao seu `.gitignore`!**

5.  **Execute o sistema:**
    ```bash
    python petcare_agents/agent.py
    ```
    O sistema interativo será iniciado no seu terminal.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para sugestões ou reportar bugs, ou enviar Pull Requests com melhorias.

## 📄 Licença

Este projeto está licenciado sob os termos da Licença MIT. Veja o arquivo [LICENSE](https://github.com/rejanegallotti/AItem_PetCare/blob/main/LICENSE) para mais detalhes.

---

Desenvolvido por Rejane Menezes Reis Gallotti

