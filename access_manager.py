from data_manager import read_data, write_data, user_file, user_keys

def carregar_usuarios():
    # Carrega a lista de usuários do arquivo
    return read_data(user_file, user_keys)

def salvar_usuarios(usuarios):
    # Salva a lista de usuários no arquivo
    write_data(user_file, usuarios, user_keys)

def login_usuario(login, senha):
    # Verifica as credenciais e retorna o objeto do usuário logado ou None
    usuarios = carregar_usuarios()
    
    for user in usuarios:
        if user['LOGIN'] == login and user['SENHA'] == senha:
            print(f"Login bem-sucedido. Bem-vindo, {user['NOME']}!")
            return user # Retorna o objeto (dicionário) do usuário autenticado
            
    print("Login ou senha incorretos.") 
    return None

def cadastrar_usuario(nome, login, senha, tipo='User'):
    # Cadastra um novo usuário no sistema
    usuarios = carregar_usuarios()
    
    # Verifica se qualquer usuário na lista já possui o login que está sendo cadastrado
    if any(u['LOGIN'] == login for u in usuarios):
        print("Login já cadastrado. Tente outro.") 
        return None

    # Gera um próximo ID único e sequencial
    novo_id = 1
    if usuarios:
        novo_id = max(u['ID'] for u in usuarios) + 1
        
    novo_usuario = {
        'ID': novo_id,
        'LOGIN': login,
        'SENHA': senha,
        'NOME': nome,
        'TIPO': tipo
    }
    
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    print(f"Cadastro concluído! ID: {novo_id}")
    return novo_usuario
