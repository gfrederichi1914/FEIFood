from data_manager import read_data, write_data, pedidos_file, pedidos_keys
from datetime import datetime

# Funções Internas de Conversão 

def itens_to_csv(itens_lista):
    # Converte a lista de itens para a string no CSV
    if not itens_lista:
        return ""
    
    itens_csv = [f"{item['id']}-{item['qtd']}" for item in itens_lista]
    return ",".join(itens_csv)

def csv_to_itens(itens_string):
    # Converte a string formatada do CSV para uma lista de itens 
    if not itens_string:
        return []
        
    itens_lista = []
    itens_pares = itens_string.split(',')
    
    for par in itens_pares:
        id_str, qtd_str = par.split('-')
        
        itens_lista.append({
            'id': int(id_str),
            'qtd': int(qtd_str)
        })
    return itens_lista


# Funções de Persistência

def carregar_pedidos():
    # Carrega todos os pedidos do arquivo
    pedidos_crus = read_data(pedidos_file, pedidos_keys)
    
    for pedido in pedidos_crus:
        pedido['ID_USUARIO'] = int(pedido['ID_USUARIO'])
        pedido['ITENS_LISTA'] = csv_to_itens(pedido['ITENS']) 
        del pedido['ITENS'] 
        
    return pedidos_crus

def salvar_pedidos(pedidos):
    # Salva todos os pedidos no arquivo
    
    pedidos_para_salvar = []
    for pedido in pedidos:
        pedido_csv = pedido.copy()
        
        pedido_csv['ITENS'] = itens_to_csv(pedido_csv['ITENS_LISTA']) 
        del pedido_csv['ITENS_LISTA']
        
        pedidos_para_salvar.append(pedido_csv)

    write_data(pedidos_file, pedidos_para_salvar, pedidos_keys)


# Funções de Lógica de Negócio 

def criar_novo_pedido(id_usuario):
    # Cria um novo pedido em memória
    pedidos = carregar_pedidos()
    
    novo_id = 1
    if pedidos:
        novo_id = max(p['ID'] for p in pedidos) + 1
        
    novo_pedido = {
        'ID': novo_id,
        'ID_USUARIO': id_usuario,
        'DATA_HORA': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ITENS_LISTA': [], 
        'STATUS': 'ABERTO'
    }
    
    pedidos.append(novo_pedido)
    salvar_pedidos(pedidos)
    return novo_pedido

def adicionar_item(pedido_aberto, id_alimento, quantidade):
    # Adiciona ou atualiza a quantidade de um item no pedido em memória
    
    id_alimento = int(id_alimento)
    quantidade = int(quantidade)
    
    for item in pedido_aberto['ITENS_LISTA']:
        if item['id'] == id_alimento:
            item['qtd'] += quantidade
            if item['qtd'] <= 0:
                pedido_aberto['ITENS_LISTA'].remove(item)
            return pedido_aberto

    if quantidade > 0:
        pedido_aberto['ITENS_LISTA'].append({'id': id_alimento, 'qtd': quantidade})
    
    return pedido_aberto

def remover_pedido(pedido_id):
    # Exclui um pedido do arquivo
    pedidos = carregar_pedidos()
    
    pedidos_atualizados = [p for p in pedidos if p['ID'] != int(pedido_id)]
    
    if len(pedidos_atualizados) < len(pedidos):
        salvar_pedidos(pedidos_atualizados)
        return True
    return False

def buscar_pedido_aberto(id_usuario):
    # Busca o pedido aberto
    pedidos = carregar_pedidos()
    
    for pedido in pedidos:
        if pedido['ID_USUARIO'] == id_usuario and pedido['STATUS'] == 'ABERTO':
            return pedido
            
    return None

def listar_pedidos_usuario(id_usuario):
    # Lista todos os pedidos do usuário
    pedidos = carregar_pedidos()
    return [p for p in pedidos if p['ID_USUARIO'] == id_usuario]

def get_total_pedido(pedido, alimentos):
    # Calcula o valor total do pedido
    total = 0.0
    
    if not pedido or not pedido['ITENS_LISTA']:
        return 0.0

    for item in pedido['ITENS_LISTA']:
        id_alimento = item['id']
        quantidade = item['qtd']
        
        alimento = next((a for a in alimentos if a['ID'] == id_alimento), None)
        
        if alimento:
            total += alimento['PRECO'] * quantidade
            
    return total
