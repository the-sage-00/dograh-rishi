"""
Exotel implementation of the TelephonyProvider interface.
Exotel is India's leading cloud telephony provider with AgentStream for voice bots.
"""

import json
import random
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import aiohttp
from loguru import logger

from api.enums import WorkflowRunMode
from api.services.telephony.base import (
    CallInitiationResult,
    NormalizedInboundData,
    TelephonyProvider,
)
from api.utils.tunnel import TunnelURLProvider

if TYPE_CHECKING:
    from fastapi import WebSocket


class ExotelProvider(TelephonyProvider):
    """
    Exotel implementation of TelephonyProvider.
    Uses Exotel's AgentStream API for voice bot functionality.
    
    Note: Exotel uses WebSocket streaming via AgentStream, similar to Twilio's MediaStreams.
    The Pipecat ExotelFrameSerializer handles the audio protocol.
    """

    PROVIDER_NAME = "exotel"  # WorkflowRunMode.EXOTEL.value when added to enums
    WEBHOOK_ENDPOINT = "exotel"

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ExotelProvider with configuration.

        Args:
            config: Dictionary containing:
                - account_sid: Exotel Account SID (e.g., "callmate4")
                - api_key: Exotel API Key
                - api_token: Exotel API Token
                - subdomain: Exotel API subdomain (e.g., "api.exotel.com")
                - from_numbers: List of phone numbers to use
        """
        self.account_sid = config.get("account_sid")
        self.api_key = config.get("api_key")
        self.api_token = config.get("api_token")
        self.subdomain = config.get("subdomain", "api.exotel.com")
        self.from_numbers = config.get("from_numbers", [])
        self.webhook_secret = config.get("webhook_secret", "")

        # Handle both single number (string) and multiple numbers (list)
        if isinstance(self.from_numbers, str):
            self.from_numbers = [self.from_numbers]

        self.base_url = f"https://{self.subdomain}/v1/Accounts/{self.account_sid}"

    async def initiate_call(
        self,
        to_number: str,
        webhook_url: str,
        workflow_run_id: Optional[int] = None,
        **kwargs: Any,
    ) -> CallInitiationResult:
        """
        Initiate an outbound call via Exotel.
        
        Note: For Exotel, outbound calls with AgentStream require the Voicebot applet
        to be configured in App Bazaar.
        """
        if not self.validate_config():
            raise ValueError("Exotel provider not properly configured")

        # Exotel API endpoint for initiating calls
        endpoint = f"{self.base_url}/Calls/connect.json"

        # Select a random phone number
        from_number = random.choice(self.from_numbers) if self.from_numbers else None
        logger.info(f"Selected phone number {from_number} for outbound call")

        # Prepare call data for Exotel
        data = {
            "From": from_number,
            "To": to_number,
            "CallerId": from_number,
            "Url": webhook_url,  # App URL for call flow
        }

        # Add status callback if workflow_run_id provided
        if workflow_run_id:
            backend_endpoint = await TunnelURLProvider.get_tunnel_url()
            callback_url = f"https://{backend_endpoint}/api/v1/telephony/exotel/status-callback/{workflow_run_id}"
            data["StatusCallback"] = callback_url

        data.update(kwargs)

        # Make the API request
        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth(self.api_key, self.api_token)
            async with session.post(endpoint, data=data, auth=auth) as response:
                if response.status not in [200, 201]:
                    error_data = await response.text()
                    raise Exception(f"Failed to initiate Exotel call: {error_data}")

                response_data = await response.json()

                # Exotel returns Call object with Sid
                call_data = response_data.get("Call", response_data)

                return CallInitiationResult(
                    call_id=call_data.get("Sid", ""),
                    status=call_data.get("Status", "queued"),
                    provider_metadata={},
                    raw_response=response_data,
                )

    async def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """
        Get the current status of an Exotel call.
        """
        if not self.validate_config():
            raise ValueError("Exotel provider not properly configured")

        endpoint = f"{self.base_url}/Calls/{call_id}.json"

        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth(self.api_key, self.api_token)
            async with session.get(endpoint, auth=auth) as response:
                if response.status != 200:
                    error_data = await response.text()
                    raise Exception(f"Failed to get Exotel call status: {error_data}")

                return await response.json()

    async def get_available_phone_numbers(self) -> List[str]:
        """
        Get list of available Exotel phone numbers.
        """
        return self.from_numbers

    def validate_config(self) -> bool:
        """
        Validate Exotel configuration.
        """
        return bool(self.account_sid and self.api_key and self.api_token)

    async def verify_webhook_signature(
        self, url: str, params: Dict[str, Any], signature: str
    ) -> bool:
        """
        Verify Exotel webhook signature for security.
        
        Note: Exotel uses HMAC-SHA256 for webhook validation if configured.
        For now, we'll use the webhook secret if provided.
        """
        if not self.webhook_secret:
            # If no webhook secret is configured, allow the request
            # (for development/testing)
            logger.warning("No Exotel webhook secret configured - skipping signature verification")
            return True

        # TODO: Implement proper HMAC verification when Exotel provides signature
        return True

    async def get_webhook_response(
        self, workflow_id: int, user_id: int, workflow_run_id: int
    ) -> str:
        """
        Generate response for starting a call session.
        
        Note: Exotel uses WebSocket streaming directly, so this returns
        connection info rather than XML like Twilio.
        """
        backend_endpoint = await TunnelURLProvider.get_tunnel_url()
        
        # Return WebSocket URL for Exotel AgentStream
        websocket_url = f"wss://{backend_endpoint}/api/v1/telephony/exotel/ws/{workflow_id}/{user_id}/{workflow_run_id}"
        
        return json.dumps({
            "websocket_url": websocket_url,
            "message": "Connect to WebSocket for audio streaming"
        })

    async def get_call_cost(self, call_id: str) -> Dict[str, Any]:
        """
        Get cost information for a completed Exotel call.
        """
        try:
            call_data = await self.get_call_status(call_id)
            
            # Exotel pricing info
            call_info = call_data.get("Call", call_data)
            
            return {
                "cost_usd": 0.0,  # Exotel bills in INR, conversion needed
                "cost_inr": float(call_info.get("Price", 0)),
                "duration": int(call_info.get("Duration", 0)),
                "status": call_info.get("Status", "unknown"),
                "raw_response": call_data,
            }

        except Exception as e:
            logger.error(f"Exception fetching Exotel call cost: {e}")
            return {"cost_usd": 0.0, "duration": 0, "status": "error", "error": str(e)}

    def parse_status_callback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Exotel status callback data into generic format.
        """
        return {
            "call_id": data.get("CallSid", ""),
            "status": data.get("Status", ""),
            "from_number": data.get("From"),
            "to_number": data.get("To"),
            "direction": data.get("Direction"),
            "duration": data.get("Duration") or data.get("CallDuration"),
            "extra": data,
        }

    async def handle_websocket(
        self,
        websocket: "WebSocket",
        workflow_id: int,
        user_id: int,
        workflow_run_id: int,
    ) -> None:
        """
        Handle Exotel-specific WebSocket connection.

        Exotel AgentStream sends:
        1. "connected" event first
        2. "start" event with streamSid
        3. Then audio messages in JSON format with base64 audio
        """
        from api.services.pipecat.run_pipeline import run_pipeline_exotel

        try:
            # Wait for "connected" event
            first_msg = await websocket.receive_text()
            msg = json.loads(first_msg)

            if msg.get("event") != "connected":
                logger.error(f"Expected 'connected' event, got: {msg.get('event')}")
                await websocket.close(code=4400, reason="Expected connected event")
                return

            logger.debug(
                f"Exotel WebSocket connected for workflow_run {workflow_run_id}"
            )

            # Wait for "start" event with stream details
            start_msg = await websocket.receive_text()
            logger.debug(f"Received start message: {start_msg}")

            start_msg = json.loads(start_msg)
            if start_msg.get("event") != "start":
                logger.error("Expected 'start' event second")
                await websocket.close(code=4400, reason="Expected start event")
                return

            # Extract Exotel-specific identifiers
            try:
                stream_sid = start_msg.get("start", {}).get("streamSid", start_msg.get("streamSid", ""))
                call_sid = start_msg.get("start", {}).get("callSid", start_msg.get("callSid", ""))
            except KeyError:
                logger.error("Missing streamSid or callSid in start message")
                await websocket.close(code=4400, reason="Missing stream identifiers")
                return

            # Run the Exotel pipeline
            await run_pipeline_exotel(
                websocket, stream_sid, call_sid, workflow_id, workflow_run_id, user_id
            )

        except Exception as e:
            logger.error(f"Error in Exotel WebSocket handler: {e}")
            raise

    # ======== INBOUND CALL METHODS ========

    @classmethod
    def can_handle_webhook(
        cls, webhook_data: Dict[str, Any], headers: Dict[str, str]
    ) -> bool:
        """
        Determine if this provider can handle the incoming webhook.

        Exotel webhooks have specific characteristics:
        - Data contains: CallSid, AccountSid (Exotel format), Direction
        - AccountSid is NOT an AC-prefixed string (that's Twilio)
        - May contain exotel-specific fields
        """
        # Check for Exotel-specific data patterns
        call_sid = webhook_data.get("CallSid", "")
        account_sid = webhook_data.get("AccountSid", "")
        
        # Exotel AccountSid is typically the account name, not AC-prefixed
        if account_sid and not account_sid.startswith("AC"):
            # Check if it looks like an Exotel account (alphanumeric, no dots)
            if call_sid and "." not in account_sid:
                return True
        
        # Check for Exotel-specific header or user-agent
        user_agent = headers.get("user-agent", "").lower()
        if "exotel" in user_agent:
            return True
            
        return False

    @staticmethod
    def parse_inbound_webhook(webhook_data: Dict[str, Any]) -> NormalizedInboundData:
        """
        Parse Exotel-specific inbound webhook data into normalized format.
        """
        return NormalizedInboundData(
            provider="exotel",
            call_id=webhook_data.get("CallSid", ""),
            from_number=ExotelProvider.normalize_phone_number(
                webhook_data.get("From", "")
            ),
            to_number=ExotelProvider.normalize_phone_number(webhook_data.get("To", "")),
            direction=webhook_data.get("Direction", "inbound"),
            call_status=webhook_data.get("Status", ""),
            account_id=webhook_data.get("AccountSid"),
            from_country=webhook_data.get("FromCountry"),
            to_country=webhook_data.get("ToCountry"),
            raw_data=webhook_data,
        )

    @staticmethod
    def normalize_phone_number(phone_number: str) -> str:
        """
        Normalize a phone number to E.164 format for Exotel.
        Exotel typically uses Indian phone numbers.
        """
        if not phone_number:
            return ""

        # Remove any spaces, dashes, or parentheses
        phone_number = "".join(c for c in phone_number if c.isdigit() or c == "+")

        # Already in E.164 format
        if phone_number.startswith("+"):
            return phone_number

        # Indian numbers - add +91 prefix
        if phone_number.startswith("91") and len(phone_number) == 12:
            return f"+{phone_number}"
        elif len(phone_number) == 10:
            return f"+91{phone_number}"

        return phone_number

    @staticmethod
    def validate_account_id(config_data: dict, webhook_account_id: str) -> bool:
        """Validate Exotel account_sid from webhook matches configuration"""
        if not webhook_account_id:
            return False

        stored_account_sid = config_data.get("account_sid")
        return stored_account_sid == webhook_account_id

    async def verify_inbound_signature(
        self, url: str, webhook_data: Dict[str, Any], signature: str
    ) -> bool:
        """
        Verify the signature of an inbound Exotel webhook for security.
        """
        return await self.verify_webhook_signature(url, webhook_data, signature)

    @staticmethod
    async def generate_inbound_response(
        websocket_url: str, workflow_run_id: int = None
    ) -> tuple:
        """
        Generate response for an inbound Exotel webhook.
        
        Note: Exotel's AgentStream uses WebSocket URL directly in the 
        App Bazaar Voicebot applet configuration, not in webhook response.
        """
        from fastapi import Response

        # Return JSON with WebSocket connection info
        response_data = {
            "status": "ok",
            "websocket_url": websocket_url,
            "workflow_run_id": workflow_run_id,
        }

        return Response(
            content=json.dumps(response_data), 
            media_type="application/json"
        )

    @staticmethod
    def generate_error_response(error_type: str, message: str) -> tuple:
        """
        Generate an Exotel-specific error response.
        """
        from fastapi import Response

        response_data = {
            "status": "error",
            "error_type": error_type,
            "message": message,
        }

        return Response(
            content=json.dumps(response_data), 
            media_type="application/json"
        )

    @staticmethod
    def generate_validation_error_response(error_type) -> tuple:
        """
        Generate Exotel-specific error response for validation failures.
        """
        from fastapi import Response

        from api.errors.telephony_errors import TELEPHONY_ERROR_MESSAGES, TelephonyError

        message = TELEPHONY_ERROR_MESSAGES.get(
            error_type, TELEPHONY_ERROR_MESSAGES[TelephonyError.GENERAL_AUTH_FAILED]
        )

        response_data = {
            "status": "error",
            "error_type": str(error_type),
            "message": message,
        }

        return Response(
            content=json.dumps(response_data), 
            media_type="application/json"
        )
