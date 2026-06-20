class Livro:

    def __init__(self, isbn: str, titulo: str, autor: str, ano_publicacao: int, qtd_exemplares: int):

        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.qtd_exemplares = qtd_exemplares

class Livro_Node:

    def __init__(self, livro):

        self.livro = livro
        self.proximo = None
        self.direita = None
        self.esquerda = None
        self.fila_espera = Fila()

class Usuario:

    def __init__(self, nome_usuario, id):

        self.nome_usuario = nome_usuario
        self.id = id

class Usuario_Node:

    def __init__(self, usuario):

        if isinstance(usuario, Usuario):

            self.usuario = usuario
            self.nome_usuario = usuario.nome_usuario

        else:

            self.usuario = Usuario(usuario, 0)
            self.nome_usuario = usuario
            
        self.proximo = None

class Hash_Node:

    def __init__(self, livro):

        self.livro = livro
        self.proximo = None

class Op_Node:

    def __init__(self, isbn, usuario):

        self.isbn = isbn
        self.usuario = usuario
        self.proximo = None


class Tabela_Hash:

    def __init__(self, tamanho=50):

        self.tamanho = tamanho
        self.baldes = [None] * tamanho

    def _funcao_hash(self, chave):

        soma = 0

        for caractere in str(chave):

            if caractere.isdigit():

                soma += int(caractere)

        return soma % self.tamanho

    def inserir(self, livro):

        posicao = self._funcao_hash(livro.isbn)
        novo_nodo = Hash_Node(livro)

        if self.baldes[posicao] is None:

            self.baldes[posicao] = novo_nodo

        else:

            atual = self.baldes[posicao]

            while atual.proximo is not None:

                if atual.livro.isbn == livro.isbn:

                    atual.livro = livro
                    return
                
                atual = atual.proximo

            if atual.livro.isbn == livro.isbn:

                atual.livro = livro

            else:

                atual.proximo = novo_nodo

    def buscar(self, isbn):

        posicao = self._funcao_hash(isbn)
        atual = self.baldes[posicao]

        while atual is not None:
            if atual.livro.isbn == isbn:
                return atual.livro
            atual = atual.proximo
        return None

    def remover(self, isbn):

        posicao = self._funcao_hash(isbn)
        atual = self.baldes[posicao]
        anterior = None

        while atual is not None:
            if atual.livro.isbn == isbn:
                if anterior is None:
                    self.baldes[posicao] = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                return True
            anterior = atual
            atual = atual.proximo
        return False

class Fila:

    def __init__(self):

        self.inicio = None
        self.fim = None

    def esta_vazia(self):

        return self.inicio is None

    def enfileirar(self, nome_usuario):

        novo_node = Usuario_Node(nome_usuario)

        if self.esta_vazia():
            self.inicio = novo_node
            self.fim = novo_node
        else:
            self.fim.proximo = novo_node
            self.fim = novo_node

        print(f"Usuário '{nome_usuario}' adicionado à fila de espera.")

    def desenfileirar(self):

        if self.esta_vazia():
            print("A fila de espera está vazia.")
            return None

        usuario_atendido = self.inicio.nome_usuario
        self.inicio = self.inicio.proximo

        if self.inicio is None:
            self.fim = None

        return usuario_atendido

    def exibir_fila(self):

        if self.esta_vazia():
            print("Nenhum usuário na fila de espera.")
            return

        atual = self.inicio
        posicao = 1
        print(" - Fila de Espera Atual -")
        while atual is not None:
            print(f"{posicao}º - {atual.nome_usuario}")
            atual = atual.proximo
            posicao += 1

class Pilha:

    def __init__(self):

        self.topo = None

    def esta_vazia(self):

        return self.topo is None

    def empilhar(self, isbn, usuario):

        novo_nodo = Op_Node(isbn, usuario)
        novo_nodo.proximo = self.topo
        self.topo = novo_nodo

    def desempilhar(self):

        if self.esta_vazia():
            return None
        
        operacao = self.topo
        self.topo = self.topo.proximo
        return operacao


class Lista_Encadeada:

    def __init__(self):

        self.head = None

    def inserir_no_inicio(self, livro):

        novo_node = Livro_Node(livro)
        novo_node.proximo = self.head
        self.head = novo_node

    def inserir(self, livro):

        novo_node = Livro_Node(livro)
        atual = self.head

        if self.head == None:
            self.head = novo_node
            self.head.proximo = None
            return
        else:
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_node
            return

    def buscar_por_isbn(self, isbn):

        atual = self.head

        while atual is not None:
            if atual.livro.isbn == isbn:
                return atual.livro
            atual = atual.proximo
        return None

    def remover_por_isbn(self, isbn):

        atual = self.head
        anterior = None

        if atual is not None and atual.livro.isbn == isbn:
            self.head = atual.proximo
            return True

        while atual is not None and atual.livro.isbn != isbn:
            anterior = atual
            atual = atual.proximo

        if atual is None:
            return False

        anterior.proximo = atual.proximo
        return True

    def exibir_todos(self):

        atual = self.head
        if atual is None:
            print("A lista está vazia.")
            return

        while atual is not None:
            print(f"Título: {atual.livro.titulo} | Autor: {atual.livro.autor} | ISBN: {atual.livro.isbn} | Qtd: {atual.livro.qtd_exemplares}")
            atual = atual.proximo


class Arvore_Binaria:

    def __init__(self):

        self.raiz = None

    def inserir(self, livro):

        novo_node = Livro_Node(livro)

        if self.raiz is None:
            self.raiz = novo_node
        else:
            self._inserir_recursivo(self.raiz, novo_node)

    def _inserir_recursivo(self, node_atual, novo_node):

        if novo_node.livro.titulo.lower() < node_atual.livro.titulo.lower():
            if node_atual.esquerda is None:
                node_atual.esquerda = novo_node
            else:
                self._inserir_recursivo(node_atual.esquerda, novo_node)
        else:
            if node_atual.direita is None:
                node_atual.direita = novo_node
            else:
                self._inserir_recursivo(node_atual.direita, novo_node)

    def exibir_em_ordem(self):

        if self.raiz is None:
            print("A árvore está vazia.")
        else:
            self._exibir_em_ordem_recursivo(self.raiz)

    def _exibir_em_ordem_recursivo(self, node_atual):

        if node_atual is not None:
            self._exibir_em_ordem_recursivo(node_atual.esquerda)
            print(f"Título: {node_atual.livro.titulo} | ISBN: {node_atual.livro.isbn}")
            self._exibir_em_ordem_recursivo(node_atual.direita)

    def remover_por_titulo(self, titulo):

        self.raiz = self._remover_recursivo(self.raiz, titulo)

    def _remover_recursivo(self, node_atual, titulo):

        if node_atual is None:
            return None

        if titulo.lower() < node_atual.livro.titulo.lower():
            node_atual.esquerda = self._remover_recursivo(node_atual.esquerda, titulo)
        elif titulo.lower() > node_atual.livro.titulo.lower():
            node_atual.direita = self._remover_recursivo(node_atual.direita, titulo)
        else:
            if node_atual.esquerda is None:
                return node_atual.direita
            elif node_atual.direita is None:
                return node_atual.esquerda

            sucessor = self._encontrar_minimo(node_atual.direita)
            node_atual.livro = sucessor.livro
            node_atual.direita = self._remover_recursivo(node_atual.direita, sucessor.livro.titulo)

        return node_atual

    def _encontrar_minimo(self, nodo):

        atual = nodo
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual


class Biblioteca:

    def __init__(self):

        self.lista_livros = Lista_Encadeada()
        self.arvore_titulo = Arvore_Binaria()
        self.tabela_hash = Tabela_Hash()
        self.historico_emprestimos = Pilha()

    def cadastrar_livro(self, livro):

        self.lista_livros.inserir(livro)
        self.arvore_titulo.inserir(livro)
        self.tabela_hash.inserir(livro)

    def remover_livro(self, livro_ISBN):

        livro = self.tabela_hash.buscar(livro_ISBN)

        if livro is not None:

            self.lista_livros.remover_por_isbn(livro_ISBN)
            self.arvore_titulo.remover_por_titulo(livro.titulo)
            self.tabela_hash.remover(livro_ISBN)
            print(f"Livro '{livro.titulo}' totalmente removido do sistema.")

        else:
            print("Livro não encontrado.")

    def buscar_livro_por_isbn(self, isbn):

        livro = self.tabela_hash.buscar(isbn)

        if livro:

            print(f"Livro Encontrado -> Título: {livro.titulo} | Autor: {livro.autor} | Exemplares: {livro.qtd_exemplares}")
            return livro
        
        print("Livro não encontrado via Tabela Hash.")

        return None

    def listar_livros_ordem_alfabetica(self):

        self.arvore_titulo.exibir_em_ordem()

    def realizar_emprestimo(self, isbn, nome_usuario):

        livro = self.tabela_hash.buscar(isbn)

        if livro is None:

            print("Impossível emprestar: Livro não cadastrado.")

            return

        if livro.qtd_exemplares > 0:

            livro.qtd_exemplares -= 1

            self.historico_emprestimos.empilhar(isbn, nome_usuario)
            print(f"Empréstimo de '{livro.titulo}' realizado para {nome_usuario}.")

        else:

            print(f"Não há exemplares de '{livro.titulo}' livres.")

            atual = self.arvore_titulo.raiz
            nodo_da_fila = None
            
            while atual is not None:
                if livro.titulo.lower() == atual.livro.titulo.lower():
                    nodo_da_fila = atual
                    break
                elif livro.titulo.lower() < atual.livro.titulo.lower():
                    atual = atual.esquerda
                else:
                    atual = atual.direita
            
            if nodo_da_fila:
                nodo_da_fila.fila_espera.enfileirar(nome_usuario)

    def realizar_devolucao(self, isbn):

        livro = self.tabela_hash.buscar(isbn)

        if livro is None:

            print("Livro inválido para devolução.")

            return

        atual = self.arvore_titulo.raiz

        nodo_da_fila = None

        while current_node := atual: 

            if livro.titulo.lower() == current_node.livro.titulo.lower():
                nodo_da_fila = current_node
                break

            elif livro.titulo.lower() < current_node.livro.titulo.lower():
                atual = current_node.esquerda

            else:
                atual = current_node.direita

        if nodo_da_fila and not nodo_da_fila.fila_espera.esta_vazia():

            proximo_usuario = nodo_da_fila.fila_espera.desenfileirar()
            print(f"Livro '{livro.titulo}' devolvido e transferido para o próximo da fila: {proximo_usuario}.")
            self.historico_emprestimos.empilhar(isbn, proximo_usuario)

        else:

            livro.qtd_exemplares += 1
            print(f"Livro '{livro.titulo}' devolvido ao acervo. Novo estoque: {livro.qtd_exemplares}")

    def desfazer_ultimo_emprestimo(self):

        ultimo_registro = self.historico_emprestimos.desempilhar()

        if ultimo_registro is None:

            print("Nenhuma operação recente para desfazer.")

            return

        livro = self.tabela_hash.buscar(ultimo_registro.isbn)

        if livro:

            livro.qtd_exemplares += 1
            print(f"Operação desfeita: O empréstimo para '{ultimo_registro.usuario}' foi cancelado.")
            print(f"Estoque restaurado para '{livro.titulo}': {livro.qtd_exemplares}")

    def gerar_relatorio_geral(self):

        print("\n - RELATÓRIO DO ACERVO - ")
        self.lista_livros.exibir_todos()

# --- Execução de Teste do Fluxo Completo ---

Oteca = Biblioteca()

livro1 = Livro("1234567890123", "Harry Potter e a Pedra Filosofal", "Juscelino K.", 2022, 3)
livro2 = Livro("2345678901234", "Persista!", "Elthon", 2026, 1)
livro3 = Livro("3456789012345", "My Campbell", "eu", 2026, 0) 

Oteca.cadastrar_livro(livro1)
Oteca.cadastrar_livro(livro2)
Oteca.cadastrar_livro(livro3)

print("\n1. Listagem em Ordem Alfabética (BST)")
Oteca.listar_livros_ordem_alfabetica()

print("\n2. Testando Busca Eficiente (Hash)")
Oteca.buscar_livro_por_isbn("2345678901234")

print("\n3. Fluxo de Empréstimo e Desfazer (Pilha)")
Oteca.realizar_emprestimo("2345678901234", "Marcos")
Oteca.desfazer_ultimo_emprestimo()

print("\n4. Fluxo de Fila de Espera (Fila)")
Oteca.realizar_emprestimo("3456789012345", "Bruna")
Oteca.realizar_devolucao("3456789012345")

print("\n5. Relatório Final Geral (Lista Encadeada)")
Oteca.gerar_relatorio_geral()
