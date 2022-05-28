import pdfkit

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from rest_framework import viewsets
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from invoicely.permissions import CreatorModifyOrReadOnly

from .serializers import InvoiceSerializer
from .models import Invoice
from team.models import Team


class InvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [CreatorModifyOrReadOnly]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        queryset =  self.queryset.filter(created_by=self.request.user)

        unpaid = self.kwargs.get('unpaid')

        if not unpaid:
            return queryset      

        if unpaid == 'yes':
            return queryset.filter(is_paid=False, is_credited=False)
        else:
            raise Http404('Request is not valid')      


    def perform_create(self, serializer):
        team = self.request.user.teams.first()
        invoice_number = team.first_invoice_number
        team.first_invoice_number = invoice_number + 1
        team.save()
        serializer.save(
            created_by=self.request.user,
            modified_by=self.request.user, 
            team=team, 
            invoice_number=invoice_number,
            bankaccount=team.bankaccount
        )


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    template_name = 'pdf.html'

    if invoice.is_credit_for:
        template_name = 'pdf_creditnote.html'

    template = get_template(template_name)
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    subject = 'Updaid invoice'
    from_email = team.email
    to_email = [invoice.client.email]
    text_content = f'You have an unpaid invoice. Invoice number: #{invoice.invoice_number}'
    html_content = f'You have an unpaid invoice. Invoice number: #{invoice.invoice_number}'

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, 'text/html')

    template = get_template('pdf.html')
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})

    if pdf:
        name = f'invoice_{invoice.invoice_number}.pdf'
        msg.attach(name, pdf, 'application/pdf')

    msg.send()

    return Response()
