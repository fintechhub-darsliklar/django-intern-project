
from django.contrib import admin
from django.urls import path
from apps.transfer.views import json_rpc_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/rpc-client/', json_rpc_view, name="jsonrpc"),
]
