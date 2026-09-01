import requests


class ServicoCEPError(Exception):
    pass


def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(
            url,
            timeout=5
        )

        response.raise_for_status()

    except requests.Timeout as exc:
        raise ServicoCEPError(
            "A consulta de CEP demorou mais que o esperado."
        ) from exc

    except requests.RequestException as exc:
        raise ServicoCEPError(
            "Não foi possível consultar o serviço de CEP."
        ) from exc

    dados = response.json()

    if dados.get("erro"):
        raise ServicoCEPError(
            "CEP não encontrado."
        )

    return dados