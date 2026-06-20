class Livro:

    def __init__(self,isbn:str,titulo:str,autor:str, ano_publicacao:int,qtd_exemplares:int):

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

class Usuario:

    def __init__(self, nome_usuario, id):
        
        self.nome_usuario = nome_usuario
        self.id = id

class Usuario_Node:

    def __init__(self, usuario):

        self.usuario = Usuario(usuario)
        self.nome_usuario = self.usuario.nome_usuario
        self.proximo = None


class Biblioteca:

    def __init__(self):
        self.lista_livros = Lista_Encadeada()
        self.arvore_titulo = Arvore_Binaria()

    def cadastrar_livro(self, livro):
        self.lista_livros.inserir(livro)
        self.arvore_titulo.inserir(livro)

    def remover_livro(self, livro_ISBN):
        self.lista_livros.remover_por_isbn()
        self.arvore_titulo.remover_por_titulo()

    def listar_livros_ordem_alfabetica(self):
        self.arvore_titulo.exibir_em_ordem()

    def realizar_emprestimo():

        pass

    def realizar_devolucao():

        pass

    
 
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
            print(f"Título: {atual.livro.titulo} | ISBN: {atual.livro.isbn}")
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

Oteca = Biblioteca()

livro1 = Livro("1234567890123","Pare de se Odiar", "Alexandrismos",2022,3)
livro2 = Livro("2345678901234","Amanhã tem prova de Cálculo", "coitado",2026,1)
livro3 = Livro("3456789012345","Eu não aguento mais", "eu",2026,100)

Oteca.cadastrar_livro(livro1)
Oteca.cadastrar_livro(livro2)
Oteca.cadastrar_livro(livro3)

Oteca.exibir_todos()