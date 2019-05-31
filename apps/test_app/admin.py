from django.contrib import admin
from .models import Knowledge, Graph, GraphEdge


@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']



@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(GraphEdge)
class GraphEdgeAdmin(admin.ModelAdmin):
    list_display = ['graph_id', 'from_id', 'to_id']

