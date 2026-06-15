FlowVolume: Interface NUI de Controle de Áudio
O FlowVolume é um projeto de Visão Computacional que permite controlar o volume principal do Windows através de gestos manuais capturados pela webcam, eliminando a necessidade de interação física com o teclado ou mouse.

🚀 Como funciona
O sistema utiliza Inteligência Artificial para mapear a anatomia da mão humana em tempo real. Ao calcular a distância geométrica entre o polegar (nó 4) e o indicador (nó 8), o software converte essa variação espacial em um sinal de controle para o driver de áudio do sistema operacional.

🛠 Tecnologias Utilizadas
Python: Linguagem principal do projeto.

OpenCV: Captura e processamento de frames de vídeo.

CVZone / MediaPipe: Motor de IA para detecção de pontos de referência da mão.

Pycaw: Interface de baixo nível para automação do Mixer de áudio do Windows.

NumPy: Processamento matemático para normalização e mapeamento linear de dados.
