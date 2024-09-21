from django.contrib import admin
from django.urls import include, path

admin.site.site_title = "Baroqah Payroll"
admin.site.site_header = "Baroqah Payroll"
admin.site.index_title = "Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("payrolls.urls")),
]
