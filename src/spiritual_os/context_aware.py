"""
Context-Aware UI System

Adapts interface based on user context:
- Westlands expat (4G, smartphone) → Full featured
- Namugongo rural (2G, basic phone) → Text-only, audio, SMS

DETECTION:
- Connection speed (4G/3G/2G/offline)
- Device type (smartphone/feature phone/tablet/desktop)
- Location (GPS or IP-based)
- Language preference
- Literacy indicators (usage patterns)

ADAPTATION:
- UI complexity (full/simplified/minimal)
- Content format (images/text-only/audio)
- Data usage (unlimited/metered/conserve)
- Interaction mode (touch/voice/SMS)
"""

from dataclasses import dataclass
from typing import Literal, Optional, List
from enum import Enum
import streamlit as st


class ConnectionSpeed(Enum):
    """Network connection speed"""
    FAST_4G = "4g"      # 4G/5G/WiFi (>= 10 Mbps)
    MEDIUM_3G = "3g"    # 3G (1-10 Mbps)
    SLOW_2G = "2g"      # 2G/EDGE (< 1 Mbps)
    OFFLINE = "offline"  # No connection


class DeviceType(Enum):
    """Type of device"""
    SMARTPHONE = "smartphone"      # iPhone, Android flagship
    BASIC_PHONE = "basic_phone"    # Feature phone (Nokia, etc.)
    TABLET = "tablet"              # iPad, Android tablet
    DESKTOP = "desktop"            # Laptop, desktop computer


class UIMode(Enum):
    """UI complexity level"""
    FULL_FEATURED = "full"         # All features, images, videos, maps
    SIMPLIFIED = "simplified"       # Reduced features, essential only
    TEXT_ONLY = "text_only"        # No images, pure text
    AUDIO_VISUAL = "audio_visual"  # Icons + audio, minimal text
    SMS_BRIDGE = "sms"             # SMS commands, no web UI
    OFFLINE_FIRST = "offline"      # Works without internet


class LiteracyLevel(Enum):
    """Inferred literacy level from usage patterns"""
    HIGH = "high"        # Comfortable with text, complex navigation
    MEDIUM = "medium"    # Basic text reading, prefers simple navigation
    BASIC = "basic"      # Struggles with text, needs audio/visual


@dataclass
class UserContext:
    """
    User's current context
    
    Detected automatically and used to adapt UI
    """
    
    # Network
    connection_speed: ConnectionSpeed
    connection_type: str  # "WiFi", "4G", "3G", "2G", "Offline"
    bandwidth_estimate: float  # Mbps
    
    # Device
    device_type: DeviceType
    screen_width: int  # pixels
    screen_height: int
    is_mobile: bool
    is_touch: bool
    
    # Location
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    country: Optional[str] = None
    city: Optional[str] = None
    timezone: Optional[str] = None
    
    # User preferences
    language: str = "en"
    languages: List[str] = None
    
    # Inferred characteristics
    literacy_level: LiteracyLevel = LiteracyLevel.HIGH
    data_conscious: bool = False  # User conserving data?
    
    def __post_init__(self):
        if self.languages is None:
            self.languages = [self.language]
    
    @property
    def ui_mode(self) -> UIMode:
        """Determine optimal UI mode based on context"""
        
        # Offline → Offline-first mode
        if self.connection_speed == ConnectionSpeed.OFFLINE:
            return UIMode.OFFLINE_FIRST
        
        # Feature phone → SMS bridge
        if self.device_type == DeviceType.BASIC_PHONE:
            return UIMode.SMS_BRIDGE
        
        # 2G + data conscious → Text-only
        if self.connection_speed == ConnectionSpeed.SLOW_2G and self.data_conscious:
            return UIMode.TEXT_ONLY
        
        # Basic literacy → Audio-visual
        if self.literacy_level == LiteracyLevel.BASIC:
            return UIMode.AUDIO_VISUAL
        
        # 3G → Simplified
        if self.connection_speed == ConnectionSpeed.MEDIUM_3G:
            return UIMode.SIMPLIFIED
        
        # Default: Full featured
        return UIMode.FULL_FEATURED
    
    @property
    def should_load_images(self) -> bool:
        """Should we load images?"""
        return self.ui_mode in [UIMode.FULL_FEATURED, UIMode.SIMPLIFIED]
    
    @property
    def should_use_audio(self) -> bool:
        """Should we provide audio alternatives?"""
        return self.ui_mode in [UIMode.AUDIO_VISUAL, UIMode.TEXT_ONLY]
    
    @property
    def max_content_size_kb(self) -> int:
        """Maximum content size to load (KB)"""
        if self.connection_speed == ConnectionSpeed.FAST_4G:
            return 5000  # 5 MB
        elif self.connection_speed == ConnectionSpeed.MEDIUM_3G:
            return 500   # 500 KB
        elif self.connection_speed == ConnectionSpeed.SLOW_2G:
            return 100   # 100 KB
        else:
            return 50    # 50 KB (offline/minimal)


class ContextDetector:
    """
    Detect user context automatically
    
    Methods:
    1. Browser API (navigator.connection, geolocation)
    2. Request headers (User-Agent, Accept-Language)
    3. Performance metrics (page load time)
    4. User behavior (clicks vs voice, image loading failures)
    """
    
    @staticmethod
    def detect() -> UserContext:
        """Detect user context from Streamlit session"""
        
        # Get Streamlit session info
        session_state = st.session_state
        
        # Detect connection speed (simplified)
        connection_speed = ContextDetector._detect_connection_speed()
        
        # Detect device type
        device_type = ContextDetector._detect_device_type()
        
        # Detect screen size (from Streamlit)
        screen_width = 1920  # Default, would come from browser
        screen_height = 1080
        is_mobile = screen_width < 768
        is_touch = is_mobile  # Assume mobile = touch
        
        # Detect location (would use IP geolocation or GPS)
        country, city = ContextDetector._detect_location()
        
        # Detect language (from browser or session)
        language = st.session_state.get("language", "en")
        
        # Create context
        context = UserContext(
            connection_speed=connection_speed,
            connection_type=connection_speed.value.upper(),
            bandwidth_estimate=ContextDetector._estimate_bandwidth(connection_speed),
            device_type=device_type,
            screen_width=screen_width,
            screen_height=screen_height,
            is_mobile=is_mobile,
            is_touch=is_touch,
            country=country,
            city=city,
            language=language,
            data_conscious=ContextDetector._is_data_conscious(),
        )
        
        # Store in session for reuse
        st.session_state["user_context"] = context
        
        return context
    
    @staticmethod
    def _detect_connection_speed() -> ConnectionSpeed:
        """Detect connection speed"""
        # In production, use:
        # - navigator.connection.effectiveType (JS)
        # - Page load time metrics
        # - Request headers
        
        # For now, check if user set preference
        speed_pref = st.session_state.get("connection_speed", "auto")
        
        if speed_pref == "4g":
            return ConnectionSpeed.FAST_4G
        elif speed_pref == "3g":
            return ConnectionSpeed.MEDIUM_3G
        elif speed_pref == "2g":
            return ConnectionSpeed.SLOW_2G
        elif speed_pref == "offline":
            return ConnectionSpeed.OFFLINE
        else:
            # Auto-detect (default to fast for demo)
            return ConnectionSpeed.FAST_4G
    
    @staticmethod
    def _detect_device_type() -> DeviceType:
        """Detect device type from User-Agent"""
        # In production, parse User-Agent header
        # For now, check session or default
        device_pref = st.session_state.get("device_type", "smartphone")
        
        device_map = {
            "smartphone": DeviceType.SMARTPHONE,
            "basic_phone": DeviceType.BASIC_PHONE,
            "tablet": DeviceType.TABLET,
            "desktop": DeviceType.DESKTOP,
        }
        
        return device_map.get(device_pref, DeviceType.SMARTPHONE)
    
    @staticmethod
    def _detect_location() -> tuple[Optional[str], Optional[str]]:
        """Detect location (country, city)"""
        # In production:
        # - IP geolocation (MaxMind, IPinfo)
        # - Browser geolocation API
        # - User profile
        
        # Check session
        country = st.session_state.get("country", None)
        city = st.session_state.get("city", None)
        
        return country, city
    
    @staticmethod
    def _estimate_bandwidth(speed: ConnectionSpeed) -> float:
        """Estimate bandwidth in Mbps"""
        bandwidth_map = {
            ConnectionSpeed.FAST_4G: 25.0,
            ConnectionSpeed.MEDIUM_3G: 3.0,
            ConnectionSpeed.SLOW_2G: 0.3,
            ConnectionSpeed.OFFLINE: 0.0,
        }
        return bandwidth_map[speed]
    
    @staticmethod
    def _is_data_conscious() -> bool:
        """Is user trying to conserve data?"""
        # Check for:
        # - Data Saver mode enabled in browser
        # - Multiple failed image loads
        # - User explicitly enabled data saver
        
        return st.session_state.get("data_saver", False)


class AdaptiveUI:
    """
    Adaptive UI components based on context
    
    Usage:
        context = ContextDetector.detect()
        ui = AdaptiveUI(context)
        
        # Show content adapted to context
        ui.show_image(url)  # Only loads if appropriate
        ui.show_text(text)  # May offer audio alternative
    """
    
    def __init__(self, context: UserContext):
        self.context = context
    
    def show_image(self, url: str, alt_text: str = "", caption: str = ""):
        """Show image only if appropriate for context"""
        if self.context.should_load_images:
            st.image(url, caption=caption)
        else:
            # Show alt text instead
            st.info(f"🖼️ {alt_text or caption}")
    
    def show_gospel_text(self, text: str, citation: str):
        """Show Gospel text with audio option if needed"""
        st.markdown(f"### {citation}")
        
        # Always show text
        st.markdown(text)
        
        # Offer audio for audio-visual mode
        if self.context.should_use_audio:
            st.info("🔊 Audio reading available (feature coming soon)")
    
    def show_prayer(self, prayer_name: str, prayer_text: str):
        """Show prayer with audio option"""
        with st.expander(f"✝️ {prayer_name}"):
            st.markdown(f"*{prayer_text}*")
            
            if self.context.should_use_audio:
                st.caption("🔊 Tap to hear audio (coming soon)")
    
    def show_context_banner(self):
        """Show context-aware banner"""
        mode = self.context.ui_mode
        
        if mode == UIMode.TEXT_ONLY:
            st.warning("📱 **Data Saver Mode Active** - Images hidden to save bandwidth")
        elif mode == UIMode.OFFLINE_FIRST:
            st.info("✈️ **Offline Mode** - Using cached content")
        elif mode == UIMode.SMS_BRIDGE:
            st.success("📲 **SMS Mode** - Send commands via SMS to 40404")
        elif mode == UIMode.AUDIO_VISUAL:
            st.info("🔊 **Audio Mode** - Voice assistance available")


# DEMO CONTEXTS

WESTLANDS_EXPAT_CONTEXT = UserContext(
    connection_speed=ConnectionSpeed.FAST_4G,
    connection_type="4G",
    bandwidth_estimate=25.0,
    device_type=DeviceType.SMARTPHONE,
    screen_width=390,
    screen_height=844,
    is_mobile=True,
    is_touch=True,
    latitude=-1.2667,
    longitude=36.8000,
    country="Kenya",
    city="Nairobi",
    language="en",
    languages=["en", "fr", "it"],
    literacy_level=LiteracyLevel.HIGH,
    data_conscious=False,
)

NAMUGONGO_RURAL_CONTEXT = UserContext(
    connection_speed=ConnectionSpeed.SLOW_2G,
    connection_type="2G",
    bandwidth_estimate=0.3,
    device_type=DeviceType.BASIC_PHONE,
    screen_width=240,
    screen_height=320,
    is_mobile=True,
    is_touch=False,
    latitude=0.3667,
    longitude=32.6500,
    country="Uganda",
    city="Namugongo",
    language="lg",  # Luganda
    languages=["lg", "en"],
    literacy_level=LiteracyLevel.BASIC,
    data_conscious=True,
)


if __name__ == "__main__":
    # Demo: Different contexts
    print("=== WESTLANDS EXPAT ===")
    print(f"UI Mode: {WESTLANDS_EXPAT_CONTEXT.ui_mode.value}")
    print(f"Load Images: {WESTLANDS_EXPAT_CONTEXT.should_load_images}")
    print(f"Max Content: {WESTLANDS_EXPAT_CONTEXT.max_content_size_kb} KB")
    print()
    
    print("=== NAMUGONGO RURAL ===")
    print(f"UI Mode: {NAMUGONGO_RURAL_CONTEXT.ui_mode.value}")
    print(f"Load Images: {NAMUGONGO_RURAL_CONTEXT.should_load_images}")
    print(f"Max Content: {NAMUGONGO_RURAL_CONTEXT.max_content_size_kb} KB")
