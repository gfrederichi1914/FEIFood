def buscar_e_listar_alimentos(alimentos):
    
    print("\n--- Busca de Alimentos ---")
    
    # Transforma o input do usuário em minúsculas
    termo = input("Digite o nome ou descrição do alimento (ou Enter para listar todos): ").strip().lower()
    
    # Filtra os alimentos com base no termo 
    resultados = []
    for alimento in alimentos:
        if not termo or termo in alimento['NOME'].lower() or termo in alimento['DESCRICAO'].lower():
            resultados.append(alimento)
    
    if not resultados:
        print("Nenhum alimento encontrado.")
        return

    print("\n> Resultados Encontrados")
    for a in resultados:
        # Formata o preço para duas casas decimais
        preco_formatado = f"R$ {a['PRECO']:.2f}".replace('.', ',') 
        
        print(f"ID: {a['ID']} | Nome: {a['NOME']} | Preço: {preco_formatado}")
        print(f"  Descrição: {a['DESCRICAO']}")
