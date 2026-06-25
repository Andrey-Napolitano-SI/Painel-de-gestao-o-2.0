from django import forms
from .models import Produto, Movimentacao
from .models import Chamado


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = '__all__'

        widgets = {

            'nome': forms.TextInput(attrs={
                'class': 'input'
            }),

            'categoria': forms.TextInput(attrs={
                'class': 'input'
            }),

            'quantidade': forms.NumberInput(attrs={
                'class': 'input'
            }),

            'minimo': forms.NumberInput(attrs={
                'class': 'input'
            }),

            'local': forms.TextInput(attrs={
                'class': 'input'
            }),

            'status': forms.Select(attrs={
                'class': 'input'
            }),
        }


class MovimentacaoForm(forms.ModelForm):

    class Meta:
        model = Movimentacao
        fields = '__all__'
        widgets = {
    'produto': forms.Select(attrs={'class': 'input'}),
    'tipo': forms.Select(attrs={'class': 'input'}),
    'quantidade': forms.NumberInput(attrs={'class': 'input'}),
    'responsavel': forms.TextInput(attrs={'class': 'input'}),
}

class ChamadoForm(forms.ModelForm):

    class Meta:
        model = Chamado
        fields = ['titulo', 'categoria', 'descricao']