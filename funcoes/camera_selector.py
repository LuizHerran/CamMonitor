import customtkinter as ctk


class CameraSelector:

    def __init__(
        self,
        parent,
        camera_manager,
        camera_atual,
        ao_selecionar
    ):
        self.parent = parent
        self.camera_manager = camera_manager
        self.camera_atual = camera_atual
        self.ao_selecionar = ao_selecionar

        self.janela = None
        self.lista_cameras = []
        self.after_id = None

        self.criar_janela()
        self.atualizar_lista()

    def criar_janela(self):

        self.janela = ctk.CTkFrame(
            self.parent,
            width=380,
            height=400,
            corner_radius=0,
            fg_color="#050505",
            border_width=3,
            border_color="#750000"
        )

        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.janela.pack_propagate(False)

        # Título
        self.titulo = ctk.CTkLabel(
            self.janela,
            text="Selecionar câmera",
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        )

        self.titulo.pack(
            pady=(22, 4)
        )

        # Quantidade de câmeras
        self.contador = ctk.CTkLabel(
            self.janela,
            text="Procurando câmeras...",
            font=("Arial", 12),
            text_color="#BDBDBD"
        )

        self.contador.pack(
            pady=(0, 15)
        )

        # Área da lista
        self.lista = ctk.CTkFrame(
            self.janela,
            fg_color="transparent"
        )

        self.lista.pack(
            fill="both",
            expand=True,
            padx=20
        )

        # Botão cancelar
        self.cancelar = ctk.CTkButton(
            self.janela,
            text="Cancelar",
            height=38,
            corner_radius=10,
            fg_color="#880000",
            hover_color="#C90202",
            border_width=1,
            border_color="#FDFDFD",
            text_color="#DDDDDD",
            font=("Arial", 12),
            command=self.fechar
        )

        self.cancelar.pack(
            fill="x",
            padx=24,
            pady=(10, 20)
        )

    def atualizar_lista(self):

        if self.janela is None:
            return

        # Detecta novamente as câmeras
        cameras = self.camera_manager.detectar_cameras()

        # Verifica se a lista mudou
        if cameras != self.lista_cameras:

            self.lista_cameras = cameras

            self.recriar_lista()

        # Atualiza novamente daqui a 2 segundos
        self.after_id = self.janela.after(
            2000,
            self.atualizar_lista
        )

    def recriar_lista(self):

        # Remove os cartões antigos
        for widget in self.lista.winfo_children():
            widget.destroy()

        quantidade = len(self.lista_cameras)

        # Atualiza contador
        if quantidade == 0:

            self.contador.configure(
                text="0 câmeras identificadas no sistema"
            )

            mensagem = ctk.CTkLabel(
                self.lista,
                text="Nenhuma câmera encontrada.\n\n"
                     "Conecte uma câmera ao computador\n"
                     "para que ela apareça aqui.",
                font=("Arial", 13),
                text_color="#FFFFFF",
                justify="center"
            )

            mensagem.pack(
                expand=True
            )

            return

        if quantidade == 1:
            texto = "1 câmera identificada no sistema"
        else:
            texto = f"{quantidade} câmeras identificadas no sistema"

        self.contador.configure(
            text=texto
        )

        # Cria os botões
        for indice in self.lista_cameras:

            selecionada = indice == self.camera_atual

            if selecionada:
                texto = f"●  Câmera {indice + 1}  •  ATIVA"
                cor_fundo = "#FF0000"
                cor_hover = "#FD2626"
            else:
                texto = f"○  Câmera {indice + 1}  •  Selecionar"
                cor_fundo = "#252525"
                cor_hover = "#333333"

            botao = ctk.CTkButton(
                self.lista,
                text=texto,
                height=52,
                corner_radius=11,
                fg_color=cor_fundo,
                hover_color=cor_hover,
                border_width=1,
                border_color="#750000",
                text_color="#FFFFFF",
                font=("Arial", 13, "bold" if selecionada else "normal"),
                anchor="w",
                command=lambda i=indice: self.selecionar(i)
            )

            botao.pack(
                fill="x",
                pady=5
            )

    def selecionar(self, indice):

        if indice != self.camera_atual:

            self.ao_selecionar(indice)

        self.fechar()

    def fechar(self):
        if self.after_id is not None:
            try:
                self.janela.after_cancel(self.after_id)
            except Exception:
                pass

            self.after_id = None

        if self.janela is not None:
            self.janela.destroy()
            self.janela = None

        self.parent.camera_selector = None