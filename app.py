from idlelib.configdialog import font_sample_text

import flet as ft
import requests
from flet import *
from flet.core.border_radius import horizontal
from datetime import datetime, timedelta
from api import get_livros, post_livro, get_users, post_user, get_emprestimos, post_emprestimo, put_livro, put_user, put_emprestimo


def main(page: ft.Page):
    page.title = "Exemplos Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667
    editando_livro = False
    livro_editando = {}

    editando_user = False
    user_editando = {}

    editando_emprestimo = False
    emprestimo_editando = {}

    # page.navigation_bar = ft.NavigationBar(
    #     destinations=[
    #         ft.NavigationBarDestination(icon=Icons.BOOK, label="Livros"),
    #         ft.NavigationBarDestination(icon=Icons.PERSON, label="Pessoas"),
    #         ft.NavigationBarDestination(icon=Icons.EMAIL_SHARP, label="Emprestimos"),
    #     ],
    # )

    pagelet = ft.Pagelet(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=Icons.BOOK, label="Livros"),
                ft.NavigationBarDestination(icon=Icons.PERSON, label="Pessoa"),
                ft.NavigationBarDestination(icon=Icons.EMAIL_SHARP, label="Emprestimos"),
            ],
            on_change=lambda e: page.go(
                ["/", "/usuarios", "/emprestimos"][
                    e.control.selected_index])
        ), content=ft.Container(),
        height=500, expand=True)

    def listarLivros(e):
        lv.controls.clear()
        dados = get_livros()
        print(dados)
        for livro in dados['livros']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'{livro["titulo"]}'),
                    subtitle=ft.Text(f'{livro["autor"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.INFO,
                        items=[
                            ft.PopupMenuItem(text="Detalhes")
                        ],
                        on_select=lambda _, lv=livro: exibirDetalhesLivro(lv['id'], lv["titulo"], lv["autor"], lv["isbn"],
                                                                            lv["resumo"], lv["status_livro"])
                    )
                )
            )

    def exibirDetalhesLivro(id, titulo, autor, isbn, resumo, status_livro):
        nonlocal livro_editando  # Permite editar a variável fora da função
        livro_editando = {
            "id": id,
            "titulo": titulo,
            "autor": autor,
            "isbn": isbn,
            "resumo": resumo,
            "status_livro": status_livro
        }
        livro.value = (f"Titulo: \n {titulo};\n\nAutor: \n {autor};\n\nISBN: \n {isbn};\n\nResumo: \n {resumo};\n\nStatus livro: \n {status_livro}")
        page.update()
        page.go("/exibirDetalhesLivro")

    def salvar_livro(titulo, autor, isbn, resumo, status_livro):
        nonlocal editando_livro, livro_editando

        # Validação dos campos obrigatórios
        if not titulo or not autor or not isbn or not resumo:
            msg_error = ft.SnackBar(
                content=Text("Não deixe campo vazio!"),
                bgcolor=Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
            return

        if editando_livro:
            resultado = put_livro(
                id=livro_editando["id"],
                titulo=titulo,
                autor=autor,
                isbn=isbn,
                resumo=resumo,
                status_livro=status_livro
            )

            if resultado and "error" not in resultado:  # Verifica se não veio erro do backend
                msg_sucess = ft.SnackBar(
                    content=Text("Livro editado com sucesso!"),
                    bgcolor=Colors.GREEN
                )
                page.overlay.append(msg_sucess)
                msg_sucess.open = True
            else:  # Se retornou erro ou resultado vazio
                erro_msg = resultado.get("error",
                                         "Erro ao editar o livro. Verifique se há empréstimos pendentes.") if resultado else "Erro na requisição."
                msg_error = ft.SnackBar(
                    content=Text(erro_msg),
                    bgcolor=Colors.RED
                )
                page.overlay.append(msg_error)
                msg_error.open = True

            editando_livro = False
            livro_editando = {}
        else:
            post_livro(titulo, autor, isbn, resumo)
            msg_sucess = ft.SnackBar(
                content=Text("Livro cadastrado!"),
                bgcolor=Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True

        # Limpa os campos após salvar ou editar
        input_titulo.value = ''
        input_autor.value = ''
        input_isbn.value = ''
        input_resumo.value = ''
        input_status_livro.value = True

        page.update()

    def editarLivroAtual():
        nonlocal editando_livro, livro_editando
        editando_livro = True

        input_titulo.value = livro_editando["titulo"]
        input_autor.value = livro_editando["autor"]
        input_isbn.value = livro_editando["isbn"]
        input_resumo.value = livro_editando["resumo"]
        input_status_livro.value = livro_editando.get("status_livro", True)

        # Navega para a tela de cadastro (usada agora como tela de edição)
        page.go("/cadastrarLivro")


    def listarUsuarios(e):
        lv.controls.clear()
        dados = get_users()
        print(dados)
        for user in dados['usuarios']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f'{user["nome"]}'),
                    subtitle=ft.Text(f'{user["cpf"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.INFO,
                        items=[
                            ft.PopupMenuItem(text="Detalhes")
                        ],
                        on_select=lambda _, u=user: exibirDetalhesUsuario(u['id'], u['nome'], u['cpf'], u['endereco'],
                                                                        u['status'])
                    )
                )
            )

    def exibirDetalhesUsuario(id, nome, cpf, endereco, status_user):
        nonlocal user_editando, editando_user
        user_editando = {
            "id": id,
            "nome": nome,
            "cpf": cpf,
            "cpf_antigo": cpf,
            "endereco": endereco,
            "status_user": status_user
        }
        editando_user = False  # ainda não está editando
        user.value = (f"Nome: \n{nome};\n\nCPF: \n{cpf};\n\nEndereço: \n{endereco};\n\nStatus: \n{status_user}")
        page.update()
        page.go("/exibirDetalhesUsuario")

    def salvarUser(nome, cpf, endereco, status_user):
        nonlocal editando_user, user_editando

        if nome == '' or cpf == '' or endereco == '':
            msg_error = ft.SnackBar(
                content=ft.Text("Não deixe campo vazio!"),
                bgcolor=ft.Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
            return

        if editando_user:
            resultado = put_user(
                id=user_editando["id"],
                nome=nome,
                cpf=cpf,
                endereco=endereco,
                status_user=status_user
            )

            if resultado and "error" not in resultado:  # Verifica se não veio erro do backend
                msg_sucess = ft.SnackBar(
                    content=Text("Usuário editado com sucesso!"),
                    bgcolor=Colors.GREEN
                )
                page.overlay.append(msg_sucess)
                msg_sucess.open = True
            else:  # Se retornou erro ou resultado vazio
                erro_msg = resultado.get("error",
                                         "Erro ao editar o Usuario. Verifique se há empréstimos pendentes.") if resultado else "Erro na requisição."
                msg_error = ft.SnackBar(
                    content=Text(erro_msg),
                    bgcolor=Colors.RED
                )
                page.overlay.append(msg_error)
                msg_error.open = True

            editando_user = False
            user_editando = {}
        else:
            post_user(nome, cpf, endereco)
            msg_sucess = ft.SnackBar(
                content=Text("Livro cadastrado!"),
                bgcolor=Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True

        # Limpa os campos após salvar ou editar
        input_nome.value = ''
        input_cpf.value = ''
        input_endereco.value = ''
        input_status_user.value = True

        page.update()

    def editarUserAtual():
        nonlocal editando_user, user_editando
        editando_user = True

        input_nome.value = user_editando.get("nome", "")
        input_cpf.value = user_editando.get("cpf", "")
        input_endereco.value = user_editando.get("endereco", "")
        input_status_user.value = user_editando.get("status", True)

        page.go("/cadastrarUsuario")

    def listarEmprestimos(e):
        lv.controls.clear()
        dados = get_emprestimos()
        print(dados)
        for emprestimo in dados['lista_emprestimos']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.EMAIL),
                    title=ft.Text(f'ID do Usuario: {emprestimo["usuario_id"]}'),
                    subtitle=ft.Text(f'ID do livro: {emprestimo["livro_id"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.INFO,
                        items=[
                            ft.PopupMenuItem(text="Detalhes")
                        ],
                        on_select=lambda _, e=emprestimo: exibirDetalhesEmprestimo(e['id'], e['usuario_id'],
                                                                                    e['livro_id'], e['data_devolucao'],
                                                                                    e['data_emprestimo'], e['status_emprestimo'])
                    )
                )
            )
        page.update()
    def exibirDetalhesEmprestimo(id, id_usuario, id_livro, data_devolucao, data_emprestimo, status_emprestimo):
        nonlocal emprestimo_editando, editando_emprestimo

        # Atualizar o emprestimo_editando com os dados atuais
        emprestimo_editando = {
            "id": id,
            "usuario_id": id_usuario,
            "livro_id": id_livro,
            "data_devolucao": data_devolucao,
            "data_emprestimo": data_emprestimo,
            "status_emprestimo": status_emprestimo,
        }

        formato_entrada = "%a, %d %b %Y %H:%M:%S %Z"

        # converter e formatar data_emprestimo
        data_emprestimo_formatada = datetime.strptime(data_emprestimo, formato_entrada).strftime("%d/%m/%Y")

        # converter e formatar data_devolucao
        data_devolucao_formatada = datetime.strptime(data_devolucao, formato_entrada).strftime("%d/%m/%Y")

        editando_user = False
        emprestimo.value = (
            f"ID: \n{id};\n\nID usuario: \n{id_usuario};\n\nID livro: \n{id_livro};\n\n"
            f"Data devolução: \n{data_devolucao_formatada};\n\nData emprestimo: \n{data_emprestimo_formatada};\n\nStatus: \n{status_emprestimo}"
        )
        input_status_emprestimo.value = status_emprestimo
        page.update()
        page.go("/exibirDetalhesEmprestimo")

    def salvarEmprestimo(id_livro, id_usuario):
        if id_usuario == '' or id_livro == '':
            msg_error = ft.SnackBar(
                content=Text("Não deixe campo vazio!"),
                bgcolor=Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
            return
        else:

            post_emprestimo(id_livro, id_usuario)
            input_livro.value = ''
            input_user.value = ''
            msg_sucess = ft.SnackBar(
                content=Text("Empréstimo cadastrado!"),
                bgcolor=Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True
            page.update()

    def editarEmprestimoAtual():
        nonlocal editando_emprestimo, emprestimo_editando
        editando_emprestimo = True

        # Atualiza checkbox com valor atual
        input_status_emprestimo.value = emprestimo_editando.get("status_emprestimo", True)

        # Navega para a página de edição do empréstimo
        page.go("/editarEmprestimo")

    def salvarStatusEmprestimo(e):
        # Pega o id do empréstimo que está sendo editado
        id_emprestimo = emprestimo_editando['id']
        novo_status = input_status_emprestimo.value

        resultado = put_emprestimo(id_emprestimo, novo_status)

        if resultado:
            # Mensagem de sucesso
            msg_sucess = ft.SnackBar(
                content=ft.Text("Status do empréstimo atualizado!"),
                bgcolor=ft.Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True

            # Atualiza a lista e volta para a tela anterior
            listarEmprestimos(e)
            page.go("/listarEmprestimos")

        else:
            # Mensagem de erro
            msg_error = ft.SnackBar(
                content=ft.Text("Falha ao atualizar status!"),
                bgcolor=ft.Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True

        page.update()

    def gerencia_rotas(e):
        page.views.clear()
        if page.route == "/":

            page.views.append(
                View(
                    "/",
                    [
                        AppBar(
                            title=Text("Biblioteca - Livros", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.ResponsiveRow(
                                controls=[
                                    ft.ElevatedButton(
                                        text="Listar Livros",
                                        icon=ft.Icons.BOOK_OUTLINED,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",  # Verde escuro
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/listarLivros"),
                                        col=6
                                    ),
                                    ft.ElevatedButton(
                                        text="Cadastrar Livros",
                                        icon=ft.Icons.LIBRARY_ADD_OUTLINED,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",  # Laranja coral
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/cadastrarLivro"),
                                        col=6
                                    )
                                ],
                                alignment="center",
                                spacing=20
                            )
                        ),
                        pagelet
                    ]
                )
            )


        if page.route == "/listarLivros":
            listarLivros(e)
            page.views.append(
                View(
                    "/listarLivros",
                    [
                        AppBar(
                            title=Text("Livros", size=22, weight=ft.FontWeight.BOLD, color="white"),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=5,
                            content=lv,  # ListView com os livros
                            bgcolor=ft.Colors.GREEN_200,
                            border_radius= 20
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(bottom=20),
                            content=ft.ElevatedButton(
                                text="Voltar",
                                icon=ft.Icons.ARROW_BACK,
                                style=ft.ButtonStyle(
                                    bgcolor="#2A9D8F",  # Verde escuro
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.padding.symmetric(horizontal=25, vertical=10),
                                    elevation=4,
                                ),
                                on_click=lambda e: page.go("/"),
                            )
                        )
                    ]
                )
            )

        if page.route == "/exibirDetalhesLivro":
            page.views.append(
                View(
                    "/exibirDetalhesLivro",
                    [
                        AppBar(
                            title=Text("Detalhes do Livro", size=22, weight=ft.FontWeight.BOLD, color="white"),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=20,
                            content=livro  # Detalhes do livro
                        ),
                        ft.Container(
                            padding=20,
                            alignment=ft.alignment.center,
                            content=ft.Row(
                                alignment="center",
                                spacing=20,
                                controls=[
                                    ft.ElevatedButton(
                                        text="Voltar",
                                        icon=ft.Icons.ARROW_BACK,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",  # Verde escuro
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/"),
                                    ),
                                    ft.ElevatedButton(
                                        text="Editar Livro",
                                        icon=ft.Icons.EDIT,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",  # Laranja coral
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: editarLivroAtual(),
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/cadastrarLivro":
            page.views.append(
                View(
                    "/cadastrarLivro",
                    [
                        AppBar(
                            title=Text("Cadastro de Livro", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    input_titulo,
                                    input_autor,
                                    input_isbn,
                                    input_resumo,
                                    input_status_livro,
                                    ft.ResponsiveRow(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Voltar",
                                                icon=ft.Icons.ARROW_BACK,
                                                col=6,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#F4A261",
                                                    color=ft.Colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                                    elevation=4,
                                                ),
                                                on_click=lambda e: page.go("/"),
                                            ),
                                            ft.ElevatedButton(
                                                text="Salvar",
                                                icon=ft.Icons.SAVE_OUTLINED,
                                                col=6,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#2A9D8F",
                                                    color=ft.Colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                                    elevation=4,
                                                ),
                                                on_click=lambda _: salvar_livro(
                                                    input_titulo.value,
                                                    input_autor.value,
                                                    input_isbn.value,
                                                    input_resumo.value,
                                                    input_status_livro.value
                                                ),
                                            )
                                        ],
                                        spacing=20
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/usuarios":
            page.views.append(
                View(
                    "/usuarios",
                    [
                        AppBar(
                            title=Text("Usuarios", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo (mesmo padrão)
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.ResponsiveRow(
                                controls=[
                                    ft.ElevatedButton(
                                        text="Listar Usuarios",
                                        icon=ft.Icons.PERSON,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",  # Verde escuro
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/listarUsuarios"),
                                        col=6,
                                    ),
                                    ft.ElevatedButton(
                                        text="Cadastrar Usuario",
                                        icon=ft.Icons.PERSON_ADD,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",  # Laranja coral
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/cadastrarUsuario"),
                                        col=6,
                                    )
                                ],
                                alignment="center",
                                spacing=20
                            )
                        ),
                        pagelet
                    ]
                )
            )

        if page.route == "/listarUsuarios":
            listarUsuarios(e)
            page.views.append(
                View(
                    "/listarUsuarios",
                    [
                        AppBar(
                            title=Text("Listar Usuarios", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=8,
                            content=lv,  # sua lista de usuários
                            bgcolor= ft.Colors.GREEN_200,
                            border_radius= 20,
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(bottom=20),
                            content=ft.ElevatedButton(
                                text="Voltar",
                                icon=ft.Icons.ARROW_BACK,
                                style=ft.ButtonStyle(
                                    bgcolor="#2A9D8F",  # Verde escuro
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.padding.symmetric(horizontal=25, vertical=10),
                                    elevation=4,
                                ),
                                on_click=lambda e: page.go("/usuarios"),
                            )
                        )
                    ]
                )
            )

        if page.route == "/exibirDetalhesUsuario":
            page.views.append(
                View(
                    "/exibirDetalhesUsuario",
                    [
                        AppBar(
                            title=Text("Detalhes do Usuario", size=22, weight=ft.FontWeight.BOLD,
                                       color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=20,
                            content=user  # Seus detalhes do usuário
                        ),
                        ft.Container(
                            padding=20,
                            alignment=ft.alignment.center,
                            content=ft.Row(
                                alignment="center",
                                spacing=20,
                                controls=[
                                    ft.ElevatedButton(
                                        text="Voltar",
                                        icon=ft.Icons.ARROW_BACK,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",  # Verde escuro
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/listarUsuarios"),
                                    ),
                                    ft.ElevatedButton(
                                        text="Editar Usuário",
                                        icon=ft.Icons.EDIT,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",  # Laranja coral
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: editarUserAtual(),
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/cadastrarUsuario":
            page.views.append(
                View(
                    "/cadastrarUsuario",
                    [
                        AppBar(
                            title=Text("Cadastrar Usuario", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    input_nome,
                                    input_cpf,
                                    input_endereco,
                                    input_status_user,
                                    ft.ResponsiveRow(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Voltar",
                                                col=6,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#F4A261",  # Laranja coral
                                                    color=ft.Colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                                    elevation=4,
                                                ),
                                                on_click=lambda e: page.go("/usuarios"),
                                            ),
                                            ft.ElevatedButton(
                                                text="Salvar",
                                                col=6,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#2A9D8F",  # Verde escuro
                                                    color=ft.Colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                                    elevation=4,
                                                ),
                                                on_click=lambda _: salvarUser(
                                                    input_nome.value,
                                                    input_cpf.value,
                                                    input_endereco.value,
                                                    input_status_user.value
                                                ),
                                            )
                                        ],
                                        spacing=20
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/emprestimos":
            page.views.append(
                View(
                    "/emprestimos",
                    [
                        AppBar(
                            title=Text("Emprestimos", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"
                        ),
                        ft.Container(
                            padding=20,
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                spacing=20,
                                alignment="center",
                                controls=[
                                    ft.ElevatedButton(
                                        text="Listar Emprestimos",
                                        icon=ft.Icons.FORMAT_LIST_BULLETED_OUTLINED,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=18, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/listarEmprestimos"),
                                    ),
                                    ft.ElevatedButton(
                                        text="Cadastrar Emprestimo",
                                        icon=ft.Icons.FORMAT_LIST_BULLETED_ADD,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=18, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/cadastrarEmprestimo"),
                                    ),
                                ],
                            ),
                        ),
                        pagelet
                    ]
                )
            )

        if page.route == "/listarEmprestimos":
            listarEmprestimos(e)
            page.views.append(
                View(
                    "/listarEmprestimos",
                    [
                        AppBar(
                            title=Text("Listar Emprestimos", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=8,
                            content=lv,  # sua ListView ou lista de empréstimos
                            bgcolor=ft.Colors.GREEN_200,
                            border_radius= 20,
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(bottom=20),
                            content=ft.ElevatedButton(
                                text="Voltar",
                                icon=ft.Icons.ARROW_BACK,
                                style=ft.ButtonStyle(
                                    bgcolor="#2A9D8F",  # Verde escuro
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.padding.symmetric(horizontal=25, vertical=10),
                                    elevation=4,
                                ),
                                on_click=lambda e: page.go("/emprestimos"),
                            )
                        )
                    ]
                )
            )

        if page.route == "/exibirDetalhesEmprestimo":
            page.views.append(
                View(
                    "/exibirDetalhesEmprestimo",
                    [
                        AppBar(
                            title=Text("Detalhes do Empréstimo", size=22, weight=ft.FontWeight.BOLD,
                                       color=ft.Colors.WHITE),
                            bgcolor="#264653"  # Azul profundo
                        ),
                        ft.Container(
                            padding=20,
                            content=emprestimo  # Detalhes do empréstimo
                        ),
                        ft.Container(
                            padding=20,
                            alignment=ft.alignment.center,
                            content=ft.Row(
                                alignment="center",
                                spacing=20,
                                controls=[
                                    ft.ElevatedButton(
                                        text="Voltar",
                                        icon=ft.Icons.ARROW_BACK,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",  # Verde escuro
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/listarEmprestimos"),
                                    ),
                                    ft.ElevatedButton(
                                        text="Editar Status",
                                        icon=ft.Icons.EDIT,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",  # Laranja coral
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: editarEmprestimoAtual(),
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/cadastrarEmprestimo":
            page.views.append(
                View(
                    "/cadastrarEmprestimo",
                    [
                        AppBar(
                            title=Text("Cadastrar Empréstimo", size=22, weight=ft.FontWeight.BOLD,
                                       color=ft.Colors.WHITE),
                            bgcolor="#264653"
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    input_livro,
                                    input_user,
                                    ft.ResponsiveRow(
                                        spacing=20,
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Voltar",
                                                col=6,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#F4A261",  # Laranja coral
                                                    color=ft.Colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                                    elevation=4,
                                                ),
                                                on_click=lambda e: page.go("/emprestimos"),
                                            ),
                                            ft.ElevatedButton(
                                                text="Salvar",
                                                col=6,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#2A9D8F",  # Verde escuro
                                                    color=ft.Colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                                    elevation=4,
                                                ),
                                                on_click=lambda e: salvarEmprestimo(input_livro.value,
                                                                                    input_user.value),
                                            ),
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/editarEmprestimo":
            page.views.append(
                ft.View(
                    "/editarEmprestimo",
                    [
                        ft.AppBar(
                            title=ft.Text("Editar Status do Empréstimo", size=22, weight=ft.FontWeight.BOLD,
                                          color=ft.Colors.WHITE),
                            bgcolor="#264653"
                        ),
                        ft.Container(
                            padding=20,
                            content=input_status_emprestimo
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.ResponsiveRow(
                                spacing=20,
                                controls=[
                                    ft.ElevatedButton(
                                        text="Cancelar",
                                        col=6,
                                        style=ft.ButtonStyle(
                                            bgcolor="#F4A261",  # Laranja coral
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=lambda e: page.go("/exibirDetalhesEmprestimo"),
                                    ),
                                    ft.ElevatedButton(
                                        text="Salvar",
                                        col=6,
                                        style=ft.ButtonStyle(
                                            bgcolor="#2A9D8F",  # Verde escuro
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                            elevation=4,
                                        ),
                                        on_click=salvarStatusEmprestimo,
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )

        page.update()

    lv = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1
    )
    livro = ft.Text("")
    input_titulo = ft.TextField(label="Titulo: ")
    input_autor = ft.TextField(label="Autor: ")
    input_isbn = ft.TextField(label="ISBN: ")
    input_resumo = ft.TextField(label="Resumo: ")

    msg_error = ft.SnackBar(
        content=Text("")
    )
    msg_sucess = ft.SnackBar(
        content=Text("")
    )

    user = ft.Text("")
    input_nome = ft.TextField(label="Nome: ")
    input_cpf = ft.TextField(label="CPF: ")
    input_endereco = ft.TextField(label="Endereço: ")
    emprestimo = ft.Text("")
    input_user = ft.TextField(label="ID do usuario: ")
    input_livro = ft.TextField(label="ID do livro: ")
    input_status_livro = ft.Checkbox(label="Livro disponível", value=True)
    input_status_user = ft.Checkbox(label="Ativo", value=True)  # ou False, conforme o padrão
    input_status_emprestimo = ft.Checkbox(label="Empréstimo ativo", value=True)
    # def voltar(e):
    #     page.views.pop()
    #     top_view = page.views[-1]
    #     page.go(top_view.route)

    page.on_route_change = gerencia_rotas
    # page.on_view_pop = voltar
    page.go(page.route)


ft.app(main)
