from django.http import Http404

from rest_framework import viewsets

from invoicely.permissions import CreatorModifyOrReadOnly

from .serializers import ClientSerializer
from .models import Client


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [CreatorModifyOrReadOnly]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset =  self.queryset.filter(created_by=self.request.user)

        newests = self.kwargs.get('newests')
        
        if not newests:
            return queryset
        
        if newests == 'yes':
            return  queryset[:6]
        else:
            raise Http404('Request is not valid')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)