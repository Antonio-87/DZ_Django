from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement, Favourite
from .serializers import AdvertisementSerializer, FavouriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdvertisementFilter
from .permissions import AuthorRights
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter


    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ["destroy", "update", "partial_update"]:
            return [AuthorRights()]
        return []

    def get_queryset(self):
        """Набор queryset для получения объекта(get_object)"""

        queryset = Advertisement.objects.filter(status__in=["OPEN", "CLOSED"])
        if self.request.user.is_authenticated:
            draft = Advertisement.objects.filter(creator=self.request.user, status="DRAFT")
            return queryset | draft
        return queryset

    @action(detail=True, methods=['POST'], url_path=r'add_fav')
    def add_fav(self, request, pk=None):
        """Добавляет в избранное"""

        advertisement = self.get_object()
        adv_favourites = Favourite.objects.filter(user=self.request.user).filter(
            advertisement=advertisement.id)
        
        if adv_favourites.exists():
            raise ValidationError({'error': 'Объявление уже в избранном'})

        if advertisement.creator == self.request.user:
            raise ValidationError({'error': 'Вы не можете добавлять свое объявление в избранное'})

        if advertisement.draft:
            raise ValidationError({'error': 'Вы не можете добавить черновик в избранное'})

        advertisement.favourite.add(self.request.user)
        advertisement.save()
        return Response({'status': f'Объявление №-{advertisement.id} добавлено в избранное'})


    @action(detail=False, serializer_class=FavouriteSerializer, url_path=r'get_fav')
    def get_fav(self, request):
        """ Показывает избранное"""

        favourites = Favourite.objects.filter(user=self.request.user).all() 
        
        page = self.paginate_queryset(favourites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(favourites, many=True)
        return Response(serializer.data)
        