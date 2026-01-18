# =============================================================================
# AUDEXLY - Exotel Integration Guide
# =============================================================================
# 
# This guide explains how to configure Exotel for your Audexly voice agents.
# 
# Stack: Exotel + Sarvam STT/TTS + OpenAI LLM
# =============================================================================

## ⚠️ IMPORTANT: Current Exotel Support Status

### What's Supported:
| Component | Status | Details |
|-----------|--------|---------|
| **Pipecat Engine** | ✅ Full Support | `ExotelFrameSerializer` handles WebSocket streaming |
| **Dograh API Layer** | ⚠️ Needs Extension | No Exotel provider class yet (has Twilio, Vonage, Vobiz) |
| **Dograh UI** | ⚠️ Needs Extension | No Exotel configuration UI yet |

### What This Means:
1. **Pipecat** (the voice engine) fully supports Exotel via `ExotelFrameSerializer`
2. The **Dograh API** has providers for Twilio, Vonage, Vobiz, and Cloudonix - but NOT Exotel yet
3. We need to create an Exotel provider class similar to the existing ones

### Options:
1. **Option A (Quick)**: Use Pipecat runner directly with Exotel bypassing Dograh's telephony layer
2. **Option B (Full Integration)**: Create Exotel provider in `api/services/telephony/providers/`

For Phase 0 testing, we'll use **Option A** to validate the voice pipeline first.

---

## 📋 Prerequisites

Before setting up Exotel integration, ensure you have:

1. ✅ Exotel account with AgentStream/Voice Streaming enabled
2. ✅ At least one Exotel phone number
3. ✅ Audexly running locally (`docker compose -f docker-compose.audexly.yaml up`)
4. ✅ Cloudflare tunnel URL (from `docker logs audexly-tunnel`)

---

## 🔧 Step 1: Get Your Tunnel URL

When you start Audexly, the cloudflared container creates a public tunnel.

```powershell
# Check the tunnel URL
docker logs audexly-tunnel 2>&1 | Select-String "trycloudflare.com"
```

You'll see something like:
```
https://random-words-here.trycloudflare.com
```

**Save this URL** - you'll need it for Exotel configuration!

> ⚠️ Note: This URL changes each time you restart Docker. For production, 
> you'll want a fixed domain.

---

## 🔧 Step 2: Configure Exotel App Bazaar

### A. Login to Exotel Console
1. Go to https://my.exotel.com/
2. Navigate to **App Bazaar** → **Build Your Own App**

### B. Create a New App Flow

1. Click **"Create New App"**
2. Name it: `Audexly Voice Agent`
3. Add the following applets in order:

#### Applet 1: Answer
- Type: **Answer**
- This answers the incoming call

#### Applet 2: Voicebot (WebSocket)
- Type: **Voicebot**
- WebSocket URL: `wss://YOUR-TUNNEL-URL/api/v1/telephony/exotel/stream`
  - Replace `YOUR-TUNNEL-URL` with your cloudflare tunnel URL
  - Example: `wss://random-words-here.trycloudflare.com/api/v1/telephony/exotel/stream`
- Enable bidirectional streaming

#### Applet 3: Hangup
- Type: **Hangup**
- This ends the call gracefully

### C. Save and Publish
1. Save the app flow
2. Publish it

---

## 🔧 Step 3: Assign Phone Number

1. Go to **Phone Numbers** in Exotel Console
2. Select your phone number
3. Under **Incoming Call Settings**:
   - Set **App to Handle** → Your `Audexly Voice Agent` app

---

## 🔧 Step 4: Configure Audexly for Exotel

### In Audexly Dashboard (http://localhost:3010):

1. Go to **Telephony Configurations**
2. Click **Add Configuration**
3. Select **Exotel** as provider
4. Enter your credentials:
   - **API Key**: Your Exotel API key
   - **API Token**: Your Exotel API token
   - **Account SID**: Your Exotel account SID
   - **Subdomain**: Your Exotel subdomain (e.g., `api4` for api4.exotel.in)

---

## 📞 Step 5: Create an Inbound Workflow

1. Go to **Workflows** → **Create New**
2. Select **Inbound** call type
3. Configure the voice agent:
   - **LLM**: OpenAI - gpt-4o-mini
   - **STT**: Sarvam - saarika:v2.5
   - **TTS**: Sarvam - bulbul:v2
4. Add your prompt (see prompts folder)
5. Save the workflow

---

## 🧪 Step 6: Test the Integration

1. Call your Exotel phone number from any phone
2. The call should connect to your Audexly voice agent
3. Have a conversation!
4. Check the Audexly dashboard for:
   - Call logs
   - Transcripts
   - Recordings

---

## 🔍 Troubleshooting

### Call doesn't connect?
1. Check tunnel is running: `docker logs audexly-tunnel`
2. Verify WebSocket URL in Exotel is correct
3. Check Audexly API is healthy: http://localhost:8000/api/v1/health

### No audio?
1. Ensure bidirectional streaming is enabled in Exotel
2. Check Sarvam API keys are configured correctly
3. View API logs: `docker logs audexly-api -f`

### High latency?
1. Check network connectivity
2. Verify STT/TTS models are correct
3. Consider using faster LLM model

### View detailed logs:
```powershell
# All logs
docker compose -f docker-compose.audexly.yaml logs -f

# Just API logs
docker logs audexly-api -f

# Just tunnel logs
docker logs audexly-tunnel -f
```

---

## 📊 Exotel WebSocket Protocol

For reference, here's how the Exotel WebSocket integration works:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     EXOTEL CALL FLOW                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📱 Caller dials Exotel number                                      │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────────────┐                                           │
│  │     EXOTEL           │                                           │
│  │  AgentStream         │                                           │
│  │  (Phone Gateway)     │                                           │
│  └──────────┬───────────┘                                           │
│             │                                                        │
│             │ WebSocket (wss://)                                    │
│             │ - Bidirectional audio streaming                       │
│             │ - Sub-20ms latency                                    │
│             │                                                        │
│             ▼                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    AUDEXLY (Pipecat)                          │   │
│  │                                                                │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │            ExotelFrameSerializer                         │ │   │
│  │  │  - Converts Exotel protocol ↔ Pipecat frames            │ │   │
│  │  │  - Handles DTMF, audio resampling                        │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  │                           │                                   │   │
│  │  ┌────────────┬───────────┴───────────┬────────────┐        │   │
│  │  │    STT     │         LLM           │    TTS     │        │   │
│  │  │  Sarvam    │       OpenAI          │  Sarvam    │        │   │
│  │  │ saarika    │    gpt-4o-mini        │  bulbul    │        │   │
│  │  └────────────┴───────────────────────┴────────────┘        │   │
│  │                                                                │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Important Notes

1. **Tunnel URL changes**: Each Docker restart gives a new tunnel URL. 
   Update Exotel webhook accordingly for testing.

2. **Production setup**: For production, use:
   - Fixed domain with SSL
   - Proper TURN server for WebRTC
   - Load balancing for scale

3. **Call recording**: Recordings are stored in MinIO (accessible at http://localhost:9001)

4. **Rate limits**: Be aware of Exotel's rate limits during testing

---

## 🔗 Useful Links

- **Exotel Console**: https://my.exotel.com/
- **Exotel Voicebot Docs**: https://support.exotel.com/support/solutions/articles/3000108630
- **Pipecat Exotel Docs**: https://docs.pipecat.ai/server/services/serializers/exotel
- **Sarvam Dashboard**: https://dashboard.sarvam.ai/
- **OpenAI Platform**: https://platform.openai.com/
