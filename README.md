# FEIFood - Sistema de Gestão de Pedidos (Terminal) 🍔🐍

O **FEIFood** é uma plataforma de pedidos desenvolvida em Python que utiliza o terminal como interface. O projeto foi construído focando em lógica de programação, persistência de dados em arquivos CSV e modularização de código.

Este projeto faz parte da minha jornada acadêmica em **Ciência da Computação na FEI** e demonstra a aplicação prática de conceitos de Engenharia de Software e I/O de dados.

## 🚀 Funcionalidades

### 🔐 Gestão de Acesso
- **Cadastro de Usuários:** Sistema de registro com geração automática de IDs únicos.
- **Autenticação:** Login seguro validando credenciais armazenadas em arquivo.

### 🍽️ Menu e Busca
- **Listagem de Alimentos:** Exibição dinâmica de itens disponíveis no `alimentos.csv`.
- **Busca Case-Insensitive:** Filtro de busca por nome ou descrição que ignora diferenças entre maiúsculas e minúsculas.

### 🛒 Carrinho e Pedidos
- **Gestão de Carrinho:** Adição, remoção e alteração de quantidades de itens em tempo real.
- **Cálculo de Total:** Soma automática do valor do pedido com base nos preços dos alimentos.
- **Persistência de Pedidos:** Os pedidos são armazenados com status (`ABERTO` ou `FECHADO`), permitindo retomar compras pendentes.

### ⭐ Avaliação
- **Feedback:** Sistema que permite ao usuário avaliar pedidos finalizados com notas de 0 a 5 estrelas.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.x
- **Persistência:** Arquivos CSV (Comma-Separated Values)
- **Bibliotecas Nativas:** `datetime`, `os`

## 📂 Estrutura do Projeto
O projeto foi desenvolvido seguindo o princípio de responsabilidade única, dividido em módulos:

- `main_app.py`: Ponto de entrada e controle dos menus.
- `data_manager.py`: Camada de I/O responsável pela leitura e escrita nos arquivos CSV.
- `access_manager.py`: Lógica de autenticação e registro de usuários.
- `food_manager.py`: Filtros e listagem de alimentos.
- `order_manager.py`: Lógica de manipulação de carrinhos e persistência de pedidos.
- `review_manager.py`: Processamento de avaliações de pedidos.

## 📖 Como Executar
1. Certifique-se de ter o Python instalado.
2. Clone o repositório.
3. Garanta que os arquivos `.csv` (usuarios, alimentos, pedidos, avaliacoes) existam na mesma pasta.
4. Execute o comando:
   ```bash
   python main_app.py