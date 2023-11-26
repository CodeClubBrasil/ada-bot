def dividir_mensagens(mensagens, limite=4000):
    mensagens_divididas = []
    mensagem_atual = ""

    for mensagem in mensagens:
        if len(mensagem_atual) + len(mensagem) > limite:
            mensagens_divididas.append(mensagem_atual)
            mensagem_atual = mensagem + "\n"  # Começa uma nova mensagem
        else:
            mensagem_atual += mensagem + "\n"  # Adiciona à mensagem atual

    if mensagem_atual:  # Adiciona a última mensagem se ela existir
        mensagens_divididas.append(mensagem_atual)

    return mensagens_divididas
