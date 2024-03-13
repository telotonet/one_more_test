from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from .models import Event, Organization
from .serializers import EventSerializer, OrganizationSerializer
from .tasks import sleep_event

"""
Вывод информации и создание записей по api доступно только зарегистрированным пользователям
Конечные точки:
1.	Создание организации
2.	Создание мероприятия
3.	Вывод мероприятия с информацией о всех действующих пользователей, которые участвуют в организации мероприятия с разбивкой по организациям (вывести информацию о организации с объединением почтового индекса и адресом).
4.	Вывод мероприятий с возможностью фильтрации и сортировки по дате, поиском по названию и лимитной пагинацией.
"""


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sleep_event.delay()


class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20


class EventFilterListView(generics.ListAPIView):
    serializer_class = EventSerializer
    pagination_class = EventPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Event.objects.all().order_by('-date')

        # Filtering by date
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Search by title
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # Sorting by date
        sort_by_date = self.request.query_params.get('sort_by_date', None)
        if sort_by_date:
            queryset = queryset.order_by('date') if sort_by_date.lower() == 'asc' else queryset

        return queryset