#TODO: implement rate limiting and req throttling (WHY DID I NOT DO THIS EARLIER ONLY :D)

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from .models import Note
from rest_framework.authtoken.models import Token
from .serializers import NoteSerializer
from django.contrib.auth.models import User

#signing up because we're gonna need so many users, hehe
#although we can add email and everything too and we could verify the email as well but for that i would need the google api keys and i don't have those :O
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            Token.objects.create(user=user)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

#login goes brrrr
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)
    #why as an unauthorized person you are trying to log in huh
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#check the auth by the header and then let's add the note to our postgres
@permission_classes([permissions.IsAuthenticated])
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        shared_user_username = self.request.data.get('shared_user')
        shared_user = User.objects.filter(username=shared_user_username).first()

        serializer.save(user=self.request.user)

        if shared_user:
            serializer.instance.shared_users.add(shared_user)

@permission_classes([permissions.IsAuthenticated])
class NoteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

#share the note with someone special maybe, or you don't have any 🤭 (us)
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def share_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    shared_user = User.objects.get(username=request.data.get('username'))

    if note.user == request.user:
        note.shared_users.add(shared_user)
        return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#searching in djagorest is so cool and simple, i love it
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def search_notes(request):
    query = request.GET.get('q', '')
    notes = Note.objects.filter(user=request.user, content__icontains=query)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#hmm but if your someone special has shared some notes with you, how will you see them? here's how (don't be sad if no one shares a note with you cause even i don't get any 😞)
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def view_shared_notes(request):
    shared_notes = Note.objects.filter(shared_users=request.user)
    
    serializer = NoteSerializer(shared_notes, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)