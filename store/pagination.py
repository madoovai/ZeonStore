from rest_framework import pagination


class TwelvePagination(pagination.PageNumberPagination):
    page_size = 12


class EightPagination(pagination.PageNumberPagination):
    page_size = 8






