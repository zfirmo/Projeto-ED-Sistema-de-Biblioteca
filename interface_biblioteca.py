import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import io
import sys
import os
import shutil
import datetime
from sistema_biblioteca import Biblioteca, Livro

COR_BEGE = "#FDFBF7"          
COR_LOCO_BG = "#FFFFFF"       
COR_MARROM = "#5C4033"        
COR_MARROM_ESCURO = "#3E2A21" 
COR_AZUL = "#004AAD"          
COR_AZUL_HOVER = "#003380"
COR_VERMELHO = "#B22222"      
COR_VERMELHO_HOVER = "#8B0000"
COR_TEXTO_INPUT = "#333333"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_TEXT = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")

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
        self.baldes = [None] * tamanho

    def _hash(self, chave):
        soma = sum(ord(c) for c in str(chave))
        return soma % self.tamanho

    def put(self, chave, valor):
        pos = self._hash(chave)
        novo = NodeMapa(chave, valor)
        if self.baldes[pos] is None:
            self.baldes[pos] = novo
        else:
            atual = self.baldes[pos]
            while atual.proximo is not None:
                if str(atual.chave) == str(chave):
                    atual.valor = valor
                    return
                atual = atual.proximo
            if str(atual.chave) == str(chave):
                atual.valor = valor
            else:
                atual.proximo = novo

    def get(self, chave):
        pos = self._hash(chave)
        atual = self.baldes[pos]
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
        self.root.title("OTECA - Sistema de Gerenciamento de Biblioteca")
        self.root.geometry("1050x700")
        self.root.configure(bg=COR_BEGE)
        
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

    def criar_botao(self, parent, text, bg_color, hover_color, command, fg="white"):
        btn = tk.Button(parent, text=text, bg=bg_color, fg=fg, font=FONT_BTN, 
                        relief="flat", cursor="hand2", command=command, padx=15, pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    def criar_input(self, parent, label_text):
        bg_color = parent.cget("bg")
        frame = tk.Frame(parent, bg=bg_color)
        tk.Label(frame, text=label_text, bg=bg_color, fg=COR_MARROM, font=FONT_TEXT).pack(anchor="w")
        entry = tk.Entry(frame, font=FONT_TEXT, fg=COR_TEXTO_INPUT, bg="white", relief="solid", bd=1)
        entry.pack(fill="x", pady=(2, 10), ipady=4)
        return frame, entry

    def criar_estruturas_principais(self):
        self.header = tk.Frame(self.root, bg=COR_LOCO_BG, height=90, bd=1, relief="groove")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        logo_container = tk.Frame(self.header, bg=COR_LOCO_BG)
        logo_container.pack(expand=True)
        
        try:
            self.logo_img = tk.PhotoImage(file="oteca_logo.png").subsample(5, 5)
            tk.Label(logo_container, image=self.logo_img, bg=COR_LOCO_BG).pack(side="left", padx=10)
        except Exception:
            tk.Label(logo_container, text="OTECA", bg=COR_LOCO_BG, fg=COR_MARROM, font=("Segoe UI", 24, "bold")).pack(side="left", padx=10)

        self.sidebar = tk.Frame(self.root, bg=COR_MARROM, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="NAVEGAÇÃO", bg=COR_MARROM, fg=COR_BEGE, font=("Segoe UI", 10, "bold")).pack(pady=(20, 10), padx=15, anchor="w")

        self.btn_nav_cadastro = self.criar_botao(self.sidebar, "Cadastrar Livro", COR_MARROM, COR_MARROM_ESCURO, lambda: self.mostrar_frame(self.frame_cadastro, self.btn_nav_cadastro), COR_BEGE)
        self.btn_nav_cadastro.pack(fill="x", pady=2, padx=10)

        self.btn_nav_emprestimo = self.criar_botao(self.sidebar, "Empréstimos", COR_MARROM, COR_MARROM_ESCURO, lambda: self.mostrar_frame(self.frame_emprestimo, self.btn_nav_emprestimo), COR_BEGE)
        self.btn_nav_emprestimo.pack(fill="x", pady=2, padx=10)

        self.btn_nav_consulta = self.criar_botao(self.sidebar, "Consultar Acervo", COR_MARROM, COR_MARROM_ESCURO, lambda: self.mostrar_frame(self.frame_consulta, self.btn_nav_consulta), COR_BEGE)
        self.btn_nav_consulta.pack(fill="x", pady=2, padx=10)

        self.main_content = tk.Frame(self.root, bg=COR_BEGE)
        self.main_content.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        self.frame_cadastro = tk.Frame(self.main_content, bg=COR_BEGE)
        self.frame_emprestimo = tk.Frame(self.main_content, bg=COR_BEGE)
        self.frame_consulta = tk.Frame(self.main_content, bg=COR_BEGE)

    def mostrar_frame(self, frame_alvo, botao_ativo):
        self.btn_nav_cadastro.config(bg=COR_MARROM)
        self.btn_nav_emprestimo.config(bg=COR_MARROM)
        self.btn_nav_consulta.config(bg=COR_MARROM)
        
        botao_ativo.config(bg=COR_MARROM_ESCURO)
        
        self.frame_cadastro.pack_forget()
        self.frame_emprestimo.pack_forget()
        self.frame_consulta.pack_forget()
        
        frame_alvo.pack(fill="both", expand=True)

    def construir_tela_cadastro(self):
        tk.Label(self.frame_cadastro, text="Cadastro de Livros no Acervo", font=FONT_TITLE, bg=COR_BEGE, fg=COR_MARROM).pack(anchor="w", pady=(0, 15))
        
        card = tk.Frame(self.frame_cadastro, bg="white", bd=1, relief="solid", padx=20, pady=20)
        card.pack(fill="x", pady=10)

        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(fill="x")

        col1 = tk.Frame(form_frame, bg="white")
        col1.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        frame_isbn, self.ent_isbn = self.criar_input(col1, "ISBN (Código de Barras):")
        frame_isbn.pack(fill="x")
        
        frame_titulo, self.ent_titulo = self.criar_input(col1, "Título do Livro:")
        frame_titulo.pack(fill="x")
        
        frame_autor, self.ent_autor = self.criar_input(col1, "Autor:")
        frame_autor.pack(fill="x")

        col2 = tk.Frame(form_frame, bg="white")
        col2.pack(side="right", fill="x", expand=True, padx=(15, 0))
        
        frame_ano, self.ent_ano = self.criar_input(col2, "Ano de Publicação:")
        frame_ano.pack(fill="x")
        
        frame_qtd, self.ent_qtd = self.criar_input(col2, "Quantidade de Exemplares:")
        frame_qtd.pack(fill="x")
        
        capa_frame = tk.Frame(col2, bg="white")
        capa_frame.pack(fill="x", pady=(5, 0))
        tk.Label(capa_frame, text="Capa do Livro (.png):", bg="white", fg=COR_MARROM, font=FONT_TEXT).pack(anchor="w")
        self.lbl_capa_status = tk.Label(capa_frame, text="Nenhuma capa anexada", bg="white", fg="#777777", font=("Segoe UI", 9, "italic"))
        self.lbl_capa_status.pack(side="left", pady=5)
        btn_upload = self.criar_botao(capa_frame, "Anexar Imagem", COR_MARROM, COR_MARROM_ESCURO, self.selecionar_capa)
        btn_upload.config(padx=10, pady=2, font=("Segoe UI", 9, "bold"))
        btn_upload.pack(side="right")

        self.criar_botao(card, "Confirmar Cadastro do Livro", COR_AZUL, COR_AZUL_HOVER, self.cadastrar_livro).pack(fill="x", pady=(20, 0))

    def construir_tela_emprestimo(self):
        tk.Label(self.frame_emprestimo, text="Controle de Circulação (Empréstimos e Devoluções)", font=FONT_TITLE, bg=COR_BEGE, fg=COR_MARROM).pack(anchor="w", pady=(0, 15))
        
        card = tk.Frame(self.frame_emprestimo, bg="white", bd=1, relief="solid", padx=20, pady=20)
        card.pack(fill="x", pady=10)

        frame_emp_isbn, self.ent_emp_isbn = self.criar_input(card, "ISBN do Livro:")
        frame_emp_isbn.pack(fill="x")
        
        frame_emp_user, self.ent_emp_user = self.criar_input(card, "Nome do Usuário (Necessário apenas para Empréstimo):")
        frame_emp_user.pack(fill="x")

        btn_box = tk.Frame(card, bg="white")
        btn_box.pack(fill="x", pady=(15, 0))
        
        self.criar_botao(btn_box, "Realizar Empréstimo", COR_AZUL, COR_AZUL_HOVER, self.realizar_emprestimo).pack(side="left", padx=(0, 10))
        self.criar_botao(btn_box, "Registrar Devolução", COR_AZUL, COR_AZUL_HOVER, self.realizar_devolucao).pack(side="left", padx=(0, 10))
        self.criar_botao(btn_box, "Desfazer Última Operação", COR_VERMELHO, COR_VERMELHO_HOVER, self.desfazer_emprestimo).pack(side="right")

    def construir_tela_consulta(self):
        tk.Label(self.frame_consulta, text="Consulta de Informações e Relatórios", font=FONT_TITLE, bg=COR_BEGE, fg=COR_MARROM).pack(anchor="w", pady=(0, 10))
        
        search_card = tk.Frame(self.frame_consulta, bg="white", bd=1, relief="solid", padx=15, pady=15)
        search_card.pack(fill="x", pady=(0, 15))
        
        frame_in, self.ent_busca_isbn = self.criar_input(search_card, "Insira o ISBN para pesquisa ou remoção:")
        frame_in.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        self.criar_botao(search_card, "Buscar Livro", COR_AZUL, COR_AZUL_HOVER, self.buscar_e_exibir_livro).pack(side="left", padx=5, pady=(15,0))
        self.criar_botao(search_card, "Remover", COR_VERMELHO, COR_VERMELHO_HOVER, self.remover_livro).pack(side="left", padx=5, pady=(15,0))
        self.criar_botao(search_card, "Relatório Geral", COR_MARROM, COR_MARROM_ESCURO, self.gerar_relatorio_caixa).pack(side="left", padx=5, pady=(15,0))
        self.criar_botao(search_card, "📄 Guardar Log (TXT)", COR_MARROM, COR_MARROM_ESCURO, self.guardar_log_txt).pack(side="left", padx=5, pady=(15,0))

        display_frame = tk.Frame(self.frame_consulta, bg=COR_BEGE)
        display_frame.pack(fill="both", expand=True)

        self.txt_output_box = scrolledtext.ScrolledText(display_frame, bg="white", fg=COR_TEXTO_INPUT, font=FONT_TEXT, bd=1, relief="solid")
        self.txt_output_box.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.txt_output_box.insert(tk.END, "Os relatórios do acervo e dados das buscas detalhadas aparecerão nesta caixa de texto.")
        self.txt_output_box.config(state=tk.DISABLED)

        self.right_capa_panel = tk.Frame(display_frame, bg="white", bd=1, relief="solid", width=220, padx=15, pady=15)
        self.right_capa_panel.pack(side="right", fill="y")
        self.right_capa_panel.pack_propagate(False)
        
        tk.Label(self.right_capa_panel, text="Capa do Livro", bg="white", fg=COR_MARROM, font=FONT_SUBTITLE).pack(pady=(0, 10))
        
        self.lbl_capa_imagem = tk.Label(self.right_capa_panel, bg="#F0F0F0", text="Sem Imagem", font=FONT_TEXT, bd=1, relief="solid")
        self.lbl_capa_imagem.pack(fill="both", expand=True, pady=(0, 10))
        
        self.btn_baixar_capa = self.criar_botao(self.right_capa_panel, "💾 Baixar Capa", COR_AZUL, COR_AZUL_HOVER, self.baixar_capa)

    def selecionar_capa(self):
        caminho = filedialog.askopenfilename(title="Selecione a Imagem da Capa", filetypes=[("Imagens PNG", "*.png")])
        if caminho:
            self.capa_temp_path = caminho
            self.lbl_capa_status.config(text=f"Pronto: {os.path.basename(caminho)[:18]}...", fg=COR_AZUL)

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
                self.lbl_capa_status.config(text="Nenhuma capa anexada", fg="#777777")

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
        self.txt_output_box.config(state=tk.NORMAL)
        self.txt_output_box.delete(1.0, tk.END)
        self.txt_output_box.insert(tk.END, texto)
        self.txt_output_box.config(state=tk.DISABLED)

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
                    self.btn_baixar_capa.pack(fill="x")
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
            conteudo_relatorio = "RELATÓRIO DO ACERVO\n" + "="*50 + "\n\nNenhum livro cadastrado na Lista Encadeada até o momento."
            
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
    root = tk.Tk()
    app = OtecaModernApp(root)
    root.mainloop()