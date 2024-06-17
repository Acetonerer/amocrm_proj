from django.urls import path
from .views import RemoveUserFromSubgroupView

urlpatterns = [
    path('groups/<int:group_id>/users/<int:user_id>/', RemoveUserFromSubgroupView.as_view(), name='del_user'),
]
