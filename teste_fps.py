import cv2
import time


def testar_camera(
    largura,
    altura,
    fps,
    formato
):
    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    if not camera.isOpened():
        print("Erro ao abrir câmera.")
        return

    camera.set(
        cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(
            *formato
        )
    )

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        largura
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        altura
    )

    camera.set(
        cv2.CAP_PROP_FPS,
        fps
    )

    largura_real = int(
        camera.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    altura_real = int(
        camera.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    fps_informado = camera.get(
        cv2.CAP_PROP_FPS
    )

    contador = 0

    inicio = time.time()

    while time.time() - inicio < 5:

        sucesso, _ = camera.read()

        if sucesso:
            contador += 1

    tempo = time.time() - inicio

    fps_real = contador / tempo

    print(
        f"{formato} | "
        f"{largura_real}x{altura_real} | "
        f"solicitado: {fps} | "
        f"informado: {fps_informado:.2f} | "
        f"real: {fps_real:.2f}"
    )

    camera.release()


print()
print("==========================================")
print(" TESTE DE FORMATOS E RESOLUÇÕES")
print("==========================================")
print()


resolucoes = [
    (320, 240),
    (640, 480),
    (800, 600),
    (1280, 720),
    (1920, 1080)
]

formatos = [
    "MJPG",
    "YUY2"
]


for formato in formatos:

    for largura, altura in resolucoes:

        testar_camera(
            largura,
            altura,
            30,
            formato
        )


print()
print("Teste concluído.")