"""
Dummy AI Service for testing frontend before ML model integration
"""
import random
import re
import hashlib
from typing import List, Dict, Any
from datetime import datetime

class DummyAIService:
    """Simulates AI responses for frontend testing"""
    
    def __init__(self):
        self.campus_responses = {
            "library": [
                "The Central Library is open Monday-Friday 8AM-10PM, weekends 10AM-8PM. Digital resources are available 24/7 through VPN access.",
                "Our library spans 4 floors: Ground floor has circulation desk and general reading area, 1st floor for group study rooms, 2nd floor for silent study, and 3rd floor houses research collections and archives.",
                "You can reserve study rooms online through the campus portal up to 7 days in advance. Each room accommodates 4-8 people and has whiteboard facilities.",
                "The library houses over 2,50,000 books, 15,000 e-books, and subscriptions to 500+ international journals. IEEE, ACM, and Springer databases are accessible.",
                "Late return fee is ₹5 per day per book. Faculty can borrow up to 10 books for 30 days, students can borrow 5 books for 14 days.",
                "Printing services available at ₹2 per page (B&W), ₹10 per page (color). Scanning and photocopying facilities also available."
            ],
            "cafeteria": [
                "Main cafeteria serves breakfast 7-10AM, lunch 12-3PM, dinner 6-9PM daily. Food court operates 8AM-8PM with 12 different vendors.",
                "Today's menu: Breakfast - Poha, Upma, Sandwiches; Lunch - North Indian thali (₹80), South Indian meals (₹70), Chinese combo (₹90); Dinner - Biryani, Dal-chawal, Roti sabzi.",
                "Food quality is maintained under FSSAI guidelines. Monthly health inspections ensure hygiene standards. Student feedback average: 4.2/5 stars.",
                "Special dietary options available: Jain food, diabetic meals, gluten-free options. Inform the counter staff about allergies or dietary restrictions.",
                "Meal plans available: Basic plan ₹4,500/month, Premium plan ₹6,500/month. Outside food delivery allowed until 8PM at the main gate.",
                "The food court includes: Amul parlor, South Indian counter, Chinese wok, Pizza corner, Juice bar, Bakery, and healthy salad station."
            ],
            "admission": [
                "Admission applications for 2025-26 session open March 1st, deadline April 30th. Merit list published May 15th, counseling starts May 20th.",
                "Required documents: Class 12th marksheet, JEE/NEET scorecard, transfer certificate, character certificate, passport photos, caste certificate (if applicable).",
                "Admission process: Online application → Document verification → Merit list → Counseling → Fee payment → Seat confirmation.",
                "Eligibility: Minimum 75% in Class 12th (70% for reserved categories). JEE Main rank under 2,50,000 for Engineering, NEET for Medical courses.",
                "Course-wise cutoffs 2024: Computer Science - 98.2%, Electronics - 96.8%, Mechanical - 94.5%, Civil - 92.1%, Chemical - 93.7%.",
                "Seat matrix: General-50%, OBC-27%, SC-15%, ST-7.5%, EWS-10%. Management quota seats available with separate counseling process."
            ],
            "hostel": [
                "Campus has 8 hostels: 4 for boys (capacity 2000), 4 for girls (capacity 1800). All rooms are twin-sharing with attached bathrooms.",
                "Hostel fees: AC rooms ₹1,20,000/year, Non-AC ₹85,000/year (including meals, electricity, wifi). Mess charges separate: ₹4,500/month.",
                "Room allocation based on merit rank and application date. Senior students get preference for single rooms. AC rooms limited to final year students.",
                "Facilities: 24x7 wifi, common room with TV, gymnasium, indoor games, library, medical room, laundry service, hot water 6-10AM & 6-10PM.",
                "Hostel timings: Entry gates close at 10:30PM (11:30PM weekends). Late entry requires warden permission. Mess timings: 7-9AM, 12:30-2:30PM, 7:30-9:30PM.",
                "Security: CCTV surveillance, biometric entry, 24x7 guards. Visitors allowed 10AM-6PM with proper ID verification and entry register."
            ],
            "fees": [
                "Semester fee structure: Tuition ₹1,85,000, Development ₹25,000, Lab ₹15,000, Library ₹3,000, Sports ₹2,000, Medical ₹1,000 = Total ₹2,31,000 per semester.",
                "Fee payment modes: Online through student portal (recommended), NEFT/RTGS, DD in favor of 'College Name'. No cash payments accepted.",
                "Payment schedule: Semester fees due 15 days before semester start. Late fee ₹500/day after due date. Installment facility for financial hardship cases.",
                "Scholarships available: Merit scholarship (top 5% - 50% fee waiver), Need-based assistance (family income <3 LPA - 75% waiver), Sports quota scholarships.",
                "Refund policy: 90% refund if withdrawal before semester start, 50% if within first month, No refund after first month. Caution deposit refundable.",
                "Additional charges: Exam fee ₹2,000/semester, Transcript fee ₹500/copy, ID card replacement ₹200, Library fine ₹5/day for overdue books."
            ],
            "transport": [
                "College operates 25 buses covering 18 routes across Mumbai, Pune, and nearby districts. Routes include Thane, Kalyan, Vasai, Panvel, and Nashik.",
                "Bus timings: Morning pickup 7:00-8:30AM (3 trips), Evening return 4:30PM, 6:30PM, 8:30PM. Saturday service available, Sunday buses for special events only.",
                "Monthly bus pass: ₹3,500 (AC buses), ₹2,800 (non-AC). Semester pass available at 10% discount. Day pass ₹80. Faculty/staff get 20% discount.",
                "Bus routes with GPS tracking available on college mobile app. Real-time location, delay notifications, and seat availability updates provided.",
                "Safety features: CCTV in all buses, female security attendant in ladies buses, emergency contact numbers displayed, speed governors installed.",
                "Special services: Exam duty buses during university exams, industrial visit transportation, pickup from railway stations during admission season."
            ],
            "placement": [
                "Placement season 2024: 450+ companies visited, 95% placement rate, average package ₹12.5 LPA, highest ₹85 LPA (Google), top recruiters: TCS, Infosys, Microsoft, Amazon.",
                "Pre-placement activities: Resume building workshops (July), aptitude training (August), mock interviews (September), coding bootcamp for CS students.",
                "Eligibility criteria: Minimum 60% aggregate, no active backlogs, 75% attendance. Companies may have additional criteria (CGPA cutoffs, specific skills).",
                "Training programs: Soft skills development, technical interview preparation, group discussion practice, presentation skills, industry-specific training modules.",
                "Top recruiting domains: Software development (40%), Data science/Analytics (25%), Consulting (15%), Core engineering (10%), Finance (10%).",
                "Alumni network: 25,000+ alumni across 50+ countries. Regular alumni talks, mentorship programs, referral assistance, and networking events organized."
            ],
            "academic": [
                "Current semester: Autumn 2024 (July-November). Mid-term exams: September 15-25, End-term exams: November 20-December 5. Results by December 15th.",
                "Grading system: O(10), A+(9), A(8), B+(7), B(6), C+(5), C(4), F(0). CGPA calculation: Credit-weighted average. Minimum 5.0 CGPA required for promotion.",
                "Attendance policy: Minimum 75% mandatory for exam eligibility. Medical leave requires doctor's certificate. Condonation available for 65-74% with valid reasons.",
                "Academic calendar: Odd semester (July-Dec), Even semester (Jan-May), Summer internship/courses (May-July). 2 weeks vacation between semesters.",
                "Online resources: LMS portal for notes/assignments, recorded lectures available, digital library access, online doubt clearing sessions every Friday 4-6PM.",
                "Academic support: Mentorship program, peer tutoring, extra classes for weak students, faculty office hours, academic counseling services available."
            ]
        }
        
        self.sources_data = {
            "library": [
                {"title": "Library Services Handbook 2024", "url": "https://college.edu/library/handbook.pdf", "snippet": "Complete guide to library facilities, timings, and digital resources"},
                {"title": "Digital Library Access Guide", "url": "https://college.edu/library/digital-access.pdf", "snippet": "Step-by-step guide for accessing online journals and databases"},
                {"title": "Study Room Booking System", "url": "https://portal.college.edu/library/booking", "snippet": "Online reservation system for group study rooms"},
                {"title": "Library Rules and Regulations", "url": "https://college.edu/library/rules.pdf", "snippet": "Borrowing policies, fines, and conduct guidelines"}
            ],
            "cafeteria": [
                {"title": "Mess Menu Weekly Schedule", "url": "https://college.edu/dining/weekly-menu.pdf", "snippet": "Current week's breakfast, lunch, and dinner menu with prices"},
                {"title": "Food Safety & Hygiene Report", "url": "https://college.edu/dining/safety-report.pdf", "snippet": "Monthly FSSAI inspection reports and hygiene ratings"},
                {"title": "Meal Plan Options 2024", "url": "https://college.edu/dining/meal-plans.pdf", "snippet": "Detailed breakdown of basic and premium meal plan benefits"},
                {"title": "Food Court Vendor Directory", "url": "https://college.edu/dining/vendors.pdf", "snippet": "List of all food court vendors with specialties and contact info"}
            ],
            "admission": [
                {"title": "Admission Prospectus 2025-26", "url": "https://college.edu/admissions/prospectus.pdf", "snippet": "Complete admission guidelines, eligibility criteria, and important dates"},
                {"title": "Course-wise Cutoff Trends", "url": "https://college.edu/admissions/cutoffs.pdf", "snippet": "Historical cutoff data for last 5 years across all branches"},
                {"title": "Document Checklist", "url": "https://college.edu/admissions/documents.pdf", "snippet": "Detailed list of required documents with sample formats"},
                {"title": "Merit List & Counseling Schedule", "url": "https://portal.college.edu/admissions/merit", "snippet": "Live merit list updates and counseling round schedules"}
            ],
            "hostel": [
                {"title": "Hostel Accommodation Guide", "url": "https://college.edu/hostel/accommodation.pdf", "snippet": "Room types, facilities, and allocation process details"},
                {"title": "Hostel Rules & Regulations", "url": "https://college.edu/hostel/rules.pdf", "snippet": "Code of conduct, timings, and disciplinary policies"},
                {"title": "Mess Menu & Nutrition Chart", "url": "https://college.edu/hostel/mess-menu.pdf", "snippet": "Daily menu with nutritional information and special dietary options"},
                {"title": "Hostel Application Form", "url": "https://portal.college.edu/hostel/application", "snippet": "Online application system for hostel room booking"}
            ],
            "fees": [
                {"title": "Fee Structure 2024-25", "url": "https://college.edu/accounts/fee-structure.pdf", "snippet": "Detailed semester-wise fee breakdown for all courses"},
                {"title": "Online Payment Guide", "url": "https://college.edu/accounts/payment-guide.pdf", "snippet": "Step-by-step instructions for online fee payment"},
                {"title": "Scholarship Schemes", "url": "https://college.edu/accounts/scholarships.pdf", "snippet": "Available scholarships, eligibility criteria, and application process"},
                {"title": "Refund Policy Document", "url": "https://college.edu/accounts/refund-policy.pdf", "snippet": "Terms and conditions for fee refund in various scenarios"}
            ],
            "transport": [
                {"title": "Bus Route Map 2024", "url": "https://college.edu/transport/route-map.pdf", "snippet": "Detailed map showing all 18 bus routes with pickup points and timings"},
                {"title": "College Transport Mobile App", "url": "https://play.google.com/store/apps/details?id=college.transport", "snippet": "Real-time bus tracking and notifications mobile application"},
                {"title": "Bus Pass Application Form", "url": "https://portal.college.edu/transport/bus-pass", "snippet": "Online application for monthly and semester bus passes"},
                {"title": "Transport Safety Guidelines", "url": "https://college.edu/transport/safety.pdf", "snippet": "Safety protocols and emergency procedures for college transport"}
            ],
            "placement": [
                {"title": "Placement Statistics Report 2024", "url": "https://college.edu/placements/stats-2024.pdf", "snippet": "Comprehensive placement data with company-wise and branch-wise analysis"},
                {"title": "Training & Development Curriculum", "url": "https://college.edu/placements/training.pdf", "snippet": "Pre-placement training modules and skill development programs"},
                {"title": "Alumni Success Stories", "url": "https://college.edu/placements/alumni-stories.pdf", "snippet": "Career journeys and achievements of notable alumni"},
                {"title": "Industry Connect Program", "url": "https://college.edu/placements/industry-connect.pdf", "snippet": "Industry partnerships, internship opportunities, and mentorship programs"}
            ],
            "academic": [
                {"title": "Academic Calendar 2024-25", "url": "https://college.edu/academics/calendar.pdf", "snippet": "Important academic dates, examination schedule, and holiday list"},
                {"title": "Examination Guidelines", "url": "https://college.edu/academics/exam-guidelines.pdf", "snippet": "Exam rules, grading system, and result declaration process"},
                {"title": "LMS User Manual", "url": "https://college.edu/academics/lms-guide.pdf", "snippet": "Learning Management System features and usage instructions"},
                {"title": "Academic Regulations", "url": "https://college.edu/academics/regulations.pdf", "snippet": "Credit system, attendance policy, and promotion criteria"}
            ]
        }
    
    def generate_response(self, query: str, language: str = "en", conversation_history: List[Dict] | None = None) -> Dict[str, Any]:
        """Generate dummy AI response based on query keywords"""
        query_lower = query.lower()
        
        # Context-aware responses based on conversation history
        context = self._analyze_conversation_context(conversation_history) if conversation_history else {}
        
        # Determine response category based on keywords
        category = self._detect_category(query_lower)
        
        # Handle greeting and context-aware responses
        if any(word in query_lower for word in ["hello", "hi", "hey", "namaste"]):
            if context.get("returning_user"):
                response_text = f"Welcome back! I see you were asking about {context.get('last_topic', 'campus information')} earlier. How can I help you today?"
            else:
                response_text = "Hello! I'm Manny, your campus assistant. I can help you with information about library, cafeteria, admissions, hostel, fees, transport, placements, and academics. What would you like to know?"
            category = "greeting"
            
        elif any(word in query_lower for word in ["thank", "thanks", "dhanyawad"]):
            follow_up_suggestions = self._get_follow_up_suggestions(context.get("last_topic"))
            response_text = f"You're welcome! {follow_up_suggestions}"
            category = "gratitude"
            
        elif "help" in query_lower or "?" in query and len(query.split()) <= 3:
            response_text = self._get_help_response(context)
            category = "help"
            
        elif category != "general":
            # Get context-aware response for specific category
            response_text = self._get_context_aware_response(category, query_lower, context)
        else:
            response_text = self._get_general_response(query_lower, context)
        
        # Generate sources based on category
        sources = self._get_relevant_sources(category, query_lower)
        
        # Generate sophisticated flags
        flags = self._generate_response_flags(query_lower, category, context, response_text)
        
        return {
            "response": response_text,
            "sources": sources,
            "flags": flags,
            "tts_audio_url": self._get_tts_url(response_text, language) if language == "en" else None
        }
    
    def _analyze_conversation_context(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation history for context"""
        if not history:
            return {}
        
        context = {
            "returning_user": len(history) > 1,
            "message_count": len(history),
            "topics_discussed": [],
            "last_topic": None,
            "user_sentiment": "neutral"
        }
        
        # Analyze recent messages for topics
        for msg in history[-3:]:  # Look at last 3 messages
            query = msg.get("user_query", "").lower()
            topic = self._detect_category(query)
            if topic != "general":
                context["topics_discussed"].append(topic)
        
        if context["topics_discussed"]:
            context["last_topic"] = context["topics_discussed"][-1]
        
        # Simple sentiment analysis
        recent_query = history[-1].get("user_query", "").lower()
        if any(word in recent_query for word in ["urgent", "immediate", "asap", "emergency"]):
            context["user_sentiment"] = "urgent"
        elif any(word in recent_query for word in ["confused", "don't understand", "unclear"]):
            context["user_sentiment"] = "confused"
        
        return context
    
    def _detect_category(self, query_lower: str) -> str:
        """Detect category from query with improved keyword matching"""
        keyword_map = {
            "library": ["library", "book", "borrow", "study room", "reading", "journal", "database", "reference"],
            "cafeteria": ["cafeteria", "food", "mess", "menu", "meal", "dining", "canteen", "breakfast", "lunch", "dinner"],
            "admission": ["admission", "apply", "application", "entrance", "eligibility", "merit", "cutoff", "counseling"],
            "hostel": ["hostel", "accommodation", "room", "mess", "warden", "staying", "residence"],
            "fees": ["fee", "payment", "dues", "scholarship", "installment", "refund", "accounts"],
            "transport": ["bus", "transport", "route", "pickup", "drop", "travel", "vehicle"],
            "placement": ["placement", "job", "company", "interview", "resume", "career", "recruitment", "internship"],
            "academic": ["exam", "grade", "result", "semester", "course", "subject", "attendance", "cgpa", "marks"]
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return "general"
    
    def _get_context_aware_response(self, category: str, query_lower: str, context: Dict) -> str:
        """Get context-aware response for specific category"""
        base_responses = self.campus_responses.get(category, [])
        
        if not base_responses:
            return self._get_general_response(query_lower, context)
        
        # Choose response based on context and specific keywords
        if category == "library" and "timing" in query_lower:
            return base_responses[0]  # Timing-specific response
        elif category == "library" and any(word in query_lower for word in ["room", "study", "booking"]):
            return base_responses[2]  # Study room response
        elif category == "cafeteria" and "menu" in query_lower:
            return base_responses[1]  # Menu-specific response
        elif category == "admission" and "document" in query_lower:
            return base_responses[1]  # Document-specific response
        elif category == "fees" and "scholarship" in query_lower:
            return base_responses[3]  # Scholarship response
        elif context.get("user_sentiment") == "urgent":
            # Provide more direct, actionable responses for urgent queries
            urgent_responses = {
                "library": "For immediate library assistance, contact the help desk at ext. 2031 or visit the circulation counter on the ground floor.",
                "cafeteria": "For urgent food service issues, contact the mess manager at ext. 2045 or visit the main cafeteria office.",
                "academic": "For urgent academic matters, contact the academic office at ext. 2001 or visit Room 101, Administrative Building."
            }
            return urgent_responses.get(category, base_responses[0])
        
        # Return random response for variety
        return random.choice(base_responses)
    
    def _get_follow_up_suggestions(self, last_topic: str | None) -> str:
        """Get follow-up suggestions based on last topic"""
        suggestions = {
            "library": "Would you like to know about digital resources or study room booking?",
            "cafeteria": "Need information about meal plans or food court vendors?",
            "admission": "Would you like details about the admission process or required documents?",
            "hostel": "Interested in room facilities or mess timings?",
            "fees": "Need help with payment methods or scholarship information?",
            "transport": "Want to know about specific routes or bus timings?",
            "placement": "Looking for training programs or company information?",
            "academic": "Need details about exam schedule or grading system?"
        }
        
        return suggestions.get(last_topic or "general", "Is there anything else I can help you with?")
    
    def _get_help_response(self, context: Dict) -> str:
        """Generate helpful response based on context"""
        if context.get("last_topic"):
            return f"I can provide more information about {context['last_topic']} or help you with other topics like library, cafeteria, admissions, hostel, fees, transport, placements, and academics. What specific information do you need?"
        else:
            return "I'm here to help you with campus information! I can assist with:\n• Library services and timings\n• Cafeteria menus and meal plans\n• Admission procedures\n• Hostel accommodation\n• Fee structure and payments\n• Transport routes\n• Placement activities\n• Academic information\n\nWhat would you like to know about?"
    
    def _get_general_response(self, query_lower: str, context: Dict) -> str:
        """Generate general response when category is not detected"""
        if context.get("user_sentiment") == "confused":
            return "I understand you might be looking for specific information. Could you please tell me which area you need help with? For example, you can ask about library timings, cafeteria menu, admission process, hostel facilities, fees, transport, placements, or academics."
        
        return f"I'm here to help with campus information. While I couldn't find specific details about '{query_lower}', I can help you with library services, dining options, admission procedures, hostel facilities, fee information, transport, placement activities, and academic matters. Could you please be more specific about what you're looking for?"
    
    def _get_relevant_sources(self, category: str, query_lower: str) -> List[Dict]:
        """Get relevant sources based on category and query"""
        if category in self.sources_data:
            all_sources = self.sources_data[category]
            
            # Filter sources based on specific keywords in query
            relevant_sources = []
            for source in all_sources:
                if any(keyword in source["title"].lower() or keyword in source["snippet"].lower() 
                      for keyword in query_lower.split()):
                    relevant_sources.append(source)
            
            # If no specific matches, return first 2 sources
            if not relevant_sources:
                relevant_sources = all_sources[:2]
            
            return relevant_sources[:3]  # Maximum 3 sources
        
        return []
    
    def _generate_response_flags(self, query_lower: str, category: str, context: Dict, response_text: str) -> Dict[str, Any]:
        """Generate sophisticated flags for the response"""
        flags = {
            "contains_personal_info": any(word in query_lower for word in ["my", "me", "i am", "student id", "name"]),
            "requires_followup": "?" in query_lower and len(query_lower.split()) > 10,
            "confidence_score": self._calculate_confidence(category, query_lower),
            "category": category,
            "language_detected": self.detect_language(query_lower),
            "sentiment": context.get("user_sentiment", "neutral"),
            "response_type": self._get_response_type(category, query_lower),
            "urgency_level": "high" if context.get("user_sentiment") == "urgent" else "normal",
            "topic_continuation": category == context.get("last_topic"),
            "contains_numbers": bool(re.search(r'\d', response_text)),
            "actionable": any(word in response_text.lower() for word in ["contact", "visit", "apply", "submit", "book"])
        }
        
        return flags
    
    def _calculate_confidence(self, category: str, query_lower: str) -> float:
        """Calculate confidence score based on category detection and query clarity"""
        if category == "general":
            return round(random.uniform(0.3, 0.6), 2)
        
        # Higher confidence for specific keywords
        specific_keywords = {
            "library": ["library", "book", "study room"],
            "cafeteria": ["cafeteria", "food", "menu"],
            "admission": ["admission", "apply", "entrance"],
            "hostel": ["hostel", "room", "accommodation"],
            "fees": ["fee", "payment", "scholarship"],
            "transport": ["bus", "transport", "route"],
            "placement": ["placement", "job", "company"],
            "academic": ["exam", "grade", "semester"]
        }
        
        keyword_matches = sum(1 for keyword in specific_keywords.get(category, []) if keyword in query_lower)
        base_confidence = 0.7 + (keyword_matches * 0.1)
        
        return round(min(base_confidence, 0.98), 2)
    
    def _get_response_type(self, category: str, query_lower: str) -> str:
        """Determine the type of response"""
        if any(word in query_lower for word in ["how", "what", "when", "where", "why"]):
            return "informational"
        elif any(word in query_lower for word in ["can i", "should i", "may i"]):
            return "guidance"
        elif "?" in query_lower:
            return "question"
        else:
            return "general"
    
    def _get_tts_url(self, text: str, language: str) -> str:
        """Generate TTS URL for the response"""
        text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
        return f"/api/tts/audio/response_{text_hash}_{language}.mp3"
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on script"""
        # Hindi/Devanagari detection
        if any('\u0900' <= char <= '\u097F' for char in text):
            return "hi"
        # Tamil detection
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):
            return "ta"
        # Add more language detection logic as needed
        else:
            return "en"
    
    def get_conversation_summary(self, messages: List[Dict]) -> str:
        """Generate a conversation summary for thread titles"""
        if not messages:
            return "New Conversation"
        
        first_message = messages[0].get('user_query', '')
        if len(first_message) > 50:
            return first_message[:47] + "..."
        return first_message or f"Conversation {datetime.now().strftime('%m/%d %H:%M')}"
