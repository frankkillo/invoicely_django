from rest_framework import viewsets

from invoicely.permissions import CreatorModifyOrReadOnly
from .serializers import TeamSerializer
from .models import Team


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = [CreatorModifyOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self):
        teams = self.request.user.teams.all()

        if not teams:
            Team.objects.create(
                name='First Team', 
                org_num='', 
                created_by=self.request.user
            )
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

