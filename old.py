import sqlite3
import json
from datetime import datetime


class Sis:
    def __init__(self):
        self.db = sqlite3.connect('loja.db')
        self.c = self.db.cursor()
        # cria tabela
        self.c.execute('''CREATE TABLE IF NOT EXISTS ped (
            id INTEGER PRIMARY KEY,
            cli TEXT,
            itens TEXT,
            tot REAL,
            st TEXT,
            dt TEXT,
            tp TEXT)''')
        self.db.commit()

    def add_ped(self, n, its, t):
        # adiciona pedido
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tot = 0
        # calcula total
        for i in its:
            if i['tipo'] == 'normal':
                tot += i['p'] * i['q']
            elif i['tipo'] == 'desc10':
                tot += i['p'] * i['q'] * 0.9  # 10% desconto
            elif i['tipo'] == 'desc20':
                tot += i['p'] * i['q'] * 0.8  # 20% desconto
        # valida cliente vip
        if t == 'vip':
            tot = tot * 0.95  # 5% desconto vip
        its_str = json.dumps(its)
        self.c.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (n, its_str, tot, 'pendente', dt, t)
        )
        self.db.commit()
        # envia email
        print(f"Email enviado para {n}: Pedido recebido!")
        return self.c.lastrowid

    def get_ped(self, id):
        # busca pedido
        self.c.execute("SELECT * FROM ped WHERE id=?", (id,))
        r = self.c.fetchone()
        if r:
            return {
                'id': r[0],
                'cli': r[1],
                'itens': json.loads(r[2]),
                'tot': r[3],
                'st': r[4],
                'dt': r[5],
                'tp': r[6]
            }
        return None

    def upd_st(self, id, s):
        # atualiza status
        p = self.get_ped(id)
        if p:
            self.c.execute("UPDATE ped SET st=? WHERE id=?", (s, id))
            self.db.commit()
            # envia notificacao
            if s == 'aprovado':
                print(f"Email enviado para {p['cli']}: Pedido aprovado!")
                print(f"SMS enviado para {p['cli']}: Pedido aprovado!")
            elif s == 'enviado':
                print(f"Email enviado para {p['cli']}: Pedido enviado!")
            elif s == 'entregue':
                print(f"Email enviado para {p['cli']}: Pedido entregue!")
            # registra pontos
            if p['tp'] == 'vip':
                pts = int(p['tot'] * 2)  # vip ganha 2x pontos
                print(f"Cliente VIP ganhou {pts} pontos!")
            else:
                pts = int(p['tot'])
                print(f"Cliente ganhou {pts} pontos!")

    def calc_tot_cli(self, n):
        # calcula total gasto pelo cliente
        self.c.execute("SELECT * FROM ped WHERE cli=?", (n,))
        rs = self.c.fetchall()
        t = 0
        for r in rs:
            t += r[3]
        return t

    def gerar_rel(self, tipo):
        # gera relatorio
        if tipo == 'vendas':
            self.c.execute("SELECT * FROM ped")
            rs = self.c.fetchall()
            print("=== RELATÓRIO DE VENDAS ===")
            tot_g = 0
            for r in rs:
                print(f"Pedido #{r[0]} - Cliente: {r[1]
                                                   } - Total: R${r[3]:.2f} - Status: {r[4]}")
                tot_g += r[3]
            print(f"Total Geral: R${tot_g:.2f}")
            # salva em arquivo
            with open('rel_vendas.txt', 'w') as f:
                f.write(f"Total de vendas: {tot_g}")
        elif tipo == 'clientes':
            self.c.execute("SELECT DISTINCT cli, tp FROM ped")
            rs = self.c.fetchall()
            print("=== RELATÓRIO DE CLIENTES ===")
            for r in rs:
                n = r[0]
                tp = r[1]
                tot = self.calc_tot_cli(n)
                print(f"Cliente: {n} ({tp}) - Total gasto: R${tot:.2f}")
            # salva em arquivo
            with open('rel_clientes.txt', 'w') as f:
                for r in rs:
                    f.write(f"{r[0]},{r[1]}\n")

    def proc_pag(self, id, m, vl):
        # processa pagamento
        p = self.get_ped(id)
        if not p:
            return False
        # valida valor
        if vl < p['tot']:
            print("Valor insuficiente!")
            return False
        # processa de acordo com metodo
        if m == 'cartao':
            print("Processando pagamento com cartao...")
            # valida cartao (simplificado)
            print("Cartao validado!")
            self.upd_st(id, 'aprovado')
            return True
        elif m == 'pix':
            print("Gerando QR Code PIX...")
            print("PIX recebido!")
            self.upd_st(id, 'aprovado')
            return True
        elif m == 'boleto':
            print("Gerando boleto ...")
            print("Boleto gerado!")
            # boleto nao aprova automaticamente
            return True
        else:
            print("Metodo de pagamento invalido!")
            return False

    def validar_estoque(self, its):
        # valida estoque (simplificado)
        est = {'produto1': 100, 'produto2': 50, 'produto3': 75}
        for i in its:
            if i['nome'] not in est:
                print(f"Produto {i['nome']} nao encontrado!")
                return False
            if est[i['nome']] < i['q']:
                print(f"Estoque insuficiente para {i['nome']}!")
                return False
        return True

    def close(self):
        self.db.close()


class PedEspecial(Sis):
    def add_ped(self, n, its, t):
        # pedido especial tem taxa extra
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tot = 0
        for i in its:
            if i['tipo'] == 'normal':
                tot += i['p'] * i['q']
            elif i['tipo'] == 'desc10':
                tot += i['p'] * i['q'] * 0.9
            elif i['tipo'] == 'desc20':
                tot += i['p'] * i['q'] * 0.8
        # taxa especial
        tot = tot * 1.15  # 15% taxa
        its_str = json.dumps(its)
        self.c.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (n, its_str, tot, 'pendente', dt, t)
        )
        self.db.commit()
        print(f"Email especial enviado para {n}: Pedido especial recebido!")
        return self.c.lastrowid


def main():
    s = Sis()
    # exemplo de uso
    its1 = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 2, 'tipo': 'desc10'}
    ]
    pid = s.add_ped('cliente@exemplo.com', its1, 'normal')
    print(s.get_ped(pid))
    s.proc_pag(pid, 'pix', 200)
    s.gerar_rel('vendas')
    s.gerar_rel('clientes')
    s.close()


if __name__ == '__main__':
    main()
