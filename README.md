# 🧠 Quiz-GPT: Gerador de Quizzes Dinâmicos com IA

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Google-Gemini_API-007bff?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Rich Library](https://img.shields.io/badge/Terminal-Rich-33B27B?style=for-the-badge&logo=python)](https://github.com/Textualize/rich)

Este projeto é um _Gerador de Quizzes Dinâmicos_ que utiliza o modelo **Gemini 2.5 Flash** da Google. A aplicação é totalmente executada no terminal, aproveitando a biblioteca `rich` para uma experiência de usuário (UX) sofisticada com cores e formatação avançada.

O foco principal do projeto é demonstrar a capacidade de **Engenharia de Prompt Estruturada** e o uso de chamadas de API com **JSON Mode** para garantir um formato de saída previsível e confiável.

---

### ✨ Destaques Técnicos

- **Inteligência Artificial Generativa:** Utilização da API Gemini para criar perguntas e respostas de múltipla escolha sobre qualquer tópico em tempo real.
- **Modo JSON (Structured Output):** O prompt é configurado para forçar a saída da IA a ser um objeto JSON estrito, crucial para o parseamento seguro de dados em aplicações críticas.
- **UX/CLI Avançada:** Implementação da biblioteca `rich` para criar uma interface de linha de comando (CLI) colorida, fácil de ler e envolvente.
- **Gerenciamento de Segredos:** Uso do arquivo `.env` e da biblioteca `python-dotenv` para manipulação segura da chave de API.

### ⚙️ Tecnologias Utilizadas

| Tecnologia                  | Descrição                                              |
| :-------------------------- | :----------------------------------------------------- |
| **Python**                  | Linguagem principal do projeto.                        |
| **Google Gemini API (SDK)** | Motor de IA para gerar as perguntas.                   |
| **`rich`**                  | Biblioteca para formatação e estilização do terminal.  |
| **`python-dotenv`**         | Para gerenciar variáveis de ambiente e a chave de API. |
| **`json`**                  | Para desserializar (parsear) a resposta JSON da IA.    |

---

### 🚀 Como Baixar e Executar o Projeto

Para testar o Quiz-GPT em sua máquina, siga os passos abaixo:

#### 1. Pré-requisitos

Você precisará ter instalado:

- **Python 3.10+**
- Uma **Chave de API do Gemini** (você pode obtê-la gratuitamente no [Google AI Studio](https://ai.google.dev/)).

#### 2. Clonagem do Repositório

Abra seu terminal ou prompt de comando e clone o projeto:

```bash
git clone [https://github.com/fau-33/projeto-quiz]
cd [projetos/projeto-quiz] # Ajuste o caminho, se necessário
```
