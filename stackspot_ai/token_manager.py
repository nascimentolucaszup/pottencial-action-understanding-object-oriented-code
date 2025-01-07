import requests


class TokenManager:
    """
    Classe para gerenciar o token de acesso, garantindo que ele seja reutilizado e atualizado quando necessário.
    """
    def __init__(self, account_slug, client_id, client_secret):
        self.account_slug = account_slug
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def get_token(self):
        """
        Retorna o token de acesso atual.
        """
        return self.access_token

    def refresh_token(self):
        """
        Atualiza o token de acesso.
        """
        print("Atualizando token de acesso...")
        url = f"https://idm.stackspot.com/{self.account_slug}/oidc/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            print("Token de acesso atualizado com sucesso.")
        else:
            raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")