from rest_framework import pagination


class TwelvePagination(pagination.PageNumberPagination):
    """Пагинация по 12"""
    page_size = 12


class EightPagination(pagination.PageNumberPagination):
    """Пагинация по 8"""
    page_size = 8


class FourPagination(pagination.PageNumberPagination):
    """Пагинация по 4"""
    page_size = 4








