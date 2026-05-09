from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from scholarships.models import Scholarship
from django.db.models import Q
import os
import requests
import re

class FreeAIAssistantViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        Free AI that searches scholarship database and generates answers
        """
        try:
            user_message = request.data.get('message', '').strip().lower()
            
            if not user_message:
                return Response(
                    {'error': 'Message cannot be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Search scholarship database based on user query
            response_text = self.generate_response(user_message)
            
            return Response({
                'message': response_text,
                'success': True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ AI Chat Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def generate_response(self, query):
        """Generate response based on database search or external GRQE search"""

        # Tip-style queries get handled first so they don't go to external search
        if any(word in query for word in ['essay', 'write', 'application', 'apply']):
            return self.get_application_tips()

        if any(word in query for word in ['eligible', 'eligibility', 'requirements', 'qualify', 'gpa', 'grade']):
            return self.get_eligibility_tips()

        if any(word in query for word in ['deadline', 'apply by', 'when', 'date']):
            return self.get_deadline_info()

        if any(word in query for word in ['amount', 'money', 'award', 'how much', 'prize']):
            return self.get_funding_info()

        if any(word in query for word in ['international', 'visa', 'country', 'abroad']):
            return self.get_international_info()

        # If GRQE env vars are present, try external search first
        external_response = self.search_grqe(query)
        if external_response:
            return external_response

        # Fallback to local DB search / canned responses
        if any(word in query for word in ['engineering', 'computer', 'tech', 'technology']):
            return self.search_by_field('Engineering') or "Check our engineering scholarships by using the search feature! 🔧"

        if any(word in query for word in ['business', 'commerce', 'finance', 'accounting']):
            return self.search_by_field('Business') or "Explore business scholarships on our platform! 💼"

        if any(word in query for word in ['science', 'biology', 'chemistry', 'physics']):
            return self.search_by_field('Science') or "We have great science scholarships available! 🔬"

        if any(word in query for word in ['medicine', 'health', 'nursing', 'healthcare']):
            return self.search_by_field('Health') or "Browse health and medical scholarships! 🏥"

        if any(word in query for word in ['art', 'music', 'design', 'creative']):
            return self.search_by_field('Arts') or "Discover creative scholarships in our database! 🎨"

        return self.general_search(query)

    def search_grqe(self, query):
        """Call Groq API when configured; return AI-generated response or None on failure."""
        api_url = os.environ.get('GRQE_API_URL')
        api_key = os.environ.get('GRQE_API_KEY')
        
        if not api_url or not api_key:
            return None

        # Get scholarship context from database
        scholarships = Scholarship.objects.all()[:10]
        scholarship_context = ""
        
        if scholarships:
            scholarship_context = "\n\nAvailable scholarships in our database:\n"
            for sch in scholarships:
                scholarship_context += f"- {sch.title}"
                if hasattr(sch, 'amount') and sch.amount:
                    scholarship_context += f" (${sch.amount})"
                if hasattr(sch, 'description') and sch.description:
                    desc = sch.description[:100] + "..." if len(sch.description) > 100 else sch.description
                    scholarship_context += f": {desc}"
                scholarship_context += "\n"

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": "llama-3.3-70b-versatile",  # Updated Groq model (Dec 2024)
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a helpful scholarship assistant. Help students find scholarships and answer their questions about applications, eligibility, and funding. Keep responses concise (2-3 paragraphs max) and friendly. Use emojis sparingly.{scholarship_context}"
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }

        try:
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=float(os.environ.get('GRQE_TIMEOUT', '10')),
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Log the error and fall back to local search
            print(f"⚠️ Groq API Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text[:200]}")
            return None

        try:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                ai_response = data['choices'][0]['message']['content'].strip()
                return f"🤖 {ai_response}"
            return None
        except (ValueError, KeyError, IndexError):
            return None
    
    def search_by_field(self, field):
        """Search scholarships by field and return summary"""
        scholarships = Scholarship.objects.filter(
            Q(title__icontains=field) | Q(description__icontains=field)
        )[:5]
        
        if not scholarships:
            return None
        
        response = f"Found {scholarships.count()} {field} scholarships! 📚\n\n"
        for scholarship in scholarships:
            response += f"💡 **{scholarship.title}** - ${scholarship.amount if hasattr(scholarship, 'amount') else 'Variable'}\n"
        
        response += "\nVisit our search page to explore more! 🔍"
        return response
    
    def general_search(self, query):
        """Search all scholarships for keywords"""
        keywords = query.split()
        query_filter = Q()
        
        for keyword in keywords:
            query_filter |= Q(title__icontains=keyword) | Q(description__icontains=keyword)
        
        scholarships = Scholarship.objects.filter(query_filter)[:3]
        
        if scholarships:
            response = f"I found {scholarships.count()} relevant scholarships! 🎓\n\n"
            for scholarship in scholarships:
                response += f"✨ **{scholarship.title}**\n"
            response += "\nUse our search page to see full details! 🔍"
            return response
        else:
            return "I couldn't find exact matches, but we have 1000+ scholarships available! Try using the search page to filter by subject, amount, or eligibility. 🚀"
    
    def get_application_tips(self):
        """Return application writing tips"""
        return """📝 **Essay & Application Tips:**

✅ **Strong Essays:**
- Be authentic and personal
- Tell your unique story
- Show passion for your goals
- Proofread carefully
- Keep it concise (250-500 words usually)

✅ **Stand Out:**
- Mention specific achievements
- Show community involvement
- Link to scholarship goals
- Be genuine, not cliché

💡 Pro tip: Use our search feature to read scholarship requirements carefully! Apply to multiple scholarships to increase chances of success! 🎯"""
    
    def get_eligibility_tips(self):
        """Return eligibility information"""
        return """✅ **Common Eligibility Requirements:**

📋 **Academic:**
- GPA: Usually 2.5-3.5+ (varies by scholarship)
- Class standing: High school, undergrad, or graduate
- Major: Some are field-specific

📍 **Demographics:**
- Citizenship (some for US only, some international)
- State/region specific
- First-generation student status
- Income level

🎯 **Other:**
- Community service hours
- Essay or application form
- Letters of recommendation
- Demonstrated financial need

💡 Check each scholarship's page for exact requirements! Most students qualify for multiple scholarships - don't skip any! 🚀"""
    
    def get_deadline_info(self):
        """Return deadline advice"""
        return """📅 **Deadline Tips:**

⏰ **Plan Ahead:**
- Mark all deadlines on calendar
- Start applications 1-2 months early
- Don't miss rolling deadlines!
- Some scholarships: ongoing (no deadline)

🚨 **Pro Tips:**
- Apply early - increases chances
- Don't miss by one day!
- Set phone reminders
- Complete incomplete applications

💪 **Strategy:**
- Apply to 10-20 scholarships
- Spread across months
- Mix safe + reach scholarships

💡 Pro tip: Use our search feature to see all deadlines at once! Set reminders so you never miss one! ⏳"""
    
    def get_funding_info(self):
        """Return funding amount information"""
        return """💰 **Scholarship Amount Guide:**

💵 **Common Award Ranges:**
- Small: $500 - $2,500
- Medium: $2,500 - $10,000  
- Large: $10,000 - $50,000
- Full Ride: Covers full tuition + living

📊 **Distribution Tips:**
- Apply to mix of small & large
- 10 x $1,000 = same as 1 x $10,000
- Every dollar counts!
- Renewable scholarships best

🎯 **Strategy:**
- Target your GPA level
- Match your field/background
- Apply to overlapping scholarships
- Total potential: $20,000+ possible

💡 Use our scholarship search to filter by amount! Apply to all you qualify for! 🚀"""
    
    def get_international_info(self):
        """Return international student information"""
        return """🌍 **International Student Scholarships:**

🗺️ **Good News:**
- Many scholarships open to internationals!
- US, UK, Canada, Australia have programs
- Check visa requirements with each
- Some cover visa fees

📋 **Requirements Often Include:**
- Valid passport/visa
- English proficiency test (TOEFL/IELTS)
- Academic transcripts (official translation)
- Sometimes higher GPA needed

🌐 **Popular for Internationals:**
- Government scholarships
- University-specific funds
- Foundation scholarships
- Merit-based (not need-based)

💡 Filter by "International eligible" in our search! 🌟"""
    
    @action(detail=False, methods=['get'])
    def scholarship_stats(self, request):
        """Get statistics about available scholarships"""
        total = Scholarship.objects.count()
        
        return Response({
            'total_scholarships': total,
            'message': f'We have {total}+ scholarships in our database! 📚'
        })
