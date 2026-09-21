from pathlib import Path
import time


def obter_pasta_monitoramento():
    """
    Retorna a pasta principal onde os vídeos
    de monitoramento serão armazenados.
    """

    documentos = Path.home() / "Documents"

    pasta_monitoramento = (
        documentos / "Monitoramento"
    )

    return pasta_monitoramento


def obter_pasta_dia():
    """
    Cria e retorna a pasta correspondente
    ao dia atual.

    Estrutura:

    Monitoramento/
        2026/
            09/
                21/
    """

    agora = time.localtime()

    ano = time.strftime(
        "%Y",
        agora
    )

    mes = time.strftime(
        "%m",
        agora
    )

    dia = time.strftime(
        "%d",
        agora
    )

    pasta_dia = (
        obter_pasta_monitoramento()
        / ano
        / mes
        / dia
    )

    pasta_dia.mkdir(
        parents=True,
        exist_ok=True
    )

    return pasta_dia


def criar_caminho_video():
    """
    Cria o caminho completo para um novo vídeo.

    Exemplo:

    Monitoramento/
        2026/
            09/
                21/
                    movimento_10-35-42.mp4
    """

    agora = time.localtime()

    horario = time.strftime(
        "%H-%M-%S",
        agora
    )

    pasta_dia = obter_pasta_dia()

    nome_video = (
        f"movimento_{horario}.mp4"
    )

    return pasta_dia / nome_video