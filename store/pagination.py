from rest_framework import pagination


class TwelvePagination(pagination.PageNumberPagination):
    page_size = 12



