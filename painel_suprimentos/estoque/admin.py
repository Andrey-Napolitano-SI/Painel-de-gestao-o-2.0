from django.contrib import admin
from .models import Produto, Movimentacao


admin.site.register(Produto)
admin.site.register(Movimentacao)