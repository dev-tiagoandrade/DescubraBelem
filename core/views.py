from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from core.forms import *

class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_usuariosenticated_user = True  # Redireciona usuário logado
    
    def form_invalid(self, form):
        print("Formulário inválido:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class SingUpView(FormView):
    template_name = "singup.html"
    form_class = AddUsuarioForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Cria o usuário com a senha criptografada
        user = User.objects.create_user(username=username, email=email, password=password)

        # Autentica e faz login do usuário automaticamente
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Exibe mensagens de erro ao usuário.
        """
        messages.error(self.request,
                       "Houve um erro ao criar o Usuário. Por favor, corrija os campos destacados.")
        return super().form_invalid(form)


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        
        # Praias (categoria = 1)
        praias = (
            PontoTuristico.objects.filter(categoria=1)
            .annotate(num_favoritos=Count('favorito'))
            .order_by('-id')[:3]
        )
        
        for praia in praias:
            praia.is_favorito = praia.favorito_set.filter(usuario=self.request.user).exists()
        
        context['praias'] = sorted(praias, key=lambda p: p.nome)
        
        cafes = (
            PontoTuristico.objects.filter(categoria=10)
            .annotate(num_favoritos=Count('favorito'))
            .order_by('-id')[:3]
        )
        
        for cafe in cafes:
            cafe.is_favorito = cafe.favorito_set.filter(usuario=self.request.user).exists()
        
        context['cafes'] = sorted(cafes, key=lambda p: p.nome)
        
        # Pontos turísticos
        pontos = (
            PontoTuristico.objects.all()
            .annotate(num_favoritos=Count('favorito'))
            .order_by('-id')[:3]
        )
        
        for ponto in pontos:
            ponto.is_favorito = ponto.favorito_set.filter(usuario=self.request.user).exists()
        
        context['pontos'] = sorted(pontos, key=lambda p: p.nome)
        
        return context
    
    def post(self, request, *args, **kwargs):
        busca = request.POST.get('busca')
        if busca != "":
            queryset = PontoTuristico.objects.filter(
                Q(nome__icontains=busca) | Q(categoria__icontains=busca)
            ).annotate(num_favoritos=Count('favorito')).order_by('-id')[:3]
            return render(request, self.template_name, {'pontos': queryset, 'busca': busca})
        return super().get(request, *args, **kwargs)


class Categorias(LoginRequiredMixin, TemplateView):
    template_name = 'core/categorias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Inicializar um dicionário para armazenar os pontos turísticos por categoria
        pontos_por_categoria = {}
        
        for id, nome in CHOICE.CATEGORIAS:
            # Buscar os 3 primeiros pontos turísticos de cada categoria
            pontos = (
                PontoTuristico.objects.filter(categoria=id)
                .annotate(num_favoritos=Count('favorito'))
                .order_by('-id')[:3]
            )
            # Adicionar ao contexto, com a chave sendo o nome da categoria
            
            for ponto in pontos:
                ponto.is_favorito = ponto.favorito_set.filter(usuario=self.request.user).exists()
            
            pontos_por_categoria[nome] = sorted(pontos, key=lambda p: p.nome)
            
        
        # Adicionar o dicionário ao contexto
        context['pontos_por_categoria'] = pontos_por_categoria
        
        return context


class FavoritarPonto(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuário não autenticado'}, status=403)
        
        ponto_id = kwargs.get('ponto_id')
        
        try:
            ponto = PontoTuristico.objects.get(id=ponto_id)
        except PontoTuristico.DoesNotExist:
            return JsonResponse({'error': 'Ponto turístico não encontrado'}, status=404)
        
        # Verificar se já é favorito
        favorito = Favorito.objects.filter(ponto_turistico=ponto, usuario=request.user).first()
        
        if favorito:
            # Caso já exista, remova o favorito
            favorito.delete()
            return JsonResponse({'message': 'Favorito removido'}, status=200)
        else:
            # Caso contrário, crie o favorito
            Favorito.objects.create(ponto_turistico=ponto, usuario=request.user)
            return JsonResponse({'message': 'Favoritado com sucesso'}, status=201)

class Favoritos(LoginRequiredMixin, TemplateView):
    template_name = 'core/favoritos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todos os pontos turísticos favoritados pelo usuário
        favoritos = (
            PontoTuristico.objects.filter(favorito__usuario=self.request.user)
            .annotate(num_favoritos=Count('favorito'))
            .order_by('nome')  # Ordenar alfabeticamente por nome
        )
        
        for favorito in favoritos:
            favorito.is_favorito = favorito.favorito_set.filter(usuario=self.request.user).exists()
        
        # Adicionar os favoritos ao contexto
        context['favoritos'] = favoritos
        
        return context

class AddLocal(FormView):
    template_name = 'core/add_ponto_turistico.html'
    form_class = AddLocalForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        try:
            form.save()  # Salva os dados no banco de dados
            messages.success(self.request, "Ponto Turístico adicionado com sucesso!")
        except Exception as e:
            messages.error(self.request, f"Erro ao salvar: {e}")
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Exibe mensagens de erro ao usuário.
        """
        messages.error(self.request, "Houve um erro ao criar o Ponto Turístico. Por favor, corrija os campos destacados.")
        return super().form_invalid(form)