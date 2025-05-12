from models.users import User, db

class UserService:
    """Classe de serviço para manipulação de dados relacionados a usuários.

    Responsável por intermediar a comunicação entre os controladores e o modelo User.
    """

    @staticmethod
    def get_all_users():
        """Busca todos os usuários no banco de dados.

        Returns:
            list: Lista de objetos User.
        """
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Busca um usuário específico pelo ID.

        Args:
            user_id (int): ID do usuário.

        Returns:
            User | None: Objeto User se encontrado, caso contrário None.
        """
        return User.query.get(user_id)

    @staticmethod
    def create_user(nome, email, ativo):
        """Cria e salva um novo usuário no banco de dados.

        Args:
            nome (str): Nome do usuário.
            email (str): E-mail do usuário.
            ativo (int): Status (0 = inativo, 1 = ativo).

        Returns:
            User: Usuário criado.
        """
        user = User(nome=nome, email=email, ativo=ativo)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user, nome, email, ativo):
        """Atualiza os dados de um usuário existente.

        Args:
            user (User): Objeto usuário a ser atualizado.
            nome (str): Novo nome.
            email (str): Novo email.
            ativo (int): Novo status (0 ou 1).

        Returns:
            User: Objeto atualizado.
        """
        user.nome = nome
        user.email = email
        user.ativo = ativo
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        """Remove um usuário do banco de dados.

        Args:
            user (User): Objeto usuário a ser deletado.
        """
        db.session.delete(user)
        db.session.commit()