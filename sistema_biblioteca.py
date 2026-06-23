class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, ano_publicacao: int, qtd_exemplares: int):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.qtd_exemplares = qtd_exemplares
        self.qtd_maxima_original = qtd_exemplares 

class Livro_Node:
    def __init__(self, livre):
        self.livro = livre
        self.proximo = None
        self.direita = None
        self.esquerda = None
        self.fila_espera = Fila()

class Usuario:
    def __init__(self, nome_usuario: str):
        self.nome_usuario = nome_usuario

class Usuario_Node:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario
        self.proximo = None

class Hash_Node:
    def __init__(self, livro):
        self.livro = livro
        self.proximo = None

class Op_Node:
    def __init__(self, tipo_op, isbn, usuario=None):
        self.tipo_op = tipo_op
        self.isbn = isbn
        self.usuario = usuario
        self.proximo = None

class Vetor_Estatico:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self._memoria = [None] * tamanho

    def get(self, indice):
        if 0 <= indice < self.tamanho:
            return self._memoria[indice]
        raise IndexError("Vetor: Índice fora dos limites")

    def set(self, indice, valor):
        if 0 <= indice < self.tamanho:
            self._memoria[indice] = valor
        else:
            raise IndexError("Vetor: Índice fora dos limites")

class Tabela_Hash:
    def __init__(self, tamanho=50):
        self.tamanho = tamanho
        self.baldes = Vetor_Estatico(tamanho)

    def _funcao_hash(self, chave):
        soma = sum(ord(caractere) for caractere in str(chave))
        return soma % self.tamanho

    def inserir(self, livro):
        posicao = self._funcao_hash(livro.isbn)
        novo_nodo = Hash_Node(livro)

        if self.baldes.get(posicao) is None:
            self.baldes.set(posicao, novo_nodo)
            return True
        else:
            atual = self.baldes.get(posicao)
            while True:
                if str(atual.livro.isbn) == str(livro.isbn):
                    return False
                if atual.proximo is None:
                    break
                atual = atual.proximo
            atual.proximo = novo_nodo
            return True

    def buscar(self, isbn):
        posicao = self._funcao_hash(isbn)
        atual = self.baldes.get(posicao)
        while atual is not None:
            if str(atual.livro.isbn) == str(isbn):
                return atual.livro
            atual = atual.proximo
        return None

    def remover(self, isbn):
        posicao = self._funcao_hash(isbn)
        atual = self.baldes.get(posicao)
        anterior = None

        while atual is not None:
            if str(atual.livro.isbn) == str(isbn):
                if anterior is None:
                    self.baldes.set(posicao, atual.proximo)
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

    def enfileirar(self, usuario: Usuario):
        novo_node = Usuario_Node(usuario)
        if self.esta_vazia():
            self.inicio = novo_node
            self.fim = novo_node
        else:
            self.fim.proximo = novo_node
            self.fim = novo_node
        print(f"Usuário '{usuario.nome_usuario}' adicionado à fila de espera.")

    def desenfileirar(self):
        if self.esta_vazia():
            print("A fila de espera está vazia.")
            return None
        usuario_atendido = self.inicio.usuario.nome_usuario
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        return usuario_atendido

    def remover_usuario_da_fila(self, nome_usuario):
        if self.esta_vazia():
            return False
        atual = self.inicio
        anterior = None
        while atual is not None:
            if atual.usuario.nome_usuario == nome_usuario:
                if anterior is None:  
                    self.inicio = atual.proximo
                    if self.inicio is None:
                        self.fim = None
                else:
                    anterior.proximo = atual.proximo
                    if atual == self.fim:  
                        self.fim = anterior
                return True
            anterior = atual
            atual = atual.proximo
        return False

class Pilha:
    def __init__(self):
        self.topo = None

    def esta_vazia(self):
        return self.topo is None

    def empilhar(self, tipo_op, isbn, usuario=None):
        novo_nodo = Op_Node(tipo_op, isbn, usuario)
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

    def inserir(self, livro):
        novo_node = Livro_Node(livro)
        if self.head is None:
            self.head = novo_node
            return
        atual = self.head
        while atual.proximo is not None:
            atual = atual.proximo
        atual.proximo = novo_node

    def buscar_por_isbn(self, isbn):
        atual = self.head
        while atual is not None:
            if str(atual.livro.isbn) == str(isbn):
                return atual.livro
            atual = atual.proximo
        return None

    def remover_por_isbn(self, isbn):
        atual = self.head
        anterior = None
        
        if atual is not None and str(atual.livro.isbn) == str(isbn):
            self.head = atual.proximo
            return True
            
        while atual is not None and str(atual.livro.isbn) != str(isbn):
            anterior = atual
            atual = atual.proximo

        if atual is None:
            return False
            
        anterior.proximo = atual.proximo
        return True

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
        if str(novo_node.livro.titulo).lower() < str(node_atual.livro.titulo).lower():
            if node_atual.esquerda is None:
                node_atual.esquerda = novo_node
            else:
                self._inserir_recursivo(node_atual.esquerda, novo_node)
        else:
            if node_atual.direita is None:
                node_atual.direita = novo_node
            else:
                self._inserir_recursivo(node_atual.direita, novo_node)

    def buscar_nodo_recursivo(self, node_atual, titulo):
        if node_atual is None:
            return None
        if str(titulo).lower() == str(node_atual.livro.titulo).lower():
            return node_atual
        if str(titulo).lower() < str(node_atual.livro.titulo).lower():
            return self.buscar_nodo_recursivo(node_atual.esquerda, titulo)
        return self.buscar_nodo_recursivo(node_atual.direita, titulo)

    def percorrer_em_ordem(self, node_atual):
        if node_atual is not None:
            self.percorrer_em_ordem(node_atual.esquerda)
            print(f"Título: {node_atual.livro.titulo} | Autor: {node_atual.livro.autor} | ISBN: {node_atual.livro.isbn} | Qtd: {node_atual.livro.qtd_exemplares}")
            self.percorrer_em_ordem(node_atual.direita)

    def remover_por_titulo(self, titulo):
        self.raiz = self._remover_recursivo(self.raiz, titulo)

    def _remover_recursivo(self, node_atual, titulo):
        if node_atual is None:
            return None
        if str(titulo).lower() < str(node_atual.livro.titulo).lower():
            node_atual.esquerda = self._remover_recursivo(node_atual.esquerda, titulo)
        elif str(titulo).lower() > str(node_atual.livro.titulo).lower():
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

        isbn_str = str(livro.isbn).strip()
        
        if not isbn_str.isdigit():
            print(f"Erro: O ISBN '{isbn_str}' deve conter apenas números.")
            return False

        tamanho = len(isbn_str)
        if tamanho != 10 and tamanho != 13:
            print(f"Erro: O ISBN deve possuir exatamente 10 ou 13 dígitos (Digitado: {tamanho}).")
            return False

        if livro.qtd_exemplares <= 0:
            print(f"Erro ao cadastrar '{livro.titulo}': A quantidade de exemplares deve ser maior que zero.")
            return False

        if self.tabela_hash.buscar(livro.isbn) is not None:
            print(f"Erro: O ISBN '{livro.isbn}' já está cadastrado no sistema (Livro duplicado).")
            return False

        self.tabela_hash.inserir(livro)
        self.lista_livros.inserir(livro)
        self.arvore_titulo.inserir(livro)
        print(f"Livro '{livro.titulo}' cadastrado com sucesso com {livro.qtd_exemplares} exemplares.")
        return True

    def remover_livro(self, livro_ISBN):
        livro = self.tabela_hash.buscar(livro_ISBN)
        if livro is not None:
            self.lista_livros.remover_por_isbn(livro_ISBN)
            self.arvore_titulo.remover_por_titulo(livro.titulo)
            self.tabela_hash.remover(livro_ISBN)
            print(f"Livro '{livro.titulo}' totalmente removido do sistema.")
        else:
            print("Livro não encontrado.")

    def realizar_emprestimo(self, isbn, nome_usuario):
        livro = self.tabela_hash.buscar(isbn)

        if not livro:
            print("Erro: Livro não encontrado.")
            return

        if livro.qtd_exemplares > 0:
            livro.qtd_exemplares -= 1
            self.historico_emprestimos.empilhar("EMPRESTIMO", isbn, nome_usuario)
            print(f"Empréstimo de '{livro.titulo}' realizado para {nome_usuario}.")
        else:
            print(f"Não há exemplares de '{livro.titulo}' livres.")
            nodo_da_fila = self.arvore_titulo.buscar_nodo_recursivo(self.arvore_titulo.raiz, livro.titulo)
            if nodo_da_fila:
                novo_usuario = Usuario(nome_usuario)
                nodo_da_fila.fila_espera.enfileirar(novo_usuario)
                self.historico_emprestimos.empilhar("ENTROU_FILA", isbn, nome_usuario)
            else:
                print("Erro interno do sistema: Estrutura do livro na árvore não encontrada.")

    def realizar_devolucao(self, isbn):
        livro = self.tabela_hash.buscar(isbn)
        if livro is None:
            print("Livro inválido para devolução (Não consta no acervo).")
            return

        nodo_da_fila = self.arvore_titulo.buscar_nodo_recursivo(self.arvore_titulo.raiz, livro.titulo)

        if nodo_da_fila and not nodo_da_fila.fila_espera.esta_vazia():
            proximo_usuario = nodo_da_fila.fila_espera.desenfileirar()
            print(f"Livro '{livro.titulo}' devolvido e transferido para o próximo da fila: {proximo_usuario}.")
            self.historico_emprestimos.empilhar("EMPRESTIMO", isbn, proximo_usuario)
        else:
            if livro.qtd_exemplares >= livro.qtd_maxima_original:
                print(f"Erro: Todos os {livro.qtd_maxima_original} exemplares de '{livro.titulo}' já estão no acervo. Devolução rejeitada.")
                return
                
            livro.qtd_exemplares += 1
            self.historico_emprestimos.empilhar("DEVOLUCAO", isbn)
            print(f"Livro '{livro.titulo}' devolvido ao acervo. Novo estoque: {livro.qtd_exemplares}")

    def desfazer_ultimo_emprestimo(self):
        ultimo_registro = self.historico_emprestimos.desempilhar()
        if ultimo_registro is None:
            print("Nenhuma operação recente para desfazer.")
            return

        livro = self.tabela_hash.buscar(ultimo_registro.isbn)
        if livro:
            if ultimo_registro.tipo_op == "EMPRESTIMO":
                nodo_da_fila = self.arvore_titulo.buscar_nodo_recursivo(self.arvore_titulo.raiz, livro.titulo)
                if nodo_da_fila and not nodo_da_fila.fila_espera.esta_vazia():
                    proximo_usuario = nodo_da_fila.fila_espera.desenfileirar()
                    print(f"Operação desfeita: Empréstimo cancelado. Exemplar redirecionado para a fila: {proximo_usuario}.")
                else:
                    livro.qtd_exemplares += 1
                    print(f"Operação desfeita: O empréstimo para '{ultimo_registro.usuario}' foi cancelado.")
            elif ultimo_registro.tipo_op == "DEVOLUCAO":
                if livro.qtd_exemplares > 0:
                    livro.qtd_exemplares -= 1
                    print(f"Operação desfeita: A devolução de '{livro.titulo}' foi cancelada.")
                else:
                    print("Erro Crítico: Não foi possível desfazer a devolução pois o estoque já está zerado.")
            elif ultimo_registro.tipo_op == "ENTROU_FILA":
                nodo_da_fila = self.arvore_titulo.buscar_nodo_recursivo(self.arvore_titulo.raiz, livro.titulo)
                if nodo_da_fila:
                    sucesso = nodo_da_fila.fila_espera.remover_usuario_da_fila(ultimo_registro.usuario)
                    if sucesso:
                        print(f"Operação desfeita: O usuário '{ultimo_registro.usuario}' foi removido da fila de espera de '{livro.titulo}'.")
                    else:
                        print("Aviso: O usuário não foi encontrado na fila (pode já ter sido atendido).")

    def gerar_relatorio_geral(self):
        print("\n - RELATÓRIO DO ACERVO (ORDEM ALFABÉTICA) - ")
        if self.arvore_titulo.raiz is None:
            print("A lista está vazia.")
        else:
            self.arvore_titulo.percorrer_em_ordem(self.arvore_titulo.raiz)
