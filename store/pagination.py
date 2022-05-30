from rest_framework import pagination


class CollectionPagination(pagination.PageNumberPagination):
    page_size = 8