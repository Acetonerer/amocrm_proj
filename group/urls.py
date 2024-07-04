from django.urls import path
from .views import GroupListCreateView, GroupDetailView, GroupMembersView, GroupLeaderView, GroupItogPutView

urlpatterns = [
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'), # создание группы
    path('group/<int:group_id>/edit/', GroupDetailView.as_view(), name='group_edit'), # редактирование имени группы
    path('group/<int:group_id>/edit/itog/', GroupItogPutView.as_view, name='group_itog_edit'), # редактирование результата группы
    path('groups/<int:group_id>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/members/', GroupMembersView.as_view(), name='group-members'), # добавить члена
    path('groups/<int:group_id>/members/<int:user_id>/', GroupMembersView.as_view(), # изменить зону ответственности
         name='update-member-responsibilities'),
    path('groups/<int:group_id>/leader/', GroupLeaderView.as_view(), name='group-leader'), # лидер
]
