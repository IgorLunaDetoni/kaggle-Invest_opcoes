# Função para obter dados da API e colocar em um DataFrame
import requests
import pandas as pd


def obter_dados_ticker(symbol):
    #Falta Criptografar o access token
    access_token = "liI5KaCPVj8vCC4vkEpckrVfVPDPKwGyoGra5DcBAHr8+V6tFJErH7H4417kQKOA--XRlwUWiYITbTp6sJBo9jeQ==--OGM3MmQwMmVjMGM1YjgxMDM0MzM2YTIzYTZiZDQzNzk="
    url = f"https://api.oplab.com.br/v3/market/options/{symbol}"
    headers = {
        "Access-Token": access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados = response.json()
        df = pd.DataFrame(dados)
        return df
    elif response.status_code == 403:
        print(f"Erro ao obter dados da API para o símbolo {symbol}. Código de status: 403 - Acesso proibido. Verifique suas credenciais e permissões.")
    else:
        print(f"Erro ao obter dados da API para o símbolo {symbol}. Código de status: {response.status_code}")
    return None

# AJEITAR O CODIGO DO LUCAS QUANDO ELE COLOCAR A API NO AR
# Definição da classe ativo
class Ativo:
    def __init__(self, strike, daysLeft, prize):
        self.strike = strike
        self.daysLeft = daysLeft
        self.prize = prize

# Criação de instâncias da classe Ativo para cada opção
#option1 = Ativo(ticker["strike"], ticker["daysLeft"], ticker["prize"])
#option2 = Ativo(ticker2["strike"], ticker2["daysLeft"], ticker2["prize"])

# Função principal para a lógica de decisão
def mainLogic(option1, option2):
    difStrikes = option2.strike - option1.strike  # Diferença entre os strikes
    spread = option1.prize - option2.prize  # Diferença entre os prêmios
    if difStrikes > spread:
        if option2.strike < minValue:
            if option1.daysLeft <= 5:
                return f"Uma trava de alta comprando o ativo no strike {option1.strike} e vendendo a um strike {option2.strike}"
    return "Condição não atendida para a estratégia de trava de alta"











##### Fazer um script que procure em cada tabela e compare as opções e sua dif de strikes - a dif do spread(Premio), com menos de 5 dias para o dia atual
# 