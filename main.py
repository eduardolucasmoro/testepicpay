from flask import Flask, make_response, jsonify, request
from config import Config
from controllers.user import UserController
from models.users import db

class FlaskApp:
    """
    Classe responsável pela execução da aplicação.

    Essa classe inicializa o app, aplica configurações, define rotas, conecta ao banco de dados
    e fornece um método para iniciar o servidor.
    """

    def __init__(self):
        """
        Inicializa a aplicação Flask, carrega as configurações do projeto, 
        registra as rotas e configura o banco de dados.
        """
        # Inicializa o app Flask
        self.app = Flask(__name__)

        # Carrega configurações do objeto Config
        self.app.config.from_object(Config)

        # Desabilita ordenação alfabética automática de chaves JSON
        self.app.json.sort_keys = False

        # Define rotas da API
        self.app.add_url_rule('/users', 'users', UserController.users, methods=['GET', 'POST'])
        self.app.add_url_rule('/users/<int:id>', 'user_get_by_id', UserController.user_get_by_id, methods=['GET', 'DELETE', 'PUT'])

        # Inicializa o banco de dados com o contexto da aplicação
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def run(self):
        """
        Inicia o servidor Flask em modo debug.
        """
        self.app.run(debug=True)


if __name__ == '__main__':
    app = FlaskApp()
    app.run()