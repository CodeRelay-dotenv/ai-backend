# EduFlow-Nexus - AI Backend 🤖  

**Powering Intelligent Campus Solutions with Scalable AI**  

This repository hosts the **AI-driven backend** for EduFlow-Nexus’s campus life transformation platform. Built on FastAPI, GCP, and Docker, it delivers core functionalities like visual query processing, automated note generation, and video-to-notes conversion to empower students and educators.  

*Deployed on GCP with Docker for scalability. Actively developed during a 30-hour hackathon!*  

---

## 🎯 Project Overview  

**Goal**: Build a robust, scalable AI backend to support peer-to-peer learning, accessible education, and seamless academic workflows.  
**Current Focus**: Optimizing AI models for visual queries, chatbots, and real-time audio processing.  

---

## 🚀 Key Features  

### **1. Canvas-Integrated AI Tools**  
- **Visual Query Engine**:  
  - **How It Works**: Analyzes hand-drawn diagrams/images → generates code, flowcharts, or explanations (e.g., sketch a graph → get Python code for traversal).  
  - **Use Case**: Students/educators quickly convert ideas into executable formats.  
  - **Business Model**: License to universities for STEM labs; premium API access for EdTech firms.  

- **Text-to-Notes Generator**:  
  - **How It Works**: Extracts key concepts from lectures/textbooks → creates structured, visual summaries.  
  - **Use Case**: Automate study guides for fast-paced courses.  

### **2. Administrative ChatBot**  
- **How It Works**:  
  - Trained on college-specific data (policies, schedules, FAQs) → answers queries.  
  - **Use Case**: “What’s the deadline for course registration?” → Instant, accurate response.  
  - **Business Model**: B2B SaaS model – colleges pay for customization and support.
    
### **3. Video-to-Notes Pipeline**  
- **How It Works**:  
- **Use Case**: Supports students with disabilities, internships, or language barriers.  
- **Business Model**: Freemium tier for students; institutional subscriptions for bulk access.  

---

## 🛠️ Technical Architecture  
- **Framework**: FastAPI + Uvicorn.  
- **Deployment**: Dockerized microservices on GCP Compute Engine.  
- **APIs**:  
  - `/generate-content` (POST): Process images → return code/diagrams.  
  - `/extract-text` (POST): Fetch answers from college-specific knowledge base.  
  - `/generate-notes` (POST): Async video-to-notes pipeline. 

---

## 🚄 Quick Setup  
```bash  
git clone https://github.com/CodeRelay-dotenv/ai-backend.git  
docker-compose up --build  # Requires GCP credentials in ./gcp-credentials
```

---

## 📌 Business Impact  

**Driving Value Through AI-Powered Solutions**  

| Feature                   | Revenue Model                          | Target Audience          | Scalability                           |  
|---------------------------|----------------------------------------|--------------------------|---------------------------------------|  
| **Canvas-Integrated AI**  | - API licensing to Universities and Edtech Firms<br>- API subscriptions for  Students | STEM departments, educators | Integrate with LMS platforms |  
| **Administrative ChatBot**| - Annual SaaS contracts<br>- Customization fees | Colleges, universities  | Deploy across multi-campus institutions |  
| **Video-to-Notes**        | - Freemium model (basic vs. premium)<br>- Institutional bulk plans | Students facing language barrier or disabilities | Partner with video platforms extensions (Zoom, Teams) |  
| **Peer-to-Peer Tutoring** | - Certification fees for reputation tiers<br>- Academic research recruitment partnerships<br>- Foster Campus Engagement | Students, Adademic researchers      | Expand to global university networks  |  

---

### College Impact • Hackathon-Built • Built for Scale
**🔗 Frontend Repository: [web2](https://github.com/CodeRelay-dotenv/web2)**

_“Empowering campuses with AI that sees, hears, and understands.”_
