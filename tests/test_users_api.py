import requests

BASE_URL = "http://127.0.0.1:5000"
created_user_id = None

def test_get_all_users():
    """
    Testa a listagem de todos os usuários.
    
    Verifica se a resposta retorna status 200 e se o conteúdo é uma lista.
    """
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    """
    Testa a criação de um novo usuário com dados válidos.

    Salva o ID retornado para ser usado nos testes seguintes.
    """
    global created_user_id
    payload = {
        "nome": "João Silva",
        "email": "joao@example.com",
        "ativo": 1
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == payload["nome"]
    assert data["email"] == payload["email"]
    assert data["ativo"] == payload["ativo"]
    created_user_id = data["id"]


def test_create_user_without_name():
    """
    Testa a criação de um usuário sem o campo 'nome'.

    Espera-se que a API retorne erro 400 e mensagem indicando erro no nome.
    """
    payload = {
        "email": "sem_nome@example.com",
        "ativo": 1
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
    assert "nome" in response.text.lower()


def test_create_user_with_empty_name():
    """
    Testa a criação de um usuário com 'nome' vazio.

    Espera-se erro 400 com indicação de erro no nome.
    """
    payload = {
        "nome": "",
        "email": "nome_vazio@example.com",
        "ativo": 1
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
    assert "nome" in response.text.lower()


def test_create_user_without_email():
    """
    Testa a criação de um usuário sem o campo 'email'.

    Espera-se erro 400 e mensagem mencionando ausência de email.
    """
    payload = {
        "nome": "Usuário Sem Email",
        "ativo": 1
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
    assert "email" in response.text.lower()


def test_create_user_with_duplicate_email():
    """
    Testa a criação de um usuário com e-mail já cadastrado.

    Espera-se erro 400 por violação de unicidade do e-mail.
    """
    payload = {
        "nome": "Duplicado",
        "email": "joao@example.com",  # Mesmo e-mail usado anteriormente
        "ativo": 1
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
    assert "email" in response.text.lower()


def test_get_user_by_id():
    """
    Testa a recuperação de um usuário pelo ID criado anteriormente.

    Verifica se os campos esperados estão presentes e corretos.
    """
    global created_user_id
    response = requests.get(f"{BASE_URL}/users/{created_user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_user_id
    assert "nome" in data
    assert "email" in data
    assert "ativo" in data


def test_update_user():
    """
    Testa a atualização de um usuário existente.

    Verifica se os dados são atualizados corretamente.
    """
    global created_user_id
    updated_data = {
        "nome": "João Atualizado",
        "email": "joao_atualizado@example.com",
        "ativo": 0
    }
    response = requests.put(f"{BASE_URL}/users/{created_user_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == updated_data["nome"]
    assert data["email"] == updated_data["email"]
    assert data["ativo"] == updated_data["ativo"]


def test_delete_user():
    """
    Testa a exclusão de um usuário pelo ID.

    Verifica se a exclusão retorna status 204 e se o usuário não é mais acessível.
    """
    global created_user_id
    response = requests.delete(f"{BASE_URL}/users/{created_user_id}")
    assert response.status_code == 204

    response = requests.get(f"{BASE_URL}/users/{created_user_id}")
    assert response.status_code == 404