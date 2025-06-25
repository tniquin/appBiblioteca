
import requests

def post_livro(titulo, autor, isbn, resumo):
    url = f"http://192.168.1.83:5000/cadastrar/livro"
    newLivro = {"titulo": titulo,
                "autor": autor,
                "isbn": isbn,
                "resumo": resumo}
    reponse_post = requests.post(url, json=newLivro)
    if reponse_post.status_code == 201:
        dados_post = reponse_post.json()
        print(f"Livro cadastrado: \n{dados_post}")
        return dados_post
    else:
        print(f"ERRO: {reponse_post.status_code}")
        print(f"ERRO: {reponse_post.json()}")

def post_user(nome, cpf, endereco):
    url = f"http://192.168.1.83:5000/cadastrar/usuario"
    newUser = {
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
    }
    response_post = requests.post(url, json=newUser)
    if response_post.status_code == 201:
        dados_post = response_post.json()
        print(f"Usuario cadastrado: \n{dados_post}")
        return dados_post
    else:
        print(f"ERRO: {response_post.status_code}")
        print(response_post.text)  # ← Mostra o motivo do erro
        return {"error": response_post.text}


def post_emprestimo(id_livro, id_usuario):
    url = "http://192.168.1.83:5000/cadastrar/emprestimo"
    newEmprestimo = {
        "id_livro": id_livro,
        "id_usuario": id_usuario,
    }
    print("Enviando dados:", newEmprestimo)
    response_post = requests.post(url, json=newEmprestimo)
    print("Resposta:", response_post.status_code, response_post.text)
    if response_post.status_code == 201:
        dados_post = response_post.json()
        print(f"Empréstimo cadastrado: \n{dados_post}")
        return dados_post
    else:
        print(f"ERRO: {response_post.status_code} - {response_post.text}")
        return None


def get_users():
    url = f"http://192.168.1.83:5000/usuarios"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Usuarios cadastrados: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_livros():
    url = "http://192.168.1.83:5000/livros"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Livros cadastrados: \n {dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")
# get_livros()
def get_user(id):
    url = f"http://192.168.1.83:5000/get/usuarios/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Usuario cadastrado: \n{dados_get}")
        return  dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_livro(id):
    url = f"http://192.168.1.83:5000/get/livros/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Livro cadastrado: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_emprestimo(id):
    url = f"http://192.168.1.83:5000/emprestimos/usuario/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Emprestimo cadastrado: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_emprestimos():
    url = f"http://192.168.1.83:5000/emprestimos"
    response_get = requests.get(url)

    if response_get.status_code == 200:
        dados_get = response_get.json()
        print(f"Emprestimos cadastrados: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {response_get.status_code}")

def get_status_livro(id):
    url = f"/status/livros/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Status do livro[{dados_get['titulo']}: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")



def put_user(id, nome, cpf, endereco, status_user):
    dados = {
        "id": id,
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
        "status_user": status_user
    }
    print("Dados enviados no PUT:", dados)
    # enviar a requisição HTTP aqui, por exemplo:
    response = requests.put(f"http://192.168.1.83:5000/editar/usuario/{id}", json=dados)
    print("Resposta:", response.status_code, response.text)
    return response.json()


def put_livro(id, titulo, autor, isbn, resumo, status_livro):
    url = f"http://192.168.1.83:5000/editar/livro/{id}"
    payload = {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "resumo": resumo,
        "status_livro": status_livro  # Nome da chave conforme backend espera
    }

    print("Enviando PUT para", url)
    print("Payload:", payload)

    response = requests.put(url, json=payload)
    print("Status_code:", response.status_code)
    print("Resposta do Servidor:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        return None  # Retorna None para indicar falha


def put_emprestimo(id, status_emprestimo):
    url = f"http://192.168.1.83:5000/status/movimentacao/{id}"
    payload = {"status_emprestimo": status_emprestimo}

    response_put = requests.put(url, json=payload)

    if response_put.status_code == 200:
        dados_put = response_put.json()
        print(f"Empréstimo atualizado: \n{dados_put}")
        return dados_put
    else:
        print(f"ERRO: {response_put.status_code}")
        print(response_put.json())
        return None

