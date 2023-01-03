from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RatingSerializer
from .services import get_ratings_from_publication, get_ratings_for_user, create_post_rating, \
    create_client_rating
from ..chargers.pagination import PaginationHandlerMixin
from ..users.permissions import Check_API_KEY_Auth, SessionAuth


# Create your views here.
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class PublicationRatingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request, publication_id):
        ratings = get_ratings_from_publication(publication_id)
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = RatingSerializer(page, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        else:
            serializer = RatingSerializer(ratings, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')

    def post(self, request, publication_id):
        print("posting rating")
        print(request.data)
        rating = request.data
        rating['publication'] = publication_id
        rating['user'] = request.user.id
        try:
            rating = create_post_rating(rating)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
            else:
                return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class ClientRatingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request, client_id):
        ratings = get_ratings_for_user(client_id)
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = RatingSerializer(page, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        else:
            serializer = RatingSerializer(ratings, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')

    def post(self, request, client_id):
        rating = request.data
        rating['client'] = client_id
        rating['user'] = request.user.id
        try:
            rating = create_client_rating(rating)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
            else:
                return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
