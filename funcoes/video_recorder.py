import time

import cv2

from funcoes.paths import criar_caminho_video


class VideoRecorder:

    def __init__(self):

        self.video = None
        self.caminho_atual = None

        self.fps = 0.0

    @property
    def gravando(self):

        return self.video is not None

    def iniciar(self, largura, altura, fps):

        if self.gravando:
            return False

        # ==========================================
        # VALIDAR FPS
        # ==========================================

        if fps <= 0:
            fps = 15.0

        self.fps = fps

        # ==========================================
        # CRIAR CAMINHO DO VÍDEO
        # ==========================================

        self.caminho_atual = criar_caminho_video()

        # ==========================================
        # CODEC
        # ==========================================

        codec = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        # ==========================================
        # CRIAR GRAVADOR
        # ==========================================

        self.video = cv2.VideoWriter(
            str(self.caminho_atual),
            codec,
            self.fps,
            (largura, altura)
        )

        # ==========================================
        # VERIFICAR SE ABRIU
        # ==========================================

        if not self.video.isOpened():

            self.video.release()

            self.video = None
            self.caminho_atual = None
            self.fps = 0.0

            print(
                "Erro ao iniciar gravação."
            )

            return False

        print(
            f"Gravação iniciada: "
            f"{self.caminho_atual}"
        )

        print(
            f"FPS utilizado na gravação: "
            f"{self.fps:.2f}"
        )

        return True

    def gravar_frame(self, frame):

        if not self.gravando:
            return

        # ==========================================
        # COPIAR FRAME
        # ==========================================

        frame_gravacao = frame.copy()

        # ==========================================
        # DATA E HORA
        # ==========================================

        data_hora = time.strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        fonte = cv2.FONT_HERSHEY_SIMPLEX

        escala = 0.5
        espessura = 1

        tamanho_texto, _ = cv2.getTextSize(
            data_hora,
            fonte,
            escala,
            espessura
        )

        texto_largura = tamanho_texto[0]

        altura, largura = (
            frame_gravacao.shape[:2]
        )

        margem = 10

        posicao_x = (
            largura
            - texto_largura
            - margem
        )

        posicao_y = (
            altura
            - margem
        )

        # ==========================================
        # SOMBRA DO TEXTO
        # ==========================================

        cv2.putText(
            frame_gravacao,
            data_hora,
            (
                posicao_x + 1,
                posicao_y + 1
            ),
            fonte,
            escala,
            (0, 0, 0),
            2,
            cv2.LINE_AA
        )

        # ==========================================
        # TEXTO
        # ==========================================

        cv2.putText(
            frame_gravacao,
            data_hora,
            (
                posicao_x,
                posicao_y
            ),
            fonte,
            escala,
            (255, 255, 255),
            espessura,
            cv2.LINE_AA
        )

        # ==========================================
        # GRAVAR FRAME
        # ==========================================

        self.video.write(
            frame_gravacao
        )

    def parar(self):

        if not self.gravando:
            return

        # ==========================================
        # FINALIZAR VÍDEO
        # ==========================================

        self.video.release()

        self.video = None

        print(
            f"Gravação encerrada: "
            f"{self.caminho_atual}"
        )

        # ==========================================
        # LIMPAR DADOS
        # ==========================================

        self.caminho_atual = None
        self.fps = 0.0