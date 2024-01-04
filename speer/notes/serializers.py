from rest_framework import serializers
from .models import Note

#serializers are fun, or are they :D
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        shared_user = self.context['request'].data.get('shared_user')
        
        validated_data.pop('user', None)
        validated_data.pop('shared_users', None)

        note = Note.objects.create(user=user, **validated_data)

        if shared_user:
            note.shared_users.add(shared_user)

        return note