# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Example: A simple API endpoint to get user data
class UserDataAPIView(APIView):
    permission_classes = [IsAuthenticated] # Only authenticated users can access

    def get(self, request, format=None):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'photo_url': user.photo.url if user.photo else None,
            'is_mentor': user.role == 'mentor', # Example derived field
            # Add more user data as needed
        }
        return Response(data, status=status.HTTP_200_OK)

# Example: A simple API endpoint for a welcome message
class WelcomeAPIView(APIView):
    # No permission_classes means it's publicly accessible
    def get(self, request, format=None):
        return Response({"message": "Welcome to the Uplifting Mentorship API!"}, status=status.HTTP_200_OK)

# You would add serializers (in api/serializers.py) and more complex views here
# from .serializers import UserSerializer, MentorshipSessionSerializer
# from mentorship.models import MentorshipSession
# from rest_framework import generics
#
# class MentorshipSessionListAPIView(generics.ListAPIView):
#     queryset = MentorshipSession.objects.all()
#     serializer_class = MentorshipSessionSerializer
#     permission_classes = [IsAuthenticated]
