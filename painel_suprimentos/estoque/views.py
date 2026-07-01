from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Produto, Movimentacao, Chamado
from .forms import ProdutoForm, MovimentacaoForm, ChamadoForm, ChamadoEditForm

def somente_admin(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_staff:
            return HttpResponseForbidden("Acesso negado.")

        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def redirecionar_usuario(request):

    if request.user.is_staff:
        return redirect('dashboard')

    else:
        return redirect('abrir_chamado')


@login_required
@somente_admin
def dashboard(request):

    produtos = Produto.objects.all()
    movimentacoes = Movimentacao.objects.order_by('-data')[:5]

    total_itens = produtos.count()
    itens_baixos = produtos.filter(status='BAIXO').count()
    itens_criticos = produtos.filter(status='CRITICO').count()

    context = {
        'produtos': produtos,
        'movimentacoes': movimentacoes,
        'total_itens': total_itens,
        'itens_baixos': itens_baixos,
        'itens_criticos': itens_criticos,
    }

    return render(request, 'estoque/dashboard.html', context)


@login_required
@somente_admin
def produtos(request):

    status = request.GET.get('status')
    if status:
        produtos = Produto.objects.filter(status=status)
    else:
        produtos = Produto.objects.all()

    return render(request, 'estoque/produtos.html', {
        'produtos': produtos
    })


@login_required
@somente_admin
def movimentacoes(request):

    movimentacoes = Movimentacao.objects.all().order_by('-data')

    return render(request, 'estoque/movimentacoes.html', {
        'movimentacoes': movimentacoes
    })


@login_required
@somente_admin
def cadastrar_item(request):

    if request.method == 'POST':

        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('produtos')

    else:
        form = ProdutoForm()

    return render(request, 'estoque/cadastrar_item.html', {
        'form': form
    })


@login_required
@somente_admin
def cadastrar_movimentacao(request):

    if request.method == 'POST':

        form = MovimentacaoForm(request.POST)

        if form.is_valid():

            movimentacao = form.save()

            produto = movimentacao.produto

            if movimentacao.tipo == 'ENTRADA':
                produto.quantidade += movimentacao.quantidade

            else:
                produto.quantidade -= movimentacao.quantidade

            if produto.quantidade <= 0:
                produto.status = 'CRITICO'

            elif produto.quantidade <= produto.minimo:
                produto.status = 'BAIXO'

            else:
                produto.status = 'OK'

            produto.save()

            return redirect('movimentacoes')

    else:
        form = MovimentacaoForm()

    return render(request, 'estoque/cadastrar_movimentacao.html', {
        'form': form
    })


@login_required
@somente_admin
def editar_item(request, id):

    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':

        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():

            form.save()

            return redirect('produtos') 

    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'estoque/editar_item.html', {
        'form': form,
        'produto': produto
    })


@login_required
@somente_admin
def estoque_baixo(request):

    produtos = Produto.objects.filter(status='BAIXO')

    return render(request, 'estoque/estoque_baixo.html', {
        'produtos': produtos
    })


@login_required
def abrir_chamado(request):

    if request.method == 'POST':

        form = ChamadoForm(request.POST)

        if form.is_valid():

            chamado = form.save(commit=False)

            chamado.usuario = request.user

            chamado.save()

            return redirect('meus_chamados')

    else:

        form = ChamadoForm()

    return render(request, 'estoque/abrir_chamado.html', {
        'form': form
    })
  


@login_required
def meus_chamados(request):

    chamados = Chamado.objects.filter(
        usuario=request.user
    ).order_by('-data_abertura')

    return render(request, 'estoque/meus_chamados.html', {
        'chamados': chamados
    })


@login_required
def chamados_admin(request):

    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado.")

    chamados = Chamado.objects.all().order_by('-data_abertura')

    return render(request, 'estoque/chamados_admin.html', {
        'chamados': chamados
    })


@login_required
def detalhe_chamado(request, id):

    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado.")

    chamado = get_object_or_404(Chamado, id=id)

    if request.method == 'POST':

        novo_status = request.POST.get('status')

        chamado.status = novo_status
        chamado.save()

        return redirect('detalhe_chamado', id=chamado.id)

    return render(request, 'estoque/detalhe_chamado.html', {
        'chamado': chamado
    })


@login_required
@somente_admin
def editar_chamado(request, id):

    chamado = get_object_or_404(Chamado, id=id)

    if request.method == 'POST':
        form = ChamadoEditForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
            return redirect('detalhe_chamado', id=chamado.id)
    else:
        form = ChamadoEditForm(instance=chamado)

    return render(request, 'estoque/editar_chamado.html', {
        'form': form,
        'chamado': chamado
    })


@login_required
def excluir_chamado(request, id):

    chamado = get_object_or_404(Chamado, id=id)

    chamado.delete()

    return redirect('chamados_admin')
