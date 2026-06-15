import cv2
import math
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# =====================================================================
# 1. CONEXÃO DIRETA COM O DISPOSITIVO MASTER DE ÁUDIO 
# =====================================================================


gerenciador_dispositivos = AudioUtilities.GetDeviceEnumerator()


alto_falante_padrao = gerenciador_dispositivos.GetDefaultAudioEndpoint(0, 1)

interface = alto_falante_padrao.Activate(
    IAudioEndpointVolume._iid_, 23, None
)

volume_master = interface.QueryInterface(IAudioEndpointVolume)

vol_min, vol_max = 0.0, 1.0

# =====================================================================
# 2. CONFIGURAÇÃO DA WEBCAM E DA IA (CVZONE)
# =====================================================================
webcam = cv2.VideoCapture(0)controla
detector_ia = HandDetector(maxHands=1, detectionCon=0.7)

print("--- SISTEMA INICIADO COM SUCESSO! ---")
print("Controlando o Volume Master Geral do Windows.")
print("Mostre a sua mão na câmera. Pressione ESC para fechar.")

# =====================================================================
# 3. LOOP PRINCIPAL
# =====================================================================
while webcam.isOpened():
    sucesso, frame = webcam.read()
    if not sucesso:
        break

    frame = cv2.flip(frame, 1)
    maos, frame = detector_ia.findHands(frame, draw=True)

    if maos:
        mao_detectada = maos[0]
        lista_pontos = mao_detectada["lmList"]
        
        x1, y1 = lista_pontos[4][0], lista_pontos[4][1]
        x2, y2 = lista_pontos[8][0], lista_pontos[8][1]
        
        centro_x, centro_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(frame, (centro_x, centro_y), 8, (0, 0, 255), cv2.FILLED)
        
        distancia = math.hypot(x2 - x1, y2 - y1)
        
        volume_final = np.interp(distancia, [20, 180], [vol_min, vol_max])
        barra_visual = np.interp(distancia, [20, 180], [400, 150])
        porcentagem = np.interp(distancia, [20, 180], [0, 100])
        
        volume_master.SetMasterVolumeLevelScalar(volume_final, None)
        
        if distancia < 25:
            cv2.circle(frame, (centro_x, centro_y), 10, (0, 255, 0), cv2.FILLED)
            
        cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(frame, (50, int(barra_visual)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f'{int(porcentagem)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Controle de Volume com IA", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

webcam.release()
cv2.destroyAllWindows()