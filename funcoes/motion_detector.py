import time

import cv2


class MotionDetector:

    def __init__(
        self,
        threshold=30,
        area_minima=500,
        tempo_sem_movimento=3
    ):
        """
        Configura o detector de movimento.

        threshold:
            Sensibilidade da diferença entre os frames.

        area_minima:
            Área mínima do contorno para ser considerada movimento.

        tempo_sem_movimento:
            Quantos segundos o movimento continua ativo
            após o último movimento real.
        """

        self.threshold = threshold
        self.area_minima = area_minima
        self.tempo_sem_movimento = tempo_sem_movimento

        self.frame_anterior = None
        self.ultimo_movimento = 0

    def detectar(self, frame):
        """
        Analisa um frame e retorna se existe movimento ativo.

        Retorna:
            True  -> movimento detectado/ativo
            False -> sem movimento
        """

        # ==========================================
        # CONVERTER PARA ESCALA DE CINZA
        # ==========================================

        frame_cinza = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # ==========================================
        # REDUZIR RUÍDO DA CÂMERA
        # ==========================================

        frame_cinza = cv2.GaussianBlur(
            frame_cinza,
            (21, 21),
            0
        )

        # ==========================================
        # PRIMEIRO FRAME
        # ==========================================

        if self.frame_anterior is None:

            self.frame_anterior = frame_cinza

            return False

        # ==========================================
        # COMPARAR FRAMES
        # ==========================================

        diferenca = cv2.absdiff(
            self.frame_anterior,
            frame_cinza
        )

        # ==========================================
        # APLICAR THRESHOLD
        # ==========================================

        _, diferenca_threshold = cv2.threshold(
            diferenca,
            self.threshold,
            255,
            cv2.THRESH_BINARY
        )

        # ==========================================
        # AUMENTAR ÁREAS DE DIFERENÇA
        # ==========================================

        diferenca_threshold = cv2.dilate(
            diferenca_threshold,
            None,
            iterations=2
        )

        # ==========================================
        # ENCONTRAR CONTORNOS
        # ==========================================

        contornos, _ = cv2.findContours(
            diferenca_threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        movimento_detectado = False

        # ==========================================
        # VERIFICAR ÁREA DOS CONTORNOS
        # ==========================================

        for contorno in contornos:

            area = cv2.contourArea(
                contorno
            )

            if area > self.area_minima:

                movimento_detectado = True

                break

        # ==========================================
        # ATUALIZAR FRAME ANTERIOR
        # ==========================================

        self.frame_anterior = frame_cinza

        # ==========================================
        # REGISTRAR MOVIMENTO
        # ==========================================

        if movimento_detectado:

            self.ultimo_movimento = time.time()

        # ==========================================
        # MANTER MOVIMENTO ATIVO
        # ==========================================

        movimento_ativo = (
            time.time()
            - self.ultimo_movimento
        ) < self.tempo_sem_movimento

        return movimento_ativo

    def resetar(self):
        """
        Reseta o detector.

        Deve ser chamado quando trocamos de câmera.
        """

        self.frame_anterior = None

        self.ultimo_movimento = 0

    def movimento_ativo(self):
        """
        Verifica se o estado de movimento ainda está ativo.

        Pode ser usado sem processar um novo frame.
        """

        return (
            time.time()
            - self.ultimo_movimento
        ) < self.tempo_sem_movimento