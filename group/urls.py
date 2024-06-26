from django.urls import path
from .views import GroupListCreateView, GroupDetailView, GroupMembersView, GroupLeaderView

urlpatterns = [
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('group/<int:group_id>/edit/', GroupDetailView.as_view(), name='group_edit'),
    path('group/<int:group_id>/edit/result/', GroupListCreateView.as_view, name='group_result_edit'),
    path('groups/<int:group_id>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/members/', GroupMembersView.as_view(), name='group-members'),
    path('groups/<int:group_id>/members/<int:user_id>/', GroupMembersView.as_view(),
         name='update-member-responsibilities'),
    path('groups/<int:group_id>/leader/', GroupLeaderView.as_view(), name='group-leader'),
]
