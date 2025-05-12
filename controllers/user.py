from flask import request, jsonify, make_response
from services.user_service import UserService
from validators import UsuarioValidator, ValidationError

class UserController:
    """Controlador de requisições HTTP para operações com usuários.

    Recebe requisições GET, POST, PUT e DELETE e realiza as validações necessárias e persistência dos dados.
    """

    @staticmethod
    def users():
        """Manipula requisições GET e POST para o endpoint /users.

        GET:
            Retorna uma lista de todos os usuários cadastrados.

        POST:
            Cria um novo usuário com base nos dados fornecidos no corpo da requisição.

        Returns:
            Response: Objeto com status e mensagem ou dados do(s) usuário(s).
        """
        if request.method == 'GET':
            users = UserService.get_all_users()
            user_list = [{"id": u.id, "nome": u.nome} for u in users]
            return make_response(jsonify(message="Lista de usuários", data=user_list)), 200

        if request.method == 'POST':
            payload = request.json
            existing_emails = [u.email for u in UserService.get_all_users()]

            validator = UsuarioValidator(existing_emails=existing_emails)
            try:
                validator.validar(payload, request.method)
            except ValidationError as e:
                return jsonify({"erros": e.args[0]}), 400

            user = UserService.create_user(payload['nome'], payload['email'], payload['ativo'])
            return make_response({
                "id": user.id, "nome": user.nome, "email": user.email, "ativo": user.ativo
            }), 201

    @staticmethod
    def user_get_by_id(id):
        """Manipula requisições GET, PUT e DELETE para o endpoint /users/<id>.

        GET:
            Retorna os dados de um usuário específico com base.

        PUT:
            Atualiza os dados do usuário identificado pelo ID.

        DELETE:
            Remove o usuário identificado pelo ID do banco de dados.

        Args:
            id (int): ID do usuário a ser buscado, atualizado ou deletado.

        Returns:
            Response: Objeto com status e mensagem ou dados do usuário.
        """
        if request.method == 'GET':
            user = UserService.get_user_by_id(id)
            if user:
                return jsonify({
                    "id": user.id, "nome": user.nome, "email": user.email, "ativo": user.ativo
                }), 200
            return jsonify(message=f'Id {id} não encontrado na base de dados'), 404

        if request.method == 'PUT':
            payload = request.json
            existing_emails = [u.email for u in UserService.get_all_users()]

            validator = UsuarioValidator(existing_emails=existing_emails)
            try:
                validator.validar(payload, request.method)
            except ValidationError as e:
                return jsonify({"erros": e.args[0]}), 400

            user = UserService.get_user_by_id(id)
            if user:
                user = UserService.update_user(user, payload['nome'], payload['email'], payload['ativo'])
                return jsonify({
                    "id": user.id, "nome": user.nome, "email": user.email, "ativo": user.ativo
                }), 200
            return jsonify(message='Usuário não encontrado na base de dados'), 404

        if request.method == 'DELETE':
            user = UserService.get_user_by_id(id)
            if user:
                UserService.delete_user(user)
                return jsonify(message='Usuário excluído com sucesso'), 204
            return jsonify(message=f'ID {id} não encontrado na base de dados'), 404