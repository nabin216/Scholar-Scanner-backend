from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import ContactMessage
from .serializers import ContactMessageSerializer, ContactMessageAdminSerializer


class ContactMessageCreateView(generics.CreateAPIView):
    """
    API endpoint to submit a contact message from the Get in Touch form.
    No authentication required.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'success': True,
            'message': 'Thank you for contacting us! We will get back to you soon.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ContactMessageListView(generics.ListAPIView):
    """
    API endpoint for admins to view all contact messages.
    Requires admin authentication.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['status', 'subject']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    ordering_fields = ['created_at', 'status']


class ContactMessageDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for admins to view/update a contact message.
    Requires admin authentication.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [IsAdminUser]
