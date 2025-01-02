import chess
import chess.engine

def obter_melhor_jogada(notacao):
    caminho_stockfish = r"C:\Users\joaoc\OneDrive\Área de Trabalho\chessvision\stockfish\stockfish-windows-x86-64.exe" 
    engine = chess.engine.SimpleEngine.popen_uci(caminho_stockfish)

    board = chess.Board()

    board.push_san(notacao)

    resultado = engine.play(board, chess.engine.Limit(time=2.0))
    melhor_jogada = resultado.move

    engine.quit()

    return melhor_jogada

# Exemplo de uso
notacao_input = "e2e4"
melhor_jogada = obter_melhor_jogada(notacao_input)
print(f"A melhor jogada do Stockfish após {notacao_input} é: {melhor_jogada}")
