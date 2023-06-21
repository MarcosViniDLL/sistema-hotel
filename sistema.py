autorizados = {
    "adm":"adm123",
    "suporte":"suporte123"
}

login = False

while not login:
    user = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    if user in autorizados and autorizados[user] == senha:
        print("Logado com sucesso!")
        login = True
    else:
        print("O usuário ou a senha está incorreto. Verifique e tente novamente.")
print("Sucesso ao fazer o login!")

print('------------------------------------------------------------')
print('----------- Seja bem vindo(a) ao Hotel das Flores! ----------')
print('------------------------------------------------------------')
print('\n')

def menu():
    print('----- MENU -----')
    print('\n')
    print('----- Selecione uma opção: -----')
    print('\n')
    print('--(1)-- Cadastrar Cliente --')
    print('--(2)-- Fazer Reserva --')
    print('--(3)-- Atualizar Cadastro --')
    print('--(4)-- Ver Reservas --')
    print('--(5)-- Excluir Cadastro --')
    print('--(6)-- Excluir Reserva --')
    print('--(7)-- Visualizar Clientes --')
    print('--(8)-- Sair --')
    print('\n')
    opcao = input("Digite a opção desejada: ")
    return opcao

clientes_cadastrados = []
reservas_feitas = []

def cadastrar():
    nome = input("Digite o seu nome completo: ")
    if not nome.replace(" ", "").isalpha():
        print("O nome deve conter apenas letras.")
        return

    cpf = input('Digite o seu CPF: ')
    if len(cpf) != 11:
        print(f"O CPF precisa ter 11 digitos!")
        return
    
    email = input("Digite o seu email: ")
    if not email.count('@') == 1 or not email.endswith(".com"):
        print("Você precisa digitar um email válido!")
        return
    
    telefone = input("Digite o seu telefone: ")
    if len(telefone) != 11:
        print("O telefone deve ter 11 dígitos.")
    if not telefone.startswith("(") or not telefone[3] == ")" or not telefone[9] == "-":
        print("O formato correto é (99) 99999-9999")
    if not telefone[1:3].isdigit() or not telefone[4:9].isdigit() or not telefone[10:].isdigit():
        print("O telefone deve ter apenas números.")

    cliente = {"nome": nome, "cpf": cpf, "email": email, "telefone": telefone}
    clientes_cadastrados.append(cliente)

    with open("clientes_cadastrados.txt", "w", encoding="utf-8") as clientes_arquivo:
        for cliente in clientes_cadastrados:
            clientes_arquivo.write(f"{cliente['nome']},{cliente['cpf']},{cliente['email']},{cliente['telefone']}\n")

    print("Cliente cadastrado com sucesso!")

def fazer_reserva():
    cpf = input("Digite o CPF do cliente: ")
    if len(cpf) != 11:
        print(f"O CPF precisa ter 11 digitos!")
        return
    
    preco_quarto = {"1":200, "2":500, "3":1000}
    print("Quarto (1) = Suite Básica [R$ 200] / Quarto (2) = Suite Economy [500] / Quarto (3) = Suite Presidencial [1000]")
    tipoquarto = input("Digite o número do quarto: ")

    if tipoquarto not in preco_quarto:
        print("O número que você digitou é inválido.")
        return
    
    entrada = input("Digite a data do Check-In (d/m/a):  ")
    saida = input("Digite a data do Check-Out: (d/m/a): ")

    dia_entrada, mes_entrada, ano_entrada = map(int, entrada.split("/"))
    dia_saida, mes_saida, ano_saida = map(int, saida.split("/"))
    estadia = (dia_saida - dia_entrada) + 30 * (mes_saida - mes_entrada) + 365 * (ano_saida - ano_entrada)

    if estadia <= 0:
        print("A data de Check-Out deve ser posterior à data de Check-In.")
        return
    
    valor_diaria = preco_quarto[tipoquarto]
    valor_total = valor_diaria * estadia

    print("Qual a forma de pagamento? ")
    print("(1) Cartão de Crédito")
    print("(2) PIX")

    pgt = input("Digite o número da forma de pagamento: ")
    if pgt not in ['1', '2']:
        print("Forma de pagamento inválida!")
        return
    
    if pgt == '1':
        print("Você vai querer dividir?")
        s_n = input("S para sim, ou N para não. ")

        if s_n == "S":
            print("Em quantas vezes? (1), (2), (3)")
            vezes = input("Digite o número de vezes: ")
            valor = preco_quarto[tipoquarto]
            valor_parcela = valor / int(vezes)
            print(f"O valor de cada parcela será de {vezes} de R$ {valor_parcela:.2f}")

        elif s_n == "N":
            print("Compra efetuada com sucesso!")

    if pgt == "2":
        NOME_HOTEL = "Hotel das Flores"
        print("Nossa chave pix é: hoteldasflores.com")
        print("Pagamento via PIX selecionado.")
        chave = input("Digite a Chave PIX: ")

        if chave != "hoteldasflores.com":
            print("A chave pix informada não existe.")
            return
        
        valor = float(input("Informe o valor: "))
        confirma = input(f"Você está enviando R$ {valor} para {NOME_HOTEL}, você confirma? [S para Sim, N para Não: ")
        if confirma == "S":
            print("Pagamento efetuado com sucesso! Muito obrigado.")
        elif confirma == "N":
            return
        else:
            print("Você deve digitar uma opção válida.")

    reserva = {"cpf":cpf, "quarto":tipoquarto, "entrada":entrada, "saida":saida}
    reservas_feitas.append(reserva)
    print("Reserva feita com sucesso!")

    with open("reservas.txt", "a", encoding="utf-8") as reservas_arquivo:
        reservas_arquivo.write(f"CPF: {cpf}, Quarto: {tipoquarto}, Check-In: {entrada}, Check-Out: {saida}, Pagamento: {pgt}\n")

def atualizar_cadastro(cpf):
    cliente_encontrado = False
    for cliente in clientes_cadastrados:
        if cliente["cpf"] == cpf:
            telefone = input("Digite o novo telefone do cliente: ")
            email = input("Digite o novo endereço de email do cliente: ")
            cliente["telefone"] = telefone
            cliente["email"] = email
            cliente_encontrado = True

    if cliente_encontrado:
        with open("clientes_cadastrados.txt", "w", encoding='utf-8') as arq:
            for cliente in clientes_cadastrados:
                arq.write(f"{cliente['nome']},{cliente['cpf']},{cliente['email']},{cliente['telefone']}\n")
        print("Cadastro atualizado com sucesso!")
    else:
        print("Cliente não encontrado.")

def visualizar_reserva(cpf):
    reserva_encontrada = False
    for reserva in reservas_feitas:
        if reserva["cpf"] == cpf:
            print("Quarto:", reserva["quarto"])
            print("Check-In:", reserva["entrada"])
            print("Check-Out:", reserva["saida"])
            reserva_encontrada = True

    if not reserva_encontrada:
        print("Reserva não encontrada.")

def excluir_cadastro(cpf):
    cliente_removido = False
    for cliente in clientes_cadastrados:
        if cliente["cpf"] == cpf:
            clientes_cadastrados.remove(cliente)
            cliente_removido = True

    if cliente_removido:
        with open("clientes_cadastrados.txt", "w", encoding='utf-8') as arq:
            for cliente in clientes_cadastrados:
                arq.write(f"{cliente['nome']},{cliente['cpf']},{cliente['email']},{cliente['telefone']}\n")
        print("Cadastro removido com sucesso!")
    else:
        print("Cliente não encontrado.")

def excluir_reserva(cpf):
    reserva_removida = False
    for reserva in reservas_feitas:
        if reserva["cpf"] == cpf:
            reservas_feitas.remove(reserva)
            reserva_removida = True

    if reserva_removida:
        with open("reservas.txt", "w", encoding='utf-8') as arq:
            for reserva in reservas_feitas:
                arq.write(f"CPF: {reserva['cpf']}, Quarto: {reserva['quarto']}, Check-In: {reserva['entrada']}, Check-Out: {reserva['saida']}\n")
        print("Reserva removida com sucesso!")
    else:
        print("Reserva não encontrada.")

def visualizar_clientes():
    if len(clientes_cadastrados) == 0:
        print("Não há clientes cadastrados.")
    else:
        print("Clientes cadastrados:")
        for cliente in clientes_cadastrados:
            print("Nome:", cliente["nome"])
            print("CPF:", cliente["cpf"])
            print("Email:", cliente["email"])
            print("Telefone:", cliente["telefone"])
            print()

while True:
    opcao = menu()
    
    if opcao == '1':
        cadastrar()
    elif opcao == '2':
        fazer_reserva()
    elif opcao == '3':
        cpf = input("Digite o CPF do cliente: ")
        atualizar_cadastro(cpf)
    elif opcao == '4':
        visualizar_reserva(cpf)
    elif opcao == '5':
        cpf = input("Digite o CPF do cliente: ")
        excluir_cadastro(cpf)
    elif opcao == '6':
        cpf = input("Digite o CPF do cliente: ")
        excluir_reserva(cpf)
    elif opcao == '7':
        visualizar_clientes()
    elif opcao == '8':
        break
    else:
        print("Opção inválida. Digite novamente.")
