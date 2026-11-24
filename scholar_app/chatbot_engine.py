"""
Enhanced AI Chatbot Engine
Natural Language Processing and Intelligent Conversation
"""

import re
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from .models import Scholarship, Application, StudentProfile


class ScholarshipChatbot:
    """Enhanced AI Chatbot for Scholarship Recommendations"""
    
    def __init__(self, user=None):
        self.user = user
        self.profile = None
        if user and user.is_authenticated:
            try:
                self.profile = user.profile
            except:
                pass
        
        # Conversation context
        self.context = {}
        
        # Currency settings
        self.currency_symbol = "₹"
        self.currency_code = "INR"
        
        # Intent patterns
        self.intents = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening|greetings)\b',
                r'^(hi|hello|hey)$'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|take care|farewell)\b',
            ],
            'thanks': [
                r'\b(thank|thanks|thx|appreciate)\b',
            ],
            'eligibility': [
                r'\b(eligible|qualify|can i apply|am i qualified)\b',
                r'\b(which scholarship|what scholarship).*\b(can|should|for me)\b',
            ],
            'deadline': [
                r'\b(deadline|due date|when.*due|time.*left|last date)\b',
            ],
            'requirements': [
                r'\b(requirement|need|document|upload|submit|what.*need)\b',
            ],
            'amount': [
                r'\b(how much|amount|money|worth|value|scholarship.*pay)\b',
            ],
            'application_process': [
                r'\b(how.*apply|application process|steps.*apply|apply.*scholarship)\b',
            ],
            'profile': [
                r'\b(my profile|update profile|edit profile|profile.*complete)\b',
            ],
            'recommendations': [
                r'\b(recommend|suggest|best.*scholarship|top.*scholarship|find.*scholarship)\b',
            ],
            'status': [
                r'\b(application status|my application|track.*application|status.*application)\b',
            ],
            'tips': [
                r'\b(tips|advice|help|improve|increase.*chance|better.*chance)\b',
            ],
            'countries': [
                r'\b(which country|countries|study abroad|international)\b',
            ],
            'fields': [
                r'\b(field|major|subject|course|program|degree)\b',
            ],
            'gpa': [
                r'\b(gpa|grade|marks|cgpa|percentage)\b',
            ],
            'count': [
                r'\b(how many|number of|count|total)\b',
            ],
        }
    
    def format_currency(self, amount):
        """Format amount in Indian Rupees"""
        if amount >= 10000000:  # 1 Crore
            return f"{self.currency_symbol}{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"{self.currency_symbol}{amount/100000:.2f} L"
        else:
            return f"{self.currency_symbol}{amount:,.0f}"
    
    def process_message(self, message):
        """Main message processing function"""
        message = message.strip()
        
        if not message:
            return "I'm here to help! Ask me anything about scholarships."
        
        # Detect intent
        intent = self.detect_intent(message)
        
        # Generate response based on intent
        if intent == 'greeting':
            return self.handle_greeting()
        elif intent == 'goodbye':
            return self.handle_goodbye()
        elif intent == 'thanks':
            return self.handle_thanks()
        elif intent == 'eligibility':
            return self.handle_eligibility(message)
        elif intent == 'deadline':
            return self.handle_deadline(message)
        elif intent == 'requirements':
            return self.handle_requirements()
        elif intent == 'amount':
            return self.handle_amount(message)
        elif intent == 'application_process':
            return self.handle_application_process()
        elif intent == 'profile':
            return self.handle_profile()
        elif intent == 'recommendations':
            return self.handle_recommendations()
        elif intent == 'status':
            return self.handle_status()
        elif intent == 'tips':
            return self.handle_tips()
        elif intent == 'countries':
            return self.handle_countries()
        elif intent == 'fields':
            return self.handle_fields()
        elif intent == 'gpa':
            return self.handle_gpa(message)
        elif intent == 'count':
            return self.handle_count(message)
        else:
            return self.handle_general(message)
    
    def detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'general'
    
    def handle_greeting(self):
        """Handle greeting messages"""
        user_name = ""
        if self.user and self.user.is_authenticated:
            user_name = f" {self.user.first_name}" if self.user.first_name else ""
        
        greetings = [
            f"Hello{user_name}! 👋 I'm your AI Scholarship Assistant. How can I help you today?",
            f"Hi{user_name}! 😊 Ready to find your perfect scholarship? Ask me anything!",
            f"Hey{user_name}! 🎓 I'm here to help you discover amazing scholarship opportunities. What would you like to know?",
        ]
        
        import random
        return random.choice(greetings)
    
    def handle_goodbye(self):
        """Handle goodbye messages"""
        return "Goodbye! 👋 Feel free to come back anytime you need help with scholarships. Good luck! 🍀"
    
    def handle_thanks(self):
        """Handle thank you messages"""
        responses = [
            "You're welcome! 😊 Happy to help. Let me know if you need anything else!",
            "My pleasure! 🎓 Don't hesitate to ask if you have more questions.",
            "Glad I could help! ✨ Feel free to ask me anything else about scholarships.",
        ]
        import random
        return random.choice(responses)
    
    def handle_eligibility(self, message):
        """Handle eligibility questions"""
        if not self.user or not self.user.is_authenticated:
            return "Please log in to check your eligibility for scholarships. I can provide personalized recommendations once you're logged in! 🔐"
        
        if not self.profile:
            return "Please complete your profile first! Go to **Profile → Edit Profile** to add your GPA, field of study, and other details. Then I can show you scholarships you're eligible for! 📝"
        
        # Get user's eligibility criteria
        user_gpa = self.profile.gpa or 0
        user_field = self.profile.field_of_study
        user_degree = self.profile.current_degree
        user_country = self.profile.country
        
        # Find eligible scholarships
        eligible = Scholarship.objects.filter(status='active', deadline__gte=timezone.now().date())
        
        if user_gpa:
            eligible = eligible.filter(Q(min_gpa__lte=user_gpa) | Q(min_gpa__isnull=True))
        
        if user_field:
            eligible = eligible.filter(
                Q(field_of_study__icontains=user_field) | Q(field_of_study='')
            )
        
        count = eligible.count()
        
        response = f"🎯 **Great news!** Based on your profile:\n\n"
        response += f"• **GPA**: {user_gpa or 'Not set'}\n"
        response += f"• **Field**: {user_field or 'Not set'}\n"
        response += f"• **Degree**: {dict(StudentProfile.DEGREE_CHOICES).get(user_degree, 'Not set')}\n"
        response += f"• **Country**: {user_country}\n\n"
        response += f"✅ You're eligible for **{count} scholarships**!\n\n"
        response += f"💡 Visit your **Dashboard** to see personalized recommendations with match scores!"
        
        return response
    
    def handle_deadline(self, message):
        """Handle deadline questions"""
        from django.db.models import Q
        
        # Check for specific timeframe
        if 'month' in message.lower() or '30 day' in message.lower():
            days = 30
            period = "next 30 days"
        elif 'week' in message.lower() or '7 day' in message.lower():
            days = 7
            period = "next week"
        elif 'today' in message.lower() or 'tomorrow' in message.lower():
            days = 2
            period = "next 2 days"
        else:
            days = 60
            period = "next 2 months"
        
        deadline_date = timezone.now().date() + timedelta(days=days)
        
        scholarships = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date(),
            deadline__lte=deadline_date
        ).order_by('deadline')
        
        count = scholarships.count()
        
        if count == 0:
            return f"📅 No urgent deadlines in the {period}. You have time to prepare! 😊"
        
        response = f"⏰ **Urgent!** {count} scholarship(s) deadline(s) in the {period}:\n\n"
        
        for i, sch in enumerate(scholarships[:5], 1):
            days_left = (sch.deadline - timezone.now().date()).days
            response += f"{i}. **{sch.title}**\n"
            response += f"   📅 Deadline: {sch.deadline.strftime('%B %d, %Y')} ({days_left} days left)\n"
            response += f"   💰 Amount: {self.format_currency(sch.amount)}\n\n"
        
        if count > 5:
            response += f"📌 ...and {count - 5} more! Check the **Scholarships** page for all deadlines."
        
        return response
    
    def handle_requirements(self):
        """Handle document requirements questions"""
        response = "📋 **Common Scholarship Requirements:**\n\n"
        response += "**Documents Needed:**\n"
        response += "1. ✅ **Resume/CV** - Your academic and work experience\n"
        response += "2. ✅ **Academic Transcripts** - Official grade records\n"
        response += "3. ✅ **Recommendation Letters** - 2-3 letters from professors/mentors\n"
        response += "4. ✅ **Personal Statement/Essay** - Why you deserve this scholarship\n"
        response += "5. ✅ **Proof of Enrollment** - Acceptance letter or student ID\n"
        response += "6. ✅ **Financial Documents** - For need-based scholarships\n\n"
        response += "**Additional Materials:**\n"
        response += "• Portfolio (for arts/design)\n"
        response += "• Research proposal (for research scholarships)\n"
        response += "• Language test scores (TOEFL/IELTS)\n\n"
        response += "💡 **Tip**: Keep digital copies ready! You can upload documents in your profile."
        
        return response
    
    def handle_amount(self, message):
        """Handle scholarship amount questions"""
        from django.db.models import Min, Max, Avg
        
        stats = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date()
        ).aggregate(
            min_amount=Min('amount'),
            max_amount=Max('amount'),
            avg_amount=Avg('amount')
        )
        
        response = "💰 **Scholarship Amounts:**\n\n"
        
        if stats['min_amount']:
            response += f"• **Lowest**: {self.format_currency(stats['min_amount'])}\n"
            response += f"• **Highest**: {self.format_currency(stats['max_amount'])}\n"
            response += f"• **Average**: {self.format_currency(stats['avg_amount'])}\n\n"
        
        # Show top scholarships by amount
        top_scholarships = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date()
        ).order_by('-amount')[:3]
        
        if top_scholarships:
            response += "🏆 **Top 3 Highest Scholarships:**\n\n"
            for i, sch in enumerate(top_scholarships, 1):
                response += f"{i}. **{sch.title}**\n"
                response += f"   💵 {self.format_currency(sch.amount)} | {sch.country}\n\n"
        
        response += "💡 **Tip**: Don't just chase the highest amounts! Apply to multiple scholarships to increase your chances."
        
        return response
    
    def handle_application_process(self):
        """Handle application process questions"""
        response = "📝 **How to Apply for Scholarships:**\n\n"
        response += "**Step 1: Complete Your Profile** ✏️\n"
        response += "• Add GPA, field of study, achievements\n"
        response += "• Upload resume and documents\n\n"
        response += "**Step 2: Browse Scholarships** 🔍\n"
        response += "• Use filters (country, amount, field)\n"
        response += "• Check eligibility requirements\n\n"
        response += "**Step 3: Get AI Recommendations** 🤖\n"
        response += "• Visit your Dashboard\n"
        response += "• See personalized matches\n\n"
        response += "**Step 4: Prepare Documents** 📄\n"
        response += "• Write compelling essays\n"
        response += "• Get recommendation letters\n\n"
        response += "**Step 5: Submit Application** 🚀\n"
        response += "• Click 'Apply Now' on scholarship page\n"
        response += "• Fill out application form\n"
        response += "• Upload required documents\n\n"
        response += "**Step 6: Track Status** 📊\n"
        response += "• Monitor on Dashboard\n"
        response += "• Respond to notifications\n\n"
        response += "⏰ **Apply early!** Most scholarships are first-come, first-served."
        
        return response
    
    def handle_profile(self):
        """Handle profile questions"""
        if not self.user or not self.user.is_authenticated:
            return "Please log in first! Once logged in, go to **Profile** in the navigation menu to complete your profile. 🔐"
        
        if not self.profile:
            return "Let's set up your profile! Go to **Profile → Edit Profile** and add:\n\n• 📚 Academic info (GPA, field of study)\n• 🎓 Degree level\n• 🌍 Country\n• 💡 Skills & interests\n\nA complete profile helps me find the best scholarships for you!"
        
        completion = self.profile.calculate_profile_completion()
        
        response = f"📊 **Your Profile Status:**\n\n"
        response += f"• **Completion**: {completion}%\n"
        response += f"• **Name**: {self.user.get_full_name() or 'Not set'}\n"
        response += f"• **Email**: {self.user.email}\n"
        response += f"• **GPA**: {self.profile.gpa or 'Not set'}\n"
        response += f"• **Field**: {self.profile.field_of_study or 'Not set'}\n"
        response += f"• **Country**: {self.profile.country}\n\n"
        
        if completion < 100:
            response += f"⚠️ Your profile is **{100-completion}%** incomplete.\n\n"
            response += "💡 **Complete your profile** to get better scholarship matches!"
        else:
            response += "✅ Great! Your profile is complete! 🎉"
        
        return response
    
    def handle_recommendations(self):
        """Handle recommendation questions"""
        if not self.user or not self.user.is_authenticated:
            return "Please log in to get personalized recommendations! I'll analyze your profile and find the best scholarships for you. 🎯"
        
        if not self.profile or not self.profile.gpa:
            return "Complete your profile first! Add your GPA, field of study, and preferences. Then visit your **Dashboard** for AI-powered recommendations! 🤖"
        
        # Get top scholarships for user
        scholarships = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date()
        )
        
        # Simple filtering based on profile
        if self.profile.gpa:
            from django.db.models import Q
            scholarships = scholarships.filter(
                Q(min_gpa__lte=self.profile.gpa) | Q(min_gpa__isnull=True)
            )
        
        if self.profile.field_of_study:
            scholarships = scholarships.filter(
                Q(field_of_study__icontains=self.profile.field_of_study) | 
                Q(field_of_study='')
            )[:5]
        
        if not scholarships:
            return "No scholarships found matching your profile. Try updating your profile or check back later for new opportunities!"
        
        response = "🎯 **Top Recommendations for You:**\n\n"
        
        for i, sch in enumerate(scholarships, 1):
            days_left = (sch.deadline - timezone.now().date()).days
            response += f"**{i}. {sch.title}**\n"
            response += f"💰 {self.format_currency(sch.amount)} | 🌍 {sch.country}\n"
            response += f"⏰ {days_left} days left | 🎓 {sch.get_degree_level_display()}\n\n"
        
        response += "📊 Visit your **Dashboard** for detailed match scores and more recommendations!"
        
        return response
    
    def handle_status(self):
        """Handle application status questions"""
        if not self.user or not self.user.is_authenticated:
            return "Please log in to check your application status! 🔐"
        
        from .models import Application
        
        applications = Application.objects.filter(student=self.user).order_by('-applied_date')
        
        if not applications:
            return "You haven't applied to any scholarships yet! 📝\n\nBrowse available scholarships and click **'Apply Now'** to get started!"
        
        response = "📋 **Your Applications:**\n\n"
        
        # Count by status
        submitted = applications.filter(status='submitted').count()
        under_review = applications.filter(status='under_review').count()
        approved = applications.filter(status='approved').count()
        rejected = applications.filter(status='rejected').count()
        
        response += f"• ⏳ **Submitted**: {submitted}\n"
        response += f"• 🔍 **Under Review**: {under_review}\n"
        response += f"• ✅ **Approved**: {approved}\n"
        response += f"• ❌ **Rejected**: {rejected}\n\n"
        
        # Show recent applications
        response += "**Recent Applications:**\n\n"
        for i, app in enumerate(applications[:3], 1):
            status_emoji = {
                'submitted': '⏳',
                'under_review': '🔍',
                'approved': '✅',
                'rejected': '❌',
            }
            emoji = status_emoji.get(app.status, '📝')
            response += f"{i}. {emoji} **{app.scholarship.title}**\n"
            response += f"   Status: {app.get_status_display()}\n"
            response += f"   Applied: {app.applied_date.strftime('%B %d, %Y')}\n\n"
        
        response += "💡 Visit your **Dashboard** to see all applications and track status!"
        
        return response
    
    def handle_tips(self):
        """Handle tips and advice questions"""
        tips = [
            "**1. Complete Your Profile 100%** 📝\nScholarships want to know who you are! Add all details.",
            
            "**2. Apply to Multiple Scholarships** 🎯\nDon't put all eggs in one basket. Apply to 10-15 scholarships.",
            
            "**3. Start Early** ⏰\nDon't wait until the deadline! Apply 2-3 weeks early.",
            
            "**4. Personalize Each Application** ✍️\nTailor your essay to each scholarship. Show you've done research!",
            
            "**5. Get Strong Recommendations** 💪\nAsk professors who know you well. Give them plenty of notice!",
            
            "**6. Proofread Everything** 🔍\nTypos can hurt your chances. Use Grammarly or ask someone to review.",
            
            "**7. Follow Instructions Exactly** 📋\nIf they ask for 500 words, don't write 700. Show you can follow directions.",
            
            "**8. Highlight Achievements** 🏆\nDon't be modest! Showcase awards, projects, leadership roles.",
            
            "**9. Show Financial Need (if applicable)** 💸\nBe honest about your financial situation for need-based scholarships.",
            
            "**10. Follow Up** 📧\nSend a thank-you email after submitting. Shows professionalism!"
        ]
        
        import random
        selected_tips = random.sample(tips, 5)
        
        response = "💡 **Top 5 Tips to Win Scholarships:**\n\n"
        response += "\n\n".join(selected_tips)
        response += "\n\n🌟 **Bonus Tip**: Quality over quantity! Better to submit 5 excellent applications than 20 mediocre ones."
        
        return response
    
    def handle_countries(self):
        """Handle country-related questions"""
        from django.db.models import Count
        
        countries = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date()
        ).values('country').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        response = "🌍 **Scholarships by Country:**\n\n"
        
        for i, item in enumerate(countries, 1):
            response += f"{i}. 🚩 **{item['country']}**: {item['count']} scholarships\n"
        
        response += "\n💡 **Tip**: Use filters on the **Scholarships** page to find opportunities in your preferred country!"
        
        return response
    
    def handle_fields(self):
        """Handle field of study questions"""
        from django.db.models import Count
        
        # Get unique fields
        fields = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date()
        ).exclude(field_of_study='').values_list('field_of_study', flat=True)
        
        # Count occurrences
        field_count = {}
        for field in fields:
            if field:
                field_count[field] = field_count.get(field, 0) + 1
        
        # Sort by count
        sorted_fields = sorted(field_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        response = "📚 **Popular Fields of Study:**\n\n"
        
        for i, (field, count) in enumerate(sorted_fields, 1):
            response += f"{i}. 🎓 **{field}**: {count} scholarships\n"
        
        response += "\n💡 Set your field of study in your **Profile** to get personalized recommendations!"
        
        return response
    
    def handle_gpa(self, message):
        """Handle GPA-related questions"""
        # Try to extract GPA from message
        gpa_match = re.search(r'\b([0-3]\.\d{1,2}|4\.0{1,2})\b', message)
        
        if gpa_match:
            gpa = float(gpa_match.group(1))
            from django.db.models import Q
            
            scholarships = Scholarship.objects.filter(
                status='active',
                deadline__gte=timezone.now().date()
            ).filter(
                Q(min_gpa__lte=gpa) | Q(min_gpa__isnull=True)
            )
            
            count = scholarships.count()
            
            response = f"📊 **With GPA {gpa}:**\n\n"
            response += f"✅ You're eligible for **{count} scholarships**!\n\n"
            
            if gpa >= 3.5:
                response += "🌟 Excellent GPA! You qualify for merit-based scholarships!"
            elif gpa >= 3.0:
                response += "👍 Good GPA! Many scholarships are available to you!"
            elif gpa >= 2.5:
                response += "💪 Don't worry! There are scholarships for all GPA levels!"
            else:
                response += "📚 Focus on need-based and community service scholarships!"
            
            response += "\n\n💡 Update your GPA in your **Profile** for accurate recommendations!"
            
            return response
        else:
            response = "📊 **About GPA Requirements:**\n\n"
            response += "• **3.5 - 4.0**: Eligible for most merit-based scholarships 🌟\n"
            response += "• **3.0 - 3.4**: Many scholarships available 👍\n"
            response += "• **2.5 - 2.9**: Focus on need-based, community service 💪\n"
            response += "• **Below 2.5**: Don't give up! Some scholarships don't require high GPA 📚\n\n"
            response += "💡 **Tip**: Many scholarships consider more than just GPA. Leadership, community service, and essays matter too!"
            
            return response
    
    def handle_count(self, message):
        """Handle counting questions"""
        active_count = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.now().date()
        ).count()
        
        featured_count = Scholarship.objects.filter(
            status='active',
            is_featured=True,
            deadline__gte=timezone.now().date()
        ).count()
        
        response = "📊 **Scholarship Statistics:**\n\n"
        response += f"• 🎓 **Total Active Scholarships**: {active_count}\n"
        response += f"• ⭐ **Featured Scholarships**: {featured_count}\n"
        
        if self.user and self.user.is_authenticated:
            from .models import Application
            applied_count = Application.objects.filter(student=self.user).count()
            response += f"• 📝 **Your Applications**: {applied_count}\n"
        
        response += "\n💡 New scholarships are added regularly. Check back often!"
        
        return response
    
    def handle_general(self, message):
        """Handle general questions"""
        responses = [
            "🤔 I'm not sure I understand. Could you rephrase that?\n\nI can help you with:\n• Finding eligible scholarships\n• Checking deadlines\n• Application tips\n• Document requirements\n• Your profile and application status",
            
            "💭 Hmm, I didn't quite catch that. Try asking about:\n• 'What scholarships am I eligible for?'\n• 'When are the deadlines?'\n• 'How do I apply?'\n• 'Show me scholarship tips'\n• 'What's my application status?'",
            
            "🤷 I'm still learning! Could you ask in a different way?\n\nPopular questions:\n• Eligibility and requirements\n• Deadlines and amounts\n• Application process\n• Countries and fields\n• Your profile and status"
        ]
        
        import random
        return random.choice(responses)


# Conversation history storage (in-memory, for demo)
# In production, use database or cache
conversation_history = {}


def get_chatbot_response(user_message, user):
    """Main function to get chatbot response"""
    chatbot = ScholarshipChatbot(user=user)
    response = chatbot.process_message(user_message)
    
    # Store in conversation history
    user_id = user.id if user and user.is_authenticated else 'anonymous'
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        'user': user_message,
        'bot': response,
        'timestamp': timezone.now()
    })
    
    # Keep only last 20 messages
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]
    
    return response
