menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = f""
numero_saques = 0
LIMITE_SAQUES = 4

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato

def sacar(saldo, valor, limite, extrato, numero_saques):
    if valor > saldo:
        print("Saldo insuficiente!")
    elif valor > limite:
        print("Valor acima do limite!")
    elif numero_saques >= LIMITE_SAQUES:
        print("Número máximo de saques atingido!")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para saque.")
    return saldo, extrato, numero_saques    

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

while True:
    opcao = input(menu).strip().lower()
    if opcao == "1":
        valor_input = input("Valor para depósito: R$ ")
        try:
            valor = float(valor_input)
        except ValueError:
            print("Valor inválido para depósito.")
            continue
        saldo, extrato = depositar(saldo, valor, extrato)
    elif opcao == "2":
        valor_input = input("Valor para saque: R$ ")
        try:
            valor = float(valor_input)
        except ValueError:
            print("Valor inválido para saque.")
            continue
        saldo, extrato, numero_saques = sacar(saldo, valor, limite, extrato, numero_saques)
    elif opcao == "3":
        exibir_extrato(saldo, extrato)
    elif opcao == "q":
        print("Saindo da conta.")
        break
    else:
        print("Opção inválida! Tente novamente.")
