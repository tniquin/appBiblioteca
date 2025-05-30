import requests

def post_livro(titulo, autor, isbn, resumo):
    url = f"http://10.135.232.18:5000/cadastrar/livro"
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

def post_user(nome, cpf, endereco, status):
    url = f"http://10.135.232.18:5000/cadastrar/usuario"
    newUser = {"nome": nome,
                "cpf": cpf,
                "endereco": endereco,
                "status": status}
    reponse_post = requests.post(url, json=newUser)
    if reponse_post.status_code == 201:
        dados_post = reponse_post.json()
        print(f"Usuario cadastrado: \n{dados_post}")
        return dados_post
    else:
        print(f"ERRO: {reponse_post.status_code}")

def post_emprestimo(dataDevolucao, dataEmprestimo, idLivro, idUser):
    url = f"http://10.135.232.18:5000/cadastrar/emprestimo"
    newEmprestimo = {"data_devolucao": dataDevolucao,
                    "data_emprestimo": dataEmprestimo,
                    "id_livro": idLivro,
                    "id_usuario": idUser}
    reponse_post = requests.post(url, json=newEmprestimo)
    if reponse_post.status_code == 201:
        dados_post = reponse_post.json()
        print(f"Emprestimo cadastrado: \n{dados_post}")
        return dados_post
    else:
        print(f"ERRO: {reponse_post.status_code}")

def get_users():
    url = f"http://10.135.232.18:5000/usuarios"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Usuarios cadastrados: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_livros():
    url = "http://10.135.232.18:5000/livros"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Livros cadastrados: \n {dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")
# get_livros()
def get_user(id):
    url = f"http://10.135.232.18:5000/get/usuarios/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Usuario cadastrado: \n{dados_get}")
        return  dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_livro(id):
    url = f"http://10.135.232.18:5000/get/livros/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Livro cadastrado: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_emprestimo(id):
    url = f"http://10.135.232.18:5000/emprestimos/usuario/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Emprestimo cadastrado: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")

def get_emprestimos():
    url = f"http://10.135.232.18:5000/emprestimos"
    response_get = requests.get(url)

    if response_get.status_code == 200:
        dados_get = response_get.json()
        print(f"Emprestimos cadastrados: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {response_get.status_code}")

def get_status_livro(id):
    url = f"http://10.135.232.18:5000/status/livros/{id}"
    reponse_get = requests.get(url)

    if reponse_get.status_code == 200:
        dados_get = reponse_get.json()
        print(f"Status do livro[{dados_get['titulo']}: \n{dados_get}")
        return dados_get
    else:
        print(f"ERRO: {reponse_get.status_code}")



def put_user(id,nome, cpf, endereco, status):
    url = f"http://10.135.232.18:5000/editar/usuario/{id}"
    newUser = {"id": id,
                "nome": nome,
                "cpf": cpf,
                "endereco": endereco,
                "status": status}
    reponse_put = requests.put(url, json=newUser)
    reponse_get = requests.get(url)
    if reponse_put.status_code == 200:
        if reponse_get.status_code == 200:
            user_old = reponse_get.json()
            print(f"usuario antigo cadastrado: \n{user_old}")
        else:
            print(f"ERRO: {reponse_put.status_code}")
        dados_put = reponse_put.json()
        print(f"Usuario atualizado: \n{dados_put}")
        return dados_put
    else:
        print(f"ERRO: {reponse_put.status_code}")

def put_livro(id, titulo, autor, isbn, resumo):
    url = f"http://10.135.232.18:5000/editar/livro/{id}"
    newLivro = {"id": id,
                "titulo": titulo,
                "autor": autor,
                "isbn": isbn.value,
                "resumo": resumo,}
    reponse_put = requests.put(url, json=newLivro)
    reponse_get = requests.get(url)
    if reponse_put.status_code == 200:
        if reponse_get.status_code == 200:
            book_old = reponse_get.json()
            print(f"Livro antigo cadastrado: \n{book_old}")
        else:
            print(f"ERRO: {reponse_put.status_code}")
        dados_put = reponse_put.json()
        print(f"Livro atualizado: \n{dados_put}")
        return dados_put
    else:
        print(f"ERRO: {reponse_put.status_code}")

def put_emprestimo(id, dataDevolucao, dataEmprestimo, idLivro, idUser):
    url = f"http://10.135.232.18:5000/status/movimentacao/{id}"
    newEmprest = {"id": id,
                "dataDevolucao": dataDevolucao,
                "dataEmprestimo": dataEmprestimo,
                "idLivro": idLivro,
                "idUser": idUser}
    reponse_put = requests.put(url, json=newEmprest)
    reponse_get = requests.get(url)
    if reponse_put.status_code == 200:
        if reponse_get.status_code == 200:
            emprestimo_old = reponse_get.json()
            print(f"Emprestimo antigo: \n{emprestimo_old}")
        else:
            print(f"ERRO: {reponse_put.status_code}")
        dados_put = reponse_put.json()
        print(f"Emprestimo atualizado: \n{dados_put}")
        return dados_put
    else:
        print(f"ERRO: {reponse_put.status_code}")