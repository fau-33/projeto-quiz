from rich.console import Console
from rich.prompt import Prompt
import json

console = Console()


def esperar_enter():
    console.input(prompt="Pressione [enter] para continuar...", password=True)


def gerar_pergunta(topico):
    pergunta = """
      {
        "enunciado": "Você gosta do Python?",
        "opcoes": ["Sim", "Nao", "Que?", "Nãããã"],
        "certa": "Sim"
      }
    """
    return json.loads(pergunta)


def gerar_quiz():
    pontos = 0
    continuar = ""

    topico = Prompt.ask("Qual e o topico do quiz ?")

    while continuar.lower() != "n":
        pergunta = gerar_pergunta(topico)
        opcoes = pergunta["opcoes"]

        console.clear()
        console.print(f"[bold] {pergunta['enunciado']} [/bold]")

        for i, opcao in enumerate(opcoes, start=1):
            console.print(f"{i}) {opcao}")

        resposta_indice = (
            int(Prompt.ask(prompt="Opção ", choices=["1", "2", "3", "4"])) - 1
        )

        resposta = opcoes[resposta_indice]
        resposta_certa = pergunta["certa"]

        console.clear()
        if resposta == resposta_certa:
            pontos += 1
            console.print(
                "[green]Resposta correta![/green] "
                "Agora voce tem "
                f"{pontos} pontos."
            )
        else:
            console.print("[red]Resposta errada![/red]")
            console.print(f"Você continua com {pontos} pontos.")
            console.print("[yellow]A resposta certa é[/yellow]")
            console.print(f"'{resposta_certa}'.")
        continuar = Prompt.ask(
            prompt="Deseja continuar?", choices=["S", "N"], default="S"
        )

        console.print(topico)


def main():
    console.clear()

    titulo = "[bold yellow]QUIZ GPT[/bold yellow]"
    console.print(f"Bem vindo ao {titulo} ?")

    gerar_quiz()


main()
