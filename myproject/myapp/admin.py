from django.contrib import admin
from myproject.myapp.models import Document 
from myproject.myapp.models import Piece
from myproject.myapp.models import Banned 
from django.utils.safestring import mark_safe
from django.conf import settings
(r'^public/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),

#admin.site.register(Piece)

# Register your models here.

fields = ( 'admin_thumbnail')
readonly_fields = ['admin_thumbnail']



class DocumentAdmin(admin.ModelAdmin):
    models = Document
    
    list_display = [ 'admin_thumbnail', 'admin_thumbnail_mosaic', 'identifier', 'owner', 'created_date', 'divx', 'divy']
    
    search_fields = ('identifier', 'owner', 'created_date')
    
    def get_date(self, obj):
        return obj.created_date

    get_date.admin_order_field  = 'created_date'  #Allows column order sorting
    #get_date.short_description = 'Creation date'  #Renames column head

class PieceAdmin(admin.ModelAdmin):
    models = Piece
    
    list_display = [ 'admin_thumbnail_piece', 'state', 'documentidentifier', 'identifier', 'owner', 'given_date', 'ip']
    
    search_fields = ('documentidentifier', 'state', 'identifier', 'owner', 'given_date', 'ip')
    
    def get_date_piece(self, obj):
        return obj.given_date

    get_date_piece.admin_order_field  = 'given_date'  #Allows column order sorting
    #get_date.short_description = 'Creation date'  #Renames column head

class BannedAdmin(admin.ModelAdmin):
    models = Banned
    
    search_fields = ('documentidentifier', 'identifier', 'ip')
    
    list_display = [ 'ip', 'documentidentifier', 'identifier']
    

admin.site.register(Document, DocumentAdmin)
admin.site.register(Piece, PieceAdmin)
admin.site.register(Banned, BannedAdmin)