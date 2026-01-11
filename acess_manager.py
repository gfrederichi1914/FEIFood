from data_manager import read_data, write_data, user_file, user_keys

def carregar_usuarios():
    # Função interna para carregar a lista de usuários.
    return read_data(user_file, user_keys)

def salvar_usuarios(usuarios):
    # Função interna para salvar a lista de usuários.
    write_data(user_file, usuarios, user_keys)

def login_usuario(login, senha):
    # Verifica as credenciais e retorna o objeto do usuário logado ou None.
    usuarios = carregar_usuarios()
    
    for user in usuarios:
        if user['LOGIN'] == login and user['SENHA'] == senha:
            print(f"Login bem-sucedido. Bem-vindo, {user['NOME']}!")
            return user
            
    print("Login ou senha incorretos.") 
    return None

def cadastrar_usuario(nome, login, senha, tipo='User'):
    # Cadastra um novo usuário no sistema.
    usuarios = carregar_usuarios()
    
    # 1. Checa se o login já existe
    if any(u['LOGIN'] == login for u in usuarios):
        print("Login já cadastrado. Tente outro.") 
        return None

    # 2. Gera o novo ID
    novo_id = 1
    if usuarios:
        novo_id = max(u['ID'] for u in usuarios) + 1
        
    # 3. Cria o novo registro
    novo_usuario = {
        'ID': novo_id,
        'LOGIN': login,
        'SENHA': senha,
        'NOME': nome,
        'TIPO': tipo
    }
    
    # 4. Adiciona à lista e salva
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    print(f"🎉 Cadastro concluído! ID: {novo_id}")
    return novo_usuario