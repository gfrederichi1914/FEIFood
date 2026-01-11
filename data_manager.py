separador = ';'

# Variáveis de Usuário
user_file = "usuarios.csv"
user_keys = ["ID", "LOGIN", "SENHA", "NOME", "TIPO"]

# Variáveis de Alimentos
alimentos_file = "alimentos.csv"
alimentos_keys = ["ID", "NOME", "DESCRICAO", "PRECO"]

# Variáveis de Pedidos
pedidos_file = "pedidos.csv"
pedidos_keys = ["ID", "ID_USUARIO", "DATA_HORA", "ITENS", "STATUS"]

# Variáveis de Avaliações
avaliacoes_file = "avaliacoes.csv"
avaliacoes_keys = ["ID_PEDIDO", "ID_USUARIO", "NOTA_ESTRELAS", "DATA_AVALIACAO"] 


def read_data(file_name, keys):

    data = []
    
    # Abre o arquivo
    with open(file_name, "r", encoding="utf-8") as file:
        linhas = file.readlines()

        if len(linhas) <= 1: 
            return [] 
            
        for linha in linhas[1:]:
            valores = linha.strip().split(separador)
            
            # Checa se o número de campos é o mesmo
            if len(valores) != len(keys):
                continue 

            record = dict(zip(keys, valores))
            
            # Converte a chave ID para INT 
            if 'ID' in record:
                record['ID'] = int(record['ID'])
            
            data.append(record)

    return data


def write_data(file_name, data_list, keys):
    # Escreve a lista de dicionários de volta no arquivo CSV
    
    with open(file_name, "w", encoding="utf-8") as file:
        
        # Escreve o Cabeçalho
        file.write(separador.join(keys) + "\n")

        # Escreve cada registro 
        for record in data_list:
            
            valores_str = []
            for chave in keys:
                # Usa .get() para garantir que a chave exista no dicionário
                valor = record.get(chave, '') 
                
                # Converte o valor para string antes de escrever
                valores_str.append(str(valor))
            
            # Junta a lista de strings com o separador e escreve no arquivo
            linha_csv = separador.join(valores_str)
            file.write(linha_csv + "\n")
