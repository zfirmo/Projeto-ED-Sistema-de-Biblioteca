# TESTES

Testes que devem ser feitos para fazer demonstração para o professor:

### Possíveis erros (Cadastro)

ISBN

 - ISBN com caracteres diferentes de números
 - ISBN com quantidade diferente de 10 ou 13 dígitos
 (Segundo as regras do ISBN que significa *International Standart Book Number*, ele é um número de indentificação de todos os livros oficialmente publicados antes até 2006 eram 10 dígitos, porém em 2007 expandiram para 13 dígitos pela alta demanda)
 - Adicionar ISBN repetido
 
Quantidade de Exemplares

 - Quantidade menor ou igual a zero

### Possíveis erros (Empréstimo)

Empréstimo
 - Realizar o empréstimo de um ISBN que não existe
 - Realizar o empréstimo de um ISBN sem exemplar disponível (entra na fila)

Devolução
 - Devolver um livro com a quantidade total de exemplares já no acervo

Desfazer
 - Não sei


### Possíveis erros (Consulta)

 - Tentar remover sem colocar ISBN
 - Gerar relatório com o acervo vazio (Só mostra que tá vazio)
 - Buscar ISBN que não existe
 - Remover um ISBN que não existe