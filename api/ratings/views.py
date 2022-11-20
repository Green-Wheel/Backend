from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from utils import BasicPagination
from .serializers import RatingSerializer
from .services import get_all_ratings, get_ratings_for_publication, get_ratings_for_user, create_post_rating, \
    create_client_rating
from ..chargers.pagination import PaginationHandlerMixin


# Create your views here.


class PublicationRatingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, publication_id):
        ratings = get_ratings_for_publication(publication_id)
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = RatingSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        else:
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, publication_id):
        rating = request.data
        rating['publication'] = publication_id
        rating['user'] = request.user.id
        try:
            rating = create_post_rating(rating)
            return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class ClientRatingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, client_id):
        ratings = get_ratings_for_user(client_id)
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = RatingSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        else:
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, client_id):
        rating = request.data
        rating['client'] = client_id
        rating['user'] = request.user.id
        try:
            rating = create_client_rating(rating)
            return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
