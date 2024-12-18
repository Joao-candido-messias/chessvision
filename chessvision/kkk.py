import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Função para desenhar um trapézio
def desenhar_trapezio(img, cx, cy, w, h):
    # Diminuir a altura em 3%
    h = int(h * 0.97)  # 97% da altura original

    # Calcular a base superior como 80% da base inferior
    top_width = 0.80 * w  # 80% da largura da base inferior
    half_bottom_width = w / 2
    half_top_width = top_width / 2

    # Ajustar a altura do trapézio para ser 5% acima da borda inferior detectada
    cy_adjusted = int(cy - 0.05 * h)  # Deslocar o centro verticalmente para cima em 5%

    # Calcular as coordenadas dos 4 vértices do trapézio
    top_left = (int(cx - half_top_width), int(cy_adjusted - h / 2))  # topo esquerdo
    top_right = (int(cx + half_top_width), int(cy_adjusted - h / 2))  # topo direito
    bottom_left = (int(cx - half_bottom_width), int(cy_adjusted + h / 2))  # base inferior esquerda
    bottom_right = (int(cx + half_bottom_width), int(cy_adjusted + h / 2))  # base inferior direita

    # Desenhar o trapézio
    pts = np.array([top_left, top_right, bottom_right, bottom_left], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    return top_left, top_right, bottom_left, bottom_right, top_width, w, h, cy_adjusted

# Função para dividir o trapézio em uma matriz 8x8 e desenhar as divisões
def dividir_em_matriz(top_left, top_right, bottom_left, bottom_right, top_width, w, h, img):
    notacao = []  # Lista para armazenar as anotações (notação algébrica)

    # Calcular as linhas horizontais que vão dividir o trapézio em 8 partes
    for i in range(1, 8):
        y = int(top_left[1] + (bottom_left[1] - top_left[1]) * i / 8)
        
        # Interpolar as coordenadas horizontais ao longo da largura do trapézio
        x1 = int(top_left[0] + (bottom_left[0] - top_left[0]) * i / 8)
        x2 = int(top_right[0] + (bottom_right[0] - top_right[0]) * i / 8)

        # Desenhar as linhas horizontais em vermelho
        cv2.line(img, (x1, y), (x2, y), (0, 0, 255), 1)

    # Calcular as linhas verticais que vão dividir o trapézio em 8 partes
    for i in range(1, 8):
        x = int(top_left[0] + (top_right[0] - top_left[0]) * i / 8)
        
        # Calcular as novas posições dos pontos verticais
        y1 = int(top_left[1] + (bottom_left[1] - top_left[1]) * i / 8)
        y2 = int(top_right[1] + (bottom_right[1] - top_right[1]) * i / 8)
        
        # Desenhar as linhas verticais em vermelho
        cv2.line(img, (x, y1), (x, y2), (0, 0, 255), 1)

    # Gerar a notação algébrica para cada célula
    for i in range(8):
        for j in range(8):
            # Calcular as coordenadas (x, y) do centro de cada célula
            x = int(top_left[0] + (bottom_left[0] - top_left[0]) * (i + 0.5) / 8)
            y = int(top_left[1] + (bottom_left[1] - top_left[1]) * (j + 0.5) / 8)

            # Desenhar um ponto vermelho no centro de cada célula
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)  # Ponto vermelho no centro

            # Determinar a notação algébrica (coluna a-h, linha 1-8)
            coluna = chr(ord('a') + i)  # 'a' a 'h'
            linha = 8 - j  # Linha 1 a 8 (invertido)

            # Adicionar a notação à lista
            notacao.append(f"{coluna}{linha}")

    return notacao

# Carregar o modelo treinado (substitua pelo caminho correto do modelo)
modelo = YOLO("best.pt")  # Substitua pelo caminho do seu modelo .pt

# Caminho da imagem
imagem = "teste4.jpg"  # Substitua pelo caminho da sua imagem

# Carregar a imagem
img = cv2.imread(imagem)

# Realizar a detecção de objetos com o modelo YOLO
resultados = modelo(img)

# Obter as caixas delimitadoras e as informações dos objetos
notacao = []  # Lista para armazenar as posições

for resultado in resultados[0].boxes:
    # Coordenadas da caixa delimitadora: centro (cx, cy), largura (w), altura (h)
    cx, cy, w, h = map(int, resultado.xywh[0])  # Obter valores inteiros

    # Verificar se o objeto detectado é um tabuleiro (classe 0)
    if int(resultado.cls[0]) == 0:  # 0 é a classe do tabuleiro (de acordo com a sua lista)
        # Desenhar o trapézio para o tabuleiro
        top_left, top_right, bottom_left, bottom_right, top_width, w, h, cy_adjusted = desenhar_trapezio(img, cx, cy, w, h)
        
        # Dividir o trapézio em uma matriz 8x8 e desenhar as divisões
        notacao = dividir_em_matriz(top_left, top_right, bottom_left, bottom_right, top_width, w, h, img)

# Exibir a notação algébrica no terminal
for posicao in notacao:
    print(posicao)

# Mostrar a imagem com a detecção do tabuleiro, o trapézio, as divisões da matriz 8x8 e os pontos vermelhos
cv2.imshow("Imagem com Detecção do Tabuleiro e Divisões da Matriz", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
