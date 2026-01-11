from access_manager import login_usuario, cadastrar_usuario
from data_manager import read_data, user_file, user_keys, alimentos_file, alimentos_keys
from food_manager import buscar_e_listar_alimentos 
from order_manager import (
    buscar_pedido_aberto, criar_novo_pedido, 
    adicionar_item, remover_pedido, salvar_pedidos, 
    carregar_pedidos, get_total_pedido 
)
from review_manager import cadastrar_avaliacao 


# Variáveis globais de estado
USUARIO_LOGADO = None
ALIMENTOS = []
PEDIDO_ABERTO = None


def carregar_alimentos():
    # Carrega os dados dos alimentos do arquivo 
    global ALIMENTOS
    
    print("Carregando menu de alimentos...")
    ALIMENTOS = read_data(alimentos_file, alimentos_keys)
    
    # Conversão de PRECO para float
    for alimento in ALIMENTOS:
        alimento['PRECO'] = float(alimento['PRECO'])
    print(f"{len(ALIMENTOS)} alimentos carregados.")


def menu_inicial():
    # Exibe o menu de opções antes do login
    print("\n---- FEIFood - Acesso ----")
    print("1. Login")
    print("2. Cadastrar Novo Usuário")
    print("3. Sair do Programa")
    
    escolha = input("Selecione uma opção: ")
    return escolha

def menu_principal(usuario):
    # Exibe o menu de opções após o login
    global PEDIDO_ABERTO
    
    status_carrinho = "Vazio"
    if PEDIDO_ABERTO and PEDIDO_ABERTO['ITENS_LISTA']:
        # Contagem de itens e total
        total_itens = sum(item['qtd'] for item in PEDIDO_ABERTO['ITENS_LISTA'])
        total_valor = get_total_pedido(PEDIDO_ABERTO, ALIMENTOS)
        total_formatado = f"R$ {total_valor:.2f}".replace('.', ',')

        status_carrinho = f"Com {total_itens} itens ({total_formatado})"
        
    print(f"\n---- Bem-vindo(a), {usuario['NOME']} ----") 
    print(f"Status do Carrinho: {status_carrinho}")
    print("1. Buscar Alimentos / Listar Menu")
    print("2. Cadastrar Pedido / Gerenciar Carrinho")
    print("3. Avaliar um Pedido")
    
    print("9. Logout")
    print("0. Sair do Programa (Salvar e Fechar)")
    
    escolha = input("Selecione uma opção: ")
    return escolha

def salvar_todos_dados():
    # Placeholder para salvar dados antes de sair
    pass

def gerenciar_carrinho(usuario, alimentos, pedido_aberto):
    # Loop para adicionar, remover e finalizar itens do pedido
    global PEDIDO_ABERTO 

    # Se não houver pedido salvo, cria uma estrutura temporária 
    if pedido_aberto is None:
        print("\n--- Novo Pedido Iniciado ---")
        pedido_aberto = {
            'ID': 0, # ID 0 significa novo
            'ID_USUARIO': usuario['ID'],
            'DATA_HORA': None,
            'ITENS_LISTA': [], 
            'STATUS': 'ABERTO'
        }
    
    while True:
        total = get_total_pedido(pedido_aberto, alimentos)
        total_formatado = f"R$ {total:.2f}".replace('.', ',')

        print("\n---- Opção 2: Gerenciar Carrinho ----")
        print(f"Total Atual: {total_formatado}")
        
        # Mostrar itens atuais do carrinho
        if pedido_aberto['ITENS_LISTA']:
            print("Itens:")
            for item in pedido_aberto['ITENS_LISTA']:
                alimento = next((a for a in alimentos if a['ID'] == item['id']), None)
                nome = alimento['NOME'] if alimento else f"[Item ID {item['id']} Desconhecido]"
                print(f"  - ID: {item['id']} | {item['qtd']}x {nome}")
        else:
            print("Carrinho vazio.")

        print("\nOpções:")
        print("1. Adicionar Item")
        print("2. Remover Item / Alterar Quantidade")
        print("3. Finalizar Pedido")
        print("4. Cancelar Pedido")
        print("9. Voltar ao Menu Principal")

        escolha = input("Selecione uma opção: ")

        if escolha == '1':
            buscar_e_listar_alimentos(alimentos) 
            try:
                id_alimento = int(input("Digite o ID do alimento a adicionar: "))
                quantidade = int(input("Quantidade: "))
                
                if quantidade <= 0:
                    print("Quantidade deve ser positiva para adicionar.")
                    continue

                # Se for um novo pedido, cria o registro no CSV e pega o ID real
                if pedido_aberto['ID'] == 0:
                    pedido_aberto = criar_novo_pedido(usuario['ID'])
                
                # Adiciona o item ao pedido em memória
                pedido_aberto = adicionar_item(pedido_aberto, id_alimento, quantidade)
                
                # Salva o estado atual do pedido no CSV
                pedidos = [p for p in carregar_pedidos() if p['ID'] != pedido_aberto['ID']]
                pedidos.append(pedido_aberto)
                salvar_pedidos(pedidos)
                print("Item adicionado e carrinho salvo.")
                
            except ValueError:
                print("ID e Quantidade devem ser números inteiros válidos.")
        
        elif escolha == '2':
            # Remoção/Alteração
            try:
                id_alimento = int(input("Digite o ID do alimento a ajustar: "))
                quantidade_ajuste = int(input("Nova quantidade desejada (ou 0 para remover): "))
                
                # Se a nova quantidade for zero ou menor, remove o item
                if quantidade_ajuste <= 0:
                    pedido_aberto['ITENS_LISTA'] = [item for item in pedido_aberto['ITENS_LISTA'] if item['id'] != id_alimento]
                    print(f"Item {id_alimento} removido ou ajustado para zero.")
                else:
                    # Atualiza ou adiciona o item com a nova quantidade
                    item_existente = next((item for item in pedido_aberto['ITENS_LISTA'] if item['id'] == id_alimento), None)
                    if item_existente:
                        item_existente['qtd'] = quantidade_ajuste
                        print(f"Quantidade ajustada para {quantidade_ajuste} do item {id_alimento}.")
                    else:
                        print("Item não encontrado no carrinho para ajuste.")
                        continue
                
                # Salva o pedido atualizado após a edição
                pedidos = [p for p in carregar_pedidos() if p['ID'] != pedido_aberto['ID']]
                pedidos.append(pedido_aberto)
                salvar_pedidos(pedidos)
                
            except ValueError:
                print("ID e Quantidade devem ser números.")
            
        elif escolha == '3':
            if not pedido_aberto['ITENS_LISTA']:
                print("O carrinho está vazio. Adicione itens antes de finalizar.")
                continue

            pedido_aberto['STATUS'] = 'FECHADO'
            
            pedidos = carregar_pedidos()
            pedidos_atualizados = [p for p in pedidos if p['ID'] != pedido_aberto['ID']]
            pedidos_atualizados.append(pedido_aberto)
            salvar_pedidos(pedidos_atualizados)

            print(f"Pedido {pedido_aberto['ID']} finalizado com sucesso! Total: {total_formatado}")
            return None 
            
        elif escolha == '4':
            if pedido_aberto['ID'] != 0:
                remover_pedido(pedido_aberto['ID'])
                print(f"Pedido {pedido_aberto['ID']} cancelado e excluído.")
            else:
                print("Carrinho vazio em memória, nenhuma ação necessária.")
                
            return None 

        elif escolha == '9':
    
            if pedido_aberto['ID'] != 0:
                print(f"Retornando ao menu principal. O pedido ID {pedido_aberto['ID']} permanece em aberto.")
            else:
                print("Retornando ao menu principal. Carrinho vazio descartado.")
            
            return pedido_aberto # Retorna o pedido atualizado para manter o estado

        else:
            print("Opção inválida.")
    
    return pedido_aberto


def main():
    # Permite que a função modifique variáveis de estado definidas fora do seu escopo local
    global USUARIO_LOGADO, PEDIDO_ABERTO
    
    print("Iniciando Plataforma FEIFood...")
    carregar_alimentos() 
    
    while True:
        if USUARIO_LOGADO is None:
            # Lógica de Pré-Login
            escolha = menu_inicial()
            
            if escolha == '1':
                log = input("Login: ")
                sen = input("Senha: ")
                USUARIO_LOGADO = login_usuario(log, sen)
                
                if USUARIO_LOGADO:
                    # Carrega o pedido aberto do usuário assim que ele loga
                    PEDIDO_ABERTO = buscar_pedido_aberto(USUARIO_LOGADO['ID'])
            
            elif escolha == '2':
                nome = input("Nome Completo: ")
                log = input("Login (escolha): ")
                sen = input("Senha: ")
                cadastrar_usuario(nome, log, sen, tipo='User') 
                
            elif escolha == '3':
                print("Programa encerrado. Até logo!")
                break
            
            else:
                print("Opção inválida.")
                
        else: 
            # Lógica Pós-Login
            escolha = menu_principal(USUARIO_LOGADO)

            if escolha == '1':
                buscar_e_listar_alimentos(ALIMENTOS)
            
            elif escolha == '2':
                # Chama a função interativa e atualiza o estado global com o resultado
                PEDIDO_ABERTO = gerenciar_carrinho(USUARIO_LOGADO, ALIMENTOS, PEDIDO_ABERTO)
                
            elif escolha == '3':
                # Avaliação de Pedidos
                print("\n--- Avaliar Pedido ---")
                
                pedidos_concluidos = [p for p in carregar_pedidos() if p['ID_USUARIO'] == USUARIO_LOGADO['ID'] and p['STATUS'] == 'FECHADO']
                
                if not pedidos_concluidos:
                    print("Você não possui pedidos finalizados que possam ser avaliados.")
                    continue
                    
                print("Pedidos Concluídos (Aguardando Avaliação):")
                for p in pedidos_concluidos:
                    print(f" - ID: {p['ID']} | Data: {p['DATA_HORA']}")

                try:
                    id_pedido = int(input("Digite o ID do pedido que deseja avaliar: "))
                    nota = input("Sua nota (0 a 5 estrelas): ")
                    
                    cadastrar_avaliacao(USUARIO_LOGADO['ID'], id_pedido, nota)
                    
                except ValueError:
                    print("Entrada inválida. O ID do pedido deve ser um número.")
            
            elif escolha == '9':
                if PEDIDO_ABERTO and PEDIDO_ABERTO['ID'] != 0:
                    print(f"Pedido ID {PEDIDO_ABERTO['ID']} mantido em aberto no CSV.")
                
                USUARIO_LOGADO = None
                PEDIDO_ABERTO = None
                print("Logout realizado com sucesso.")

            elif escolha == '0':
                salvar_todos_dados() 
                print("Salvando dados e encerrando o programa...")
                break 

            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    # Garante que a função 'main' seja executada apenas quando o arquivo for o programa principal.
    main()
