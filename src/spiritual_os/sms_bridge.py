"""
SMS Bridge for Feature Phone Access

CRITICAL: Not everyone has smartphones or data
- Feature phones (Nokia, etc.) are common in rural Africa
- SMS works everywhere (2G sufficient)
- Zero data cost (pay per SMS, ~$0.01 each)
- Accessible to elderly, low-income, rural populations

ARCHITECTURE:
- Shortcode (e.g., 40404) for incoming SMS
- Africa's Talking API (Kenya, Uganda, Tanzania)
- Twilio (global fallback)
- Commands: Simple, natural language
- Responses: 160 chars or multi-part

COMMANDS SUPPORTED:
- GOSPEL → Today's Gospel (abbreviated)
- MASS [location] → Mass times near you
- PRAY [prayer] → Prayer text via SMS
- CHURCH [location] → Find church via SMS
- GIVE [amount] → Record M-Pesa offering
- HELP → List all commands

EXAMPLE FLOW:
User SMS: "GOSPEL"
System SMS: "Today's Gospel (Jn 3:16-21): God so loved the world that he gave his only Son..."
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
import re


class SMSCommand(Enum):
    """Supported SMS commands"""
    GOSPEL = "gospel"
    MASS = "mass"
    PRAY = "pray"
    CHURCH = "church"
    GIVE = "give"
    REGISTER = "register"
    HELP = "help"
    UNKNOWN = "unknown"


@dataclass
class SMSMessage:
    """Incoming SMS message"""
    from_number: str          # "+254722123456"
    to_number: str            # Shortcode "40404"
    message: str              # "GOSPEL"
    timestamp: str            # ISO format
    message_id: str           # Provider's message ID
    
    @property
    def command(self) -> SMSCommand:
        """Extract command from message"""
        msg = self.message.strip().upper()
        
        if msg.startswith("GOSPEL"):
            return SMSCommand.GOSPEL
        elif msg.startswith("MASS"):
            return SMSCommand.MASS
        elif msg.startswith("PRAY"):
            return SMSCommand.PRAY
        elif msg.startswith("CHURCH"):
            return SMSCommand.CHURCH
        elif msg.startswith("GIVE"):
            return SMSCommand.GIVE
        elif msg.startswith("REGISTER"):
            return SMSCommand.REGISTER
        elif msg.startswith("HELP"):
            return SMSCommand.HELP
        else:
            return SMSCommand.UNKNOWN
    
    @property
    def args(self) -> List[str]:
        """Extract arguments from message"""
        parts = self.message.strip().split()
        return parts[1:] if len(parts) > 1 else []


@dataclass
class SMSResponse:
    """Outgoing SMS response"""
    to_number: str
    message: str
    cost_usd: float = 0.01    # Typical SMS cost
    
    def chunk(self, max_length: int = 160) -> List[str]:
        """Split long message into 160-char chunks"""
        if len(self.message) <= max_length:
            return [self.message]
        
        chunks = []
        words = self.message.split()
        current_chunk = ""
        
        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_length:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Add part numbers if multiple chunks
        if len(chunks) > 1:
            chunks = [f"({i+1}/{len(chunks)}) {chunk}" 
                     for i, chunk in enumerate(chunks)]
        
        return chunks


class SMSBridge:
    """
    SMS Bridge for Feature Phone Access
    
    Provides zero-data access to Catholic Spiritual OS via SMS.
    
    Architecture:
    1. User sends SMS to shortcode (e.g., "GOSPEL" to 40404)
    2. SMS gateway (Africa's Talking/Twilio) receives
    3. Webhook calls our handler
    4. Handler parses command, generates response
    5. Response sent back via SMS (one or more parts)
    
    Cost model:
    - Incoming SMS: Free (absorbed by platform)
    - Outgoing SMS: $0.01-0.03 per message
    - Funded by: Parish subscriptions, donor support, telco CSR
    """
    
    def __init__(self, provider: str = "africastalking"):
        self.provider = provider
        
        # Command handlers
        self.handlers = {
            SMSCommand.GOSPEL: self.handle_gospel,
            SMSCommand.MASS: self.handle_mass,
            SMSCommand.PRAY: self.handle_pray,
            SMSCommand.CHURCH: self.handle_church,
            SMSCommand.GIVE: self.handle_give,
            SMSCommand.REGISTER: self.handle_register,
            SMSCommand.HELP: self.handle_help,
            SMSCommand.UNKNOWN: self.handle_unknown,
        }
    
    def process(self, sms: SMSMessage) -> SMSResponse:
        """Process incoming SMS and generate response"""
        command = sms.command
        handler = self.handlers.get(command, self.handle_unknown)
        
        return handler(sms)
    
    def handle_gospel(self, sms: SMSMessage) -> SMSResponse:
        """Handle GOSPEL command"""
        # In production: Fetch from MassReadingsAPI
        # For now: Demo response
        
        gospel_text = """Today's Gospel (Jn 3:16-21):
        
God so loved the world that he gave his only Son, so that everyone who believes in him might not perish but might have eternal life.

For God did not send his Son into the world to condemn the world, but that the world might be saved through him.

Reply MASS [city] for Mass times
Reply PRAY for daily prayers
Reply HELP for all commands"""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=gospel_text,
        )
    
    def handle_mass(self, sms: SMSMessage) -> SMSResponse:
        """Handle MASS command"""
        # Extract location from args
        location = " ".join(sms.args) if sms.args else "your area"
        
        # In production: Query ChurchDirectory
        # For now: Demo response
        
        if "nakuru" in location.lower():
            response = """Nakuru Cathedral:
Sun: 7am, 9am, 11am, 5pm
Mon-Fri: 6:30am, 12:15pm
Sat: 6:30am, 6pm (vigil)

Call: 0722-XXX-XXX
Location: Kenyatta Ave

Reply CHURCH NAKURU for more churches"""
        
        elif "namugongo" in location.lower():
            response = """Uganda Martyrs Shrine:
Sun: 8am (Luganda), 10am (English)
Daily: 7am, 5pm

5km from Namugongo town
Call: 0772-XXX-XXX"""
        
        else:
            response = f"""Mass times in {location}:
To get specific times, send:
MASS [church name]

Example: MASS NAKURU
or: MASS KAMPALA

Reply CHURCH {location.upper()} to find churches"""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=response,
        )
    
    def handle_pray(self, sms: SMSMessage) -> SMSResponse:
        """Handle PRAY command"""
        prayer_name = " ".join(sms.args).lower() if sms.args else "our father"
        
        prayers = {
            "our father": """Baba Yetu (Our Father):

Baba yetu uliye mbinguni,
Jina lako litukuzwe.
Ufalme wako uje.
Mapenzi yako yatimizwe
duniani kama mbinguni.

Utupe leo chakula chetu cha kila siku.
Utusamehe makosa yetu
kama tunavyowasamehe
waliotukosea.

Usitutie katika majaribu,
lakini utuokoe na yule mwovu.

Amina.""",
            
            "hail mary": """Salamu Maria:

Salamu Maria, umejaa neema,
Bwana yu pamoja nawe.
Umebarikiwa kuliko wanawake wote,
na amebarikiwa mzao wa tumbo lako Yesu.

Maria Mtakatifu, Mama wa Mungu,
utuombee sisi wenye dhambi,
sasa na saa ya kufa kwetu.

Amina.""",
            
            "glory be": """Utukufu (Glory Be):

Utukufu kwa Baba,
na kwa Mwana,
na kwa Roho Mtakatifu.

Kama ulivyokuwa mwanzoni,
sasa na siku zote,
hata milele na milele.

Amina.""",
        }
        
        prayer_text = prayers.get(prayer_name, prayers["our father"])
        
        return SMSResponse(
            to_number=sms.from_number,
            message=prayer_text,
        )
    
    def handle_church(self, sms: SMSMessage) -> SMSResponse:
        """Handle CHURCH command"""
        location = " ".join(sms.args) if sms.args else ""
        
        if not location:
            response = """Find a Church:

Send: CHURCH [location]

Examples:
- CHURCH NAIROBI
- CHURCH WESTLANDS
- CHURCH KAMPALA
- CHURCH THIMPHU BHUTAN

We'll send church names, Mass times, and contacts."""
        
        else:
            # In production: Query ChurchDirectory
            response = f"""Churches in {location.upper()}:

[Demo data - real results coming soon]

To get full directory:
1. Visit: catholic-spiritual-os.streamlit.app
2. Go to "Find a Church"
3. Search: {location}

Or call our helpline:
Kenya: 0800-XXX-XXX (toll-free)"""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=response,
        )
    
    def handle_give(self, sms: SMSMessage) -> SMSResponse:
        """Handle GIVE command (M-Pesa integration)"""
        amount = sms.args[0] if sms.args else "0"
        
        try:
            amount_int = int(amount)
            
            response = f"""Record Offering:

Amount: KES {amount_int}

[M-Pesa integration coming soon]

For now, give at:
- Mass collection
- Parish office
- Bank: St. Austin's Parish
  A/C: 123-456-789

Thank you for your generosity!"""
        
        except ValueError:
            response = """Invalid amount.

Usage: GIVE [amount]
Example: GIVE 500

This records a KES 500 offering.

M-Pesa integration coming soon."""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=response,
        )
    
    def handle_register(self, sms: SMSMessage) -> SMSResponse:
        """Handle REGISTER command"""
        response = """Register for SMS Updates:

You'll receive:
- Daily Gospel (7am)
- Sunday Mass times
- Parish announcements
- Prayer reminders

Cost: FREE (sponsored)

To confirm registration:
Reply: YES REGISTER

To stop: Reply STOP anytime"""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=response,
        )
    
    def handle_help(self, sms: SMSMessage) -> SMSResponse:
        """Handle HELP command"""
        response = """Catholic Spiritual OS - SMS Commands:

GOSPEL - Today's Gospel reading
MASS [city] - Mass times near you
PRAY [name] - Get prayer text
CHURCH [city] - Find churches
GIVE [amount] - Record offering
REGISTER - Daily updates
HELP - This message

All commands are FREE (sponsored)

Support: 0800-XXX-XXX"""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=response,
        )
    
    def handle_unknown(self, sms: SMSMessage) -> SMSResponse:
        """Handle unknown command"""
        response = f"""Unknown command: "{sms.message}"

Valid commands:
GOSPEL, MASS, PRAY, CHURCH, GIVE, HELP

Example: Send "GOSPEL" for today's reading

Reply HELP for full list"""
        
        return SMSResponse(
            to_number=sms.from_number,
            message=response,
        )


class AfricasTalkingAPI:
    """
    Africa's Talking SMS Gateway Integration
    
    Covers: Kenya, Uganda, Tanzania, Rwanda, Malawi, Nigeria
    
    Features:
    - SMS sending/receiving
    - Premium SMS (for paid services)
    - USSD (for interactive menus)
    - Voice calls
    
    Cost: ~$0.01 per SMS
    """
    
    def __init__(self, api_key: str, username: str):
        self.api_key = api_key
        self.username = username
        self.base_url = "https://api.africastalking.com/version1"
    
    def send_sms(self, to: str, message: str) -> Dict:
        """Send SMS via Africa's Talking"""
        # In production: Make actual API call
        # For now: Return mock response
        
        return {
            "status": "success",
            "message_id": "ATXid_abc123",
            "cost": "KES 1.00",
            "recipient": to,
        }
    
    def register_webhook(self, url: str) -> Dict:
        """Register webhook for incoming SMS"""
        # In production: Configure webhook in AT dashboard
        # Webhook receives POST with:
        # - from: sender number
        # - to: shortcode
        # - text: message content
        # - date: timestamp
        
        return {
            "status": "success",
            "webhook_url": url,
            "note": "Configure this URL in Africa's Talking dashboard",
        }


# DEMO

if __name__ == "__main__":
    # Create SMS bridge
    bridge = SMSBridge(provider="africastalking")
    
    # Test commands
    test_messages = [
        SMSMessage(
            from_number="+254722123456",
            to_number="40404",
            message="GOSPEL",
            timestamp="2026-02-13T10:00:00Z",
            message_id="msg_001",
        ),
        SMSMessage(
            from_number="+254722123456",
            to_number="40404",
            message="MASS NAKURU",
            timestamp="2026-02-13T10:01:00Z",
            message_id="msg_002",
        ),
        SMSMessage(
            from_number="+256772123456",
            to_number="40404",
            message="PRAY OUR FATHER",
            timestamp="2026-02-13T10:02:00Z",
            message_id="msg_003",
        ),
        SMSMessage(
            from_number="+254722123456",
            to_number="40404",
            message="HELP",
            timestamp="2026-02-13T10:03:00Z",
            message_id="msg_004",
        ),
    ]
    
    print("=== SMS BRIDGE DEMO ===\n")
    
    for msg in test_messages:
        print(f"📱 FROM: {msg.from_number}")
        print(f"📥 MESSAGE: {msg.message}")
        print(f"🔍 COMMAND: {msg.command.value}")
        
        response = bridge.process(msg)
        
        chunks = response.chunk()
        print(f"📤 RESPONSE ({len(chunks)} SMS):")
        for chunk in chunks:
            print(f"   {chunk[:80]}...")
        
        print(f"💰 COST: ${response.cost_usd * len(chunks):.3f}\n")
