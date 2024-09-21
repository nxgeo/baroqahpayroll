from django.urls import path

from payrolls import views

urlpatterns = [path("payslips/<int:salary_id>/", views.payslip_view, name="payslip")]
