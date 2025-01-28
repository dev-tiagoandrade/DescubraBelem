from django.contrib.auth.models import User
from django.db import models

class CHOICE:
    # Unidade Federativa (UF)
    UF = (
        ('PA', 'Pará'),
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AM', 'Amazonas'),
        ('AP', 'Amapá'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MG', 'Minas Gerais'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('PB', 'Paraíba'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('PR', 'Paraná'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('RS', 'Rio Grande do Sul'),
        ('SC', 'Santa Catarina'),
        ('SE', 'Sergipe'),
        ('SP', 'São Paulo'),
        ('TO', 'Tocantins'),
    )
    
    CATEGORIAS = (
        ('Praia', 'Praia'),
        ('Bar', 'Bar'),
        ('Museu', 'Museu'),
        ('Igreja', 'Igreja'),
        ('Praça', 'Praça'),
        ('Mercado', 'Mercado'),
        ('Teatro', 'Teatro'),
        ('Parque', 'Parque'),
        ('Restaurante', 'Restaurante'),
        ('Café', 'Café'),
        ('Feira', 'Feira'),
        ('Trilha', 'Trilha'),
        ('Shopping', 'Shopping'),
        ('Centro Cultural', 'Centro Cultural'),
        ('Espaço Público', 'Espaço Público'),
        ('Rio', 'Rio'),
    )
    
    CATEGORIAS_PLURAL = {
        1: 'Praias',
        2: 'Bares',
        3: 'Museus',
        4: 'Igrejas',
        5: 'Praças',
        6: 'Mercados',
        7: 'Teatros',
        8: 'Parques',
        9: 'Restaurantes',
        10: 'Cafés',
        11: 'Feiras',
        12: 'Trilhas',
        13: 'Shoppings',
        14: 'Centros Culturais',
        15: 'Espaços Públicos',
        16: 'Rios'
    }
    
    class Meta:
        abstract = True


class PontoTuristico(models.Model):
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome do Ponto Turístico"
    )
    
    categoria = models.CharField(
        max_length=50,
        choices=CHOICE.CATEGORIAS,
        verbose_name="Nome do Ponto Turístico"
    )
    
    descricao = models.TextField(
        verbose_name="Descrição do Ponto Turístico"
    )
    
    site = models.URLField('URL do Ponto Turístico')
    
    foto = models.ImageField(
        upload_to='fotos/',
        null=True,
        blank=True,
        verbose_name="Foto do Ponto Turístico"
    )
    
    logradouro = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Logradouro"
    )
    numero = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Número"
    )

    bairro = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Bairro"
    )
    
    cidade = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Cidade"
    )
    uf = models.CharField(
        max_length=255,
        choices=CHOICE.UF,
        blank=True,
        null=True,
        verbose_name="Estado"
    )
    cep = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        verbose_name="CEP"
    )
    
    class Meta:
        db_table = 'ponto_turistico'
        verbose_name = 'Ponto Turístico'
        verbose_name_plural = 'Pontos Turísticos'


class Favorito(models.Model):
    ponto_turistico = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Favoritos')
    
    class Meta:
        db_table = 'favorito'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
