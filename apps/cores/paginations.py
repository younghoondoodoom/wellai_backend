from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    """
    기준 페이지네이션

    받는 수를 정하고 싶으면 param에 size=13 이런 식으로 쓰면 됨.
    """

    page_size = 5
    page_size_query_param = "size"
    max_page_size = 100
