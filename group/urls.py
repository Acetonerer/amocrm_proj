from django.urls import path
from .views import GroupListCreateView, GroupDetailView, GroupMembersView, GroupLeaderView

urlpatterns = [
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:pk>/members/', GroupMembersView.as_view(), name='group-members'),
    path('groups/<int:pk>/leader/', GroupLeaderView.as_view(), name='group-leader'),
]
