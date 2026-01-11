from data_manager import read_data, write_data, avaliacoes_file, avaliacoes_keys
from order_manager import carregar_pedidos, salvar_pedidos # Para verificar o status do pedido
from datetime import datetime

def cadastrar_avaliacao(id_usuario, id_pedido, nota):
    # Cadastra uma avaliação para um pedido finalizado
    
    # Validação da Nota
    nota = int(nota) 
    
    if not (0 <= nota <= 5): 
        print("Nota inválida. A avaliação deve ser entre 0 e 5 estrelas.")
        return False

    # Carrega todos os pedidos para verificar o status
    pedidos = carregar_pedidos()
    
    pedido_encontrado = next((p for p in pedidos if p['ID'] == int(id_pedido) and p['ID_USUARIO'] == id_usuario), None)

    if not pedido_encontrado:
        print(f"Pedido ID {id_pedido} não encontrado ou não pertence a este usuário.")
        return False
        
    if pedido_encontrado['STATUS'] != 'FECHADO':
        print("Apenas pedidos FINALIZADOS podem ser avaliados.")
        return False
        
    # Carrega avaliações para verificar se já existe
    avaliacoes = read_data(avaliacoes_file, avaliacoes_keys)
    
    # Verifica se já existe avaliação para este pedido (comparando com a string do id_pedido)
    if any(a['ID_PEDIDO'] == str(id_pedido) for a in avaliacoes): 
        print(f"O Pedido ID {id_pedido} já foi avaliado anteriormente.")
        return False

    # Cria e salva a nova avaliação
    nova_avaliacao = {
        'ID_PEDIDO': str(id_pedido), 
        'ID_USUARIO': str(id_usuario), 
        'NOTA_ESTRELAS': nota,
        'DATA_AVALIACAO': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    avaliacoes.append(nova_avaliacao)
    write_data(avaliacoes_file, avaliacoes, avaliacoes_keys)
    
    print(f"Pedido ID {id_pedido} avaliado com {nota} estrelas. Obrigado!")
    return True