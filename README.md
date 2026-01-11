PROJETO FEIFOOD

=======================================================
1. SOBRE O PROJETO
=======================================================

O FEIFood é uma plataforma simplificada para pedidos de comida, desenvolvida como projeto final para a disciplina CCP110 – Fundamentos de Algoritmos. O objetivo central é simular a lógica de um sistema de pedidos, focando na manipulação e persistência de dados.

Escopo: O projeto contempla todas as funcionalidades essenciais para o perfil de Usuário.
Restrições: Não foram implementadas as lógicas de pagamento, acompanhamento de entrega ou mudança de status logístico.

=======================================================
2. TECNOLOGIAS UTILIZADAS
=======================================================

- Linguagem: Python
- Persistência: Arquivos de Texto (.csv)
- I/O: Terminal (CLI)

=======================================================
3. ESTRUTURA DO PROJETO
=======================================================

O código é modularizado em vários arquivos .py, cada um com responsabilidade específica:

- main_app.py: Ponto de entrada (Loop Principal e Menus).
- data_manager.py: Responsável por todas as operações de I/O (leitura e escrita) nos arquivos CSV e conversão de tipos.
- access_manager.py: Lógica de Gestão de Acesso (Login e Cadastro).
- food_manager.py: Lógica de Busca e Listagem de Alimentos.
- order_manager.py: Lógica de Gestão de Pedidos/Carrinho.
- review_manager.py: Lógica para Avaliação de Pedidos.

=======================================================
4. FUNCIONALIDADES IMPLEMENTADAS (PERFIL USUÁRIO)
=======================================================

4.1. Gestão de Acesso
- Cadastrar Novo Usuário: Cria um novo registro no usuarios.csv com ID sequencial.
- Login de Usuário: Autentica o usuário e inicia a sessão.
- Logout: Finaliza a sessão atual.

4.2. Busca e Listagem (Opção 1)
- Listagem Completa: Exibe todos os alimentos cadastrados.
- Busca: Permite buscar por Nome ou Descrição (case-insensitive).

4.3. Gestão de Pedidos (Opção 2)
- Criação/Carregamento: Inicia um novo pedido ou carrega o pedido em status ABERTO.
- Adicionar/Alterar Item: Ajusta a quantidade de itens no carrinho.
- Finalizar Pedido: Altera o STATUS do pedido para FECHADO.
- Cancelar Pedido: Remove o pedido do arquivo pedidos.csv.

4.4. Avaliação (Opção 3)
- Permite atribuir uma nota de 0 a 5 estrelas a pedidos que estejam com o status FECHADO.

=======================================================
5. INSTALAÇÃO E EXECUÇÃO
=======================================================

PRÉ-REQUISITOS
- Ter o Python 3 instalado na sua máquina.

EXECUÇÃO
1. Crie os Arquivos CSV: Garanta que os 4 arquivos CSV necessários (usuarios.csv, alimentos.csv, pedidos.csv, avaliacoes.csv) estejam presentes na pasta do projeto com o cabeçalho correto.
2. Abra o Terminal: Navegue até a pasta raiz do projeto.
3. Execute o Arquivo Principal:
   python main_app.py
4. Interaja: Utilize o menu de opções para começar a usar a plataforma.

=======================================================
6. ESTRUTURA DE ARQUIVOS CSV
=======================================================

Os arquivos utilizam ponto e vírgula (;) como separador.

- usuarios.csv: ID;LOGIN;SENHA;NOME;TIPO
- alimentos.csv: ID;NOME;DESCRICAO;PRECO (PRECO usa ponto '.' como decimal)
- pedidos.csv: ID;ID_USUARIO;DATA_HORA;ITENS;STATUS (ITENS serializado: 1-2,3-1)
- avaliacoes.csv: ID_PEDIDO;ID_USUARIO;NOTA_ESTRELAS;DATA_AVALIACAO