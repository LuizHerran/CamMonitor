import cv2
import time


class CameraManager:

    def __init__(self):
        self.camera = None
        self.camera_index = None

        self.largura = 0
        self.altura = 0
        self.fps = 0.0

    def detectar_cameras(self, quantidade=6):

        cameras_disponiveis = []

        for indice in range(quantidade):

            # A câmera que já está aberta não precisa
            # ser aberta novamente para ser testada.
            if (
                indice == self.camera_index
                and self.esta_aberta()
            ):
                cameras_disponiveis.append(indice)
                continue

            camera = cv2.VideoCapture(
                indice,
                cv2.CAP_DSHOW
            )

            if camera.isOpened():

                sucesso, _ = camera.read()

                if sucesso:
                    cameras_disponiveis.append(indice)

            camera.release()

        return cameras_disponiveis

    def abrir(self, indice):

        self.fechar()

        camera = cv2.VideoCapture(
            indice,
            cv2.CAP_DSHOW
        )

        if not camera.isOpened():

            camera.release()
            return False

        self.camera = camera
        self.camera_index = indice

        self.largura = int(
            self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self.altura = int(
            self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        if self.largura <= 0:
            self.largura = 640

        if self.altura <= 0:
            self.altura = 480

        self.fps = self.camera.get(
            cv2.CAP_PROP_FPS
        )

        if self.fps <= 0:
            self.fps = 30.0

        print(
            f"Câmera {indice}: "
            f"{self.largura}x{self.altura} "
            f"FPS: {self.fps:.2f}"
        )

        return True

    def ler_frame(self):

        if not self.esta_aberta():
            return None

        sucesso, frame = self.camera.read()

        if not sucesso:
            return None

        return frame

    def fechar(self):

        if self.camera is not None:

            self.camera.release()

        self.camera = None
        self.camera_index = None

        self.largura = 0
        self.altura = 0
        self.fps = 0.0

    def esta_aberta(self):

        return (
            self.camera is not None
            and self.camera.isOpened()
        )