from rest_framework import pagination


class CollectionProductsPagination(pagination.PageNumberPagination):
    page_size = 12



