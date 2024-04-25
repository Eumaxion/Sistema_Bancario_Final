from datetime import datetime
from abc import ABC, abstractmethod
import textwrap

class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizarTransacao(self,conta, transacao):
        transacao.registrar(conta)
        
    def adicionarConta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, dataDeNascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.dataDeNascimento = dataDeNascimento

class Conta():
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        semSaldo = valor > saldo
        valorIncorreto = valor <= 0
        if semSaldo:
            print("saldo insuficiente!")
        elif valorIncorreto:
            print("valor incorreto!")
        else:
            self._saldo -= valor
            print (f"€{valor:2f} sacado com sucesso, novo saldo = €{self._saldo}")
            return True
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print (f"€{valor:.2f} depositado com sucesso, novo saldo = €{self._saldo}")
            return True
        else:
            print("valor informado inválido!")

    def verificarSaldo(self):
        return f"€{self.saldo}"
    
    def novaConta(self, numero):
        numero =+ 1
        return f"Nome: {self.cliente}\n Conta nº:{numero}\n"

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500,limiteSaque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limiteSaque = limiteSaque
        
    def sacar(self, valor):
        numero_saques = len(transacao for trasacao in self.historico.transacoes if transacao["tipo"]== Saque.__name__)
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limiteSaque

        if excedeu_limite:
            print("valor requerido excedeu o limite!")
        elif excedeu_saque:
            print("excedeu numero de saques!")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\nAgencia: \t{self.agencia} 
        CC: \t\t{self.numero} 
        Titular\t{self.cliente.nome}"""

class Historico():
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes

    def adicionarTransacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor":transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self,conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionarTransacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionarTransacao(self)

def menu():
        menu = """
-----------Menu Principal -----------
            [d] - Depositar
            [s] - Sacar
            [e] - Extrato
            [c] - Cadastrar Usuario
            [cc] - Cadastrar Conta
            [lc] - Listar Contas
            [q] - Sair
--------------------------------------
             """
        return input(textwrap.dedent(menu))

def checarCPF(cpf, clientes):
    filtragem = [cliente for cliente in clientes if cliente.cpf == cpf]
    '''for cliente in clientes:
        if cliente.cpf == cpf:
            filtragem += cliente'''
    return filtragem[0] if filtragem else None

def checarConta(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return 
    conta = input("insira o numero da conta: ")
    if not cliente.contas[conta]:
        print("conta não encontrada.")
        return
    return cliente.contas[conta]

def depositar(clientes):
    cpf = input("insira o CPF: ")
    cliente = checarCPF(cpf, clientes)
    if not cliente:
        print("cliente não encontrado")
        return

    valor = float(input("insira o valor a ser depositado: "))
    transacao = Deposito(valor)

    conta = checarConta(cliente)
    if not conta:
        return
    
    cliente.realizarTransacao(conta, transacao)

def sacar(clientes):
    cpf = input("insira o CPF: ")
    cliente = checarCPF(cpf, clientes)
    if not cliente:
        print("cliente não encontrado")
        return
    
    valor = float(input("insira o valor a ser sacado: "))
    transacao = Saque(valor)

    conta = checarConta(cliente)
    if not conta:
        return
    
    cliente.realizarTransacao(conta, transacao)

def extrato(clientes):
    cpf = input("insira o CPF: ")
    cliente = checarCPF(cpf, clientes)

    if not cliente:
        print("cliente não encontrado")
        return
    
    conta = checarConta(cliente)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes()
    extrato = ""

    if not transacoes:
        extrato = "Não há transações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo: \tR$ {conta.saldo:.2f}")
    print("****************************************************************")

def cadastrarUsuario(clientes): 
    cpf = input("insira o CPF: ")
    cliente = checarCPF(cpf, clientes)
    
    if  cliente:
        print("cliente já cadastrado")
        return
    
    nome = input("Informe o nome completo:")
    dataDeNascimento = input("Informe a data de nascimento(dd/mm/aaaa): ")
    endereco = input("informe o endereço(logradouro,numero,cidade)")

    cliente = PessoaFisica(nome=nome, dataDeNascimento=dataDeNascimento,cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("cliente cadastrado com sucesso.")

def cadastrarConta(numeroContas, clientes, contas):
    cpf = input("insira o CPF: ")
    cliente = checarCPF(cpf, clientes)
    
    if not cliente:
        print("cliente não encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numeroContas)
    contas.append(conta)
    clientes.contas.append(conta)

    print("conta criada com sucesso.")

def listarContas(contas):
    for conta in contas:
        print('-' * 100)
        print(textwrap.dedent(str(conta)))

def main():    
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            extrato(clientes)
        elif opcao == "c":
            cadastrarUsuario(clientes)
        elif opcao == "cc":
            numeroConta = len(contas) + 1
            cadastrarConta(numeroConta, clientes, contas)
        elif opcao == "lc":
            listarContas(contas)
        elif opcao == "q":
            print("saindo")
            break
        else:
            print("operação invalida, tente novamente.")
            return
main()
