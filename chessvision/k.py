import cv2
from ultralytics import YOLO

modelo = YOLO("best.pt")

imagem = "teste4.jpg"

img = cv2.imread(imagem)

resultados = modelo(img)

resultados[0].show() 

