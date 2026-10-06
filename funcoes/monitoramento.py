import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path
from funcoes.camera_manager import CameraManager
from funcoes.camera_selector import CameraSelector
from funcoes.motion_detector import MotionDetector
from funcoes.video_recorder import VideoRecorder
import sys
from pathlib import Path


def caminho_recurso(nome):
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent

    return base / "icones" / nome


class Monitoramento(ctk.CTk):

    def __init__(self):

        super().__init__()
        
        self.configure(fg_color="#000000")
        
        caminho_icone = caminho_recurso("ec.ico")
        self.iconbitmap(str(caminho_icone))

        self.camera_manager = CameraManager()

        self.motion_detector = MotionDetector(
            threshold=30,
            area_minima=500,
            tempo_sem_movimento=3
        )

        self.video_recorder = VideoRecorder()

        self.camera_indisponivel = False
        self.procurando_camera = False
        
        caminho_icone_camera = caminho_recurso( "camera.png" )

        self.icone_camera = Image.open(
            caminho_icone_camera
        )

        self.icone_camera = Image.open(
            caminho_icone
        ).convert("RGBA")

        self.icone_camera = self.icone_camera.resize(
            (28, 28),
            Image.Resampling.LANCZOS
        )

        self.icone_camera_tk = ImageTk.PhotoImage(
            self.icone_camera
        )

        self.title("Monitoramento")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        self.camera_selector = None

        self.criar_interface()

        self.cameras_disponiveis = (
            self.camera_manager.detectar_cameras()
        )
        if self.cameras_disponiveis:
            self.camera_index = (
                self.cameras_disponiveis[0]
            )
            self.abrir_camera(
                self.camera_index
            )
        else:
            self.camera_index = None

        self.atualizar_camera()

    def mostrar_sem_camera(self):

        if self.camera_indisponivel:
            return

        self.camera_indisponivel = True

        self.video_canvas.delete("video")
        self.video_canvas.delete("sem_camera")

        largura = self.video_canvas.winfo_width()
        altura = self.video_canvas.winfo_height()

        if largura <= 1:
            largura = 800

        if altura <= 1:
            altura = 600

        self.video_canvas.create_text(
            largura / 2,
            altura / 2,
            text="NENHUMA CÂMERA DISPONÍVEL",
            fill="white",
            font=("Arial", 24, "bold"),
            anchor="center",
            tags="sem_camera"
        )
    
    def remover_aviso_sem_camera(self):

        if not self.camera_indisponivel:
            return

        self.camera_indisponivel = False

        self.video_canvas.delete(
            "sem_camera"
        )
    
    def criar_interface(self):

        self.video_canvas = ctk.CTkCanvas(
            self,
            bg="#000000",
            highlightthickness=0,
            borderwidth=0
        )

        self.video_canvas.pack(
            fill="both",
            expand=True
        )

        # =========================
        # BOTÃO DA CÂMERA
        # =========================

        self.criar_botao_camera()

        # =========================
        # ATUALIZAR POSIÇÃO
        # =========================

        self.video_canvas.bind(
            "<Configure>",
            self.atualizar_botao_camera
        )

    def abrir_camera(self, indice):

        sucesso = self.camera_manager.abrir(indice)

        if not sucesso:

            print(
                f"Não foi possível abrir a câmera {indice}."
            )

            return

        self.camera_index = indice

        self.motion_detector.resetar()

    def atualizar_camera(self):

        # =====================================================
        # 1. VERIFICAR SE EXISTE UMA CÂMERA ABERTA
        # =====================================================

        if not self.camera_manager.esta_aberta():

            self.mostrar_sem_camera()

            self.after(
                1000,
                self.atualizar_camera
            )

            return

        # =====================================================
        # 2. LER FRAME
        # =====================================================

        frame = self.camera_manager.ler_frame()

        # =====================================================
        # 3. CÂMERA PERDEU CONEXÃO
        # =====================================================

        if frame is None:

            print("Câmera perdeu conexão.")

            if self.video_recorder.gravando:
                self.video_recorder.parar()

            self.camera_manager.fechar()

            self.motion_detector.resetar()

            self.mostrar_sem_camera()

            self.after(
                1000,
                self.atualizar_camera
            )

            return

        # =====================================================
        # 4. CÂMERA FUNCIONANDO
        # =====================================================

        self.remover_aviso_sem_camera()

        movimento = self.motion_detector.detectar(
            frame
        )

        self.controlar_gravacao(
            frame,
            movimento
        )

        # =====================================================
        # 5. DESENHAR STATUS
        # =====================================================

        frame_exibicao = self.desenhar_status(
            frame.copy(),
            movimento
        )

        # =====================================================
        # 6. CONVERTER BGR -> RGB
        # =====================================================

        frame_rgb = cv2.cvtColor(
            frame_exibicao,
            cv2.COLOR_BGR2RGB
        )

        imagem_pil = Image.fromarray(
            frame_rgb
        )

        # =====================================================
        # 7. TAMANHO DO CANVAS
        # =====================================================

        largura_area = self.video_canvas.winfo_width()
        altura_area = self.video_canvas.winfo_height()

        if largura_area <= 1 or altura_area <= 1:

            self.after(
                33,
                self.atualizar_camera
            )

            return

        # =====================================================
        # 8. MANTER PROPORÇÃO DA CÂMERA
        # =====================================================

        largura_original = imagem_pil.width
        altura_original = imagem_pil.height

        proporcao = min(
            largura_area / largura_original,
            altura_area / altura_original
        )

        nova_largura = max(
            1,
            int(largura_original * proporcao)
        )

        nova_altura = max(
            1,
            int(altura_original * proporcao)
        )

        imagem_pil = imagem_pil.resize(
            (nova_largura, nova_altura),
            Image.Resampling.LANCZOS
        )

        # =====================================================
        # 9. CONVERTER PARA TK
        # =====================================================

        imagem_tk = ImageTk.PhotoImage(
            imagem_pil
        )

        self.imagem_tk = imagem_tk

        # =====================================================
        # 10. ATUALIZAR VÍDEO
        # =====================================================

        self.video_canvas.delete(
            "video"
        )

        self.video_canvas.create_image(
            largura_area / 2,
            altura_area / 2,
            image=self.imagem_tk,
            anchor="center",
            tags="video"
        )

        # =====================================================
        # 11. BOTÃO DA CÂMERA FICA NA FRENTE
        # =====================================================

        self.video_canvas.tag_raise(
            "camera_button"
        )

        # =====================================================
        # 12. PRÓXIMO FRAME
        # =====================================================

        self.after(
            33,
            self.atualizar_camera
        )
    
    def controlar_gravacao(
        self,
        frame,
        movimento
    ):

        # =========================
        # INICIAR GRAVAÇÃO
        # =========================

        if (
            movimento
            and
            not self.video_recorder.gravando
        ):

            largura = (
                self.camera_manager.largura
            )

            altura = (
                self.camera_manager.altura
            )

            fps = (
                self.camera_manager.fps
            )

            self.video_recorder.iniciar(
                largura,
                altura,
                fps
            )

        # =========================
        # GRAVAR FRAME
        # =========================

        if self.video_recorder.gravando:

            self.video_recorder.gravar_frame(
                frame
            )

        # =========================
        # PARAR GRAVAÇÃO
        # =========================

        if (
            self.video_recorder.gravando
            and
            not movimento
        ):

            self.video_recorder.parar()

    def desenhar_status(
        self,
        frame,
        movimento
    ):

        texto = (
            "MOVIMENTO DETECTADO"
            if movimento
            else "MONITORANDO"
        )

        fonte = cv2.FONT_HERSHEY_SIMPLEX

        escala = 0.6
        espessura = 1

        tamanho_texto, _ = cv2.getTextSize(
            texto,
            fonte,
            escala,
            espessura
        )

        texto_largura = (
            tamanho_texto[0]
        )

        texto_altura = (
            tamanho_texto[1]
        )

        margem = 15

        x = margem

        y = (
            frame.shape[0]
            - margem
        )

        # =========================
        # FUNDO DO STATUS
        # =========================

        padding_x = 12
        padding_y = 8

        x1 = x - padding_x

        y1 = (
            y
            - texto_altura
            - padding_y
        )

        x2 = (
            x
            + texto_largura
            + padding_x
        )

        y2 = y + padding_y

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (x1, y1),
            (x2, y2),
            (30, 30, 30),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.65,
            frame,
            0.35,
            0,
            frame
        )

        # =========================
        # TEXTO
        # =========================

        cv2.putText(
            frame,
            texto,
            (x, y),
            fonte,
            escala,
            (255, 255, 255),
            espessura,
            cv2.LINE_AA
        )

        return frame

    def criar_botao_camera(self):

        self.botao_camera_window = None

        self.video_canvas.bind(
            "<Button-1>",
            self.clique_camera
        )

        self.video_canvas.bind(
            "<Motion>",
            self.movimento_mouse
        )
   
    def atualizar_botao_camera(self, event=None):

        largura = self.video_canvas.winfo_width()

        if largura <= 1:
            return

        # =========================
        # CONFIGURAÇÕES
        # =========================

        tamanho = 50
        margem = 15

        x1 = largura - margem - tamanho
        y1 = margem

        x2 = x1 + tamanho
        y2 = y1 + tamanho

        # =========================
        # APAGAR BOTÃO ANTERIOR
        # =========================

        self.video_canvas.delete(
            "camera_button"
        )

        # =========================
        # QUADRADO AZUL
        # =========================

        self.video_canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="#680202",
            outline="",
            tags="camera_button"
        )

        # =========================
        # ÍCONE
        # =========================

        self.video_canvas.create_image(
            x1 + tamanho / 2,
            y1 + tamanho / 2,
            image=self.icone_camera_tk,
            anchor="center",
            tags="camera_button"
        )

        # =========================
        # DEIXAR NA FRENTE
        # =========================

        self.video_canvas.tag_raise(
            "camera_button"
        )

    def movimento_mouse(self, event):

        largura = self.video_canvas.winfo_width()

        tamanho = 50
        margem = 15

        x1 = largura - margem - tamanho
        y1 = margem

        x2 = x1 + tamanho
        y2 = y1 + tamanho

        dentro = (
            x1 <= event.x <= x2
            and
            y1 <= event.y <= y2
        )

        if dentro:

            self.video_canvas.configure(
                cursor="hand2"
            )

        else:

            self.video_canvas.configure(
                cursor=""
            )

    def clique_camera(self, event):

        if self.camera_selector is not None:
            return

        largura = (
            self.video_canvas.winfo_width()
        )

        tamanho = 50
        margem = 15

        x1 = (
            largura
            - margem
            - tamanho
        )

        y1 = margem

        x2 = x1 + tamanho
        y2 = y1 + tamanho

        if (
            x1 <= event.x <= x2
            and
            y1 <= event.y <= y2
        ):

            self.abrir_seletor_camera()    

    def abrir_seletor_camera(self):

        if self.camera_selector is not None:
            return

        self.camera_selector = CameraSelector(
            self,
            self.camera_manager,
            self.camera_index,
            self.selecionar_camera
        )

    def selecionar_camera(self, indice):

        # =========================
        # PARAR GRAVAÇÃO
        # =========================

        if self.video_recorder.gravando:

            self.video_recorder.parar()

        # =========================
        # ABRIR NOVA CÂMERA
        # =========================

        self.abrir_camera(indice)

    def fechar(self):

        # =========================
        # PARAR GRAVAÇÃO
        # =========================

        if self.video_recorder.gravando:

            self.video_recorder.parar()

        # =========================
        # FECHAR CÂMERA
        # =========================

        self.camera_manager.fechar()

        # =========================
        # FECHAR JANELA
        # =========================

        self.destroy()