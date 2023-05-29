import cv2

from qr_code_ready import qrcode

imag = "http://192.168.4.1/capture"
# imag = 0
qq = qrcode()
# print(qq.angulo)
# print(qq.valor)
# print(qq.distancia)
# print(qq.pospxl)


dec = int(input("Manda!"))
while dec == 1:
    cap = cv2.VideoCapture(imag)
    ret, frame = cap.read()
    b = qq.detectAnddecod(frame, ret)
    # print("b:", b)
    if (b == 0):
        print("Qr code identificado mas não Decodificado")
    elif (b == -1):
        print("Qr code não identificado!")
    else:
        print(b)
        print(qq.qr_dict)
    dec = int(input("Manda!"))
