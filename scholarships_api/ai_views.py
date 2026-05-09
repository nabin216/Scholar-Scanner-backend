from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import os
import openai

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class AIAssistantViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        Endpoint to handle AI chat messages
        Expected input: { "message": "user message here" }
        """
        try:
            user_message = request.data.get('message', '').strip()
            
            if not user_message:
                return Response(
                    {'error': 'Message cannot be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # System prompt for scholarship guidance
            system_prompt = """You are a helpful AI scholarship assistant for ScholarScanner, 
            a platform that helps students find and apply for scholarships. 
            
            You should:
            - Help students understand scholarship requirements and eligibility
            - Provide tips on scholarship applications and essays
            - Answer questions about financial aid and education funding
            - Suggest strategies for finding scholarships
            - Be encouraging and supportive
            - Keep responses concise (2-3 sentences)
            - Use emojis to make responses friendly
            
            If users ask about specific scholarships in our database, 
            suggest they use our search feature on the platform."""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            ai_message = response.choices[0].message.content
            
            return Response({
                'message': ai_message,
                'success': True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
