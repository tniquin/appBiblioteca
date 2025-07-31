import flet as ft
import requests
from flet import SnackBar, Text
import threading
import base64
import json
import jwt

def main(page: ft.Page):
    page.title = "Gerenciador de Clientes"
    page.theme_mode = "light"
    page.padding = 30
    page.window.width = 423
    page.window.height = 862

    token = None

    def get_token():
        global token
        return token

    def set_token(new_token):
        global token
        token = new_token


    def ir_listar_clientes(e):
        page.go("/listar_clientes")

    def ir_para_adicionar(e):
        page.go("/adicionar")

    def ir_para_editar(e):
        page.go("/editar")

    def listar_veiculos(e):
        page.go("/listar_veiculos")

    def adicionar_veiculo(e):
        page.go("/adicionar_veiculo")

    def editar_veiculo(id_veiculo, page):
        page.go(f"/editar_veiculo/{id_veiculo}")

    def listar_servicos(e):
        page.go("/listar_servicos")

    def adicionar_servico(e):
        page.go("/adicionar_servico")

    def editar_servico(id_servico, page):
        page.go(f"/editar_servico/{id_servico}")

    def cadastro(e):
        page.go("/cadastro")

    def login(e):
        page.go("/login")

    def listar_usuario(e):
        page.go("/listar_usuarios")

    def ir_para_clientes(e):
        page.go("/clientes")

    def ir_para_veiculos(e):
        page.go("/veiculos")

    def ir_para_servico(e):
        page.go("/servicos")

    def usuario(e):
        page.go("/usuario")


    def reativar_cliente(cliente_id, page):
        print(f"Reativando cliente ID {cliente_id}")  # debug

        msg_sucesso_reativar = ft.SnackBar(
            content=ft.Text("Cliente reativado com sucesso!", weight="bold", color="white"),
            bgcolor="green",
        )
        msg_erro_reativar = ft.SnackBar(
            content=ft.Text("Falha ao reativar cliente!", weight="bold", color="white"),
            bgcolor="red",
        )

        page.overlay.append(msg_sucesso_reativar)
        page.overlay.append(msg_erro_reativar)

        try:
            resposta = requests.put(
                f"http://192.168.1.83:5000/reativarCliente/{cliente_id}",
                headers={"Authorization": f"Bearer {get_token()}"}
            )

            print("Código da resposta:", resposta.status_code)
            print("Resposta JSON:", resposta.json())

            if resposta.status_code == 200:
                page.snack_bar = msg_sucesso_reativar
            else:
                page.snack_bar = msg_erro_reativar

        except Exception as e:
            print("Erro ao reativar:", e)
            page.snack_bar = msg_erro_reativar

        page.snack_bar.open = True
        page.update()

        # força reload manual
        page.go("/reload")
        page.go("/listar_clientes")


    def alterar_status_cliente(cliente_id, page):
        motivo = "Ocultado pelo usuário"  # Você pode substituir por um TextField depois, se quiser

        msg_sucesso_ocultar = ft.SnackBar(
            content=ft.Text("Cliente ocultado com sucesso!", weight="bold", color="white"),
            bgcolor="green",
        )

        msg_erro_ocultar = ft.SnackBar(
            content=ft.Text("Falha ao ocultar cliente!", weight="bold", color="white"),
            bgcolor="red",
        )

        page.overlay.append(msg_sucesso_ocultar)
        page.overlay.append(msg_erro_ocultar)

        try:
            resposta = requests.put(
                f"http://192.168.1.83:5000/ocultarClient/{cliente_id}",
                headers={"Authorization": f"Bearer {get_token()}"},
                json={"motivo": motivo}
            )

            print("Código da resposta:", resposta.status_code)
            print("Resposta JSON:", resposta.json())

            if resposta.status_code == 200:
                page.snack_bar = msg_sucesso_ocultar
            else:
                page.snack_bar = msg_erro_ocultar

        except Exception as e:
            print("Erro:", e)
            page.snack_bar = msg_erro_ocultar

        page.snack_bar.open = True
        page.update()

        # força reload da rota
        page.go("/reload")
        page.go("/listar_clientes")


    pagelet = ft.Pagelet(
        content=ft.Container(),
        expand=True,
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Início"),
                ft.NavigationBarDestination(icon=ft.Icons.PEOPLE, label="Clientes"),
                ft.NavigationBarDestination(icon=ft.Icons.DIRECTIONS_CAR, label="Veículos"),
                ft.NavigationBarDestination(icon=ft.Icons.BUILD, label="Serviços"),
                ft.NavigationBarDestination(icon=ft.Icons.ACCOUNT_CIRCLE, label="Perfil"),
            ],
            on_change=lambda e: page.go(
                ["/", "/clientes", "/veiculos", "/servicos", "/usuario"][e.control.selected_index]
            ),
        ),
    )

    def gerenciar_rotas(route):
        page.views.clear()
        if page.route == "/":
            email = ft.TextField(
                label="EMAIL",
                text_style=ft.TextStyle(weight="bold"),
                border_color="black",
                border_radius=10,
                autofocus=True,
            )

            password = ft.TextField(
                label="SENHA",
                password=True,
                can_reveal_password=True,
                text_style=ft.TextStyle(weight="bold"),
                border_color="black",
                border_radius=10,
            )

            msg_sucesso_login = ft.SnackBar(
                content=ft.Text("Login realizado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_login = ft.SnackBar(
                content=ft.Text("Falha ao fazer login!", weight="bold", color="white"),
                bgcolor="red",
            )
            page.overlay.append(msg_sucesso_login)
            page.overlay.append(msg_erro_login)

            def verificar_login(e):
                dados = {
                    "email": email.value,
                    "senha": password.value,
                }
                try:
                    resposta = requests.post("http://192.168.1.83:5000/login", json=dados)

                    if resposta.status_code == 200:
                        token = resposta.json().get('access_token')
                        set_token(token)

                        payload = jwt.decode(token, options={"verify_signature": False})
                        role = payload["sub"]["role"]

                        if role == "admin":
                            page.go("/home")
                            return

                        # 🟩 1. Buscar CPF do usuário pelo e-mail
                        cpf_resposta = requests.get(
                            "http://192.168.1.83:5000/buscar_cpf_por_email",
                            params={"email": email.value}
                        )

                        if cpf_resposta.status_code == 200:
                            cpf_usuario = cpf_resposta.json()["cpf"]
                        else:
                            raise Exception("Não foi possível obter o CPF do usuário.")

                        # 🟩 2. Buscar dados do cliente
                        cliente_resposta = requests.get(
                            f"http://192.168.1.83:5000/dados_cliente/{cpf_usuario}"
                        )

                        # 🟩 3. Buscar dados do veículo
                        veiculo_resposta = requests.get(
                            f"http://192.168.1.83:5000/veiculo_cliente/{cpf_usuario}"
                        )

                        if cliente_resposta.status_code == 200:
                            cliente = cliente_resposta.json()

                            # Verifica se o veículo foi encontrado
                            if veiculo_resposta.status_code == 200:
                                veiculo = veiculo_resposta.json()
                            else:
                                veiculo = {}  # previne erro se não tiver veículo
                            # Armazena os dados para usar na rota depois
                            page.client_storage.set("cliente", cliente)
                            page.client_storage.set("veiculo", veiculo)

                            page.go("/cliente_dashboard")


                        else:
                            page.go("/home")

                    else:
                        msg_erro_login.content = ft.Text(
                            f"Erro: {resposta.status_code} - {resposta.text}",
                            weight="bold", color="white"
                        )
                        msg_erro_login.open = True
                        page.update()

                except Exception as err:
                    msg_erro_login.content = ft.Text(f"Erro na requisição: {err}", weight="bold", color="white")
                    msg_erro_login.open = True
                    page.update()

            botao_entrar = ft.ElevatedButton(
                "ENTRAR",
                on_click=verificar_login,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor="black",
                    color="white",
                    text_style=ft.TextStyle(weight="bold"),
                ),
            )

            link_cadastro = ft.Row(
                [
                    ft.Text("NOVO USUÁRIO?", weight="bold"),
                    ft.TextButton("ENTÃO CADASTRE-SE", on_click=lambda _: page.go("/cadastro"),
                                  style=ft.ButtonStyle(color="blue")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            icone_usuario = ft.Icon(name="account_circle", size=100, color="black")

            page.views.append(
                ft.View(
                    "/login",
                    controls=[
                        ft.Column(
                            [
                                icone_usuario,
                                email,
                                password,
                                botao_entrar,
                                link_cadastro,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif page.route == "/cliente_dashboard":
            cliente = page.client_storage.get("cliente")
            veiculo = page.client_storage.get("veiculo")

            ordens = []
            veiculo_id = veiculo.get("id_veiculo")

            if veiculo_id:
                try:
                    resp_ordens = requests.get(f"http://192.168.1.83:5000/ordens_por_veiculo/{veiculo_id}")
                    if resp_ordens.status_code == 200:
                        ordens = resp_ordens.json()
                except Exception as e:
                    print("Erro ao buscar ordens:", e)

            page.views.append(
                ft.View(
                    "/cliente_dashboard",
                    controls=[
                        ft.Text(f"Olá {cliente['nome']}", size=24, weight="bold", text_align="center"),

                        ft.Container(
                            padding=15,
                            bgcolor=ft.Colors.GREY_800,
                            border_radius=15,
                            content=ft.Column(
                                spacing=5,
                                controls=[
                                    ft.Text("SEU CARRO", color="white", weight="bold", size=16),
                                    ft.Text(f"MODELO: {veiculo.get('modelo', 'N/A')}", color="white"),
                                    ft.Text(f"MARCA: {veiculo.get('marca', 'N/A')}", color="white"),
                                ]
                            )
                        ),

                        ft.Container(
                            padding=15,
                            margin=10,
                            border=ft.border.all(2, "black"),
                            border_radius=12,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                                controls=[
                                    ft.Text("Serviço do seu carro:", size=16, weight="bold"),
                                    ft.Container(
                                        height=560,  # Altura com scroll
                                        content=ft.ListView(
                                            expand=True,
                                            spacing=15,
                                            controls=[
                                                ft.Container(
                                                    padding=10,
                                                    bgcolor="#F5F5F5",
                                                    border_radius=10,
                                                    content=ft.Column(
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Text(f"Serviço: {ordem['descricao_servico']}",
                                                                    weight="bold"),
                                                            ft.Text(f"Status: {ordem['status']}"),
                                                            ft.Text(f"Valor estimado: R$ {ordem['valor_estimado']}"),
                                                            ft.Text(
                                                                f"Data de Abertura: {ordem['data_abertura'].split('T')[0]}"),
                                                            ft.Text(
                                                                f"Data que o Serviço foi fechado: {ordem.get('data_fechamento', '—')[:10] if ordem.get('data_fechamento') else '—'}"
                                                            ),
                                                            ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=48, color="blue")
                                                        ]
                                                    )
                                                )
                                                for ordem in ordens
                                            ]
                                        )
                                    )
                                ]
                            )
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(
                                        name=ft.Icons.HOME,
                                        size=80,
                                        color=ft.Colors.BLACK,
                                    ),
                                    ft.Text(
                                        "Bem-vindo ao Sistema de Gestão",
                                        size=28,
                                        weight="bold",
                                        text_align="center",
                                    ),
                                    ft.Text(
                                        "Gerencie seus clientes, veiculos e serviços com eficiência.",
                                        size=16,
                                        color=ft.Colors.GREY_700,
                                        text_align="center",
                                    ),

                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            width=400,
                            height=700,
                            padding=30,
                            alignment=ft.alignment.center,
                            border_radius=20,
                            bgcolor=ft.Colors.WHITE,
                            shadow=ft.BoxShadow(
                                spread_radius=3,
                                blur_radius=8,
                                color=ft.Colors.GREY_400,
                                offset=ft.Offset(2, 2),
                            ),
                        ),
                        pagelet
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/clientes":
            page.views.append(

                ft.View(
                    controls=[
                        ft.Icon(name=ft.Icons.PEOPLE, size=80, color=ft.Colors.BLACK),
                        ft.Text("CLIENTES!", size=22, weight="bold"),
                        ft.ElevatedButton(
                            "VER CLIENTES",
                            on_click=ir_listar_clientes,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                                                       ),
                        ),
                        ft.ElevatedButton(
                            "ADICIONAR CLIENTE",
                            on_click=ir_para_adicionar,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        pagelet
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                )

            ),

        elif page.route == "/listar_clientes":
            def criar_callback(cliente_id, ativo):
                def callback(e):
                    if ativo:
                        alterar_status_cliente(cliente_id, page)
                    else:
                        reativar_cliente(cliente_id, page)
                return callback
            try:
                print("Token atual:", get_token())
                resposta = requests.get(
                    "http://192.168.1.83:5000/listarClientes",
                    headers={"Authorization": f"Bearer {get_token()}"}
                )
                print("Resposta JSON do login:", resposta.json())

                dados = resposta.json()
                lista_clientes = []

                for cliente in dados:
                    cliente_ativo = cliente.get('ativo', True)

                    cor_fundo = ft.Colors.BLUE_500 if cliente_ativo else ft.Colors.GREY_600
                    cor_texto = "white" if cliente_ativo else ft.Colors.GREY_300

                    lista_clientes.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text("Nome:", width=80, weight="bold", color=cor_texto),
                                                ft.Text(cliente.get('nome', 'Não informado'), weight="bold",
                                                        expand=True, max_lines=1,
                                                        overflow="ellipsis", color=cor_texto),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("CPF:", width=80, weight="bold", color=cor_texto),
                                                ft.Text(cliente.get('cpf', 'Não informado'), weight="bold", expand=True,
                                                        max_lines=1,
                                                        overflow="ellipsis", color=cor_texto),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Telefone:", width=80, weight="bold", color=cor_texto),
                                                ft.Text(cliente.get('telefone', 'Não informado'), weight="bold",
                                                        expand=True,
                                                        max_lines=1, overflow="ellipsis", color=cor_texto),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Endereço:", width=80, weight="bold", color=cor_texto),
                                                ft.Text(cliente.get('endereco', 'Não informado'), weight="bold",
                                                        expand=True,
                                                        max_lines=1, overflow="ellipsis", color=cor_texto),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.ElevatedButton(
                                            text="Editar",
                                            icon=ft.Icons.EDIT,
                                            bgcolor="white",
                                            color="black",
                                            on_click=(lambda id=cliente.get('id_cliente'): lambda e: page.go(f"/editar/{id}"))(),
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.VISIBILITY_OFF if not cliente.get('ativo',
                                                                                            True) else ft.Icons.VISIBILITY,
                                            icon_color="white",
                                            bgcolor="black",
                                            tooltip="Ocultar" if cliente.get('ativo', True) else "Reativar",
                                            on_click=(lambda id=cliente.get('id_cliente'),
                                                             ativo=cliente.get('ativo', True): criar_callback(id, ativo))(),




                                        ),

                                    ],
                                    spacing=8,
                                ),
                                padding=15,
                                border_radius=15,
                                bgcolor=cor_fundo,
                                width=390,
                            ),
                            elevation=2,
                            margin=8,
                        ),
                    )

            except Exception as err:
                lista_clientes = [
                    ft.Text(f"PRECISA ESTAR LOGADO", color=ft.Colors.RED)
                ]

            page.views.append(
                ft.View(
                    "/listar_clientes",
                    controls=[
                        ft.Text("Lista de Clientes", size=22, weight="bold"),

                        ft.Container(
                            content=ft.Column(lista_clientes, scroll=ft.ScrollMode.ALWAYS, spacing=1),
                            expand=True,
                        ),

                        ft.ElevatedButton(
                            text="VOLTAR",
                            bgcolor="black",
                            color="white",
                            on_click=lambda e: page.go("/clientes"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                    ],
                )
            )

        elif page.route == "/reload":
            page.views.append(
                ft.View("/reload", controls=[])
            )


        elif page.route == "/adicionar":
            nome = ft.TextField(
                label="NOME",
                border_color="black",
                border_radius=10,
                text_style=ft.TextStyle(weight="bold")
            )
            cpf = ft.TextField(
                label="CPF",
                border_color="black",
                border_radius=10,
                text_style=ft.TextStyle(weight="bold")
            )
            telefone = ft.TextField(
                label="TELEFONE",
                border_color="black",
                border_radius=10,
                text_style=ft.TextStyle(weight="bold")
            )
            endereco = ft.TextField(
                label="ENDEREÇO",
                border_color="black",
                border_radius=10,
                text_style=ft.TextStyle(weight="bold")
            )
            email = ft.TextField(
                label="EMAIL",
                border_color="black",
                border_radius=10,
                text_style=ft.TextStyle(weight="bold")
            )

            msg_sucesso_cliente = ft.SnackBar(
                content=ft.Text("Cliente cadastrado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_cliente = ft.SnackBar(
                content=ft.Text("Falha ao cadastrar cliente!", weight="bold", color="white"),
                bgcolor="red",
            )

            page.overlay.append(msg_sucesso_cliente)
            page.overlay.append(msg_erro_cliente)

            resultado = ft.Text("")

            def enviar_dados(e):
                dados = {
                    "nome": nome.value,
                    "cpf": cpf.value,
                    "telefone": telefone.value,
                    "endereco": endereco.value,
                    "email": email.value
                }

                try:
                    r = requests.post(
                        "http://192.168.1.83:5000/adicionarClientes",
                        json=dados,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    print(r.status_code, r.text)

                    if r.status_code == 201:
                        msg_sucesso_cliente.open = True
                        resultado.value = "Cliente cadastrado com sucesso!"

                        import threading
                        def delayed_redirect():
                            import time
                            time.sleep(0.2)
                            page.go("/listar_clientes")

                        threading.Thread(target=delayed_redirect).start()
                    else:
                        msg_erro_cliente.open = True
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/adicionar",
                    controls=[
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.PERSON_ADD, size=90, color="black"),
                            alignment=ft.alignment.center,
                            padding=50,
                        ),
                        nome,
                        ft.Container(padding=5, ),
                        cpf,
                        ft.Container(padding=5, ),
                        telefone,
                        ft.Container(padding=5, ),
                        endereco,
                        ft.Container(padding=5, ),
                        email,
                        ft.Container(padding=10, ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text="SALVAR",
                                    bgcolor="black",
                                    color="white",
                                    on_click=enviar_dados,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=50,
                        ),
                        resultado,
                        pagelet,
                    ],
                )
            )

        elif page.route.startswith("/editar/"):
            try:
                id_cliente = int(page.route.split("/editar/")[1])

                resultado = ft.Text("")

                # Snackbars
                msg_sucesso_login = ft.SnackBar(
                    content=ft.Text("Cliente atualizado com sucesso!", weight="bold", color="white"),
                    bgcolor="green",
                )

                msg_erro_login = ft.SnackBar(
                    content=ft.Text("Falha ao atualizar cliente!", weight="bold", color="white"),
                    bgcolor="red",
                )

                page.overlay.append(msg_sucesso_login)
                page.overlay.append(msg_erro_login)
                try:
                    r = requests.get(
                        f"http://192.168.1.83:5000/listarClientes",
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        clientes = r.json()
                        cliente = next((c for c in clientes if c["id_cliente"] == id_cliente), None)
                        if cliente:
                            nome = ft.TextField(
                                label="NOME",
                                value=cliente["nome"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                            cpf = ft.TextField(
                                label="CPF",
                                value=cliente["cpf"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                            telefone = ft.TextField(
                                label="TELEFONE",
                                value=cliente["telefone"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                            endereco = ft.TextField(
                                label="ENDEREÇO",
                                value=cliente["endereco"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                        else:
                            resultado = ft.Text("Cliente não encontrado.", color="red")
                    else:
                        resultado = ft.Text(f"Erro ao buscar cliente: {r.status_code}", color="red")
                except Exception as err:
                    resultado = ft.Text(f"Erro ao carregar cliente: {err}", color="red")

                def salvar_edicao(e):
                    dados = {
                        "nome": nome.value,
                        "cpf": cpf.value,
                        "telefone": telefone.value,
                        "endereco": endereco.value,
                    }
                    try:
                        r = requests.put(
                            f"http://192.168.1.83:5000/editarClients/{id_cliente}",
                            json=dados,
                            headers={"Authorization": f"Bearer {get_token()}"}
                        )
                        if r.status_code == 200:
                            page.snack_bar = msg_sucesso_login
                            page.snack_bar.open = True

                            import threading
                            def delayed_redirect():
                                import time
                                time.sleep(0.2)
                                page.go("/listar_clientes")

                            threading.Thread(target=delayed_redirect).start()
                        else:
                            page.snack_bar = msg_erro_login
                            page.snack_bar.open = True
                    except Exception as err:
                        resultado = ft.Text(f"Erro ao salvar: {err}", color="red")
                        page.snack_bar = msg_erro_login
                        page.snack_bar.open = True
                    page.update()

                page.views.append(
                    ft.View(
                        f"/editar/{id_cliente}",
                        controls=[
                            ft.Container(
                                content=ft.Icon(name=ft.Icons.EDIT, size=60, color="black"),
                                alignment=ft.alignment.center,
                                padding=10,
                            ),
                            nome,
                            cpf,
                            telefone,
                            endereco,
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text="VOLTAR",
                                        bgcolor="black",
                                        color="white",
                                        on_click=lambda e: page.go("/listar_clientes"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                    ft.ElevatedButton(
                                        text="SALVAR",
                                        bgcolor="black",
                                        color="white",
                                        on_click=salvar_edicao,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            pagelet,
                        ],
                        padding=20,
                    )
                )

            except Exception as err:
                page.views.append(
                    ft.View(
                        "/erro",
                        controls=[
                            ft.Text(f"Erro ao abrir tela de edição: {err}", color="red")
                        ]
                    )
                )





        elif page.route == "/veiculos":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=80, color=ft.Colors.BLACK),
                        ft.Text("GERENCIADOR DE VEÍCULOS", size=22, weight="bold"),
                        ft.ElevatedButton(
                            "VER VEÍCULOS",
                            on_click=listar_veiculos,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        ft.ElevatedButton(
                            "ADICIONAR VEÍCULO",
                            on_click=adicionar_veiculo,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        pagelet
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/listar_veiculos":
            try:
                resposta = requests.get(
                    "http://192.168.1.83:5000/listarVeiculos",
                    headers={"Authorization": f"Bearer {get_token()}"}
                )
                dados = resposta.json()
                lista_veiculos = []

                for veiculo in dados:
                    modelo = veiculo.get("modelo", "Não informado")
                    marca = veiculo.get("marca", "Não informado")
                    cliente_id = veiculo.get("cliente_id", "Desconhecido")
                    placa = veiculo.get("placa", "Não informada")

                    lista_veiculos.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text("Modelo:", width=90, weight="bold", color="white"),
                                                ft.Text(modelo, weight="bold", expand=True, max_lines=1,
                                                        overflow="ellipsis", color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Marca:", width=90, weight="bold", color="white"),
                                                ft.Text(marca, weight="bold", expand=True, max_lines=1,
                                                        overflow="ellipsis", color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Placa:", width=90, weight="bold", color="white"),
                                                ft.Text(placa, weight="bold", expand=True, max_lines=1,
                                                        overflow="ellipsis", color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Cliente:", width=90, weight="bold", color="white"),
                                                ft.Text(f"ID {cliente_id}", weight="bold", expand=True, max_lines=1,
                                                        overflow="ellipsis", color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.ElevatedButton(
                                            text="Editar",
                                            icon=ft.Icons.EDIT,
                                            bgcolor="white",
                                            color="black",
                                            on_click=lambda e, id=veiculo.get('id_veiculo'): editar_veiculo(id, page),
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                padding=15,
                                border_radius=15,
                                bgcolor=ft.Colors.LIGHT_BLUE_300,
                                width=390,
                            ),
                            elevation=2,
                            margin=8,
                        )
                    )

            except Exception as err:
                lista_veiculos = [
                    ft.Text(f"Erro ao buscar veículos: {err}", color=ft.Colors.RED)
                ]

            page.views.append(
                ft.View(
                    "/listar_veiculos",
                    controls=[
                        ft.Text("Lista de Veículos", size=22, weight="bold"),
                        ft.Container(
                            content=ft.Column(lista_veiculos, scroll=ft.ScrollMode.ALWAYS, spacing=1),
                            expand=True,
                        ),
                        ft.ElevatedButton(
                            text="VOLTAR",
                            bgcolor="black",
                            color="white",
                            on_click=lambda e: page.go("/veiculos"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/adicionar_veiculo":
            modelo = ft.TextField(label="MODELO", border_radius=8, border_color=ft.Colors.BLACK)
            marca = ft.TextField(label="MARCA", border_radius=8, border_color=ft.Colors.BLACK)
            placa = ft.TextField(label="PLACA", border_radius=8, border_color=ft.Colors.BLACK)
            ano_fabricacao = ft.TextField(label="ANO DE FABRICAÇÃO", border_radius=8, border_color=ft.Colors.BLACK)
            cliente_id = ft.TextField(label="ID DO CLIENTE", border_radius=8, border_color=ft.Colors.BLACK)
            resultado = ft.Text("")

            msg_sucesso_veiculo = ft.SnackBar(
                content=ft.Text("Veiculo adicionado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_veiculo = ft.SnackBar(
                content=ft.Text("Falha ao adicionar Veiculo!", weight="bold", color="white"),
                bgcolor="red",
            )

            page.overlay.append(msg_sucesso_veiculo)
            page.overlay.append(msg_erro_veiculo)

            def enviar_dados(e):
                dados = {
                    "modelo": modelo.value,
                    "marca": marca.value,
                    "placa": placa.value,
                    "ano_fabricacao": ano_fabricacao.value,
                    "cliente_id": cliente_id.value,
                }
                try:
                    r = requests.post(
                        "http://192.168.1.83:5000/adicionarVeiculo",
                        json=dados,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 201:
                        page.snack_bar = msg_sucesso_veiculo
                        page.snack_bar.open = True
                        resultado.value = "Veículo cadastrado com sucesso!"
                        page.update()
                        page.go("/listar_veiculos")

                    else:
                        page.snack_bar = msg_erro_veiculo
                        page.snack_bar.open = True
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/adicionar_veiculo",
                    controls=[
                        ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=80, color=ft.Colors.BLACK),
                        ft.Text("ADICIONAR VEÍCULO", size=22, weight="bold"),
                        modelo,
                        marca,
                        placa,
                        ano_fabricacao,
                        cliente_id,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "ENVIAR",
                                    on_click=enviar_dados,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        padding=10,
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif page.route.startswith("/editar_veiculo/"):
            try:
                id_veiculo = int(page.route.split("/editar_veiculo/")[1])

                resultado = ft.Text("")

                # Snackbars
                msg_sucesso = ft.SnackBar(
                    content=ft.Text("Veículo atualizado com sucesso!", weight="bold", color="white"),
                    bgcolor="green",
                )
                msg_erro = ft.SnackBar(
                    content=ft.Text("Erro ao atualizar veículo!", weight="bold", color="white"),
                    bgcolor="red",
                )

                page.overlay.append(msg_sucesso)
                page.overlay.append(msg_erro)

                try:
                    r = requests.get(
                        "http://192.168.1.83:5000/listarVeiculos",
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        veiculos = r.json()
                        veiculo = next((v for v in veiculos if v["id_veiculo"] == id_veiculo), None)
                        if veiculo:
                            modelo = ft.TextField(
                                label="MODELO",
                                value=veiculo["modelo"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                            marca = ft.TextField(
                                label="MARCA",
                                value=veiculo["marca"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                            placa = ft.TextField(
                                label="PLACA",
                                value=veiculo["placa"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                            ano_fabricacao = ft.TextField(
                                label="ANO DE FABRICAÇÃO",
                                value=veiculo["ano_fabricacao"],
                                border_color="black",
                                border_radius=10,
                                text_style=ft.TextStyle(weight="bold")
                            )
                        else:
                            resultado = ft.Text("Veículo não encontrado.", color="red")
                    else:
                        resultado = ft.Text(f"Erro ao buscar veículo: {r.status_code}", color="red")
                except Exception as err:
                    resultado = ft.Text(f"Erro ao carregar veículo: {err}", color="red")

                def salvar_edicao(e):
                    dados = {
                        "modelo": modelo.value,
                        "marca": marca.value,
                        "placa": placa.value,
                        "ano_fabricacao": ano_fabricacao.value,
                    }
                    try:
                        r = requests.put(
                            f"http://192.168.1.83:5000/editarVeiculos/{id_veiculo}",
                            json=dados,
                            headers={"Authorization": f"Bearer {get_token()}"}
                        )
                        if r.status_code == 200:
                            page.snack_bar = msg_sucesso
                            page.snack_bar.open = True

                            import threading
                            def delayed_redirect():
                                import time
                                time.sleep(0.2)
                                page.go("/listar_veiculos")

                            threading.Thread(target=delayed_redirect).start()
                        else:
                            resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                            page.snack_bar = msg_erro
                            page.snack_bar.open = True
                    except Exception as err:
                        resultado.value = f"Erro ao salvar: {err}"
                        page.snack_bar = msg_erro
                        page.snack_bar.open = True
                    page.update()

                page.views.append(
                    ft.View(
                        f"/editar_veiculo/{id_veiculo}",
                        controls=[
                            ft.Container(
                                content=ft.Icon(name=ft.Icons.EDIT, size=60, color="black"),
                                alignment=ft.alignment.center,
                                padding=10,
                            ),
                            modelo,
                            marca,
                            placa,
                            ano_fabricacao,
                            resultado,
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text="VOLTAR",
                                        bgcolor="black",
                                        color="white",
                                        on_click=lambda e: page.go("/listar_veiculos"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                    ft.ElevatedButton(
                                        text="SALVAR",
                                        bgcolor="black",
                                        color="white",
                                        on_click=salvar_edicao,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            pagelet,
                        ],
                        padding=20,
                    )
                )

            except Exception as err:
                page.views.append(
                    ft.View(
                        "/erro",
                        controls=[
                            ft.Text(f"Erro ao abrir tela de edição: {err}", color="red")
                        ]
                    )
                )


        elif page.route == "/servicos":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Icon(name=ft.Icons.BUILD, size=80, color=ft.Colors.BLACK),
                        ft.Text("GERENCIADOR DE SERVIÇOS", size=22, weight="bold"),
                        ft.ElevatedButton(
                            "VER SERVIÇOS",
                            on_click=listar_servicos,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        ft.ElevatedButton(
                            "ADICIONAR SERVIÇO",
                            on_click=adicionar_servico,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )


        elif page.route == "/listar_servicos":
            try:
                resposta = requests.get(
                    "http://192.168.1.83:5000/listarOrdemServicos",
                    headers={"Authorization": f"Bearer {get_token()}"}
                )
                dados = resposta.json()
                lista_servicos = []

                for s in dados:
                    id_servico = s['id_servico']
                    status = s['status'].capitalize()
                    data_abertura = s['data_abertura']
                    descricao = s['descricao_servico']
                    valor = s['valor_estimado']
                    veiculo_id = s['veiculo_id']
                    data_fechamento = s.get('data_fechamento', '')

                    if status.lower() in ['terminado', 'concluído', 'finalizado'] and data_fechamento:
                        data_fechamento = data_fechamento.split('T')[0]
                    else:
                        data_fechamento = "Em andamento"

                    lista_servicos.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text("Serviço:", width=120, weight="bold", color="white"),
                                                ft.Text(descricao, expand=True, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Status:", width=120, weight="bold", color="white"),
                                                ft.Text(status, expand=True, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Abertura:", width=120, weight="bold", color="white"),
                                                ft.Text(data_abertura, expand=True, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Fechamento:", width=120, weight="bold", color="white"),
                                                ft.Text(data_fechamento, expand=True, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Valor Estimado:", width=120, weight="bold", color="white"),
                                                ft.Text(f"R${valor}", expand=True, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text("Veículo ID:", width=120, weight="bold", color="white"),
                                                ft.Text(str(veiculo_id), expand=True, color="white"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.ElevatedButton(
                                            text="Editar",
                                            icon=ft.Icons.EDIT,
                                            bgcolor="white",
                                            color="black",
                                            on_click=lambda e, id=id_servico: editar_servico(id, page),
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                        )
                                    ],
                                    spacing=6,
                                ),
                                padding=15,
                                border_radius=15,
                                bgcolor=ft.Colors.BLUE_GREY_700,
                                width=390,
                            ),
                            elevation=2,
                            margin=8,
                        )
                    )

            except Exception as err:
                lista_servicos = [
                    ft.Text(f"PRECISA ESTAR LOGADO: {err}", color=ft.Colors.RED)
                ]

            page.views.append(
                ft.View(
                    "/listar_servicos",
                    controls=[
                        ft.Text("Lista de Serviços", size=22, weight="bold"),
                        ft.Container(
                            content=ft.Column(lista_servicos, scroll=ft.ScrollMode.ALWAYS, spacing=1),
                            expand=True,
                        ),
                        ft.ElevatedButton(
                            text="VOLTAR",
                            bgcolor="black",
                            color="white",
                            on_click=lambda e: page.go("/servicos"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )


        elif page.route == "/adicionar_servico":
            valor_estimado = ft.TextField(label="VALOR ESTIMADO", border_radius=8, border_color=ft.Colors.BLACK)
            status_label = ft.Text("STATUS", weight="bold", size=14)
            status = ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="Terminado", label="Terminado"),
                    ft.Radio(value="Em andamento", label="Em andamento"),
                    ft.Radio(value="Não começou", label="Não começou"),
                ]),
                value="Não começou",
            )

            descricao_servico = ft.TextField(label="DESCRIÇÃO DO SERVIÇO", border_radius=8,
                                             border_color=ft.Colors.BLACK)

            veiculo_id = ft.TextField(label="ID DO VEÍCULO", border_radius=8, border_color=ft.Colors.BLACK)
            resultado = ft.Text("")

            msg_sucesso_servico = ft.SnackBar(
                content=ft.Text("Serviço adicionado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_servico = ft.SnackBar(
                content=ft.Text("Falha ao adicionar um Serviço!", weight="bold", color="white"),
                bgcolor="red",
            )

            page.overlay.append(msg_sucesso_servico)
            page.overlay.append(msg_erro_servico)

            def enviar_dados(e):
                dados = {
                    "valor_estimado": valor_estimado.value,
                    "status": status.value,  # Aqui já pega a opção selecionada
                    "descricao_servico": descricao_servico.value,
                    "veiculo_id": veiculo_id.value,
                }
                try:
                    r = requests.post(
                        "http://192.168.1.83:5000/adicionarOrdemServico",
                        json=dados,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 201:
                        page.snack_bar = msg_sucesso_servico
                        page.snack_bar.open = True
                        resultado.value = "Serviço cadastrado com sucesso!"
                        page.go("/servicos")
                    else:
                        page.snack_bar = msg_erro_servico
                        page.snack_bar.open = True
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/adicionar_servico",
                    controls=[
                        ft.Icon(name=ft.Icons.BUILD, size=80, color=ft.Colors.BLACK),
                        ft.Text("ADICIONAR SERVIÇO", size=22, weight="bold"),
                        valor_estimado,
                        status_label,
                        status,
                        descricao_servico,
                        veiculo_id,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "ENVIAR",
                                    on_click=enviar_dados,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        padding=10
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif page.route.startswith("/editar_servico/"):
            id_servico = page.route.split("/")[-1]

            valor_estimado = ft.TextField(
                label="VALOR ESTIMADO",
                border_radius=8,
                border_color=ft.Colors.BLACK,
                keyboard_type=ft.KeyboardType.NUMBER,
            )

            descricao_servico = ft.TextField(
                label="DESCRIÇÃO DO SERVIÇO",
                border_radius=8,
                border_color=ft.Colors.BLACK,
            )

            status_label = ft.Text("STATUS", weight="bold", size=14)
            status = ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="Terminado", label="Terminado"),
                    ft.Radio(value="Em andamento", label="Em andamento"),
                    ft.Radio(value="Não começou", label="Não começou"),
                ]),
                value="Não começou",
            )

            msg_sucesso_servico = ft.SnackBar(
                content=ft.Text("Serviço editado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_servico = ft.SnackBar(
                content=ft.Text("Falha ao editar Serviço!", weight="bold", color="white"),
                bgcolor="red",
            )

            page.overlay.append(msg_sucesso_servico)
            page.overlay.append(msg_erro_servico)

            resultado = ft.Text("")

            def salvar_edicao(e):
                dados = {
                    "valor_estimado": valor_estimado.value,
                    "status": status.value,
                    "descricao_servico": descricao_servico.value,
                }

                # Se o status for Terminado, adiciona data_fechamento
                if status.value == "Terminado":
                    from datetime import datetime
                    agora = datetime.now()
                    data_formatada = agora.strftime("%d-%m-%Y %H:%M")  # Ex: 30-07-2025 15:34
                    dados["data_fechamento"] = data_formatada

                try:
                    r = requests.put(
                        f"http://192.168.1.83:5000/editarServico/{id_servico}",
                        json=dados,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        page.snack_bar = msg_sucesso_servico
                        page.snack_bar.open = True
                        resultado.value = "Serviço editado com sucesso!"
                        page.update()
                        page.go("/listar_servicos")  # redireciona para a lista

                    elif r.status_code == 404:
                        page.snack_bar = msg_erro_servico
                        page.snack_bar.open = True
                        resultado.value = "Serviço não encontrado."
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"

                page.update()

            def buscar_dados_servico():
                try:
                    r = requests.get(
                        "http://192.168.1.83:5000/listarOrdemServicos",
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        servicos = r.json()
                        servico = next((s for s in servicos if str(s["id_servico"]) == id_servico), None)
                        if servico:
                            valor_estimado.value = str(servico["valor_estimado"])
                            status.value = servico["status"]
                            descricao_servico.value = servico["descricao_servico"]
                            resultado.value = "Serviço carregado com sucesso!"
                        else:
                            resultado.value = "Serviço não encontrado."
                    else:
                        resultado.value = f"Erro ao buscar serviço: {r.status_code}"
                except Exception as err:
                    resultado.value = f"Erro: {err}"
                page.update()

            buscar_dados_servico()

            page.views.append(
                ft.View(
                    route=f"/editar_servico/{id_servico}",
                    controls=[
                        ft.Icon(name=ft.Icons.BUILD, size=80, color=ft.Colors.BLACK),
                        ft.Text("EDITAR SERVIÇO", size=22, weight="bold"),
                        valor_estimado,
                        status_label,
                        status,
                        descricao_servico,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "VOLTAR",
                                    on_click=lambda e: page.go("/listar_servicos"),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        padding=10
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "SALVAR",
                                    on_click=salvar_edicao,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        padding=10
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )


        elif page.route == "/usuario":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Icon(name=ft.Icons.PERSON, size=80, color=ft.Colors.BLACK),
                        ft.Text("GERENCIAR USUÁRIOS", size=22, weight="bold"),
                        ft.ElevatedButton(
                            "VER USUÁRIOS",
                            on_click=listar_usuario,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        ft.ElevatedButton(
                            "CADASTRAR USUÁRIO",
                            on_click=cadastro,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        ft.ElevatedButton(
                            "LOGIN",
                            on_click=lambda e: page.go("/"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )


        elif page.route == "/cadastro":
            icone_usuario = ft.Icon(name="PERSON_ADD", size=100, color="black")

            nome = ft.TextField(
                label="NOME",
                border_radius=10,
                border_color="black",
                text_style=ft.TextStyle(weight="bold")
            )
            email = ft.TextField(
                label="EMAIL",
                border_radius=10,
                border_color="black",
                text_style=ft.TextStyle(weight="bold")
            )
            cpf = ft.TextField(
                label="CPF",
                border_radius=10,
                border_color="black",
                text_style=ft.TextStyle(weight="bold")
            )
            password = ft.TextField(
                label="SENHA",
                password=True,
                can_reveal_password=True,
                border_radius=10,
                border_color="black",
                text_style=ft.TextStyle(weight="bold")
            )
            papel = ft.TextField(
                label="PAPEL",
                hint_text="NÃO PRECISA PREENCHER ESSE CAMPO",
                hint_style=ft.TextStyle(color="grey"),
                border_radius=10,
                border_color="black",
                text_style=ft.TextStyle(weight="bold")
            )

            resultado = ft.Text()

            msg_sucesso = ft.SnackBar(
                content=ft.Text("Usuário cadastrado com sucesso!", weight="bold", color="white"),
                bgcolor="green"
            )

            msg_erro = ft.SnackBar(
                content=ft.Text("Erro ao cadastrar usuário!", weight="bold", color="white"),
                bgcolor="red"
            )

            def enviar_dados(e):
                dados = {
                    "nome": nome.value,
                    "email": email.value,
                    "cpf": cpf.value,
                    "password": password.value,
                    "papel": papel.value,
                }
                try:
                    r = requests.post("http://192.168.1.83:5000/cadastro_usuario", json=dados)
                    if r.status_code == 201:
                        page.overlay.append(msg_sucesso)
                        msg_sucesso.open = True
                        page.update()
                        page.go("/")
                    else:
                        page.overlay.append(msg_erro)
                        msg_erro.content = ft.Text(f"Erro: {r.json().get('mensagem', 'Erro desconhecido')}",
                                                   color="white")
                        msg_erro.open = True
                        page.update()
                except Exception as err:
                    page.overlay.append(msg_erro)
                    msg_erro.content = ft.Text(f"Erro na requisição: {err}", color="white")
                    msg_erro.open = True
                    page.update()

            page.views.append(
                ft.View(
                    "/cadastro",
                    controls=[
                        ft.Column(
                            [
                                icone_usuario,
                                nome,
                                email,
                                cpf,
                                password,
                                papel,
                                ft.Row(
                                    [
                                        ft.Text("JÁ TEM UMA CONTA?", weight="bold"),
                                        ft.TextButton(
                                            "ENTRE AGORA",
                                            style=ft.ButtonStyle(color="blue"),
                                            on_click=lambda e: page.go("/"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.ElevatedButton(
                                    "CRIAR",
                                    on_click=enviar_dados,
                                    style=ft.ButtonStyle(
                                        bgcolor="black",
                                        color="white",
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                    width=150,
                                    height=50,
                                ),

                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=25
                        ),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/listar_usuarios":
            try:
                resposta = requests.get(
                    "http://192.168.1.83:5000/listarUsuario",
                    headers={"Authorization": f"Bearer {get_token()}"}
                )
                dados = resposta.json()

                usuarios = []
                for u in dados:
                    usuarios.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(f"👤 Nome: {u['nome']}", size=18, weight="bold"),
                                    ft.Text(f"🆔 CPF: {u['cpf']}"),
                                    ft.Text(f"📧 Email: {u['email']}"),
                                    ft.Text(f"🛠️ Função: {u['papel']}"),
                                ]),
                                padding=10,
                                border_radius=10,
                                bgcolor=ft.Colors.BLACK26,

                            ),
                            width=450,
                        )
                    )
            except Exception as err:
                usuarios = [ft.Text(f"Erro ao buscar usuários: {err}", color=ft.Colors.RED)]

            page.views.append(
                ft.View(
                    "/listar_usuarios",
                    controls=[
                        ft.Text("Lista de Usuários", size=25, weight="bold"),
                        ft.Column(usuarios, scroll=ft.ScrollMode.ALWAYS),
                        pagelet,
                    ],
                )
            )
        page.update()


    page.on_route_change = gerenciar_rotas
    page.go("/")


ft.app(target=main)
