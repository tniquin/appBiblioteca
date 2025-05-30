import flet as ft
import requests
from flet import *
from api import get_livros, post_livro, get_users, post_user, get_emprestimos


def main(page: ft.Page):
    page.title = "Exemplos Rotas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667
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
                ft.NavigationBarDestination(icon=Icons.EMAIL_SHARP, label="Emprestimo"),
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
                        on_select=lambda _, lv=livro: exibirDetalhesLivro(lv['titulo'], lv['autor'], lv['isbn'], lv['resumo'])
                    )
                )
            )
    def exibirDetalhesLivro(titulo, autor, isbn, resumo):
        livro.value = (f"Titulo: \n {titulo};\n\nAutor: \n {autor};\n\nISBN: \n {isbn};\n\nResumo: \n {resumo}")
        page.update()
        page.go("/exibirDetalhesLivro")

    def salvar_livro(titulo, autor, isbn, resumo):
        if titulo == '' or autor == '' or isbn == '' or resumo == '':
            msg_error = ft.SnackBar(
                content=Text("Não deixe campo vazio!"),
                bgcolor=Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
            return
        else:
            post_livro(titulo, autor, isbn, resumo)
            input_titulo.value = ''
            input_autor.value = ''
            input_isbn.value = ''
            input_resumo.value = ''
            msg_sucess = ft.SnackBar(
                content=Text("Livro cadastrado!"),
                bgcolor=Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True
            page.update()

    def listarUsuario(e):
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
                        on_select=lambda _, u=user:  exibirDetalhesUser(u['nome'], u['cpf'], u['endereco'], u['status_user'])
                    )
                )
            )
    def exibirDetalhesUser(nome, cpf, endereco, status_user):
        user.value = (f"Nome: \n{nome};\n\nCPF: \n{cpf};\n\nEndereço: \n{endereco};\n\nStatus: \n{status_user}")
        page.update()
        page.go("/exibirDetalhesUser")

    def salvarUser(nome, cpf, endereco):

        if nome == '' or cpf == '' or endereco == '':
            msg_error = ft.SnackBar(
                content=Text("Não deixe campo vazio!"),
                bgcolor=Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
            return
        else:
            post_user(nome, cpf, endereco)
            input_nome.value = ''
            input_cpf.value = ''
            input_endereco.value = ''
            msg_sucess = ft.SnackBar(
                content=Text("Usuario cadastrado!"),
                bgcolor=Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True
            page.update()

    def listarEmprestimos(e):
        lv.controls.clear()
        dados = get_emprestimos()
        print(dados)
        for emprestimo in dados['lista_emprestimos']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.EMAIL),
                    title=ft.Text(f'{emprestimo["usuario_id"]}'),
                    subtitle=ft.Text(f'{emprestimo["livro_id"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.INFO,
                        items=[
                            ft.PopupMenuItem(text="Detalhes")
                        ],
                        on_select=lambda _, e=emprestimo: exibirDetalhesEmprestimo(e['id'], e['usuario_id'], e['livro_id'], e['data_devolucao'], e['data_emprestimo'])
                    )
                )
            )

    def exibirDetalhesEmprestimo(id, id_usuario, id_livro, data_devolucao, data_emprestimo):
        emprestimo.value = (f"ID: \n{id};\n\nID usuario: \n{id_usuario};\n\nID livro: \n{id_livro};\n\nData devolução: \n{data_devolucao};\n\nData emprestimo: \n{data_emprestimo}")
        page.update()
        page.go("/exibirDetalhesEmprestimo")

    def salvarEmprestimo(id_livro, id_usuario, id_devolucao, data_emprestimo):
        if id_usuario == '' or id_livro == '' or id_devolucao == '' or data_emprestimo == '':
            msg_error = ft.SnackBar(
                content=Text("Não deixe campo vazio!"),
                bgcolor=Colors.RED
            )
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
            return
        else:
            post_user(input_devolucao, input_emprestimo, input_livro, input_emprestimo)
            input_devolucao.value = ''
            input_emprestimo.value = ''
            input_livro.value = ''
            input_emprestimo.value = ''
            msg_sucess = ft.SnackBar(
                content=Text("Usuario cadastrado!"),
                bgcolor=Colors.GREEN
            )
            page.overlay.append(msg_sucess)
            msg_sucess.open = True
            page.update()

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
                View(
                    "/",
                    [
                            AppBar(title=Text("Biblioteca - Livros"), bgcolor=Colors.SECONDARY),
                            ft.ResponsiveRow([
                                ft.ElevatedButton(text="Pessoas", on_click=lambda e: page.go("/usuarios"), col=6),
                                ft.ElevatedButton(text="Emprestimos", on_click=lambda e: page.go("/emprestimos"), col=6),
                            ]),
                            ft.ResponsiveRow([
                                ft.ElevatedButton(
                                    text="Listar Livros",
                                    on_click=lambda e: page.go("/listarLivros"),
                                ),
                                ft.ElevatedButton(
                                    text="Cadastrar Livros",
                                    on_click=lambda e: page.go("/cadastrarLivros"),
                                )
                            ])

                            ]
                    )
                        )
        if page.route == "/listarLivros":
            listarLivros(e)
            page.views.append(
                View(
                    "/listarLivros",
                    [
                        AppBar(title=Text("Livros"), bgcolor=Colors.SECONDARY), ft.ElevatedButton(text="Voltar", width=page.window.width, on_click=lambda e: page.go("/")),
                        lv,
                    ]
                )
            )
        page.update()
        if page.route == "/exibirDetalhesLivro":
            page.views.append(
                View(
                    "/exibirDetalhesLivro",
                    [
                        AppBar(title=Text("Detalhes do Livro"), bgcolor=Colors.SECONDARY), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/listarLivros")),
                        livro,
                    ]
                )
            )

        if page.route == "/cadastrarLivros":
            page.views.append(
                View(
                    "/cadastrarLivros",
                    [
                        AppBar(title=Text("Cadastro de Livro"), bgcolor=Colors.SECONDARY),
                        input_titulo,
                        input_autor,
                        input_isbn,
                        input_resumo,
                        ft.ResponsiveRow(
                            [
                                ft.ElevatedButton(text="Voltar",
                                                    on_click=lambda e: page.go("/"),
                                                    col=6),
                                ft.ElevatedButton(
                                    text="Salvar",
                                    on_click=lambda _: salvar_livro(input_titulo.value, input_autor.value,
                                                                    input_isbn.value,
                                                                    input_resumo.value),
                                    col=6),
                            ]
                        ),


                    ],
                )
            )




        page.update()

        if page.route == "/usuarios":
            page.views.clear()
            page.views.append(
                    View(
                        "/usuarios",
                        [
                            AppBar(title=Text("Usuarios"), bgcolor=Colors.SECONDARY),
                            ft.ElevatedButton(
                                text="Listar Usuarios",
                                on_click=lambda e: page.go("/listarUsuarios"),
                            ),
                            ft.ElevatedButton(
                                text="Cadastrar Usuarios",
                                on_click=lambda e: page.go("/cadastrarUsuarios"),
                            ),
                            pagelet
                        ]
                    )
            )
        if page.route == "/listarUsuarios":
            listarUsuario(e)
            page.views.append(
                View(
                    "/listarUsuarios",
                    [
                        AppBar(title=Text("Listar usuarios"), bgcolor=Colors.SECONDARY), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/usuarios")),
                        lv,
                    ]
                )
            )
        if page.route == "/exibirDetalhesUsuarios":
            page.views.append(
                View(
                    "/exibirDetalhesUsuarios",
                    [
                        AppBar(title=Text("Detalhes do usuario:")), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/listarUsuarios")),
                        user,
                    ]
                )
            )
        if page.route == "/cadastrarUsuarios":
            page.views.append(
                View(
                    "/cadastrarUsuarios",
                    [
                        AppBar(title=Text("Cadastrar usuario:")), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/listarUsuarios")),
                        input_nome,
                        input_cpf,
                        input_endereco,
                        ft.ElevatedButton(
                            text="Salvar",
                            on_click=lambda _: salvarUser(input_nome.value, input_cpf.value, input_endereco.value.value)
                        ),
                    ]
                )
            )
        if page.route == "/emprestimos":
            page.views.append(
                View(
                    "/emprestimos",
                    [
                        AppBar(title=Text("Emprestimos:")),
                        ft.ElevatedButton(
                            text="Listar Emprestimos",
                            on_click=lambda e: page.go("/listarEmprestimos"),
                        ),
                        ft.ElevatedButton(
                            text="Cadastrar Emprestimos",
                            on_click=lambda e: page.go("/cadastrarEmprestimos"),
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
                        AppBar(title=Text("Listar Emprestimos:")), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/emprestimos")),
                        lv,
                    ]
                )
            )
        if page.route == "/exibirDetalhesEmprestimos":
            page.views.append(
                View(
                    "/exibirDetalhesEmprestimos",
                    [
                        AppBar(title=Text("Detalhes do Emprestimo: ")), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/listarEmprestimos")),
                        emprestimo,
                    ]
                )
            )
        if page.route == "/cadastrarEmprestimosEmprestimos":
            page.views.append(
                View(
                    "/cadastrarEmprestimosEmprestimos",
                    [
                        AppBar(title=Text("Cadastrar Emprestimo: ")), ft.ElevatedButton(text="Voltar", on_click=lambda e: page.go("/listarEmprestimos")),
                        input_devolucao,
                        input_emprestimo,
                        input_user,
                        input_cpf,
                        ft.ElevatedButton(
                            text="Salvar",
                            on_click=lambda e: salvarEmprestimo(input_devolucao.value, input_emprestimo.value.value, input_livro.value, input_user.value)
                        )
                    ]
                )
            )
    # def voltar(e):
    #     page.views.pop()
    #     top_view = page.views[-1]
    #     page.go(top_view.route)
    #
    page.on_route_change = gerencia_rotas
    #page.on_view_pop = voltar
    page.go(page.route)


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
    input_devolucao = ft.TextField(label="Data de Devolucao: ")
    input_emprestimo = ft.TextField(label="DataEmprestimo: ")
    input_user = ft.TextField(label="ID do usuario: ")
    input_livro = ft.TextField(label="ID do livro: ")

    page.go(page.route)
ft.app(main)