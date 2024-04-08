import cv2
import paho.mqtt.client as mqtt
import qrcode


# Função de callback para conexão ao broker MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker with "+str(reason_code))
    else:
        print("Failed to connect to MQTT broker with "+str(reason_code))


def on_message(client, userdata, msg):
    pass

#mqtt_broker =   # Endereço do broker MQTT
cap = cv2.VideoCapture(0)  # Inicializa a captura de vídeo da webcam
#cap = cv2.VideoCapture("10.7.220.153:81")  # LARS

# Inicializa o cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect  # Define a função de callback para conexão
# client.on_publish = on_publish  # Define a função de callback para publicação
client.on_message = on_message

# Conecta ao broker MQTT
client.connect("10.7.220.187", 1883)
client.loop_start()

qc = qrcode.qrcode()
qc.setQrDimensions(0.075, 0.075)
qc.setQrOperation("RT")
dec = list()
while True:
    ret, frame = cap.read()  # Captura um frame da webcam
    if ret:
        dec = qc.detectAndDecode(frame, ret)
        if (dec != -1):
            msg = f'{{"r":{dec[0,0]},"theta":{dec[0,1]},"id":{dec[0,2]}}}'
            client.publish('slam/observation', msg)

    # #cv2.imshow("Ler QR:", frame)
    # # Ao clicar "ESC", encerra o programa
    if cv2.waitKey(1) == 27:
        break