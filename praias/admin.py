from django.contrib import admin
from django.utils.html import format_html
from .models import Regiao
from .models import Servico
from .models import Praia

admin.site.register(Regiao)
admin.site.register(Servico)
admin.site.register(Praia)