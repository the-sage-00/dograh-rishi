# 🎙️ Audexly - Voice AI Platform

> Building a commercial Voice AI SaaS platform based on Dograh, optimized for the Indian market.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [What We've Done](#-what-weve-done)
3. [Current Status](#-current-status)
4. [Technology Stack](#-technology-stack)
5. [Architecture](#-architecture)
6. [Phase 0: Testing (Current)](#-phase-0-testing-current)
7. [Future Phases](#-future-phases)
8. [How to Run](#-how-to-run)
9. [Files & Structure](#-files--structure)
10. [Roadmap](#-roadmap)

---

## 🎯 Project Overview

### What is Audexly?

Audexly is a **Voice AI SaaS Platform** that enables businesses to deploy AI-powered voice agents for:
- 📞 **Customer Support** - 24/7 automated support calls
- 💼 **Sales Outreach** - Lead qualification and follow-ups
- 📊 **Surveys** - Automated feedback collection
- ⏰ **Reminders** - Appointment confirmations and notifications

### Why Audexly?

| Problem | Audexly Solution |
|---------|------------------|
| Expensive call centers | AI agents at fraction of cost |
| Limited working hours | 24/7 availability |
| Inconsistent quality | Consistent, trained AI responses |
| Language barriers | Multi-language support (Hindi/English) |
| Scaling challenges | Instant scaling with AI |

### Target Market

- **India-first** with Exotel telephony
- **SMBs and Enterprises** needing voice automation
- **Industries**: Healthcare, E-commerce, Banking, Real Estate

---

## ✅ What We've Done

### Session Summary (January 18, 2026)

#### 1. Business Analysis & Planning
- ✅ Analyzed Dograh repository for commercial viability
- ✅ Confirmed **BSD 2-Clause License** allows commercial use
- ✅ Identified all telemetry points (Sentry, PostHog)
- ✅ Created business analysis document

#### 2. Repository Setup
- ✅ Forked Dograh to: `github.com/the-sage-00/dograh-rishi`
- ✅ Cloned with Pipecat submodule
- ✅ Created `audexly/` working directory

#### 3. Configuration & Security
- ✅ Created `docker-compose.audexly.yaml` with **ALL TELEMETRY DISABLED**
- ✅ Created `.env.audexly.example` template
- ✅ Created `.env` with your actual API keys (not in git)
- ✅ Removed Sentry DSN and PostHog keys from config

#### 4. Documentation Created
- ✅ `AUDEXLY_SETUP_GUIDE.md` - Step-by-step setup
- ✅ `docs/EXOTEL_INTEGRATION_GUIDE.md` - Exotel configuration
- ✅ `docs/EXOTEL_INTEGRATION_TODO.md` - Remaining work
- ✅ `DOGRAH_BUSINESS_ANALYSIS.md` - Business viability analysis

#### 5. Voice Agent Prompts
Created 5 professional prompt templates:
- ✅ `prompts/test_agent.md` - Initial testing
- ✅ `prompts/sales_agent.md` - Outbound sales
- ✅ `prompts/support_agent.md` - Customer support
- ✅ `prompts/survey_agent.md` - Feedback collection
- ✅ `prompts/appointment_reminder.md` - Reminders

#### 6. Exotel Integration (Partial)
- ✅ Created `ExotelProvider` class in backend
- ✅ Updated telephony factory to include Exotel
- ⏳ Transport and pipeline integration pending

#### 7. Docker Deployment
- ✅ Started all services with `docker compose`
- ✅ Verified dashboard accessible at http://localhost:3010
- ✅ Cloudflare tunnel running for webhook access

---

## 📊 Current Status

### Services Running

| Service | URL | Status |
|---------|-----|--------|
| Dashboard UI | http://localhost:3010 | ✅ Running |
| API Backend | http://localhost:8000 | ✅ Healthy |
| API Docs | http://localhost:8000/docs | ✅ Available |
| PostgreSQL | localhost:5432 | ✅ Healthy |
| Redis | localhost:6379 | ✅ Healthy |
| MinIO | http://localhost:9001 | ✅ Running |
| Cloudflare Tunnel | *.trycloudflare.com | ✅ Active |

### Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| **Web Call (WebRTC)** | ✅ Ready | Test voice agents in browser |
| **Twilio Telephony** | ✅ Ready | Built into Dograh |
| **Vonage Telephony** | ✅ Ready | Built into Dograh |
| **Exotel Telephony** | 🔄 50% | Provider created, needs transport |
| **OpenAI LLM** | ✅ Ready | Configure in Models |
| **Sarvam STT/TTS** | ✅ Ready | Configure in Models |
| **Telemetry** | ✅ Disabled | No data to external services |

### API Keys Configured

```
✅ OpenAI: sk-proj-euw4Rszw6Y8G... (in .env)
✅ Sarvam: sk_f5xrqolc_JQhTwUSm... (in .env)
✅ Exotel: callmate4 / 6965b8a... (in .env)
```

---

## 🛠️ Technology Stack

### Your Stack (Audexly)

| Component | Technology | Why |
|-----------|------------|-----|
| **Telephony** | Exotel | India-optimized, local numbers |
| **STT** | Sarvam AI | Best Hindi/English accuracy |
| **TTS** | Sarvam AI | Natural Indian voices |
| **LLM** | OpenAI GPT-4o-mini | Fast, cost-effective, smart |
| **Frontend** | Next.js + TailwindCSS | Modern, responsive UI |
| **Backend** | FastAPI (Python) | Fast, async, well-structured |
| **Voice Engine** | Pipecat | Modular, low-latency pipeline |
| **Database** | PostgreSQL | Reliable, feature-rich |
| **Cache** | Redis | Fast session/cache storage |
| **Storage** | MinIO (S3-compatible) | Call recordings, files |

### Dograh Foundation

| Component | Status |
|-----------|--------|
| Multi-tenant architecture | ✅ Built-in |
| User/Organization management | ✅ Built-in |
| Workflow builder (visual) | ✅ Built-in |
| Call recording & transcription | ✅ Built-in |
| Analytics & usage tracking | ✅ Built-in |
| Campaign management | ✅ Built-in |
| API key management | ✅ Built-in |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AUDEXLY PLATFORM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         FRONTEND (Next.js)                          │    │
│  │  • Dashboard & Analytics        • Workflow Builder                  │    │
│  │  • Model Configuration          • Campaign Management               │    │
│  │  • User Management              • Telephony Configuration           │    │
│  │                                                                     │    │
│  │  URL: http://localhost:3010                                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         BACKEND (FastAPI)                           │    │
│  │  • REST API                      • WebSocket Handlers               │    │
│  │  • Authentication                • Telephony Routes                 │    │
│  │  • Database Operations           • Pipeline Orchestration           │    │
│  │                                                                     │    │
│  │  URL: http://localhost:8000                                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                    │                 │                    │                  │
│         ┌─────────┴──────┐   ┌──────┴──────┐   ┌────────┴────────┐        │
│         ▼                ▼   ▼              ▼   ▼                ▼        │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────────┐   │
│  │ PostgreSQL │   │   Redis    │   │   MinIO    │   │    Pipecat     │   │
│  │ (Database) │   │  (Cache)   │   │ (Storage)  │   │ (Voice Engine) │   │
│  │            │   │            │   │            │   │                │   │
│  │ • Users    │   │ • Sessions │   │ • Recordings│  │ • STT Pipeline │   │
│  │ • Workflows│   │ • Cache    │   │ • Transcripts│ │ • LLM Pipeline │   │
│  │ • Calls    │   │ • Queues   │   │ • Files     │  │ • TTS Pipeline │   │
│  └────────────┘   └────────────┘   └────────────┘   └────────────────┘   │
│                                                              │             │
│                                                              ▼             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     EXTERNAL SERVICES (Your Keys)                   │   │
│  │                                                                     │   │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────────┐  │   │
│  │  │   EXOTEL    │   │  SARVAM AI  │   │        OPENAI           │  │   │
│  │  │ (Telephony) │   │ (STT + TTS) │   │        (LLM)            │  │   │
│  │  │             │   │             │   │                         │  │   │
│  │  │ • Inbound   │   │ • saarika   │   │ • gpt-4o-mini           │  │   │
│  │  │ • Outbound  │   │ • bulbul    │   │ • Context management    │  │   │
│  │  │ • AgentStream│  │             │   │                         │  │   │
│  │  └─────────────┘   └─────────────┘   └─────────────────────────┘  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Phase 0: Testing (Current)

### Objective
Test the core voice agent locally until:
- ✅ Latency < 2-3 seconds response
- ✅ Prompts work perfectly
- ✅ Call quality is production-ready

### How to Test NOW

#### 1. Start Services
```powershell
cd c:\Users\saini\OneDrive\Desktop\onelastmore\audexly
docker compose -f docker-compose.audexly.yaml up -d
```

#### 2. Open Dashboard
Navigate to: http://localhost:3010

#### 3. Configure API Keys (via UI)
1. Go to **Models** in sidebar
2. Add your OpenAI key
3. Add your Sarvam key

#### 4. Create a Voice Agent
1. Click **"Create Voice Agent"**
2. Choose **Inbound** for testing
3. Use this test prompt:

```
You are a friendly AI assistant testing voice calls.

Rules:
1. Keep responses SHORT - 1-2 sentences only
2. Be helpful and conversational
3. If asked your name, say "I'm Alex, your AI assistant"

Start by saying: "Hello! I'm Alex. How can I help you today?"
```

#### 5. Test with Web Call
1. Open your workflow
2. Click **"Web Call"** button
3. Allow microphone access
4. Start talking!

### Metrics to Track

| Metric | Target | How to Measure |
|--------|--------|----------------|
| First response time | < 2s | Stopwatch from end of speech |
| Turn-around time | < 3s | Full response cycle |
| STT accuracy | > 95% | Compare transcript to speech |
| Natural conversation | Subjective | Does it feel smooth? |

---

## 🚀 Future Phases

### Phase 1: Core Platform (2-3 weeks)
- [ ] Complete Exotel integration
- [ ] Custom branding (rename Dograh → Audexly)
- [ ] User authentication polish
- [ ] Basic billing setup

### Phase 2: Production Ready (2-3 weeks)  
- [ ] Production deployment (AWS/DigitalOcean)
- [ ] SSL certificates
- [ ] Domain setup
- [ ] Payment integration (Razorpay)

### Phase 3: Customer Features (3-4 weeks)
- [ ] Multi-tenant improvements
- [ ] White-label support
- [ ] Advanced analytics
- [ ] API documentation

### Phase 4: Scale (Ongoing)
- [ ] Performance optimization
- [ ] Auto-scaling
- [ ] Enterprise features
- [ ] More telephony providers

---

## 🖥️ How to Run

### Prerequisites
- Docker Desktop installed and running
- Git
- API keys: OpenAI, Sarvam, Exotel

### Quick Start

```powershell
# 1. Navigate to project
cd c:\Users\saini\OneDrive\Desktop\onelastmore\audexly

# 2. Copy environment template (if not done)
cp .env.audexly.example .env

# 3. Edit .env with your API keys
# (Already done with your keys)

# 4. Start all services
docker compose -f docker-compose.audexly.yaml up -d

# 5. Check status
docker ps

# 6. View logs
docker compose -f docker-compose.audexly.yaml logs -f
```

### Access Points

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:3010 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MinIO Console | http://localhost:9001 |

### Useful Commands

```powershell
# Stop all services
docker compose -f docker-compose.audexly.yaml down

# Restart services
docker compose -f docker-compose.audexly.yaml restart

# View specific logs
docker logs audexly-api -f
docker logs audexly-ui -f

# Get tunnel URL (for Exotel webhooks)
docker logs audexly-tunnel 2>&1 | Select-String "trycloudflare"

# Reset everything (WARNING: deletes data)
docker compose -f docker-compose.audexly.yaml down -v
```

---

## 📁 Files & Structure

```
c:\Users\saini\OneDrive\Desktop\onelastmore\
├── audexly/                              # Your forked Dograh repository
│   ├── docker-compose.audexly.yaml       # ✅ Telemetry-disabled config
│   ├── .env.audexly.example              # ✅ API key template
│   ├── .env                              # ✅ Your actual keys (gitignored)
│   ├── AUDEXLY_SETUP_GUIDE.md            # ✅ Setup instructions
│   │
│   ├── api/                              # Backend (FastAPI)
│   │   ├── services/
│   │   │   ├── telephony/
│   │   │   │   ├── providers/
│   │   │   │   │   ├── exotel_provider.py    # ✅ NEW: Exotel integration
│   │   │   │   │   ├── twilio_provider.py
│   │   │   │   │   ├── vonage_provider.py
│   │   │   │   │   └── vobiz_provider.py
│   │   │   │   └── factory.py            # ✅ MODIFIED: Added Exotel
│   │   │   └── pipecat/                  # Voice pipeline services
│   │   ├── routes/                       # API endpoints
│   │   └── db/                           # Database models
│   │
│   ├── ui/                               # Frontend (Next.js)
│   │   ├── src/
│   │   │   ├── app/                      # Pages
│   │   │   └── components/               # React components
│   │   └── public/                       # Static assets
│   │
│   ├── pipecat/                          # Voice engine (submodule)
│   │   └── src/pipecat/
│   │       └── serializers/
│   │           └── exotel.py             # ✅ Exotel audio handling
│   │
│   ├── prompts/                          # ✅ Voice agent prompts
│   │   ├── test_agent.md
│   │   ├── sales_agent.md
│   │   ├── support_agent.md
│   │   ├── survey_agent.md
│   │   └── appointment_reminder.md
│   │
│   └── docs/                             # Documentation
│       ├── EXOTEL_INTEGRATION_GUIDE.md   # ✅ Exotel setup guide
│       └── EXOTEL_INTEGRATION_TODO.md    # ✅ Remaining work
│
├── AUDEXLY_PLATFORM_PLAN.md              # Overall platform vision
├── PHASE0_AGENT_TESTING.md               # Current phase objectives
└── DOGRAH_BUSINESS_ANALYSIS.md           # Business viability analysis
```

---

## 🗺️ Roadmap

### Immediate (This Week)
- [x] Fork and clone Dograh
- [x] Disable telemetry
- [x] Configure API keys
- [x] Start services locally
- [x] Create prompt templates
- [x] Start Exotel integration
- [ ] Test voice agent with Web Call
- [ ] Iterate on prompts

### Short-term (2-4 weeks)
- [ ] Complete Exotel integration
- [ ] Rebrand to Audexly
- [ ] Production deployment
- [ ] First customer demo

### Medium-term (1-3 months)
- [ ] Payment integration
- [ ] Multi-tenant polish
- [ ] Marketing website
- [ ] First paying customers

### Long-term (3-6 months)
- [ ] Scale infrastructure
- [ ] Add more features
- [ ] Enterprise customers
- [ ] Team expansion

---

## 📞 Support & Links

### Repository
- **Fork**: https://github.com/the-sage-00/dograh-rishi
- **Original**: https://github.com/dograh-hq/dograh

### API Providers
- **OpenAI**: https://platform.openai.com/
- **Sarvam AI**: https://dashboard.sarvam.ai/
- **Exotel**: https://my.exotel.com/

### Documentation
- **Dograh Docs**: https://docs.dograh.com/
- **Pipecat Docs**: https://docs.pipecat.ai/

---

## 📝 Notes

### Security
- ✅ `.env` file is in `.gitignore` - credentials not in git
- ✅ Telemetry disabled - no data to external services
- ✅ All data stored locally in your PostgreSQL/MinIO

### License
- Dograh: BSD 2-Clause (commercial use allowed)
- Your modifications: Your choice
- Requirement: Keep original license in source

---

**Last Updated**: January 18, 2026  
**Session Duration**: ~1 hour  
**Status**: Phase 0 - Testing

---

*Built with ❤️ for the Indian market*
