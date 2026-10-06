from pathlib import Path
import time

def obter_pasta_monitoramento():

    video = Path.home() / "Videos"

    pasta_monitoramento = (
        video / "Monitoramento"
    )

    return pasta_monitoramento

def obter_pasta_dia():
    """
    Estrutura:

     Vídeos/
        Ano 2026/
            Mês 10/
                Dia 06/
    """

    agora = time.localtime()

    ano = time.strftime( "Ano %Y", agora )

    mes = time.strftime( "Mês %m", agora )

    dia = time.strftime( "Dia %d", agora )

    pasta_dia = ( obter_pasta_monitoramento() / ano / mes / dia )

    pasta_dia.mkdir( parents=True, exist_ok=True )
    return pasta_dia

def criar_caminho_video():
    """
    Estrutura:

    Monitoramento/
        2026/
            09/
                21/
                    movimento_10h 35m 42s.mp4
    """

    agora = time.localtime()

    horario = time.strftime(
        "%Hh %Mm %Ss ",
        agora
    )

    pasta_dia = obter_pasta_dia()

    nome_video = (
        f"movimento_{horario}.mp4"
    )

    return pasta_dia / nome_video