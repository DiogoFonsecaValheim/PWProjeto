from django.contrib import admin
from django.utils.html import format_html
from .models import Post
from .models import Comen
from .models import Rating

admin.site.register(Post)
admin.site.register(Comen)
admin.site.register(Rating)