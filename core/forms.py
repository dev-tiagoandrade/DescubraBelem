from django.contrib.auth.forms import AuthenticationForm

from .models import *
from django.forms import *


class LoginForm(AuthenticationForm):
    username = CharField()
    password = CharField(widget=PasswordInput)


class AddUsuarioForm(Form):
    username = CharField(max_length=150, required=True, label="Nome de Usuário")
    email = EmailField(required=True, label="Email")
    password = CharField(widget=PasswordInput, required=True, label="Senha")


class AddLocalForm(ModelForm):
    nome = CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. Estação das Docas'
        }),
        label="Nome do Ponto Turístico"
    )

    categoria = ChoiceField(
        choices=CHOICE.CATEGORIAS,
        widget=Select(attrs={
            'class': 'form-select form-select-solid',
        }),
        label="Categoria"
    )

    descricao = CharField(
        widget=Textarea(attrs={
            'class': 'form-control form-control-solid',
            'rows': 3,
            'placeholder': 'Descreva o ponto turístico'
        }),
        label="Descrição do Ponto Turístico"
    )

    site = URLField(
        widget=URLInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. https://www.exemplo.com'
        }),
        label="URL do Ponto Turístico",
        required=False
    )

    logradouro = CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. Rua da Paz'
        }),
        label="Logradouro",
        required=False
    )

    numero = CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. 123'
        }),
        label="Número",
        required=False
    )

    bairro = CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. Centro'
        }),
        label="Bairro",
        required=False
    )

    cidade = CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. Belém'
        }),
        label="Cidade",
        required=False
    )

    uf = ChoiceField(
        choices=CHOICE.UF,
        widget=Select(attrs={
            'class': 'form-select form-select-solid',
        }),
        label="Estado",
        required=False
    )

    cep = CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-solid',
            'placeholder': 'Ex. 66000-000',
            'maxlength': 9
        }),
        label="CEP",
        required=False
    )

    class Meta:
        model = PontoTuristico
        fields = [
            'nome', 'categoria', 'descricao', 'site', 'foto',
            'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep'
        ]
