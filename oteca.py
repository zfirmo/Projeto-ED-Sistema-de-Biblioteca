import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import os
import shutil
import datetime
from sistema_biblioteca import Biblioteca, Livro, Vetor_Estatico

ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

COR_FUNDO_GERAL = "#C8AB92"     
COR_CARD_BG = "#FFFFFF"         
COR_SIDEBAR = "#A8998E"         
COR_SIDEBAR_ATIVO = "#4A3B32"  
COR_TEXTO_MAIN = "#1A1A1A"      
COR_TEXTO_MUTED = "#5E544F"    
COR_LINHA_INPUT = "#B0A6A0"     
COR_AZUL_BOTON = "#4C6B9C"      
COR_AZUL_HOVER = "#3B537A"      
COR_VERMELHO = "#C95A5A"        
COR_VERMELHO_HOVER = "#A84444"  

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 11)   
FONT_TEXT = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 12, "bold")

class NodeSimples:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class Lista_Encadeada_Historico:
    def __init__(self):
        self.head = None
        self.tail = None
        self.tamanho = 0

    def adicionar(self, valor):
        novo = NodeSimples(valor)
        if self.head is None:
            self.head = novo
            self.tail = novo
        else:
            self.tail.proximo = novo
            self.tail = novo
        self.tamanho += 1

    def extrair_texto(self):
        atual = self.head
        texto = ""
        while atual is not None:
            texto += atual.valor + "\n"
            atual = atual.proximo
        return texto

class NodeMapa:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.proximo = None

class Tabela_Hash_Capas:
    def __init__(self, tamanho=50):
        self.tamanho = tamanho
        self.baldes = Vetor_Estatico(tamanho)

    def _hash(self, chave):
        soma = sum(ord(c) for c in str(chave))
        return soma % self.tamanho

    def put(self, chave, valor):
        pos = self._hash(chave)
        novo = NodeMapa(chave, valor)
        if self.baldes.get(pos) is None:
            self.baldes.set(pos, novo)
        else:
            atual = self.baldes.get(pos)
            while True:
                if str(atual.chave) == str(chave):
                    atual.valor = valor
                    return
                if atual.proximo is None:
                    break
                atual = atual.proximo
            atual.proximo = novo

    def get(self, chave):
        pos = self._hash(chave)
        atual = self.baldes.get(pos)
        while atual is not None:
            if str(atual.chave) == str(chave):
                return atual.valor
            atual = atual.proximo
        return None

    def contem(self, chave):
        return self.get(chave) is not None

class OtecaModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OTECA - Sistema de Biblioteca")
        self.root.geometry("1180x750")
        self.root.configure(fg_color=COR_FUNDO_GERAL)
        
        self.biblio = Biblioteca()
        self.historico_acoes = Lista_Encadeada_Historico()
        self.registrar_acao("Sistema iniciado.")
        
        self.capas_db = Tabela_Hash_Capas()
        self.capa_temp_path = None
        self.img_ref_atual = None

        self.criar_estruturas_principais()
        self.construir_tela_cadastro()
        self.construir_tela_emprestimo()
        self.construir_tela_consulta()
        
        self.mostrar_frame(self.frame_cadastro, self.btn_nav_cadastro)

    def registrar_acao(self, mensagem):
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.historico_acoes.adicionar(f"[{agora}] {mensagem}")

    def criar_input_moderno(self, parent, label_text, icone=""):
        frame = ctk.CTkFrame(parent, fg_color=COR_CARD_BG)
        texto_label = f"{icone}  {label_text}" if icone else label_text
        lbl = ctk.CTkLabel(frame, text=texto_label, font=FONT_LABEL, text_color=COR_TEXTO_MUTED, anchor="w")
        lbl.pack(fill="x", pady=(0, 4))
        
        entry = ctk.CTkEntry(frame, font=FONT_TEXT, text_color=COR_TEXTO_MAIN, fg_color=COR_CARD_BG, 
                             border_color=COR_LINHA_INPUT, border_width=1, height=35, corner_radius=6)
        entry.pack(fill="x", pady=(0, 18))
        return frame, entry

    def criar_estruturas_principais(self):
        self.header = ctk.CTkFrame(self.root, fg_color=COR_FUNDO_GERAL, height=120, corner_radius=0)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        logo_container = ctk.CTkFrame(self.header, fg_color=COR_FUNDO_GERAL)
        logo_container.pack(expand=True)
        
        try:
            imagem_pil = Image.open("oteca_logo.png") 
            self.logo_ctk = ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(250, 250))
            lbl_logo = ctk.CTkLabel(logo_container, image=self.logo_ctk, text="")
            lbl_logo.pack(anchor="center")
        except Exception:
            lbl_brand = ctk.CTkLabel(logo_container, text="OTECA 📚", text_color=COR_SIDEBAR_ATIVO, font=("Segoe UI", 28, "bold"))
            lbl_brand.pack(anchor="center")

        lbl_subbrand = ctk.CTkLabel(logo_container, text="Sistema de Gerenciamento de Biblioteca", text_color=COR_TEXTO_MUTED, font=("Segoe UI", 11))
        lbl_subbrand.pack(anchor="center", pady=(5, 0))

        self.sidebar = ctk.CTkFrame(self.root, fg_color=COR_SIDEBAR, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        lbl_nav = ctk.CTkLabel(self.sidebar, text="NAVEGAÇÃO", text_color="#F4EFEA", font=("Segoe UI", 10, "bold"), anchor="w")
        lbl_nav.pack(pady=(40, 15), padx=25, fill="x")

        self.btn_nav_cadastro = ctk.CTkButton(self.sidebar, text="  📋   Cadastrar Livro", fg_color=COR_SIDEBAR, 
                                             text_color="#ECE6E1", hover_color=COR_SIDEBAR_ATIVO, font=FONT_BTN,
                                             height=45, corner_radius=8, anchor="w", command=lambda: self.mostrar_frame(self.frame_cadastro, self.btn_nav_cadastro))
        self.btn_nav_cadastro.pack(fill="x", pady=4, padx=12)

        self.btn_nav_emprestimo = ctk.CTkButton(self.sidebar, text="  ⇄   Empréstimos", fg_color=COR_SIDEBAR, 
                                               text_color="#ECE6E1", hover_color=COR_SIDEBAR_ATIVO, font=FONT_BTN,
                                               height=45, corner_radius=8, anchor="w", command=lambda: self.mostrar_frame(self.frame_emprestimo, self.btn_nav_emprestimo))
        self.btn_nav_emprestimo.pack(fill="x", pady=4, padx=12)

        self.btn_nav_consulta = ctk.CTkButton(self.sidebar, text="  ⌕   Consultar Acervo", fg_color=COR_SIDEBAR, 
                                             text_color="#ECE6E1", hover_color=COR_SIDEBAR_ATIVO, font=FONT_BTN,
                                             height=45, corner_radius=8, anchor="w", command=lambda: self.mostrar_frame(self.frame_consulta, self.btn_nav_consulta))
        self.btn_nav_consulta.pack(fill="x", pady=4, padx=12)

        self.main_content = ctk.CTkFrame(self.root, fg_color=COR_FUNDO_GERAL, corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True, padx=40, pady=10)

        self.frame_cadastro = ctk.CTkFrame(self.main_content, fg_color=COR_FUNDO_GERAL)
        self.frame_emprestimo = ctk.CTkFrame(self.main_content, fg_color=COR_FUNDO_GERAL)
        self.frame_consulta = ctk.CTkFrame(self.main_content, fg_color=COR_FUNDO_GERAL)

    def mostrar_frame(self, frame_alvo, botao_ativo):
        self.btn_nav_cadastro.configure(fg_color=COR_SIDEBAR, text_color="#ECE6E1")
        self.btn_nav_emprestimo.configure(fg_color=COR_SIDEBAR, text_color="#ECE6E1")
        self.btn_nav_consulta.configure(fg_color=COR_SIDEBAR, text_color="#ECE6E1")
        
        botao_ativo.configure(fg_color=COR_SIDEBAR_ATIVO, text_color="white")
        self.frame_cadastro.pack_forget()
        self.frame_emprestimo.pack_forget()
        self.frame_consulta.pack_forget()
        frame_alvo.pack(fill="both", expand=True)

    def construir_tela_cadastro(self):
        lbl_secao = ctk.CTkLabel(self.frame_cadastro, text="Cadastro de Livros no Acervo", font=("Segoe UI Light", 18), text_color=COR_TEXTO_MAIN, anchor="w")
        lbl_secao.pack(fill="x", pady=(10, 15))
        
        card = ctk.CTkFrame(self.frame_cadastro, fg_color=COR_CARD_BG, corner_radius=12, border_color="#E1DCD6", border_width=1)
        card.pack(fill="x", anchor="n", ipady=15)

        form_frame = ctk.CTkFrame(card, fg_color=COR_CARD_BG)
        form_frame.pack(fill="x", padx=35, pady=30)

        col1 = ctk.CTkFrame(form_frame, fg_color=COR_CARD_BG)
        col1.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        frame_isbn, self.ent_isbn = self.criar_input_moderno(col1, "ISBN (Apenas números - 10 ou 13 dígitos):", "║▌║")
        frame_isbn.pack(fill="x")
        
        frame_titulo, self.ent_titulo = self.criar_input_moderno(col1, "Título do Livro:", "📖")
        frame_titulo.pack(fill="x")
        
        frame_autor, self.ent_autor = self.criar_input_moderno(col1, "Autor Principal:", "👥")
        frame_autor.pack(fill="x")

        col2 = ctk.CTkFrame(form_frame, fg_color=COR_CARD_BG)
        col2.pack(side="right", fill="x", expand=True, padx=(20, 0))
        
        frame_ano, self.ent_ano = self.criar_input_moderno(col2, "Ano de Publicação:", "📅")
        frame_ano.pack(fill="x")
        
        frame_qtd, self.ent_qtd = self.criar_input_moderno(col2, "Quantidade de Exemplares:", "📚")
        frame_qtd.pack(fill="x")
        
        capa_frame = ctk.CTkFrame(col2, fg_color=COR_CARD_BG)
        capa_frame.pack(fill="x")
        ctk.CTkLabel(capa_frame, text="🖼  Capa do Livro (.png):", font=FONT_LABEL, text_color=COR_TEXTO_MUTED, anchor="w").pack(fill="x")
        
        status_container = ctk.CTkFrame(capa_frame, fg_color=COR_CARD_BG)
        status_container.pack(fill="x", pady=(4, 0))
        
        self.lbl_capa_status = ctk.CTkLabel(status_container, text="Nenhuma imagem anexada", text_color="#948A84", font=("Segoe UI", 10, "italic"))
        self.lbl_capa_status.pack(side="left", pady=5)
        
        btn_upload = ctk.CTkButton(status_container, text="Anexar Imagem", fg_color="white", text_color=COR_TEXTO_MUTED,
                                   hover_color="#F4EFEA", border_color=COR_LINHA_INPUT, border_width=1,
                                   height=30, corner_radius=6, font=("Segoe UI", 10, "bold"), command=self.selecionar_capa)
        btn_upload.pack(side="right")

        btn_confirmar = ctk.CTkButton(card, text="Confirmar Cadastro do Livro", fg_color=COR_AZUL_BOTON,
                                     hover_color=COR_AZUL_HOVER, font=FONT_BTN, text_color="white",
                                     height=45, corner_radius=8, command=self.cadastrar_livro)
        btn_confirmar.pack(fill="x", padx=35, pady=(0, 20))

    def selecionar_capa(self):
        caminho = filedialog.askopenfilename(title="Selecione a Imagem da Capa", filetypes=[("Imagens PNG", "*.png")])
        if caminho:
            self.capa_temp_path = caminho
            self.lbl_capa_status.configure(text=f"Pronto: {os.path.basename(caminho)[:18]}...", text_color=COR_AZUL_BOTON)

    def cadastrar_livro(self):
        isbn = self.ent_isbn.get().strip()
        titulo = self.ent_titulo.get().strip()
        autor = self.ent_autor.get().strip()
        raw_ano = self.ent_ano.get().strip()
        raw_qtd = self.ent_qtd.get().strip()
        
        if not (isbn and titulo and autor and raw_ano and raw_qtd):
            messagebox.showerror("Campos Vazios", "Todos os campos do formulário devem ser preenchidos.")
            return

        try:
            ano = int(raw_ano)
            qtd = int(raw_qtd)
        except ValueError:
            messagebox.showerror("Erro de Tipo", "Ano e Quantidade devem ser números inteiros.")
            return

        novo_livro = Livro(isbn, titulo, autor, ano, qtd)
        sucesso = self.biblio.cadastrar_livro(novo_livro)
        
        if sucesso:
            if self.capa_temp_path:
                self.capas_db.put(isbn, self.capa_temp_path)
                self.capa_temp_path = None
                self.lbl_capa_status.configure(text="Nenhuma capa anexada", text_color="#777777")

            self.registrar_acao(f"Cadastro: O livro '{titulo}' foi adicionado.")
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")
            
            self.ent_isbn.delete(0, tk.END)
            self.ent_titulo.delete(0, tk.END)
            self.ent_autor.delete(0, tk.END)
            self.ent_ano.delete(0, tk.END)
            self.ent_qtd.delete(0, tk.END)
        else:
            messagebox.showerror("Erro de Validação", "Não foi possível cadastrar. Verifique os critérios (ISBN repetido, tamanho ou caracteres inválidos).")

    def construir_tela_emprestimo(self):
        ctk.CTkLabel(self.frame_emprestimo, text="Controle de Circulação", font=("Segoe UI Light", 18), text_color=COR_TEXTO_MAIN, anchor="w").pack(fill="x", pady=(10, 15))
        card = ctk.CTkFrame(self.frame_emprestimo, fg_color=COR_CARD_BG, corner_radius=12, border_color="#E1DCD6", border_width=1)
        card.pack(fill="x", anchor="n", padx=1, pady=1)

        fields_frame = ctk.CTkFrame(card, fg_color=COR_CARD_BG)
        fields_frame.pack(fill="x", padx=35, pady=30)

        frame_emp_isbn, self.ent_emp_isbn = self.criar_input_moderno(fields_frame, "ISBN do Livro:", "║▌║")
        frame_emp_isbn.pack(fill="x")
        
        frame_emp_user, self.ent_emp_user = self.criar_input_moderno(fields_frame, "Nome do Usuário (Apenas para Empréstimos):", "👤")
        frame_emp_user.pack(fill="x")

        btn_box = ctk.CTkFrame(card, fg_color=COR_CARD_BG)
        btn_box.pack(fill="x", padx=35, pady=(0, 30))
        
        ctk.CTkButton(btn_box, text="Realizar Empréstimo", fg_color=COR_AZUL_BOTON, hover_color=COR_AZUL_HOVER, font=FONT_BTN, height=40, corner_radius=8, command=self.realizar_emprestimo).pack(side="left", padx=(0, 15))
        ctk.CTkButton(btn_box, text="Registrar Devolução", fg_color=COR_AZUL_BOTON, hover_color=COR_AZUL_HOVER, font=FONT_BTN, height=40, corner_radius=8, command=self.realizar_devolucao).pack(side="left", padx=(0, 15))
        ctk.CTkButton(btn_box, text="Desfazer Última Operação", fg_color=COR_VERMELHO, hover_color=COR_VERMELHO_HOVER, font=FONT_BTN, height=40, corner_radius=8, command=self.desfazer_emprestimo).pack(side="right")

    def realizar_emprestimo(self):
        isbn = self.ent_emp_isbn.get().strip()
        user = self.ent_emp_user.get().strip()
        
        if not isbn or not user:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha o ISBN e o Nome do Usuário.")
            return

        livro = self.biblio.tabela_hash.buscar(isbn)
        if not livro:
            messagebox.showerror("Erro no Empréstimo", "Erro: O livro com o ISBN informado não foi localizado no acervo.")
            return

        tinha_estoque = livro.qtd_exemplares > 0
        sucesso = self.biblio.realizar_emprestimo(isbn, user)
        
        if sucesso:
            if tinha_estoque:
                msg_sucesso = f"Empréstimo realizado!\n\n👤 Usuário: {user}\n📖 Livro: {livro.titulo}\n🔢 ISBN: {isbn}\n\nRetirada registrada com sucesso."
                self.registrar_acao(f"Empréstimo de '{livro.titulo}' para {user}.")
                messagebox.showinfo("Sucesso no Empréstimo", msg_sucesso)
            else:
                msg_fila = f"Estoque esgotado!\n\n👤 Usuário: {user}\n📖 Livro: {livro.titulo}\n\n{user} foi adicionado com sucesso à fila de espera deste livro."
                self.registrar_acao(f"{user} entrou na fila de espera de '{livro.titulo}'.")
                messagebox.showinfo("Fila de Espera", msg_fila)
            
            self.ent_emp_isbn.delete(0, tk.END)
            self.ent_emp_user.delete(0, tk.END)

    def realizar_devolucao(self):
        isbn = self.ent_emp_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Campos Incompletos", "Por favor, insira o código ISBN para registrar a devolução.")
            return
            
        livro = self.biblio.tabela_hash.buscar(isbn)
        if not livro:
            messagebox.showerror("Erro na Devolução", "Erro: O livro com o ISBN informado não foi localizado no acervo.")
            return
            
        if livro.qtd_exemplares >= livro.qtd_maxima_original:
            messagebox.showerror("Erro na Devolução", f"Erro: Todos os {livro.qtd_maxima_original} exemplares de '{livro.titulo}' já constam no acervo. Devolução rejeitada.")
            return

        nodo_da_fila = self.biblio.arvore_titulo.buscar_nodo_recursivo(self.biblio.arvore_titulo.raiz, livro.titulo)
        tem_fila = nodo_da_fila and not nodo_da_fila.fila_espera.esta_vazia()
        
        proximo_da_fila = "Próximo usuário"
        if tem_fila and nodo_da_fila.fila_espera.inicio:
            proximo_da_fila = nodo_da_fila.fila_espera.inicio.usuario.nome_usuario

        self.biblio.realizar_devolucao(isbn)
        
        if tem_fila:
            msg_dev_fila = f"Devolução processada!\n\n📖 Livro: {livro.titulo}\n🔄 Status: Exemplar transferido imediatamente.\n👤 Destinatário: {proximo_da_fila} (Saiu da fila de espera)."
            self.registrar_acao(f"Livro '{livro.titulo}' devolvido e passado para {proximo_da_fila}.")
            messagebox.showinfo("Devolução com Fila Atendida", msg_dev_fila)
        else:
            msg_dev_sucesso = f"Devolução concluída!\n\n📖 Livro: {livro.titulo}\n📦 Novo Estoque: {livro.qtd_exemplares} exemplar(es)."
            self.registrar_acao(f"Livro '{livro.titulo}' devolvido ao acervo.")
            messagebox.showinfo("Sucesso na Devolução", msg_dev_sucesso)
            
        self.ent_emp_isbn.delete(0, tk.END)
        self.ent_emp_user.delete(0, tk.END)

    def desfazer_emprestimo(self):

        ultimo_registro = self.biblio.historico_emprestimos.topo
        
        if ultimo_registro is None:
            messagebox.showinfo("Pilha Vazia", "Nenhuma operação recente para desfazer no histórico.")
            return
            
        tipo_op = ultimo_registro.tipo_op
        isbn = ultimo_registro.isbn
        usuario = ultimo_registro.usuario
        
        livro = self.biblio.tabela_hash.buscar(isbn)
        titulo_livro = livro.titulo if livro else "Livro Desconhecido"

        self.biblio.desfazer_ultimo_emprestimo()
        
        if tipo_op == "EMPRESTIMO":
            self.registrar_acao(f"Desfazer: Empréstimo de '{titulo_livro}' para {usuario} foi cancelado.")
            messagebox.showinfo("Operação Desfeita", f"O empréstimo do livro '{titulo_livro}' para o usuário '{usuario}' foi cancelado com sucesso e o exemplar retornou ao estoque.")
        elif tipo_op == "DEVOLUCAO":
            self.registrar_acao(f"Desfazer: Devolução de '{titulo_livro}' foi cancelada.")
            messagebox.showinfo("Operação Desfeita", f"A devolução do livro '{titulo_livro}' foi cancelada e o exemplar foi retirado do estoque.")
        elif tipo_op == "ENTROU_FILA":
            self.registrar_acao(f"Desfazer: {usuario} removido da fila de '{titulo_livro}'.")
            messagebox.showinfo("Operação Desfeita", f"O usuário '{usuario}' foi removido com sucesso da fila de espera do livro '{titulo_livro}'.")

    def construir_tela_consulta(self):
        ctk.CTkLabel(self.frame_consulta, text="Consulta de Informações", font=("Segoe UI Light", 18), text_color=COR_TEXTO_MAIN, anchor="w").pack(fill="x", pady=(10, 15))
        search_card = ctk.CTkFrame(self.frame_consulta, fg_color=COR_CARD_BG, corner_radius=12, border_color="#E1DCD6", border_width=1)
        search_card.pack(fill="x", pady=(0, 20), anchor="n")
        
        frame_in, self.ent_busca_isbn = self.criar_input_moderno(search_card, "Insira o ISBN para pesquisar ou remover:", "⌕")
        frame_in.pack(side="left", fill="x", expand=True, padx=25, pady=20)
        
        btn_container = ctk.CTkFrame(search_card, fg_color=COR_CARD_BG)
        btn_container.pack(side="right", padx=25, pady=(15, 0))
        
        ctk.CTkButton(btn_container, text="Buscar", fg_color=COR_AZUL_BOTON, hover_color=COR_AZUL_HOVER, height=36, width=80, corner_radius=6, command=self.buscar_e_exibir_livro).pack(side="left", padx=3)
        ctk.CTkButton(btn_container, text="Remover", fg_color=COR_VERMELHO, hover_color=COR_VERMELHO_HOVER, height=36, width=80, corner_radius=6, command=self.remover_livro).pack(side="left", padx=3)
        ctk.CTkButton(btn_container, text="Relatório", fg_color=COR_SIDEBAR_ATIVO, hover_color="#332822", height=36, width=80, corner_radius=6, command=self.exibir_relatorio_na_tela).pack(side="left", padx=3)
        ctk.CTkButton(btn_container, text="Salvar Log", fg_color=COR_SIDEBAR, hover_color=COR_SIDEBAR_ATIVO, height=36, width=80, corner_radius=6, command=self.guardar_log_txt).pack(side="left", padx=3)

        display_frame = ctk.CTkFrame(self.frame_consulta, fg_color=COR_FUNDO_GERAL)
        display_frame.pack(fill="both", expand=True)

        self.txt_output_box = ctk.CTkTextbox(display_frame, fg_color="white", text_color=COR_TEXTO_MAIN, font=FONT_TEXT, border_color="#E1DCD6", border_width=1, corner_radius=10, activate_scrollbars=True)
        self.txt_output_box.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.txt_output_box.insert(tk.END, "Os relatórios e dados das buscas detalhadas aparecerão nesta caixa.")
        self.txt_output_box.configure(state="disabled")

        self.right_capa_panel = ctk.CTkFrame(display_frame, fg_color=COR_CARD_BG, border_color="#E1DCD6", border_width=1, width=220, corner_radius=10)
        self.right_capa_panel.pack(side="right", fill="y")
        self.right_capa_panel.pack_propagate(False)
        
        ctk.CTkLabel(self.right_capa_panel, text="Capa do Livro", text_color=COR_TEXTO_MUTED, font=("Segoe UI", 11, "bold")).pack(pady=(15, 10))
        
        self.lbl_capa_imagem = tk.Label(self.right_capa_panel, bg="#FBF9F6", text="Sem Imagem", font=FONT_TEXT, bd=0, highlightbackground="#E1DCD6", highlightthickness=1)
        self.lbl_capa_imagem.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.btn_baixar_capa = ctk.CTkButton(self.right_capa_panel, text="💾 Baixar Capa", fg_color=COR_AZUL_BOTON, hover_color=COR_AZUL_HOVER, corner_radius=6, command=self.baixar_capa)

    def atualizar_caixa_texto(self, texto):
        self.txt_output_box.configure(state="normal")
        self.txt_output_box.delete("1.0", tk.END)
        self.txt_output_box.insert(tk.END, texto)
        self.txt_output_box.configure(state="disabled")

    def buscar_e_exibir_livro(self):
        isbn = self.ent_busca_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Aviso", "Insira um código ISBN para realizar a busca.")
            return
            
        livro = self.biblio.tabela_hash.buscar(isbn)
        
        if livro:
            self.isbn_em_foco = isbn
            info_formatada = (
                f"DETALHES DO LIVRO:\n\n"
                f"Título: {livro.titulo}\n"
                f"Autor: {livro.autor}\n"
                f"Ano de Lançamento: {livro.ano_publicacao}\n"
                f"Estoque Disponível: {livro.qtd_exemplares}\n"
                f"Código ISBN: {livro.isbn}\n"
            )
            self.atualizar_caixa_texto(info_formatada)
            
            if self.capas_db.contem(isbn) and os.path.exists(self.capas_db.get(isbn)):
                try:
                    img = tk.PhotoImage(file=self.capas_db.get(isbn)).subsample(3, 3)
                    self.lbl_capa_imagem.config(image=img, text="")
                    self.img_ref_atual = img
                    self.btn_baixar_capa.pack(fill="x", padx=15, pady=(0, 15))
                except Exception:
                    self.lbl_capa_imagem.config(image='', text="Erro ao abrir imagem")
            else:
                self.lbl_capa_imagem.config(image='', text="Sem capa")
        else:
            self.isbn_em_foco = None
            self.atualizar_caixa_texto(f"O livro com o ISBN '{isbn}' não foi localizado.")
            self.lbl_capa_imagem.config(image='', text="Sem Imagem")

    def exibir_relatorio_na_tela(self):
        def percorrer_arvore_para_texto(nodo):
            if nodo is None:
                return ""
            texto_esquerda = percorrer_arvore_para_texto(nodo.esquerda)
            texto_atual = f"📖 Título: {nodo.livro.titulo}\n✍️ Autor: {nodo.livro.autor}\n🔢 ISBN: {nodo.livro.isbn}\n📦 Estoque: {nodo.livro.qtd_exemplares} exemplar(es)\n"
            texto_atual += "--------------------------------------------------\n"
            texto_direita = percorrer_arvore_para_texto(nodo.direita)
            return texto_esquerda + texto_atual + texto_direita

        self.registrar_acao("Relatório Geral do acervo gerado na tela.")
        raiz_arvore = self.biblio.arvore_titulo.raiz
        
        if raiz_arvore is None:
            self.atualizar_caixa_texto("O acervo está completamente vazio. Nenhum livro cadastrado.")
        else:
            cabecalho = "==================================================\n"
            cabecalho += "       RELATÓRIO GERAL DO ACERVO (ORDEM ALFABÉTICA)       \n"
            cabecalho += "==================================================\n\n"
            corpo_relatorio = percorrer_arvore_para_texto(raiz_arvore)
            self.atualizar_caixa_texto(cabecalho + corpo_relatorio)

    def guardar_log_txt(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(self.historico_acoes.extrair_texto())
            messagebox.showinfo("Sucesso", "Log salvo com sucesso!")

    def baixar_capa(self):
        if not hasattr(self, 'isbn_em_foco') or not self.isbn_em_foco:
            return
        origem = self.capas_db.get(self.isbn_em_foco)
        destino = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imagens PNG", "*.png")])
        if destino and origem:
            shutil.copy(origem, destino)
            messagebox.showinfo("Sucesso", "Capa salva com sucesso!")

    def remover_livro(self):
        isbn = self.ent_busca_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Aviso", "Insira um código ISBN para remoção.")
            return
        livro = self.biblio.tabela_hash.buscar(isbn)
        if livro:
            self.biblio.remover_livro(isbn)
            self.registrar_acao(f"Remoção: O livro '{livro.titulo}' foi removido.")
            messagebox.showinfo("Remoção", f"Livro '{livro.titulo}' removido com sucesso.")
            self.ent_busca_isbn.delete(0, tk.END)
            self.atualizar_caixa_texto("")
            self.lbl_capa_imagem.config(image='', text="Sem Imagem")
        else:
            messagebox.showerror("Erro na Remoção", "Erro: Livro não encontrado no acervo.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = OtecaModernApp(root)
    root.mainloop()