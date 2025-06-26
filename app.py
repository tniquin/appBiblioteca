import flet as ft
import requests


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

    #CLIENTE

    def ir_listar_clientes(e):
        page.go("/listar_clientes")

    def ir_para_adicionar(e):
        page.go("/adicionar")

    def ir_para_editar(e):
        page.go("/editar")

    #VEICULO

    def listar_veiculos(e):
        page.go("/listar_veiculos")

    def adicionar_veiculo(e):
        page.go("/adicionar_veiculo")

    def editar_veiculo(e):
        page.go("/editar_veiculo")


    #SERVIÇÕS

    def listar_servicos(e):
        page.go("/listar_servicos")

    def adicionar_servico(e):
        page.go("/adicionar_servico")

    def editar_servico(e):
        page.go("/editar_servico")


    #Usuario

    def cadastro(e):
        page.go("/cadastro")

    def login(e):
        page.go("/login")

    def listar_usuario(e):
        page.go("/listar_usuarios")

    def alterar_status_cliente(id_cliente):
        try:
            r = requests.patch(
                f"http://192.168.1.83:5000/alterarStatusCliente/{id_cliente}",
                headers={"Authorization": f"Bearer {get_token()}"}
            )
            if r.status_code == 200:
                page.go("/listar_clientes")  # Recarrega a lista
        except Exception as e:
            print(f"Erro ao alterar status: {e}")

    def ir_para_clientes(e):
        page.go("/clientes")

    def ir_para_veiculos(e):
        page.go("/veiculos")

    def ir_para_servico(e):
        page.go("/servicos")

    def usuario(e):
        page.go("/usuario")

    pagelet = ft.Pagelet(
        content=ft.Container(),  # conteúdo será atualizado nas rotas
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
            page.views.append(
                ft.View(
                    "/",
                    controls=[
                        ft.Text("Bem-vindo!", size=30),

                        pagelet
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                )
            )

        elif page.route == "/login":
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

            # Adiciona os Snackbars no overlay UMA VEZ
            page.overlay.append(msg_sucesso_login)
            page.overlay.append(msg_erro_login)

            def verificar_login(e):
                dados = {
                    "email": email.value,
                    "senha": password.value,
                }
                try:
                    resposta = requests.post("http://192.168.1.83:5000/login", json=dados)
                    print(resposta.text)
                    if resposta.status_code == 200:
                        set_token(resposta.json().get('access_token'))


                        # Mostra o Snackbar de sucesso antes de trocar de página
                        msg_sucesso_login.open = True
                        page.update()

                        # Pequeno delay pra dar tempo do usuário ver o Snackbar antes de redirecionar
                        import threading
                        def delayed_redirect():
                            import time
                            time.sleep(0.4)  # 1 segundo
                            page.go("/")

                        threading.Thread(target=delayed_redirect).start()

                    else:
                        # Atualiza o conteúdo antes de abrir
                        msg_erro_login.content = ft.Text(f"Erro: {resposta.status_code} - {resposta.text}",
                                                         weight="bold", color="white")
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

        elif page.route == "/clientes":
            page.views.append(

                ft.View(
                    controls=[
                        ft.Text("clientes!", size=30),
                        ft.ElevatedButton("Ver Clientes", on_click=ir_listar_clientes),
                        ft.ElevatedButton("Adicionar Cliente", on_click=ir_para_adicionar),
                        pagelet
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                )

            ),

        elif page.route == "/listar_clientes":
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
                                            on_click=lambda e, id=cliente.get('id_cliente'): page.go(f"/editar/{id}"),
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.VISIBILITY_OFF if not cliente.get('ativo',
                                                                                            True) else ft.Icons.VISIBILITY,
                                            icon_color="white",
                                            bgcolor="black",
                                            on_click=lambda e, id=cliente.get('id_cliente'): alterar_status_cliente(id),

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

                    pagelet

                    ],
                )
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


            msg_sucesso_cliente = ft.SnackBar(
                content=ft.Text("Cliente cadastrado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_cliente = ft.SnackBar(
                content=ft.Text("Falha ao cadastrar cliente!", weight="bold", color="white"),
                bgcolor="red",
            )

            # Adiciona os Snackbars no overlay UMA VEZ
            page.overlay.append(msg_sucesso_cliente)
            page.overlay.append(msg_erro_cliente)


            resultado = ft.Text("")

            def enviar_dados(e):
                dados = {
                    "nome": nome.value,
                    "cpf": cpf.value,
                    "telefone": telefone.value,
                    "endereco": endereco.value,
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
                        ft.Container(padding=5,),
                        cpf,
                        ft.Container(padding=5,),
                        telefone,
                        ft.Container(padding=5,),
                        endereco,

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

                # Buscar dados do cliente
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
                        else:
                            page.snack_bar = msg_erro_login
                            page.snack_bar.open = True
                    except Exception as err:
                        resultado = ft.Text(f"Erro ao salvar: {err}", color="red")
                        page.snack_bar = msg_erro_login
                        page.snack_bar.open = True
                    page.update()

                # Montar tela
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
                        ft.ElevatedButton(
                            "EDITAR VEÍCULO",
                            on_click=editar_veiculo,
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
                veiculos = [
                    ft.Container(
                        content=ft.Text(
                            f"Modelo: {v['modelo']} | Marca: {v['marca']} | Placa: {v['placa']} | Cliente ID: {v['cliente_id']}",
                            size=16
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.BLACK),
                        border_radius=8,
                        margin=5,
                        bgcolor=ft.Colors.WHITE,
                    )
                    for v in dados
                ]
            except Exception as err:
                veiculos = [
                    ft.Text(
                        f"Erro ao buscar veículos: {err}",
                        color=ft.Colors.RED
                    )
                ]

            page.views.append(
                ft.View(
                    "/listar_veiculos",
                    controls=[
                        ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=70, color=ft.Colors.BLACK),
                        ft.Text("LISTA DE VEÍCULOS", size=22, weight="bold"),
                        ft.Column(veiculos, scroll=ft.ScrollMode.ALWAYS),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
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

        elif page.route == "/editar_veiculo":
            id_veiculo = ft.TextField(label="ID DO VEÍCULO PARA EDITAR", border_radius=8, border_color=ft.Colors.BLACK,
                                      width=250)
            modelo = ft.TextField(label="MODELO", border_radius=8, border_color=ft.Colors.BLACK)
            marca = ft.TextField(label="MARCA", border_radius=8, border_color=ft.Colors.BLACK)
            placa = ft.TextField(label="PLACA", border_radius=8, border_color=ft.Colors.BLACK)
            ano_fabricacao = ft.TextField(label="ANO DE FABRICAÇÃO", border_radius=8, border_color=ft.Colors.BLACK)

            resultado = ft.Text("")

            msg_sucesso_veiculo = ft.SnackBar(
                content=ft.Text("Veiculo editado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_veiculo = ft.SnackBar(
                content=ft.Text("Falha ao editar Veiculo!", weight="bold", color="white"),
                bgcolor="red",
            )

            msg_sucesso_busca = ft.SnackBar(
                content=ft.Text("Veiculo encontrado com sucesso!", weight="bold", color="white"),
                bgcolor="green",
            )

            msg_erro_busca = ft.SnackBar(
                content=ft.Text("Falha ao buscar Veiculo!", weight="bold", color="white"),
                bgcolor="red",
            )

            page.overlay.append(msg_sucesso_veiculo)
            page.overlay.append(msg_erro_veiculo)

            page.overlay.append(msg_sucesso_busca)
            page.overlay.append(msg_erro_busca)
            def buscar_veiculo(e):
                try:
                    r = requests.get(
                        "http://192.168.1.83:5000/listarVeiculos",
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        veiculos = r.json()
                        page.snack_bar = msg_sucesso_busca
                        page.snack_bar.open = True
                        veiculo = next((v for v in veiculos if v["id_veiculo"] == int(id_veiculo.value)), None)
                        if veiculo:
                            modelo.value = veiculo["modelo"]
                            marca.value = veiculo["marca"]
                            ano_fabricacao.value = veiculo["ano_fabricacao"]
                            placa.value = veiculo["placa"]
                            page.snack_bar = msg_sucesso_busca
                            page.snack_bar.open = True
                            resultado.value = "Veículo encontrado. Edite os dados e clique em salvar."
                        else:
                            page.snack_bar = msg_erro_busca
                            page.snack_bar.open = True
                            resultado.value = "Veículo não encontrado."
                    else:
                        page.snack_bar = msg_erro_busca
                        page.snack_bar.open = True
                        resultado.value = f"Erro ao buscar veículo: {r.status_code}"
                except Exception as err:
                    page.snack_bar = msg_erro_busca
                    page.snack_bar.open = True
                    resultado.value = f"Erro: {err}"
                page.update()

            def salvar_edicao(e):
                if not id_veiculo.value.strip():
                    resultado.value = "Informe o ID do veículo para editar."
                    page.update()
                    return

                dados = {
                    "modelo": modelo.value,
                    "marca": marca.value,
                    "placa": placa.value,
                    "ano_fabricacao": ano_fabricacao.value,
                }
                try:
                    r = requests.put(
                        f"http://192.168.1.83:5000/editarVeiculos/{id_veiculo.value}",
                        json=dados,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        page.snack_bar = msg_sucesso_veiculo
                        page.snack_bar.open = True
                        resultado.value = "Veículo editado com sucesso!"
                    elif r.status_code == 404:
                        page.snack_bar = msg_erro_veiculo
                        page.snack_bar.open = True
                        resultado.value = "Veículo não encontrado."
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/editar_veiculo",
                    controls=[
                        ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=80, color=ft.Colors.BLACK),
                        ft.Text("EDITAR VEÍCULO", size=22, weight="bold"),
                        id_veiculo,
                        ft.ElevatedButton(
                            "BUSCAR VEÍCULO",
                            on_click=buscar_veiculo,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10,
                            ),
                        ),
                        modelo,
                        marca,
                        placa,
                        ano_fabricacao,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "SALVAR",
                                    on_click=salvar_edicao,
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
                        ft.ElevatedButton(
                            "EDITAR SERVIÇO",
                            on_click=editar_servico,
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
                servicos = [
                    ft.Container(
                        content=ft.Text(
                            f"Data de abertura: {s['data_abertura']} | Serviço: {s['descricao_servico']} | "
                            f"Status: {s['status']}"
                            + (f" | Data de fechamento: {s['data_fechamento'].split('T')[0]}" if s[
                                'status'].lower() in ['terminado', 'concluído', 'finalizado'] and s['data_fechamento'] else "")
                            + f" | Valor: R${s['valor_estimado']} | Veículo ID: {s['veiculo_id']}",
                            size=16
                        ),
                        padding=10,
                        margin=5,
                        border=ft.border.all(1, ft.Colors.BLACK),
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE
                    )
                    for s in dados
                ]


            except Exception as err:
                servicos = [
                    ft.Text(f"PRECISA ESTAR LOGADO: {err}", color=ft.Colors.RED)
                ]

            page.views.append(
                ft.View(
                    "/listar_servicos",
                    controls=[
                        ft.Icon(name=ft.Icons.BUILD, size=70, color=ft.Colors.BLACK),
                        ft.Text("LISTA DE SERVIÇOS", size=22, weight="bold"),
                        ft.Column(servicos, scroll=ft.ScrollMode.ALWAYS),
                        pagelet,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
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
            data_abertura = ft.TextField(label="DATA DE ABERTURA", border_radius=8, border_color=ft.Colors.BLACK)
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
                    "data_abertura": data_abertura.value,
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
                        data_abertura,
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

        elif page.route == "/editar_servico":
            id_servico = ft.TextField(
                label="ID DO SERVIÇO PARA EDITAR",
                border_radius=8,
                border_color=ft.Colors.BLACK,
                width=250
            )
            valor_estimado = ft.TextField(
                label="VALOR ESTIMADO",
                border_radius=8,
                border_color=ft.Colors.BLACK,
                keyboard_type=ft.KeyboardType.NUMBER,
            )

            descricao_servico = ft.TextField(
                label="DESCRIÇÃO DO SERVIÇO",
                border_radius=8,
                border_color=ft.Colors.BLACK
            )

            status_label = ft.Text("STATUS", weight="bold", size=14)
            status = ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="Terminado", label="Terminado"),
                    ft.Radio(value="Em andamento", label="Em andamento"),
                    ft.Radio(value="Não começou", label="Não começou"),
                ]),
                value="Não começou",  # valor padrão
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

            def buscar_servico(e):
                try:
                    r = requests.get(
                        "http://192.168.1.83:5000/listarOrdemServicos",
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        servicos = r.json()
                        servico = next((s for s in servicos if s["id_servico"] == int(id_servico.value)), None)
                        if servico:
                            valor_estimado.value = servico["valor_estimado"]
                            status.value = servico["status"]
                            descricao_servico.value = servico["descricao_servico"]
                            data_abertura.value = servico["data_abertura"]
                            resultado.value = "Serviço encontrado. Edite os dados e clique em salvar."
                        else:
                            resultado.value = "Serviço não encontrado."
                    else:
                        resultado.value = f"Erro ao buscar serviço: {r.status_code}"
                except Exception as err:
                    resultado.value = f"Erro: {err}"
                page.update()

            def salvar_edicao(e):
                if not id_servico.value.strip():
                    resultado.value = "Informe o ID do serviço para editar."
                    page.update()
                    return

                dados = {
                    "valor_estimado": valor_estimado.value,
                    "status": status.value,
                    "descricao_servico": descricao_servico.value,
                }
                try:
                    r = requests.put(
                        f"http://192.168.1.83:5000/editarServico/{id_servico.value}",
                        json=dados,
                        headers={"Authorization": f"Bearer {get_token()}"}
                    )
                    if r.status_code == 200:
                        page.snack_bar = msg_sucesso_servico
                        page.snack_bar.open = True
                        resultado.value = "Serviço editado com sucesso!"
                    elif r.status_code == 404:
                        page.snack_bar = msg_erro_servico
                        page.snack_bar.open = True
                        resultado.value = "Serviço não encontrado."
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/editar_servico",
                    controls=[
                        ft.Icon(name=ft.Icons.BUILD, size=80, color=ft.Colors.BLACK),
                        ft.Text("EDITAR SERVIÇO", size=22, weight="bold"),
                        id_servico,
                        ft.ElevatedButton(
                            "BUSCAR SERVIÇO",
                            on_click=buscar_servico,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLACK,
                                color=ft.Colors.WHITE,
                                padding=10
                            ),
                        ),
                        valor_estimado,
                        status_label,
                        status,
                        descricao_servico,
                        ft.Row(
                            [
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
                            on_click=login,
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
                        page.go("/")  # redireciona depois
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
                                            on_click=lambda e: page.go("/login"),
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
                resposta = requests.get("http://192.168.1.83:5000/listarUsuario",
                                        headers={"Authorization": f"Bearer {get_token()}"})
                dados = resposta.json()
                usuarios = [
                    ft.Text(
                        f"Nome: {u['nome']} | CPF: {u['cpf']} | Email: {u['email']} | Função: {u['papel']}"
                    )
                    for u in dados
                ]
            except Exception as err:
                usuarios = [ft.Text(f"Erro ao buscar usuario: {err}")]

            page.views.append(
                ft.View(
                    "/listar_usuarios",
                    controls=[
                        ft.Text("Lista de Usuarios", size=25, weight="bold"),
                        ft.Column(usuarios, scroll=ft.ScrollMode.ALWAYS),
                        pagelet,
                    ],
                )
            )
        page.update()

    page.on_route_change = gerenciar_rotas
    page.go("/")


ft.app(target=main)
