from django.contrib import admin

from models import Tree, TreeNode


# Register your models here.
@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    change_list_template = 'admin/tree_change_list.html'
    list_display = ('name',)
    fields = ('name',)

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.nestable.min.js',
            'js/tree_submit.js',
        )

        css = {
            'all': ('css/jquery.nestable.min.css', 'css/column.css')
        }


@admin.register(TreeNode)
class TreeNodeAdmin(admin.ModelAdmin):
    pass
