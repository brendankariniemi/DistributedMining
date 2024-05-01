from django.contrib import admin
from .models import Pool, Hardware, Block, Reward

admin.site.register(Pool)
admin.site.register(Hardware)
admin.site.register(Block)
admin.site.register(Reward)