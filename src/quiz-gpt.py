from rich.console import Console
from rich.prompt import Prompt
from google import genai
from dotenv import load_dotenv
import json
import os

# Carrega as variáveis de ambiente (como a chave da API) de um arquivo .env
load_dotenv()

# Verifica se a chave da API está configurada.
if "GEMINI_API_KEY" not in os.environ:
    print("ERRO: A variável de ambiente GEMINI_API_KEY não está configurada.")
    print("Crie um arquivo .env e adicione 'GEMINI_API_KEY=SUA_CHAVE_AQUI'.")
    exit()

console = Console()

try:
    client = genai.Client()
except Exception as e:
    # Quebra de linha longa
    print(f"ERRO ao inicializar o cliente Gemini. Verifique a instalação: {e}")
    exit()

MODEL_NAME = "gemini-2.5-flash"


def esperar_enter():
    """Pausa a execução até o usuário pressionar Enter."""
    console.input(prompt="Pressione [enter] para continuar...")


def gerar_pergunta(topico):
    """
    Cria uma pergunta de múltipla escolha sobre o tópico,
    solicitando especificamente um formato JSON estruturado.
    """
    prompt_texto = f"""
Crie uma ÚNICA pergunta de múltipla escolha sobre o tema "{topico}"
e retorne APENAS o objeto JSON. Não inclua nenhum texto adicional,
explicações ou blocos de código (ex: ```json).

O objeto JSON DEVE seguir estritamente este formato:
{{
    "enunciado": "A pergunta...",
    "opcoes": ["Opção 1", "Opção 2", "Opção 3", "Opção 4"],
    "certa": "A resposta correta (deve ser uma das 'opcoes')"
}}
"""

    resposta = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt_texto,
        config={"response_mime_type": "application/json"},
    )

    conteudo = resposta.text
    return json.loads(conteudo)


def gerar_quiz():
    """Lógica principal do quiz, loop para gerar perguntas."""
    pontos = 0
    continuar = "S"

    topico = Prompt.ask("Qual é o topico do quiz ?").strip()

    if not topico:
        topico = "Conhecimentos Gerais"
        console.print(f"[yellow]Tópico. Usando: {topico}[/yellow]")

    while continuar.lower() != "n":
        console.clear()
        console.print(
            f"[bold magenta]TÓPICO ATUAL:[/bold magenta] [cyan]{topico}[/cyan]"
        )
        console.print("-" * 30)

        try:
            pergunta = gerar_pergunta(topico)
        except Exception as e:

            console.print(f"[red]ERRO ao gerar pergunta do Gemini: {e}[/red]")
            console.print(
                "[red]Verifique a sua API Key e conexão com a internet.[/red]"
            )
            esperar_enter()
            continue

        enunciado = pergunta.get("enunciado", "Erro ao carregar enunciado")
        opcoes = pergunta.get("opcoes", [])
        resposta_certa = pergunta.get("certa", "")

        if not opcoes or len(opcoes) != 4:
            console.print(
                "[red]Erro: O formato JSON do Gemini não retornou 4 opções "
                "válidas. Pulando para a próxima pergunta.[/red]"
            )
            esperar_enter()
            continue

        console.print(f"[bold]{enunciado}[/bold]\n")

        for i, opcao in enumerate(opcoes, start=1):
            console.print(f"{i}) {opcao}")

        escolha = Prompt.ask(
            "\n[bold]Sua opção (1-4):[/bold]", choices=["1", "2", "3", "4"]
        )
        resposta_indice = int(escolha) - 1
        resposta = opcoes[resposta_indice]

        console.clear()
        if resposta == resposta_certa:
            pontos += 1

            console.print(
                "[green]Resposta correta![/green] Agora você tem "
                f"[bold green]{pontos} pontos[/bold green]!"
            )
        else:
            console.print("[red]Resposta errada![/red]")
            console.print(
                f"Você continua com [bold yellow]{pontos} pontos[/bold yellow]"
            )
            console.print("\n[yellow]A resposta certa é:[/yellow]")
            console.print(f"[bold]{resposta_certa}[/bold]")

            console.print("\n")

        console.print("-" * 30)
        continuar = Prompt.ask("\nDeseja continuar?", choices=["S", "N"])
        if continuar.upper() == "N":
            break
        console.print("\n")

    console.print("\n" * 2)
    console.print("[bold magenta]Fim do Quiz![/bold magenta]")

    console.print(
        "Você terminou com um total de "
        f"[bold yellow]{pontos} pontos[/bold yellow] no tópico: "
        f"[cyan]{topico}[/cyan]."
    )
    console.print("\n" * 2)


def main():
    console.clear()

    titulo = "[bold yellow]QUIZ GPT[/bold yellow]"
    console.print(f"Bem vindo ao {titulo}!")

    gerar_quiz()


if __name__ == "__main__":
    main()
