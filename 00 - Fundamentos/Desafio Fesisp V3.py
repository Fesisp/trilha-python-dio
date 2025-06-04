import datetime
import time
import sqlite3

menu1 = """
Seja Bem-Vindo ao Fesisbank
Voce ja é cliente do nosso banco?
[1] Sim
[2] Não
[3] Sair
"""
menu2 = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """



saldo = 0
limite = 500
extrato = f""
transacoes = 0
LIMITE_TRANSACOES = 10
data = datetime.datetime.now().strftime("%A %d/%m/%Y")
hora = datetime.datetime.now().strftime("%H:%M")
limite_tentativa = 5
suporte = "Se precisar de ajuda, entre em contato com o suporte através do e-mail ou telefone\n fesisbanksup@gmail.com\n (99)99999-9999"
banco_dados = "fesisbank"

conn = sqlite3.connect('fesisbank_users.db', isolation_level=None)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nascimento TEXT,
    cpf TEXT UNIQUE,
    endereco TEXT,
    telefone TEXT,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')
# Criação da tabela de contas, cada conta pertence a um usuário
cursor.execute('''
CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agencia TEXT NOT NULL,
    numero_conta INTEGER NOT NULL,
    usuario_login TEXT NOT NULL,
    FOREIGN KEY(usuario_login) REFERENCES usuarios(login)
)
''')
conn.commit()
contas = []
NUMERO_AGENCIA = "0001"

def get_proximo_numero_conta():
    cursor.execute('SELECT MAX(numero_conta) FROM contas')
    resultado = cursor.fetchone()
    if resultado and resultado[0]:
        return resultado[0] + 1
    return 1

def depositar(saldo, valor, extrato, transacoes, data, hora):
    if valor <= 0:
        print("Valor inválido para depósito.")
    elif transacoes >= LIMITE_TRANSACOES:
        print("Número máximo de transacoes atingido!")
    elif valor > 0:
        data = datetime.datetime.now().strftime("%A %d/%m/%Y")
        hora = datetime.datetime.now().strftime("%H:%M")
        saldo += valor
        extrato += f"{data} {hora} - Depósito: R$ {valor:.2f}\n"
        transacoes += 1
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato, transacoes, data, hora
def sacar(saldo, valor, limite, extrato, transacoes, data, hora):
    if valor > saldo:
        print("Saldo insuficiente!")
    elif valor > limite:
        print("Valor acima do limite!")
    elif transacoes >= LIMITE_TRANSACOES:
        print("Número máximo de transacoes atingido!")
    elif valor > 0:
        data = datetime.datetime.now().strftime("%A %d/%m/%Y")
        hora = datetime.datetime.now().strftime("%H:%M")
        saldo -= valor
        extrato += f"{data} {hora} - Saque: R$ {valor:.2f}\n"
        transacoes += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para saque.")
    return saldo, extrato, transacoes, data, hora
def exibir_extrato(saldo, extrato, data, hora):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
def cadastrar_usuario():
    print("===> Cadastro de Novo Cliente <===")
    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    cpf = input("CPF (apenas números): ").strip()
    endereco = input("Endereço completo: ").strip()
    telefone = input("Telefone (apenas números): ").strip()
    login = input("Escolha um login: ").strip().lower()
    senha = input("Escolha uma senha: ").strip()

    try:
        cursor.execute(
            'INSERT INTO usuarios (nome, nascimento, cpf, endereco, telefone, login, senha) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (nome, nascimento, cpf, endereco, telefone, login, senha)
        )
        conn.commit()
        print("Cadastro realizado com sucesso!")
    except sqlite3.IntegrityError as e:
        if "cpf" in str(e).lower():
            print("CPF já cadastrado. Faça o seu login.")
        elif "login" in str(e).lower():
            print("Login já existe. Tente novamente com outro login.")
        else:
            print("Erro ao cadastrar usuário. Tente novamente.")

def recuperar_login_ou_senha():
    print("===> Recuperação de Login/Senha <===")
    print("[1] Recuperar login")
    print("[2] Recuperar senha")
    escolha = input("Escolha uma opção: ").strip()
    if escolha == "1":
        cpf = input("CPF (apenas números): ").strip()
        senha = input("Senha atual: ").strip()
        nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
        cursor.execute(
            'SELECT login FROM usuarios WHERE cpf=? AND senha=? AND nascimento=?',
            (cpf, senha, nascimento)
        )
        resultado = cursor.fetchone()
        if resultado:
            print(f"Seu login (usuário) é: {resultado[0]}")
        else:
            print("Dados não encontrados ou incorretos. Tente novamente.")
    elif escolha == "2":
        cpf = input("CPF (apenas números): ").strip()
        login_usuario = input("Login: ").strip().lower()
        nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
        cursor.execute(
            'SELECT senha FROM usuarios WHERE cpf=? AND login=? AND nascimento=?',
            (cpf, login_usuario, nascimento)
        )
        resultado = cursor.fetchone()
        if resultado:
            print(f"Sua senha é: {resultado[0]}")
        else:
            print("Dados não encontrados ou incorretos. Tente novamente.")
    else:
        print("Opção inválida.")

def criar_conta(usuario_login):
    proximo_numero_conta = get_proximo_numero_conta()
    conta = {
        "agencia": NUMERO_AGENCIA,
        "numero_conta": proximo_numero_conta,
        "usuario": usuario_login
    }
    contas.append(conta)
    cursor.execute(
        'INSERT INTO contas (agencia, numero_conta, usuario_login) VALUES (?, ?, ?)',
        (NUMERO_AGENCIA, proximo_numero_conta, usuario_login)
    )
    conn.commit()
    print(f"Conta criada com sucesso! Agência: {NUMERO_AGENCIA} Conta: {proximo_numero_conta:04d} Usuário: {usuario_login}")

def listar_contas_do_usuario(usuario_login):
    print(f"Contas do usuário {usuario_login}:")
    encontrou = False
    cursor.execute('SELECT agencia, numero_conta FROM contas WHERE usuario_login=?', (usuario_login,))
    contas_db = cursor.fetchall()
    for agencia, numero_conta in contas_db:
        print(f"Agência: {agencia} Conta: {numero_conta:04d}")
        encontrou = True
    if not encontrou:
        print("Nenhuma conta encontrada para este usuário.")

def alterar_senha(usuario_login):
    print("===> Alteração de Senha <===")
    senha_atual = input("Digite sua senha atual: ").strip()
    cursor.execute('SELECT senha FROM usuarios WHERE login=?', (usuario_login,))
    resultado = cursor.fetchone()
    if resultado and resultado[0] == senha_atual:
        nova_senha = input("Digite a nova senha: ").strip()
        confirmar = input("Confirme a nova senha: ").strip()
        if nova_senha == confirmar:
            cursor.execute('UPDATE usuarios SET senha=? WHERE login=?', (nova_senha, usuario_login))
            conn.commit()
            print("Senha alterada com sucesso!")
        else:
            print("As senhas não coincidem. Tente novamente.")
    else:
        print("Senha atual incorreta.")

def login(limite_tentativa, suporte):
    tentativas = limite_tentativa
    while tentativas > 0:
        login_input = input("Insira o seu login: ").strip().lower()
        senha_input = input("Insira sua senha: ").strip()
        cursor.execute('SELECT * FROM usuarios WHERE login=? AND senha=?', (login_input, senha_input))
        usuario = cursor.fetchone()
        if usuario:
            print("Login realizado com sucesso!")
            return login_input
        else:
            tentativas -= 1
            print(f"Login ou Senha incorreta.\nVocê ainda tem {tentativas} tentativas.")
            if tentativas == 0:
                print("Número máximo de tentativas atingido. Acesso Bloqueado, aguarde um momento.")
                time.sleep(3)
                print(suporte)
                return None
            print("[0] Recuperar login/senha")
            rec = input("Deseja tentar recuperar login ou senha? (0 para sim, Enter para não): ").strip()
            if rec == "0":
                recuperar_login_ou_senha()

while True:
    
    opcao1 = input(menu1).strip().lower()
    if opcao1 == "1":
        usuario_login = login(limite_tentativa, suporte)
        if usuario_login:
            print("Bem-vindo de volta ao Fesisbank!\nO que deseja fazer hoje?")
            while True:
                print("[5] Criar nova conta")
                print("[6] Listar minhas contas")
                print("[7] Alterar minha senha")
                opcao2 = input(menu2).strip().lower()
                if opcao2 == "1":
                    valor_input = input("Valor para depósito: R$ ")
                    try:
                        valor = float(valor_input)
                    except ValueError:
                        print("Valor inválido para depósito.")
                        continue
                    saldo, extrato, transacoes, data, hora = depositar(saldo, valor, extrato, transacoes, data, hora)
                elif opcao2 == "2":
                    valor_input = input("Valor para saque: R$ ")
                    try:
                        valor = float(valor_input)
                    except ValueError:
                        print("Valor inválido para saque.")
                        continue
                    saldo, extrato, transacoes, data, hora = sacar(saldo, valor, limite, extrato, transacoes, data, hora)
                elif opcao2 == "3":
                    exibir_extrato(saldo, extrato, data, hora)
                elif opcao2 == "4":
                    print("Saindo da conta.")
                    break
                elif opcao2 == "5":
                    criar_conta(usuario_login)
                elif opcao2 == "6":
                    listar_contas_do_usuario(usuario_login)
                elif opcao2 == "7":
                    alterar_senha(usuario_login)
                else:
                    print("Opção inválida! Tente novamente.")
        else:
            break
    elif opcao1 == "2":
        cadastrar_usuario()
    elif opcao1 == "3":
        print("Saindo do Fesisbank. Até logo!")
        break
    else:
        print("Opção inválida! Tente novamente.")
conn.close()
