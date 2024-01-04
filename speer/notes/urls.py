from django.urls import path
from .views import (
    signup,
    login_view,
    NoteListCreateView,
    NoteRetrieveUpdateDeleteView,
    share_note,
    search_notes,
    view_shared_notes,
)

#pk reminds me of a movie of Rajkumar hirani :O
urlpatterns = [
    path('api/auth/signup/', signup, name='signup'),
    path('api/auth/login/', login_view, name='login'),
    path('api/notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('api/notes/<int:pk>/', NoteRetrieveUpdateDeleteView.as_view(), name='note-retrieve-update-delete'),
    path('api/notes/<int:pk>/share/', share_note, name='share-note'),
    path('api/search/', search_notes, name='search-notes'),
    path('api/notes/shared/', view_shared_notes, name='view-shared-notes'),
]
