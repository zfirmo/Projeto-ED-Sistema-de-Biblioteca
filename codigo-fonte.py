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

class Biblioteca:

    def __init__(self):
        self.lista_livros = Lista_Encadeada()

    def cadastrar_livro(self, livro):
        self.lista_livros.inserir(livro)

    def exibir_todos(self):
        self.lista_livros.exibir_todos()

 
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

Oteca = Biblioteca()

livro1 = Livro("1234567890123","Pare de se Odiar", "Alexandrismos",2022,3)
livro2 = Livro("2345678901234","Amanhã tem prova de Cálculo", "coitado",2026,1)
livro3 = Livro("3456789012345","Eu não aguento mais", "eu",2026,100)

Oteca.cadastrar_livro(livro1)
Oteca.cadastrar_livro(livro2)
Oteca.cadastrar_livro(livro3)

Oteca.exibir_todos()