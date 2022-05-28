from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, generate_pdf, send_reminder


router = DefaultRouter()
router.register('invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('invoices/<int:invoice_id>/generate-pdf/', generate_pdf, name='generate-pdf'),
    path('invoices/<int:invoice_id>/send-reminder/', send_reminder, name='send-reminder'),
    path('invoices/unpaid/<str:unpaid>/', InvoiceViewSet.as_view({"get": "list"}), name="invoicee-unpaid")
]