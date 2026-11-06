import tkinter as tk
from tkinter import messagebox

LINHAS = 6
COLUNAS = 7
TAMANHO_CELULA = 80
MARGEM = 10

COR_TABULEIRO = "#7a7a00"
COR_FUNDO = "#222222"
COR_VAZIA = "#1e1e1e"
CORES = {1: "#d62828", 2: "#4a6cf7"}
NOMES = {1: "Jogador 1 (Vermelho)", 2: "Jogador 2 (Azul)"}
COR_DESTAQUE = "#ffffff"


def criar_tabuleiro():
    """Cria uma matriz LINHAS x COLUNAS preenchida com 0 (vazio)."""
    return [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]


def coluna_cheia(tabuleiro, coluna):
    """A coluna está cheia quando a posição do topo (linha 0) está ocupada."""
    return tabuleiro[0][coluna] != 0


def inserir_ficha(tabuleiro, coluna, jogador):
    """Aplica a gravidade: a ficha cai até a linha mais baixa livre.
    Retorna a linha onde a ficha parou, ou None se a coluna estiver cheia."""
    if coluna < 0 or coluna >= COLUNAS or coluna_cheia(tabuleiro, coluna):
        return None
    for linha in range(LINHAS - 1, -1, -1):
        if tabuleiro[linha][coluna] == 0:
            tabuleiro[linha][coluna] = jogador
            return linha
    return None


def verificar_vitoria(tabuleiro, jogador):
    """Procura 4 fichas seguidas do jogador em todas as direções.
    Retorna a lista das 4 posições vencedoras, ou uma lista vazia."""
    direcoes = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for dl, dc in direcoes:
                posicoes = []
                for passo in range(4):
                    l = linha + dl * passo
                    c = coluna + dc * passo
                    if 0 <= l < LINHAS and 0 <= c < COLUNAS and tabuleiro[l][c] == jogador:
                        posicoes.append((l, c))
                    else:
                        break
                if len(posicoes) == 4:
                    return posicoes
    return []


def tabuleiro_cheio(tabuleiro):
    """Empate: todas as colunas estão cheias."""
    return all(coluna_cheia(tabuleiro, c) for c in range(COLUNAS))


def desenhar_tabuleiro(window, tabuleiro, vencedoras=None):
    """Redesenha o tabuleiro no Canvas da janela."""
    canvas = window.canvas
    canvas.delete("all")
    largura = COLUNAS * TAMANHO_CELULA + 2 * MARGEM
    altura = LINHAS * TAMANHO_CELULA + 2 * MARGEM
    canvas.create_rectangle(0, 0, largura, altura, fill=COR_TABULEIRO, outline="")
    vencedoras = vencedoras or []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x1 = MARGEM + coluna * TAMANHO_CELULA + 8
            y1 = MARGEM + linha * TAMANHO_CELULA + 8
            x2 = x1 + TAMANHO_CELULA - 16
            y2 = y1 + TAMANHO_CELULA - 16
            valor = tabuleiro[linha][coluna]
            cor = CORES.get(valor, COR_VAZIA)
            if (linha, coluna) in vencedoras:
                canvas.create_oval(x1, y1, x2, y2, fill=cor, outline=COR_DESTAQUE, width=5)
            else:
                canvas.create_oval(x1, y1, x2, y2, fill=cor, outline="#000000", width=2)
                if valor != 0:
                    canvas.create_oval(x1 + 12, y1 + 10, x1 + 26, y1 + 22,
                                       fill="#ffffff", outline="", stipple="gray50")


def main():
    estado = {"tabuleiro": criar_tabuleiro(), "jogador": 1, "fim": False}

    window = tk.Tk()
    window.title("Connect Four - Quatro em Linha")
    window.configure(bg=COR_FUNDO)
    window.resizable(False, False)

    titulo = tk.Label(window, text="CONNECT FOUR", font=("Arial", 22, "bold"),
                      fg="white", bg=COR_FUNDO)
    titulo.pack(pady=(10, 0))

    turno = tk.Label(window, font=("Arial", 14, "bold"), bg=COR_FUNDO)
    turno.pack(pady=5)

    frame_botoes = tk.Frame(window, bg=COR_FUNDO)
    frame_botoes.pack()
    botoes = []
    for c in range(COLUNAS):
        b = tk.Button(frame_botoes, text="▼", font=("Arial", 14, "bold"), width=4,
                      command=lambda col=c: jogar(col))
        b.grid(row=0, column=c, padx=(MARGEM if c == 0 else 6, 6))
        botoes.append(b)

    window.canvas = tk.Canvas(window,
                              width=COLUNAS * TAMANHO_CELULA + 2 * MARGEM,
                              height=LINHAS * TAMANHO_CELULA + 2 * MARGEM,
                              bg=COR_TABULEIRO, highlightthickness=0)
    window.canvas.pack(padx=15, pady=5)

    reiniciar = tk.Button(window, text="Reiniciar Jogo", font=("Arial", 12, "bold"),
                          bg="#444444", fg="white", activebackground="#666666",
                          command=lambda: reiniciar_jogo())
    reiniciar.pack(pady=(5, 15))

    def atualizar_turno():
        j = estado["jogador"]
        turno.config(text=f"Vez do {NOMES[j]}", fg=CORES[j])

    def atualizar_botoes():
        for c, b in enumerate(botoes):
            if estado["fim"] or coluna_cheia(estado["tabuleiro"], c):
                b.config(state="disabled")
            else:
                b.config(state="normal")

    def jogar(coluna):
        if estado["fim"]:
            return
        tabuleiro = estado["tabuleiro"]
        jogador = estado["jogador"]

        if inserir_ficha(tabuleiro, coluna, jogador) is None:
            messagebox.showwarning("Coluna cheia", "Essa coluna está cheia! Escolha outra.")
            return

        vencedoras = verificar_vitoria(tabuleiro, jogador)
        desenhar_tabuleiro(window, tabuleiro, vencedoras)

        if vencedoras:
            estado["fim"] = True
            turno.config(text=f"{NOMES[jogador]} venceu!", fg=CORES[jogador])
            atualizar_botoes()
            messagebox.showinfo("Vitória", f"Parabéns! {NOMES[jogador]} venceu!")
            return

        if tabuleiro_cheio(tabuleiro):
            estado["fim"] = True
            turno.config(text="Empate! Tabuleiro cheio.", fg="white")
            atualizar_botoes()
            messagebox.showinfo("Empate", "O tabuleiro está cheio. Deu empate!")
            return

        estado["jogador"] = 2 if jogador == 1 else 1
        atualizar_turno()
        atualizar_botoes()

    def clique_canvas(evento):
        coluna = (evento.x - MARGEM) // TAMANHO_CELULA
        if 0 <= coluna < COLUNAS:
            jogar(coluna)

    def reiniciar_jogo():
        estado["tabuleiro"] = criar_tabuleiro()
        estado["jogador"] = 1
        estado["fim"] = False
        desenhar_tabuleiro(window, estado["tabuleiro"])
        atualizar_turno()
        atualizar_botoes()

    window.canvas.bind("<Button-1>", clique_canvas)

    reiniciar_jogo()
    window.mainloop()


if __name__ == "__main__":
    main()