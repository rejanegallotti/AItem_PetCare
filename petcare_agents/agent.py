import os
from dotenv import load_dotenv
import google.generativeai as genai # Apenas esta importação de genai é necessária
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import textwrap
from IPython.display import display, Markdown # Pode ser ignorado se não estiver em ambiente de notebook
import warnings
import re

warnings.filterwarnings("ignore")

print("Iniciando script...")

# --- Configuração da API Key ---
load_dotenv()
print("Arquivo .env carregado.")

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Valor da API_KEY (encontrada/não encontrada): {api_key is not None}")

if api_key:
    # A configuração da API Key é feita diretamente na inicialização do cliente genai.Client()
    # O método genai.configure() não é mais usado desta forma para as versões mais recentes.
    print("API do Google Gemini sendo configurada...")
else:
    print("ERRO: Variável de ambiente 'GOOGLE_API_KEY' NÃO encontrada.")
    print("Por favor, defina sua chave API como uma variável de ambiente ou em um arquivo .env na raiz do projeto.")
    exit()

# Inicializa o cliente genai com a API Key
MODEL_ID = "gemini-2.0-flash" # Modelo mais estável e disponível

# --- Função para filtrar resposta ---
def filtrar_resposta_revisor(resposta_bruta):
    """
    Filtra a resposta do agente revisor para mostrar apenas o conteúdo relevante ao usuário,
    removendo logs técnicos e metadados gerados pelo revisor.
    """
    padrao = r"Resposta revisada:(.*?)(?=\n-{3,}|\Z)"
    match = re.search(padrao, resposta_bruta, re.DOTALL | re.IGNORECASE)

    if match:
        resposta_limpa = match.group(1).strip()
        resposta_limpa = re.sub(r'\*\*Revisões:\*\*.*?(?=\*\*Resposta revisada:\*\*|\Z)', '', resposta_limpa, flags=re.DOTALL | re.IGNORECASE)
        resposta_limpa = re.sub(r'^(?:agente \w+ está pensando|ferramenta \w+ usada:).*', '', resposta_limpa, flags=re.MULTILINE | re.IGNORECASE)
        return resposta_limpa.strip()
    return resposta_bruta # Fallback: retorna a resposta bruta se o padrão não for encontrado

# --- Funções Auxiliares ---
def call_agent(agent: Agent, message_text: str) -> str:
    """
    Envia uma mensagem para um agente usando o Runner do Google ADK e retorna a resposta final.
    """
    session_service = InMemorySessionService()
    # Para este exemplo, manter 'session_pet_care' está ok para execuções independentes
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session_pet_care")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session_pet_care", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    final_response += part.text
            break
    return final_response

def format_response(text):
    """
    Formata o texto para exibição em Markdown (ou para console).
    """
    text = text.replace('•', ' *') # Seu PDF mostrava '•', corrigi para '*'
    # Se estiver no VS Code e não usando um notebook Jupyter, 'display(Markdown(...)) não renderizará.
    # 'textwrap.indent' ajuda na leitura do console.
    return textwrap.indent(text, '> ')

# --- Agentes --- (Todos centralizados aqui)

def agente_saude(sintomas: str, pet_name: str):
    """
    Agente especializado em avaliar sintomas de pets e fornecer recomendações preliminares.
    Utiliza a ferramenta de busca do Google para obter informações adicionais.
    """
    saude_agent = Agent(
        name="agente_saude",
        model=MODEL_ID,
        instruction=f"""
        Você é um veterinário virtual, especialista em triagem de sintomas de pets.
        Seu objetivo é analisar os sintomas fornecidos pelo tutor sobre seu pet, {pet_name}.
        1. Dê um diagnóstico inicial provável ou lista de possíveis causas.
        2. Liste sinais de alerta claros que indicariam uma emergência (ex: vômito com sangue = urgência, dificuldade respiratória = emergência).
        3. Recomende ações claras para o tutor, incluindo quando e se deve "Levar ao veterinário imediatamente", "Observar por X horas e se persistir levar ao veterinário", ou "Pode ser cuidado em casa com observação".
        Use um tom empático, informativo e evite termos técnicos sem explicação.
        SEMPRE inclua um aviso CLARO que sua resposta NÃO SUBSTITUI um diagnóstico profissional
        de um veterinário e que, em caso de emergência, o pet deve ser levado a um veterinário imediatamente.
        """,
        description="Agente de diagnóstico veterinário para triagem de sintomas.",
        tools=[google_search]
    )
    return call_agent(saude_agent, f"Os sintomas de {pet_name} são: {sintomas}")

def agente_dieta(pet_name: str, especie: str, peso: str, alergias: str = ""):
    """
    Agente especialista em fornecer dicas de dieta personalizada e natural para pets.
    Pode usar a ferramenta de busca do Google para pesquisar informações nutricionais.
    """
    dieta_agent = Agent(
        name="agente_dieta",
        model=MODEL_ID,
        instruction=f"""
        Você é um nutricionista de pets AI, especialista em dietas balanceadas e naturais.
        Seu objetivo é criar um plano alimentar ou dar orientações dietéticas para o pet, {pet_name}.
        1. Baseado na espécie, peso e alergias informadas, sugira diretrizes gerais de dieta (ex: proporções de proteínas, carboidratos, vegetais).
        2. Liste alimentos seguros e perigosos comuns para a espécie.
        3. Forneça exemplos de refeições ou lanches.
        SEMPRE inclua um aviso CLARO que esta é uma orientação geral e NÃO substitui a consulta e o
        plano personalizado de um nutricionista veterinário qualificado, e que dietas desbalanceadas podem ser
        prejudiciais.
        """,
        description="Agente de nutrição animal para planos alimentares e orientações.",
        tools=[google_search]
    )
    input_message = f"Crie um plano alimentar para o pet {pet_name}:\n- Espécie: {especie}\n- Peso: {peso}\n- Alergias: {alergias if alergias else 'Nenhuma'}"
    return call_agent(dieta_agent, input_message)

def agente_treinamento(pet_name: str, comando: str):
    """
    Agente especialista em fornecer dicas de adestramento doméstico com reforço positivo.
    Pode usar a ferramenta de busca do Google para pesquisar técnicas específicas.
    """
    treino_agent = Agent(
        name="agente_treinamento",
        model=MODEL_ID,
        instruction=f"""
        Você é um adestrador de pets AI, focado em técnicas de reforço positivo.
        Seu objetivo é ensinar o tutor como treinar seu pet, {pet_name}, para o comando ou comportamento
        específico: '{comando}'.
        1. Descreva o passo a passo claro para o treinamento.
        2. Mencione a importância de paciência, consistência e sessões curtas.
        3. Sugira tipos de recompensas eficazes.
        SEMPRE inclua um aviso CLARO que para problemas de comportamento persistentes ou
        complexos, um adestrador profissional ou comportamentalista veterinário é recomendado.
        """,
        description="Agente de treinamento animal para dicas e passo a passo.",
        tools=[google_search]
    )
    return call_agent(treino_agent, f"Como treinar {pet_name} para '{comando}'?")

def agente_revisor(resposta_para_revisar: str) -> str:
    """
    Agente revisor de conteúdo, focado na segurança e clareza das respostas geradas.
    """
    revisor_agent = Agent(
        name="agente_revisor",
        model=MODEL_ID, # Você pode considerar um modelo mais "robusto" aqui como 'gemini-1.5-pro'
        instruction="""
        Você é um Editor e Revisor de Conteúdo meticuloso, especializado em conselhos sobre pets.
        Sua função é revisar uma resposta gerada por outro agente sobre cuidados com pets.
        1. Verifique se há conselhos potencialmente perigosos, enganosos ou eticamente incorretos (ex: "dê remédio humano", "ignore dor"). Se encontrar, aponte e sugira a remoção.
        2. Garanta que a linguagem seja clara, concisa, empática e fácil de entender para tutores leigos.
        3. Assegure-se de que todos os avisos de segurança e a recomendação de procurar um profissional
        (veterinário, adestrador, nutricionista) estejam presentes e sejam proeminentes.
        4. Sugira melhorias gerais na redação, estrutura ou tom se necessário.
        5. Sua saída final deve ser formatada como "Resposta revisada: [a resposta polida e segura]".
        Se houver problemas significativos que você corrigiu, detalhe as "Revisões:" antes da "Resposta
        revisada:".
        Se a resposta original é *muito* perigosa, diga "Atenção: A resposta original contém conselhos
        perigosos e foi drasticamente alterada para segurança. [Nova resposta segura]".
        """,
        description="Revisor de segurança e qualidade para conselhos sobre pets."
    )
    return call_agent(revisor_agent, f'Por favor, revise a seguinte resposta sobre cuidados com pets:\n\n{resposta_para_revisar}')

# --- Sistema Unificado AI tem PetCare ---
def ai_tem_petcare():
    print("🐾 Bem-vindo ao AI tem PetCare! Escolha uma opção para seu amigo de quatro patas:")
    print("1. Diagnóstico de Saúde (Sintomas, alertas e recomendações)")
    print("2. Dieta Personalizada (Orientações de nutrição e alimentos)")
    print("3. Treinamento (Dicas para comandos e comportamentos)")
    print("4. Sair")

    pet_name = input("Qual o nome do seu pet? (Ou deixe em branco para 'seu pet'): ").strip()
    if not pet_name:
        pet_name = "seu pet"

    while True:
        print("\n--- Menu Principal ---")
        print("1. Saúde\n2. Dieta\n3. Treinamento\n4. Sair")
        opcao = input("Digite o número da opção desejada: ")

        resposta_bruta_agente = ""
        resposta_do_revisor = ""
        resposta_final_exibicao = ""

        if opcao == "1":
            sintomas = input(f"Descreva os sintomas ou preocupações de saúde de {pet_name}: ")
            if sintomas:
                print(f"\n--- 📝 Consultando o Agente de Saúde sobre {pet_name} ---")
                resposta_bruta_agente = agente_saude(sintomas, pet_name)
                print(f"\n--- 🔎 Enviando para Revisão de Qualidade ---")
                resposta_do_revisor = agente_revisor(resposta_bruta_agente)
                resposta_final_exibicao = filtrar_resposta_revisor(resposta_do_revisor)
            else:
                print("Por favor, descreva os sintomas.")
                continue
        elif opcao == "2":
            especie = input("Espécie (ex: 'cachorro', 'gato'): ")
            peso = input("Peso (ex: '5kg', '20kg'): ")
            alergias = input("Alergias conhecidas (deixe em branco se não houver): ")
            if especie and peso:
                print(f"\n--- 📝 Consultando o Agente de Nutrição sobre {pet_name} ---")
                resposta_bruta_agente = agente_dieta(pet_name, especie, peso, alergias)
                print(f"\n--- 🔎 Enviando para Revisão de Qualidade ---")
                resposta_do_revisor = agente_revisor(resposta_bruta_agente)
                resposta_final_exibicao = filtrar_resposta_revisor(resposta_do_revisor)
            else:
                print("Por favor, forneça a espécie e o peso.")
                continue
        elif opcao == "3":
            comando = input(f"O que você gostaria de ensinar {pet_name}? (ex: 'sentar', 'não latir'): ")
            if comando:
                print(f"\n--- 📝 Consultando o Agente de Treinamento sobre {pet_name} ---")
                resposta_bruta_agente = agente_treinamento(pet_name, comando)
                print(f"\n--- 🔎 Enviando para Revisão de Qualidade ---")
                resposta_do_revisor = agente_revisor(resposta_bruta_agente)
                resposta_final_exibicao = filtrar_resposta_revisor(resposta_do_revisor)
            else:
                print("Por favor, descreva o que deseja ensinar.")
                continue
        elif opcao == "4":
            print(f"Obrigado por usar o AI tem PetCare para cuidar de {pet_name}! Volte sempre.")
            break
        else:
            print("Opção inválida. Por favor, digite um número de 1 a 4.")
            continue

        if resposta_final_exibicao:
            print("\n--- ✅ Resposta Final AI tem PetCare ---")
            print(format_response(resposta_final_exibicao))
        else:
            print("\nNenhuma resposta gerada para a opção selecionada ou houve um problema na geração/revisão.")
        print("\n--------------------------------------------------------------")

if __name__ == "__main__":
    print("Chamando a função principal 'ai_tem_petcare()'")
    ai_tem_petcare()