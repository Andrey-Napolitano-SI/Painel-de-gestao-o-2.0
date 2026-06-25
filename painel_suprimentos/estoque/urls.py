from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.redirecionar_usuario,
        name='inicio'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'produtos/',
        views.produtos,
        name='produtos'
    ),

    path(
        'movimentacoes/',
        views.movimentacoes,
        name='movimentacoes'
    ),

    path(
        'cadastrar-item/',
        views.cadastrar_item,
        name='cadastrar_item'
    ),

    path(
        'editar-item/<int:id>/',
        views.editar_item,
        name='editar_item'
    ),

    path(
        'cadastrar-movimentacao/',
        views.cadastrar_movimentacao,
        name='cadastrar_movimentacao'
    ),

    path(
        'estoque-baixo/',
        views.estoque_baixo,
        name='estoque_baixo'
    ),

    path(
        'abrir-chamado/',
        views.abrir_chamado,
        name='abrir_chamado'
    ),

    path('redirecionar/'
    , views.redirecionar_usuario, 
    name='redirecionar_usuario'),

    
    path('meus-chamados/',
    views.meus_chamados,
    name='meus_chamados'
),


   path('chamados-admin/', 
   views.chamados_admin, 
   name='chamados_admin'),

   path('chamado/<int:id>/', 
   views.detalhe_chamado, 
   name='detalhe_chamado'),

   path(
    'chamado/editar/<int:id>/',
    views.editar_chamado,
    name='editar_chamado'
),

path(
    'chamado/excluir/<int:id>/',
    views.excluir_chamado,
    name='excluir_chamado'
),
 
]
