from rest_framework import pagination


class ArticlePagination(pagination.LimitOffsetPagination):
    default_limit = 3
    limit_query_param = "limit"
    offset_query_param = "offset"


class PurchaseLinksPagination(pagination.LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "limit"
    offset_query_param = "offset"