from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Modelo de usuário para a tabela 'users' no banco de dados.

    Representa um usuário da aplicação com os seguintes campos:
    - id: Identificador único.
    - nome: Nome completo do usuário.
    - email: Endereço de e-mail único.
    - ativo: Flag indicando se o usuário está ativo (1) ou inativo (0).
    """

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Integer)

    def __init__(self, nome, email, ativo):
        """
        Inicializa uma instância do modelo User.

        Args:
            nome (str): Nome do usuário.
            email (str): E-mail do usuário (único).
            ativo (int): Indica se o usuário está ativo (1) ou inativo (0).
        """
        self.nome = nome
        self.email = email
        self.ativo = ativo