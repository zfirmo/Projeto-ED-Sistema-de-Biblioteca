import sys
from sistema_biblioteca import Biblioteca, Livro

def exibir_menu():
    print("\n" + "="*45)
    print("      OTECA - SISTEMA DE GERENCIAMENTO      ")
    print("="*45)
    print("1. Cadastrar Novo Livro")
    print("2. Remover Livro do Sistema")
    print("3. Buscar Livro por ISBN")
    print("4. Listar Livros (Ordem Alfabética)")
    print("5. Realizar Empréstimo")
    print("6. Registrar Devolução")
    print("7. Desfazer Última Operação (Pilha)")
    print("8. Gerar Relatório Geral do Acervo")
    print("0. Sair do Sistema")
    print("="*45)
 
def main():
    biblioteca = Biblioteca()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n--- CADASTRO DE LIVRO ---")
            isbn = input("ISBN: ").strip()
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            
            try:
                ano = int(input("Ano de publicação: "))
                qtd = int(input("Quantidade de exemplares: "))
                novo_livro = Livro(isbn, titulo, autor, ano, qtd)
                biblioteca.cadastrar_livro(novo_livro)
            except ValueError:
                print("Erro: Ano e Quantidade devem ser números inteiros.")
                
        elif opcao == "2":
            print("\n--- REMOVER LIVRO ---")
            isbn = input("Insira o ISBN do livro para exclusão: ").strip()
            biblioteca.remover_livro(isbn)
            
        elif opcao == "3":
            print("\n--- BUSCAR LIVRO POR ISBN ---")
            isbn = input("Insira o ISBN para pesquisa: ").strip()
            livro = biblioteca.tabela_hash.buscar(isbn)
            
            if livro:
                print("\n[Livro Localizado Via Tabela Hash]")
                print(f"Título: {livro.titulo}")
                print(f"Autor: {livro.autor}")
                print(f"Ano: {livro.ano_publicacao}")
                print(f"Estoque Atual: {livro.qtd_exemplares} exemplar(es)")
            else:
                print("O livro com o ISBN informado não foi localizado.")
                
        elif opcao == "4":

            biblioteca.gerar_relatorio_geral()
            
        elif opcao == "5":

            print("\n--- REALIZAR EMPRÉSTIMO ---")
            isbn = input("ISBN do livro desejado: ").strip()
            usuario = input("Nome do usuário solicitante: ").strip()
            if isbn and usuario:
                biblioteca.realizar_emprestimo(isbn, usuario)
            else:
                print("Erro: Todos os campos são obrigatórios.")
                
        elif opcao == "6":

            print("\n--- REGISTRAR DEVOLUÇÃO ---")
            isbn = input("ISBN do livro a ser devolvido: ").strip()
            if isbn:
                biblioteca.realizar_devolucao(isbn)
            else:
                print("Erro: O campo ISBN é obrigatório.")
                
        elif opcao == "7":

            print("\n--- DESFAZER ÚLTIMA OPERAÇÃO ---")
            biblioteca.desfazer_ultimo_emprestimo()
            
        elif opcao == "8":

            biblioteca.gerar_relatorio_geral()
            
        elif opcao == "0":

            print("\nFinalizando o sistema Oteca. Até logo!")
            sys.exit(0)

        else:

            print("Opção inválida! Por favor, escolha um número de 0 a 8.")

if __name__ == "__main__":
    main()