import cv2
import paho.mqtt.client as mqtt
from qr_code_ready import qrcode


# Função de callback para conexão ao broker MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker with "+str(reason_code))
        client.publish('robot/imresp', "READY")

    else:
        print("Failed to connect to MQTT broker with "+str(reason_code))


def on_message(client, userdata, msg):
    pass

#mqtt_broker =   # Endereço do broker MQTT
#cap = cv2.VideoCapture(0)  # Inicializa a captura de vídeo da webcam
#cap = cv2.VideoCapture("http://10.0.0.101:81/")  # SlamNet
#cap = cv2.VideoCapture("http://10.7.220.153:81/")  # LARS
cap = cv2.VideoCapture("http://10.7.220.159:81/")

if not cap.isOpened():
    print("Cam não abriu!!")

# Inicializa o cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect  # Define a função de callback para conexão
# client.on_publish = on_publish  # Define a função de callback para publicação
client.on_message = on_message

# Conecta ao broker MQTT
client.connect("10.7.220.187", 1883)
#client.connect("test.mosquitto.org", 1883)
client.loop_start()

qc = qrcode()
qc.setQrDimensions(0.07, 0.07)
qc.setQrOperation("RT_LABEL")

while True:
    #print(cap.get(cv2.CAP_PROP_FPS))

    ret, frame = cap.read()  # Captura um frame da webcam
    if ret:
        ret, dec = qc.detectAndDecode(frame, ret)

        if (ret != -1 and ret != 0 and qc.valor != -1):
            match qc.operation:
                case  "RT_ID":
                    msg = f'{{"r":{dec[0]},"theta":{dec[1]},"id":{dec[2]}}}'
                    client.publish('robot/observation', msg)
                case "RT_LABEL":
                    print("Detectou qr :", dec[2])
                    msg = f'{{"r":{dec[0]},"theta":{dec[1]},"label":"{dec[2]}"}}'
                    client.publish('robot/observation', msg)
                case "RT_ID_LABEL":
                    msg = f'{{"r":{dec[0]},"theta":{dec[1]},"id":{dec[2]}, "label":"{dec[3]}"}}'
                    client.publish('robot/observation', msg)
                case "RT":
                    msg = f'{{"r":{dec[0]},"theta":{dec[1]}}}'
                    client.publish('robot/observation', msg)
                case "ID_LABEL":
                    msg = f'{{"id":{dec[0]}, "label":{dec[1]}}}'
                    client.publish('robot/observation', msg)
                case _:
                    msg = f'{{"r":{dec[0]},"theta":{dec[1]},"id":{dec[2]}}}'
                    client.publish('robot/observation', msg)
        else:
            msg = f'{{"r":{dec[0]},"theta":{dec[1]},"label":{-1}}}'
            client.publish('robot/observation', msg)
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
