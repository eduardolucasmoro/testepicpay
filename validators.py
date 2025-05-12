import re

class ValidationError(Exception):
    """
    Exceção personalizada para erros de validação de dados do usuário.
    
    Attributes:
        message (str): Lista de mensagens de erro.
    """
    pass


class UsuarioValidator:
    """
    Classe responsável por validar os dados de entrada de usuários.

    Attributes:
        MAX_NOME (int): Tamanho máximo permitido para o campo 'nome'.
        MAX_EMAIL (int): Tamanho máximo permitido para o campo 'email'.
        existing_emails (set): Conjunto de e-mails já existentes no sistema.
    """

    MAX_NOME = 200
    MAX_EMAIL = 150

    def __init__(self, existing_emails=None):
        """
        Inicializa o validador com uma lista de e-mails já existentes.

        Args:
            existing_emails (list, optional): Lista de e-mails cadastrados para validação.
        """
        self.existing_emails = set(existing_emails or [])

    def validar(self, dados, method):
        """
        Valida os dados fornecidos de acordo com regras.

        Args:
            dados (dict): Dicionário com os dados do usuário (nome, email, ativo).
            method (str): Método HTTP da requisição (ex: 'POST' ou 'PUT').

        Raises:
            ValidationError: Caso algum dos campos seja inválido.
        """
        erros = []

        nome = dados.get("nome")
        email = dados.get("email")
        ativo = dados.get("ativo")

        print(f"Metodo-> {method}")

        if not nome or not nome.strip():
            erros.append("O campo 'nome' é obrigatório.")
        elif len(nome.strip()) > self.MAX_NOME:
            erros.append(f"O campo 'nome' deve ter no máximo {self.MAX_NOME} caracteres.")

        if not email or not email.strip():
            erros.append("O atributo 'email' é obrigatório")
        elif len(email.strip()) > self.MAX_EMAIL:
            erros.append(f"O campo 'email' deve ter no máximo {self.MAX_EMAIL} caracteres.")
        elif not self._email_valido(email):
            erros.append("O campo 'email' deve ser um e-mail válido.")
        elif (email in self.existing_emails and method == 'POST'):
            erros.append("O email informado já está em uso.")

        if "ativo" in dados and ativo not in (0, 1):
            erros.append("O campo 'ativo' deve ser 0 - Inativo ou 1 - Ativo.")

        if erros:
            raise ValidationError(erros)

    def _email_valido(self, email):
        """
        Verifica se o e-mail possui um formato válido.

        Args:
            email (str): Endereço de e-mail a ser validado.

        Returns:
            bool: True se o e-mail for válido, False caso contrário.
        """
        regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(regex, email.strip()) is not None