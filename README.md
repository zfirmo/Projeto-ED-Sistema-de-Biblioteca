# OTECA - Sistema de Gerenciamento de Biblioteca

Projeto desenvolvido para a disciplina de Estrutura de Dados do curso de Ciência da Computação (UFAL - Campus Arapiraca). O objetivo principal foi a implementação manual de diversas estruturas de dados clássicas para gerenciar um acervo bibliográfico, integrando lógica de backend robusta com uma interface gráfica intuitiva.

## Sobre o Projeto
O OTECA simula o funcionamento completo de uma biblioteca, permitindo operações como cadastro, busca, empréstimo, devolução e gestão de filas de espera. Todas as estruturas de dados foram implementadas do zero, sem o uso de bibliotecas nativas de coleções, cumprindo estritamente os requisitos acadêmicos da disciplina.

## Estruturas de Dados Implementadas

* Tabela Hash: Utilizada para a busca eficiente de livros por ISBN, com tratamento de colisões via encadeamento.

* Árvore Binária de Busca (BST): Responsável pela organização do acervo e listagem dos livros em ordem alfabética de título.
* Lista Encadeada: Utilizada para o armazenamento linear e sequencial dos livros cadastrados no sistema.
* Fila: Implementa a lógica FIFO (First In, First Out) para gerir usuários em espera por livros indisponíveis.

* Pilha: Gerencia o histórico de transações, permitindo a funcionalidade de reversão (Undo) das últimas operações realizadas.

## Tecnologias Utilizadas

* Linguagem: Python 3.x
* Interface Gráfica: CustomTkinter
* Manipulação de Imagem: Pillow

## Como Instalar e Executar

### Pré-requisitos
Certifique-se de ter o Python instalado em seu ambiente.

### Instalação
1. Clone o repositório:
   `git clone https://github.com/zfirmo/Projeto-ED-Sistema-de-Biblioteca`
2. Instale as dependências necessárias:
   `pip install customtkinter pillow`

### Execução
* **Para a Interface Gráfica:**
  `python oteca.py`
* **Para a execução via terminal:**
  `python main.py`

## Equipe

* Adryan Victor (2025027518)
* Artur Barbosa (2025027151)
* Elias Sales (2025027204)
* Saulo Firmo (2025027320)

**Orientador:** Prof. Patrick Brito

---
*Projeto acadêmico - Ciência da Computação - UFAL 2026.*