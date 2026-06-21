import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import io
import sys
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


# ESTRUTURAS DE DADOS

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


# APLICAÇÃO EM CUSTOMTKINTER

class OtecaModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OTECA - Sistema de Biblioteca")
        self.root.geometry("1180x750")
        self.root.configure(fg_color=COR_FUNDO_GERAL)
        
        self.biblio = Biblioteca()
        self.historico_acoes = Lista_Encadeada_Historico()
        self.registrar_acao("Sistema iniciado com CustomTkinter.")
        
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
        
        # Entrada no estilo "BorderBottom" simulada perfeitamente sumindo com as outras bordas
        entry = ctk.CTkEntry(frame, font=FONT_TEXT, text_color=COR_TEXTO_MAIN, fg_color=COR_CARD_BG, 
                             border_color=COR_LINHA_INPUT, border_width=1, height=35, corner_radius=6)
        entry.pack(fill="x", pady=(0, 18))
        
        return frame, entry

    def criar_estruturas_principais(self):
        # Header Superior Totalmente Flat
        self.header = ctk.CTkFrame(self.root, fg_color=COR_FUNDO_GERAL, height=100, corner_radius=0)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        logo_container = ctk.CTkFrame(self.header, fg_color=COR_FUNDO_GERAL)
        logo_container.pack(expand=True)
        
        try:
            imagem_pil = Image.open("oteca_logo.png") 
            self.logo_ctk = ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(250, 250))
            
            # 2. Cria o label usando 'image=' em vez de 'text='
            lbl_logo = ctk.CTkLabel(logo_container, image=self.logo_ctk, text="")
            lbl_logo.pack(anchor="center")
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            # Fallback caso a imagem não carregue
            lbl_brand = ctk.CTkLabel(logo_container, text="OTECA 📚", text_color=COR_SIDEBAR_ATIVO, font=("Segoe UI", 28, "bold"))
            lbl_brand.pack(anchor="center")
        # ----------------------------

        lbl_subbrand = ctk.CTkLabel(logo_container, text="Sistema de Gerenciamento de Biblioteca", text_color=COR_TEXTO_MUTED, font=("Segoe UI", 11))
        lbl_subbrand.pack(anchor="center")

        # Sidebar Lateral Moderna
        self.sidebar = ctk.CTkFrame(self.root, fg_color=COR_SIDEBAR, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        lbl_nav = ctk.CTkLabel(self.sidebar, text="NAVEGAÇÃO", text_color="#F4EFEA", font=("Segoe UI", 10, "bold"), anchor="w")
        lbl_nav.pack(pady=(40, 15), padx=25, fill="x")

        # CustomTkinter Buttons com Cantos Arredondados
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

        # Container Principal
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
        
        # O Card Central em CustomTkinter com cantos arredondados nativos de alta qualidade!
        card = ctk.CTkFrame(self.frame_cadastro, fg_color=COR_CARD_BG, corner_radius=12, border_color="#E1DCD6", border_width=1)
        card.pack(fill="x", anchor="n", ipady=15)

        form_frame = ctk.CTkFrame(card, fg_color=COR_CARD_BG)
        form_frame.pack(fill="x", padx=35, pady=30)

        # Divisão em duas colunas simétricas
        col1 = ctk.CTkFrame(form_frame, fg_color=COR_CARD_BG)
        col1.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        frame_isbn, self.ent_isbn = self.criar_input_moderno(col1, "ISBN (Código de Barras):", "║▌║")
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
        
        # Bloco de Anexo Customizado de Acordo com o Mockup Web
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

        # Botão Principal Macio e Moderno
        btn_confirmar = ctk.CTkButton(card, text="Confirmar Cadastro do Livro", fg_color=COR_AZUL_BOTON,
                                     hover_color=COR_AZUL_HOVER, font=FONT_BTN, text_color="white",
                                     height=45, corner_radius=8, command=self.cadastrar_livro)
        btn_confirmar.pack(fill="x", padx=35, pady=(0, 20))

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

    def construir_tela_consulta(self):
        ctk.CTkLabel(self.frame_consulta, text="Consulta de Informações", font=("Segoe UI Light", 18), text_color=COR_TEXTO_MAIN, anchor="w").pack(fill="x", pady=(10, 15))
        
        search_card = ctk.CTkFrame(self.frame_consulta, fg_color=COR_CARD_BG, corner_radius=12, border_color="#E1DCD6", border_width=1)
        search_card.pack(fill="x", pady=(0, 20), anchor="n")
        
        frame_in, self.ent_busca_isbn = self.criar_input_moderno(search_card, "Insira o ISBN para pesquisar ou remover:", "⌕")
        frame_in.pack(side="left", fill="x", expand=True, padx=25, pady=20)
        
        btn_container = ctk.CTkFrame(search_card, fg_color=COR_CARD_BG)
        btn_container.pack(side="right", padx=25, pady=(15, 0))
        
        ctk.CTkButton(btn_container, text="Buscar", fg_color=COR_AZUL_BOTON, hover_color=COR_AZUL_HOVER, height=36, width=90, corner_radius=6, command=self.buscar_e_exibir_livro).pack(side="left", padx=4)
        ctk.CTkButton(btn_container, text="Remover", fg_color=COR_VERMELHO, hover_color=COR_VERMELHO_HOVER, height=36, width=90, corner_radius=6, command=self.remover_livro).pack(side="left", padx=4)
        ctk.CTkButton(btn_container, text="Relatório", fg_color=COR_SIDEBAR, hover_color=COR_SIDEBAR_ATIVO, height=36, width=90, corner_radius=6, command=self.gerar_relatorio_caixa).pack(side="left", padx=4)
        ctk.CTkButton(btn_container, text="Salvar Log", fg_color=COR_SIDEBAR, hover_color=COR_SIDEBAR_ATIVO, height=36, width=90, corner_radius=6, command=self.guardar_log_txt).pack(side="left", padx=4)

        display_frame = ctk.CTkFrame(self.frame_consulta, fg_color=COR_FUNDO_GERAL)
        display_frame.pack(fill="both", expand=True)

        # Caixa de texto nativa do CustomTkinter com scroll suave e bordas arredondadas incorporadas
        self.txt_output_box = ctk.CTkTextbox(display_frame, fg_color="white", text_color=COR_TEXTO_MAIN, font=FONT_TEXT, border_color="#E1DCD6", border_width=1, corner_radius=10, activate_scrollbars=True)
        self.txt_output_box.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.txt_output_box.insert(tk.END, "Os relatórios do acervo e dados das buscas detalhadas aparecerão nesta caixa de texto.")
        self.txt_output_box.configure(state="disabled")

        self.right_capa_panel = ctk.CTkFrame(display_frame, fg_color=COR_CARD_BG, border_color="#E1DCD6", border_width=1, width=220, corner_radius=10)
        self.right_capa_panel.pack(side="right", fill="y")
        self.right_capa_panel.pack_propagate(False)
        
        ctk.CTkLabel(self.right_capa_panel, text="Capa do Livro", text_color=COR_TEXTO_MUTED, font=("Segoe UI", 11, "bold")).pack(pady=(15, 10))
        
        self.lbl_capa_imagem = tk.Label(self.right_capa_panel, bg="#FBF9F6", text="Sem Imagem", font=FONT_TEXT, bd=0, highlightbackground="#E1DCD6", highlightthickness=1)
        self.lbl_capa_imagem.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.btn_baixar_capa = ctk.CTkButton(self.right_capa_panel, text="💾 Baixar Capa", fg_color=COR_AZUL_BOTON, hover_color=COR_AZUL_HOVER, corner_radius=6, command=self.baixar_capa)

    def selecionar_capa(self):
        caminho = filedialog.askopenfilename(title="Selecione a Imagem da Capa", filetypes=[("Imagens PNG", "*.png")])
        if caminho:
            self.capa_temp_path = caminho
            self.lbl_capa_status.configure(text=f"Pronto: {os.path.basename(caminho)[:18]}...", text_color=COR_AZUL_BOTON)

    def cadastrar_livro(self):
        try:
            isbn = self.ent_isbn.get().strip()
            titulo = self.ent_titulo.get().strip()
            autor = self.ent_autor.get().strip()
            raw_ano = self.ent_ano.get().strip()
            raw_qtd = self.ent_qtd.get().strip()
            
            if not all([isbn, titulo, autor, raw_ano, raw_qtd]):
                messagebox.showerror("Campos Vazios", "Todos os campos do formulário devem ser preenchidos.")
                return

            ano = int(raw_ano)
            qtd = int(raw_qtd)
            
            captura_buffer = io.StringIO()
            sys.stdout = captura_buffer
            
            livro = Livro(isbn, titulo, autor, ano, qtd)
            self.biblio.cadastrar_livro(livro)
            
            sys.stdout = sys.__stdout__
            resultado_mensagem = captura_buffer.getvalue().strip()
            
            if "Erro" in resultado_mensagem:
                messagebox.showerror("Erro de Cadastro", resultado_mensagem)
                return
                
            if self.capa_temp_path:
                self.capas_db.put(isbn, self.capa_temp_path)
                self.capa_temp_path = None
                self.lbl_capa_status.configure(text="Nenhuma capa anexada", text_color="#777777")

            mensagem = f"Cadastro: O livro '{titulo}' (ISBN: {isbn}) foi cadastrado com {qtd} exemplares."
            self.registrar_acao(mensagem)
            messagebox.showinfo("Sucesso", resultado_mensagem if resultado_mensagem else mensagem)
            
            self.ent_isbn.delete(0, tk.END)
            self.ent_titulo.delete(0, tk.END)
            self.ent_autor.delete(0, tk.END)
            self.ent_ano.delete(0, tk.END)
            self.ent_qtd.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro de Tipo", "Ano de Publicação e Quantidade de Exemplares devem ser números inteiros válidos.")

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
        self.registrar_acao(f"Busca: Realizada busca pelo ISBN '{isbn}'.")
        
        if livro:
            self.isbn_em_foco = isbn
            info_formatada = (
                f"DETALHES DO LIVRO ENCONTRADO (Via Tabela Hash)\n"
                f"{'='*50}\n\n"
                f"Título: {livro.titulo}\n"
                f"Autor: {livro.autor}\n"
                f"Ano de Lançamento: {livro.ano_publicacao}\n"
                f"Estoque Disponível: {livro.qtd_exemplares} exemplar(es)\n"
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
                    self.lbl_capa_imagem.config(image='', text="Erro ao abrir arquivo")
                    self.btn_baixar_capa.pack_forget()
            else:
                self.lbl_capa_imagem.config(image='', text="Sem capa cadastrada")
                self.btn_baixar_capa.pack_forget()
        else:
            self.isbn_em_foco = None
            self.atualizar_caixa_texto(f"O livro com o ISBN '{isbn}' não foi localizado no sistema.")
            self.lbl_capa_imagem.config(image='', text="Sem Imagem")
            self.btn_baixar_capa.pack_forget()

    def gerar_relatorio_caixa(self):
        self.registrar_acao("Relatório: Foi gerado o Relatório Geral do Acervo.")
        captura_buffer = io.StringIO()
        sys.stdout = captura_buffer
        
        self.biblio.gerar_relatorio_geral()
        
        sys.stdout = sys.__stdout__
        conteudo_relatorio = captura_buffer.getvalue()
        
        if not conteudo_relatorio.strip() or "vazia" in conteudo_relatorio:
            conteudo_relatorio = "RELATÓRIO DO ACERVO\n" + "="*50 + "\n\nNenhum livro cadastrado na Árvore até o momento."
            
        self.atualizar_caixa_texto(conteudo_relatorio)

    def guardar_log_txt(self):
        if self.historico_acoes.tamanho == 0:
            messagebox.showinfo("Aviso", "Não há ações registadas no sistema.")
            return

        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Arquivo de Texto", "*.txt")],
            initialfile="log_completo_oteca.txt",
            title="Guardar Log Completo de Ações"
        )
        
        if caminho:
            try:
                with open(caminho, "w", encoding="utf-8") as f:
                    f.write("=== LOG COMPLETO DE AÇÕES - OTECA ===\n\n")
                    f.write(self.historico_acoes.extrair_texto())
                    
                    f.write("\n\n=== STATUS ATUAL DO ACERVO NO MOMENTO DO LOG ===\n")
                    captura = io.StringIO()
                    sys.stdout = captura
                    self.biblio.gerar_relatorio_geral()
                    sys.stdout = sys.__stdout__
                    f.write(captura.getvalue())
                    
                self.registrar_acao("Log exportado para arquivo TXT.")
                messagebox.showinfo("Sucesso", "Log completo de ações salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o log: {e}")

    def baixar_capa(self):
        if not hasattr(self, 'isbn_em_foco') or not self.isbn_em_foco or not self.capas_db.contem(self.isbn_em_foco):
            return
            
        origem = self.capas_db.get(self.isbn_em_foco)
        destino = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("Imagens PNG", "*.png")],
            initialfile=f"capa_{self.isbn_em_foco}.png",
            title="Exportar Imagem da Capa"
        )
        
        if destino:
            try:
                shutil.copy(origem, destino)
                self.registrar_acao(f"Download de Capa: A capa do ISBN '{self.isbn_em_foco}' foi exportada.")
                messagebox.showinfo("Sucesso", "O download da capa foi concluído e salvo no seu computador!")
            except Exception as e:
                messagebox.showerror("Erro no Download", f"Não foi possível salvar o arquivo de imagem: {e}")

    def remover_livro(self):
        isbn = self.ent_busca_isbn.get().strip()
        if not isbn:
            return
            
        livro = self.biblio.tabela_hash.buscar(isbn)
        if livro:
            titulo = livro.titulo
            self.biblio.remover_livro(isbn)
            
            mensagem = f"Remoção: O livro '{titulo}' (ISBN: {isbn}) foi apagado de todas as estruturas."
            self.registrar_acao(mensagem)
            messagebox.showinfo("Remoção Realizada", mensagem)
            
            self.atualizar_caixa_texto(f"O livro '{titulo}' (ISBN: {isbn}) foi inteiramente apagado do sistema.")
            self.lbl_capa_imagem.config(image='', text="Sem Imagem")
            self.btn_baixar_capa.pack_forget()
        else:
            self.registrar_acao(f"Tentativa Falha de Remoção: ISBN '{isbn}' não encontrado.")
            messagebox.showwarning("Não encontrado", "Livro não localizado para remoção.")

    def realizar_emprestimo(self):
        isbn = self.ent_emp_isbn.get().strip()
        user = self.ent_emp_user.get().strip()
        if not isbn or not user:
            messagebox.showwarning("Dados Incompletos", "Insira o ISBN do livro e o nome do usuário destinatário.")
            return
            
        captura_buffer = io.StringIO()
        sys.stdout = captura_buffer
        self.biblio.realizar_emprestimo(isbn, user)
        sys.stdout = sys.__stdout__
        
        resultado_mensagem = captura_buffer.getvalue().strip()
        if resultado_mensagem:
            self.registrar_acao(f"Operação de Empréstimo: {resultado_mensagem}")
            if "Impossível" in resultado_mensagem:
                messagebox.showerror("Erro de Circulação", resultado_mensagem)
            else:
                messagebox.showinfo("Operação de Empréstimo", resultado_mensagem)
                self.ent_emp_isbn.delete(0, tk.END)
                self.ent_emp_user.delete(0, tk.END)

    def realizar_devolucao(self):
        isbn = self.ent_emp_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Dados Incompletos", "Por favor, insira o código ISBN para registrar a devolução.")
            return
            
        captura_buffer = io.StringIO()
        sys.stdout = captura_buffer
        self.biblio.realizar_devolucao(isbn)
        sys.stdout = sys.__stdout__
        
        resultado_mensagem = captura_buffer.getvalue().strip()
        if resultado_mensagem:
            self.registrar_acao(f"Operação de Devolução: {resultado_mensagem}")
            if "Erro" in resultado_mensagem or "inválido" in resultado_mensagem:
                messagebox.showerror("Erro de Devolução", resultado_mensagem)
            else:
                messagebox.showinfo("Operação de Devolução", resultado_mensagem)
                self.ent_emp_isbn.delete(0, tk.END)

    def desfazer_emprestimo(self):
        captura_buffer = io.StringIO()
        sys.stdout = captura_buffer
        self.biblio.desfazer_ultimo_emprestimo()
        sys.stdout = sys.__stdout__
        
        resultado_mensagem = captura_buffer.getvalue().strip()
        if resultado_mensagem:
            self.registrar_acao(f"Ação de Desfazer (Pilha): {resultado_mensagem}")
            if "Erro" in resultado_mensagem:
                messagebox.showerror("Erro ao Desfazer", resultado_mensagem)
            else:
                messagebox.showinfo("Desfazer Operação (Pilha)", resultado_mensagem)

if __name__ == "__main__":
    root = ctk.CTk()
    app = OtecaModernApp(root)
    root.mainloop()