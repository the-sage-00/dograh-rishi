# 🚀 Audexly - Phase 0 Setup Guide

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Your API keys:
  - OpenAI API key
  - Sarvam API key  
  - Exotel credentials (for telephony)

---

## Step 1: Configure Environment

```powershell
# Navigate to project
cd c:\Users\saini\OneDrive\Desktop\onelastmore\audexly

# Copy the environment template
cp .env.audexly.example .env

# Edit .env and add your API keys
# (Use your preferred editor - VS Code, Notepad, etc.)
```

---

## Step 2: Start the Platform

```powershell
# Start all services with telemetry disabled
docker compose -f docker-compose.audexly.yaml up
```

**First startup takes 2-3 minutes** to download images.

---

## Step 3: Access the Dashboard

Once running, open your browser:

| Service | URL | Purpose |
|---------|-----|---------|
| **Dashboard** | http://localhost:3010 | Main UI |
| **API** | http://localhost:8000 | Backend API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **MinIO Console** | http://localhost:9001 | File storage |

---

## Step 4: Configure Your Voice Agent

1. Open http://localhost:3010
2. Create a new user/organization (first-time setup)
3. Go to **Model Configurations**
4. Add your API keys:

### LLM Configuration
- **Provider**: OpenAI
- **API Key**: Your OpenAI key
- **Model**: `gpt-4o-mini` (fast + cheap)

### STT Configuration
- **Provider**: Sarvam
- **API Key**: Your Sarvam key
- **Model**: `saarika:v2.5`

### TTS Configuration
- **Provider**: Sarvam
- **API Key**: Your Sarvam key  
- **Model**: `bulbul:v2`
- **Voice**: `abhilash` (or your preferred voice)

---

## Step 5: Create Your First Voice Agent

1. Click **"New Workflow"**
2. Choose **Inbound** (for testing with Web Call)
3. Name it: `Test Sales Agent`
4. Use this prompt:

```
You are a sales representative for Audexly, an AI voice agent platform.

Your job is to:
1. Greet the caller warmly
2. Ask about their business needs
3. Explain how AI voice agents can help them
4. Collect their interest level (high/medium/low)
5. Thank them and end the call

Rules:
- Keep responses short (1-2 sentences max)
- Be friendly and professional
- Don't interrupt the customer
- Speak in simple, clear language

Start by saying: "Hello! This is Alex from Audexly. How are you doing today?"
```

5. Click **Save**

---

## Step 6: Test with Web Call

1. Open your workflow
2. Click **"Web Call"** button
3. Allow microphone access
4. Start talking!

### What to Test:
- [ ] Response latency (target: < 2.5 seconds)
- [ ] Voice quality
- [ ] Conversation flow
- [ ] Interruption handling
- [ ] Silence handling

---

## Step 7: Check Tunnel URL (for Exotel)

The cloudflared container creates a public tunnel. Check the logs:

```powershell
docker logs audexly-tunnel
```

You'll see something like:
```
Your quick Tunnel has been created! Visit it at:
https://random-words-here.trycloudflare.com
```

**This URL is needed for Exotel webhook configuration!**

---

## Troubleshooting

### Docker not starting?
```powershell
# Restart Docker Desktop
# Then try again:
docker compose -f docker-compose.audexly.yaml up
```

### Port already in use?
```powershell
# Check what's using the port
netstat -ano | findstr :3010
netstat -ano | findstr :8000

# Stop conflicting services or change ports in docker-compose
```

### Database issues?
```powershell
# Reset everything (WARNING: deletes all data)
docker compose -f docker-compose.audexly.yaml down -v
docker compose -f docker-compose.audexly.yaml up
```

### View logs?
```powershell
# All services
docker compose -f docker-compose.audexly.yaml logs -f

# Specific service
docker logs audexly-api -f
docker logs audexly-ui -f
```

---

## Next Steps After Testing

Once your voice agent works well locally:

1. **Document your configuration**
   - Which STT/TTS/LLM settings work best
   - Optimal VAD settings
   - Best performing prompts

2. **Test with real phone calls**
   - Configure Exotel webhooks
   - Point to your cloudflare tunnel URL
   - Make test calls

3. **Begin rebranding**
   - Replace "Dograh" with "Audexly"
   - Update logos and branding

---

## Files Created

| File | Purpose |
|------|---------|
| `docker-compose.audexly.yaml` | Telemetry-disabled Docker config |
| `.env.audexly.example` | Environment template |
| `AUDEXLY_SETUP_GUIDE.md` | This guide |

---

## Useful Commands

```powershell
# Start services
docker compose -f docker-compose.audexly.yaml up

# Start in background
docker compose -f docker-compose.audexly.yaml up -d

# Stop services
docker compose -f docker-compose.audexly.yaml down

# Stop and remove volumes (clean slate)
docker compose -f docker-compose.audexly.yaml down -v

# View logs
docker compose -f docker-compose.audexly.yaml logs -f

# Rebuild images
docker compose -f docker-compose.audexly.yaml build --no-cache
```

---

**Ready to start? Run the docker compose command above!** 🚀
