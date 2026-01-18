# Exotel Integration TODO

## Current Status

### ✅ Completed
1. Created `ExotelProvider` class in `api/services/telephony/providers/exotel_provider.py`
2. Updated `factory.py` to include Exotel provider
3. Pipecat already has `ExotelFrameSerializer` for audio handling
4. Added `.env` with Exotel credentials

### ⚠️ Still Needed for Full Integration

#### Backend (API Layer)
1. **Add Exotel to WorkflowRunMode enum** (`api/enums.py`)
   - Add `EXOTEL = "exotel"`

2. **Create Exotel transport** (`api/services/pipecat/transport_setup.py`)
   - Add `create_exotel_transport()` function
   - Use `ExotelFrameSerializer` from pipecat

3. **Create Exotel pipeline runner** (`api/services/pipecat/run_pipeline.py`)
   - Add `run_pipeline_exotel()` function
   - Similar to `run_pipeline_twilio()` but with Exotel transport

4. **Add Exotel audio config** (`api/services/pipecat/audio_config.py`)
   - Add Exotel-specific audio configuration (8kHz, PCM)

5. **Add Exotel telephony routes** (`api/routes/telephony.py`)
   - Add WebSocket endpoint for Exotel
   - Add webhook endpoint for Exotel callbacks

#### Frontend (UI Layer)
1. **Add Exotel to telephony configuration UI** 
   - `ui/src/app/telephony-configurations/page.tsx`
   - Add Exotel as a provider option
   - Add form fields for:
     - Account SID
     - API Key  
     - API Token
     - Subdomain
     - From Number

2. **Add Exotel icon/branding**
   - Add Exotel logo to `ui/public/`

#### Testing
1. Test outbound call initiation
2. Test inbound call handling
3. Test WebSocket audio streaming
4. Test call status callbacks

## Workaround for Phase 0

For now, you can:
1. **Use Web Call** (WebRTC) for testing - this works immediately!
2. Test your voice agent with browser-based calling
3. Once satisfied, we can complete Exotel integration

## Estimated Effort
- Backend completion: 2-3 hours
- Frontend UI: 1-2 hours
- Testing: 1-2 hours
- **Total: ~5-7 hours**

## Alternative: Direct Pipecat Exotel

The Pipecat development runner already supports Exotel:
```bash
uv run bot.py -t exotel
```

This could be used for quick testing while we complete the Dograh integration.
