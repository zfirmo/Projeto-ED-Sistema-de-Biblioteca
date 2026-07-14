# OTECA - Sistema de Gerenciamento de Biblioteca

Projeto acadêmico desenvolvido para a disciplina de Estrutura de Dados do curso de Ciência da Computação na Universidade Federal de Alagoas (UFAL - Campus Arapiraca). O sistema consiste em uma solução completa para a gestão de acervos bibliográficos, empréstimos, devoluções e filas de espera, integrando uma lógica de backend com uma interface gráfica de usuário (GUI).

A parte imporatne do projeto reside na implementação manual de todas as estruturas de dados utilizadas, cumprindo estritamente as restrições acadêmicas de não utilizar coleções ou dicionários nativos da linguagem Python (como `list` ou `dict`) para as operações centrais.

## Demonstração da Interface

<p align="center">
  <img src="Imagens/Oteca - Cadastro.png" alt="Tela de Cadastro OTECA" width="800">
</p>
<p align="center">
  <img src="Imagens/Oteca - Empréstimos.png" alt="Tela de Empréstimos OTECA" width="800">
</p>
<p align="center">
  <img src="Imagens/Oteca - Acervo.png" alt="Tela do Acervo OTECA" width="800">
</p>

## Funcionalidades do Sistema

* **Cadastro de Obras:** Registro de livros contendo ISBN (validação estrita para 10 ou 13 dígitos numéricos), título, autor, ano de publicação e quantidade de exemplares em estoque.
* **Remoção de Obras:** Exclusão completa de um livro do acervo, garantindo que o registro seja eliminado simultaneamente de todas as estruturas indexadas para evitar inconsistência de dados.
* **Busca Eficiente por ISBN:** Localização instantânea de qualquer obra cadastrada no sistema através de indexação direta.
* **Listagem Alfabética (Relatório do Acervo):** Geração de relatórios ordenados de forma nativa pelo título das obras.
* **Controle de Circulação (Empréstimo e Devolução):** Decremento e incremento automatizado de estoque de exemplares disponíveis.
* **Fila de Espera Automatizada:** Quando um usuário solicita o empréstimo de um livro esgotado, ele é inserido de forma automática em uma fila de prioridade para aquela obra específica. Ao ocorrer a devolução, o livro é atribuído imediatamente ao próximo usuário da fila.
* **Mecanismo de Reversão (Undo):** Capacidade de desfazer as últimas operações de circulação realizadas (empréstimos, devoluções ou entradas em fila), restaurando o estado anterior do sistema de forma exata através de operações de compensação.
* **Gestão Multimídia de Capas:** Armazenamento e associação de imagens de capa (`.png`) para cada livro cadastrado, permitindo a visualização da arte no painel de consulta e a exportação do arquivo.
* **Salvamento de Logs:** Exportação do histórico completo de ações registradas na sessão para um arquivo externo de texto (`.txt`).

## Arquitetura de Estruturas de Dados

Para atender aos requisitos de desempenho e às restrições do projeto, foram implementadas cinco estruturas de dados clássicas do zero:

1. **Tabela Hash (`Tabela_Hash`):** Indexa os livros pelo código ISBN. Utiliza uma função hash baseada no somatório do valor ASCII dos caracteres com tratamento de colisões por encadeamento. Garante busca, inserção e remoção com complexidade média de tempo O(1).
2. **Árvore Binária de Busca (`Arvore_Binaria`):** Organiza as obras alfabeticamente pelo título. É a estrutura responsável por permitir que o relatório geral do acervo seja gerado em ordem alfabética de forma nativa através do percorrimento em-ordem (In-Order Traversal), sem custos adicionais de algoritmos de ordenação.
3. **Lista Encadeada (`Lista_Encadeada`):** Fornece o armazenamento linear e sequencial dos nós dos livros, atuando como o registro base dinâmico do acervo.
4. **Fila (`Fila`):** Controla os usuários em espera de cada livro individual que se encontra esgotado. Segue estritamente a política FIFO (First-In, First-Out), garantindo a prioridade justa no atendimento de reservas.
5. **Pilha (`Pilha`):** Mantém o histórico cronológico invertido das transações de circulação do sistema sob a política LIFO (Last-In, First-Out). Cada nó armazena os metadados da operação executada, servindo de base para o mecanismo de *Undo*.

*Nota: Todas as estruturas acima foram estruturadas sobre a classe customizada `Vetor_Estatico`, que aloca slots fixos de memória e encapsula os ponteiros de acesso de forma puramente manual.*

## Tecnologias Utilizadas

* **Linguagem Principal:** Python 3.x
* **Interface Gráfica (GUI):** CustomTkinter (Extensão moderna do Tkinter com suporte a temas e widgets customizados)
* **Processamento de Imagens:** Pillow (PIL - Python Imaging Library)

## Organização e Planejamento

A organização e planejamento do projeto foi relizada em diversas p´lataformar mas focando em uma principal sendo ela o Miro:
<p align="center">
  <img src="Imagens/Oteca - Miro.png" alt="Tela de Cadastro OTECA" width="800">
</p>

## Estrutura do Repositório

```text
├── main.py               # Ponto de entrada para execução do sistema via Terminal (Modo Texto)
├── oteca.py              # Ponto de entrada para execução do sistema via Interface Gráfica (GUI)
├── sistema_biblioteca.py # Core do Backend (Implementação manual de todas as Estruturas de Dados e Regras de Negócio)
├── oteca_logo.png        # Logotipo utilizado na identidade visual da aplicação gráfica
├── imagens/              # Diretório contendo capturas de tela e assets de documentação
│   └── tela_cadastro.png
└── README.md             # Documentação principal do projeto