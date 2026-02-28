# SIH25 - Manny Multilingual Campus Chatbot Project

## 🎯 **Project Overview**

**Manny** is a multilingual campus chatbot designed to be embedded inside college SLCM (Student Life Cycle Management) portals. Students can authenticate through their existing SLCM login and interact with an AI-powered assistant for campus-related queries in multiple languages.

## 🏗️ **Current Project Structure**

```
SIH25/
├── .git/                                    # Git repository
└── frontend/                                # React TypeScript Frontend
    ├── public/
    │   ├── favicon.ico
    │   ├── robots.txt
    │   └── placeholder.svg
    ├── src/
    │   ├── assets/
    │   │   └── muj-logo.png                 # University logo
    │   ├── components/
    │   │   ├── dashboard/
    │   │   │   ├── ChatWidget.tsx           # 🤖 Main Manny chat component
    │   │   │   ├── Header.tsx               # Dashboard header
    │   │   │   ├── MainContent.tsx          # Dashboard main content
    │   │   │   └── Sidebar.tsx              # Dashboard sidebar
    │   │   ├── ui/                          # shadcn/ui components (50+ components)
    │   │   │   ├── button.tsx
    │   │   │   ├── card.tsx
    │   │   │   ├── input.tsx
    │   │   │   ├── dialog.tsx
    │   │   │   └── ... (complete UI library)
    │   │   └── theme-provider.tsx           # Dark/light theme support
    │   ├── hooks/
    │   │   ├── use-toast.ts                 # Toast notifications
    │   │   └── use-mobile.tsx               # Mobile detection
    │   ├── lib/
    │   │   └── utils.ts                     # Utility functions
    │   ├── pages/
    │   │   ├── Dashboard.tsx                # 🏠 Main SLCM dashboard
    │   │   ├── Login.tsx                    # 🔐 SLCM login page
    │   │   ├── Index.tsx
    │   │   └── NotFound.tsx
    │   ├── App.tsx                          # Main app component
    │   ├── App.css
    │   ├── index.css                        # Global styles
    │   ├── main.tsx                         # App entry point
    │   └── vite-env.d.ts
    ├── package.json                         # Dependencies & scripts
    ├── package-lock.json
    ├── vite.config.ts                       # Vite configuration
    ├── tailwind.config.ts                   # Tailwind CSS config
    ├── tsconfig.json                        # TypeScript config
    ├── eslint.config.js                     # ESLint config
    ├── postcss.config.js                    # PostCSS config
    ├── components.json                      # shadcn/ui config
    └── .gitignore
```

## 🚀 **Tech Stack**

### **Frontend (Current)**
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **UI Library:** shadcn/ui (Radix UI primitives)
- **Styling:** Tailwind CSS with custom gradients
- **State Management:** React Query (@tanstack/react-query)
- **Routing:** React Router DOM
- **Form Handling:** React Hook Form with Zod validation
- **Icons:** Lucide React
- **Theme:** Dark/Light mode support with next-themes

### **Backend (Missing - Needs Implementation)**
- **Planned:** FastAPI with Python
- **Database:** PostgreSQL/SQLite
- **AI Integration:** LangChain + ML pipeline (handled by other teammates)

## 🎨 **Key Features Implemented**

### **✅ Chat Widget (Manny)**
- **3 States:** Floating button → Docked panel → Fullscreen mode
- **Responsive:** Mobile-first design with bottom sheet on mobile
- **Features:**
  - Real-time messaging interface
  - Chat history sidebar (fullscreen mode)
  - Typing indicators and animations
  - Avatar-based message bubbles
  - Smooth transitions between states
  - Glass-morphism design effects

### **✅ SLCM Portal Simulation**
- **Login Page:** University-branded login with MUJ logo
- **Dashboard:** Complete SLCM portal simulation
- **Authentication:** Mock authentication system
- **Responsive:** Mobile and desktop optimized

### **✅ UI/UX Excellence**
- **Design System:** Complete shadcn/ui component library
- **Gradients:** Custom orange gradient theming
- **Animations:** Smooth transitions and micro-interactions
- **Glass Effects:** Modern glass-morphism styling
- **Accessibility:** Proper ARIA labels and keyboard navigation

## 🔧 **Development Setup**

### **Prerequisites**
```bash
Node.js 18+ 
npm or bun
```

### **Current Setup Commands**
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### **Development URLs**
- **Frontend:** `http://localhost:5173` (Vite default)
- **Backend API:** Not implemented yet

## 🎯 **What's Missing / Next Steps**

### **🔴 Critical Missing Components**

1. **Backend API Integration**
   - Need FastAPI backend with chat endpoints
   - Database for conversation logging
   - API integration in ChatWidget component

2. **AI/ML Integration**
   - Connect to LangChain pipeline (teammate responsibility)
   - Message processing and response generation
   - Multilingual support implementation

3. **Real SLCM Integration**
   - Authentication system integration
   - Student data API endpoints
   - Campus resource APIs (timetable, notices, etc.)

### **🟡 Enhancement Opportunities**

1. **Chat Functionality**
   - File upload support
   - Voice input/output
   - Message search and filtering
   - Export chat history

2. **Campus Features**
   - Timetable integration
   - Notice board integration
   - Fee payment status
   - Exam schedules
   - Library book availability

3. **Advanced Features**
   - Push notifications
   - Offline mode support
   - Multi-language UI
   - Admin dashboard for chat analytics

## 🤖 **Manny Chat Widget Details**

### **Component Architecture**
```tsx
ChatWidget.tsx
├── State Management (3 modes)
│   ├── floating: Minimized button
│   ├── docked: Panel view
│   └── fullscreen: Full app takeover
├── Message System
│   ├── User messages
│   ├── Bot responses
│   └── Chat history
├── UI Variations
│   ├── Mobile: Bottom sheet
│   ├── Desktop: Floating panel
│   └── Fullscreen: Sidebar + main chat
└── Features
    ├── Real-time messaging
    ├── Responsive design
    ├── Theme support
    └── Accessibility
```

### **Integration Points for Backend**
```typescript
// API calls needed in ChatWidget
const sendMessage = async (message: string) => {
  // POST /api/chat/message
  // Send user message to backend
  // Receive AI response
}

const getChatHistory = async (studentId: string) => {
  // GET /api/chat/history/{studentId}
  // Load previous conversations
}

const getResources = async (type: string) => {
  // GET /api/resources/{type}
  // Get campus resources (timetable, notices, etc.)
}
```

## 🎨 **Design System**

### **Color Scheme**
- **Primary:** Orange gradient (`bg-gradient-orange`)
- **Secondary:** Gray-based with proper contrast
- **Glass Effects:** Semi-transparent backgrounds with blur
- **Theme Support:** Dark/light mode switching

### **Typography**
- **Modern Sans-serif** font stack
- **Responsive sizing** with Tailwind utilities
- **Proper hierarchy** with semantic HTML

### **Components Available**
- 50+ shadcn/ui components ready to use
- Custom chat-specific components
- Responsive navigation components
- Form components with validation

## 🚀 **Deployment Ready**

### **Frontend Deployment**
- **Vite build** optimized for production
- **Environment variables** support
- **PWA ready** (can be converted)
- **Vercel/Netlify** deployment ready

### **Missing for Production**
- Backend API endpoints
- Database setup
- Authentication integration
- Environment configuration

## 🤝 **Team Integration Guide**

### **For Backend Developer**
1. Create FastAPI backend with these endpoints:
   - `POST /api/chat/message`
   - `GET /api/chat/history/{studentId}`
   - `GET /api/resources/{type}`
2. Update ChatWidget.tsx to call real APIs
3. Add authentication middleware

### **For AI/ML Team**
1. Frontend will send messages to backend
2. Backend will forward to your AI pipeline
3. Return structured responses with resources
4. Multilingual processing on your end

### **For DevOps Team**
1. Frontend: Deploy to Vercel/Netlify
2. Backend: Deploy to cloud platform
3. Database: Set up PostgreSQL
4. Configure environment variables

---

**The frontend is 90% complete and production-ready. The main missing piece is the backend API integration and AI pipeline connection.**
