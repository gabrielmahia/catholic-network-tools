"""
Voice-First Interface for Oral Cultures

CRITICAL INSIGHT: Many African Catholics prefer audio over text
- Oral tradition (storytelling culture)
- Variable literacy levels
- Audio more accessible than reading

FEATURES:
1. Text-to-Speech (TTS) for all content
2. Voice commands (Swahili, English, Luganda)
3. Audio prayers (recorded + synthesized)
4. Voice notes for prayer requests
5. Audio Gospel readings

IMPLEMENTATION:
- Web Speech API (browser-native, free)
- Fallback: Pre-recorded audio files
- Mobile-optimized (works on basic smartphones)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum


class VoiceCommand(Enum):
    """Supported voice commands"""
    # Gospel & Readings
    READ_GOSPEL = "soma injili"          # Swahili: read gospel
    READ_FIRST_READING = "soma masomo"   # Swahili: read readings
    
    # Prayers
    PRAY_OUR_FATHER = "ombi la baba"     # Swahili: Our Father
    PRAY_HAIL_MARY = "salamu maria"      # Swahili: Hail Mary
    PRAY_ROSARY = "ombi la rosary"       # Swahili: Rosary prayer
    
    # Church Finder
    FIND_CHURCH = "tafuta kanisa"        # Swahili: find church
    FIND_MASS = "misa lini"              # Swahili: when is Mass
    
    # Help
    HELP = "msaada"                      # Swahili: help
    STOP = "simama"                      # Swahili: stop


@dataclass
class AudioContent:
    """Audio content metadata"""
    content_type: str                    # "prayer", "gospel", "homily", etc.
    title: str
    text: str
    audio_url: Optional[str] = None      # Pre-recorded audio
    language: str = "en"
    duration_seconds: Optional[int] = None
    speaker: Optional[str] = None        # Who recorded it


class VoiceInterface:
    """
    Voice-first interface for oral cultures
    
    Capabilities:
    1. Read any text aloud (TTS)
    2. Recognize voice commands
    3. Play pre-recorded audio
    4. Record voice notes
    
    Usage:
        voice = VoiceInterface(language="sw")
        voice.speak("Jina langu ni Yesu")  # Speaks in Swahili
        voice.listen_for_command()         # Waits for voice command
    """
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.is_speaking = False
        self.is_listening = False
        
        # Map languages to TTS voices
        self.voice_map = {
            "en": "en-US",
            "sw": "sw-KE",      # Swahili (Kenya)
            "lg": "lg-UG",      # Luganda (Uganda)
            "fr": "fr-FR",
            "es": "es-ES",
        }
    
    def speak(self, text: str, rate: float = 1.0) -> None:
        """
        Speak text aloud using TTS
        
        Args:
            text: Text to speak
            rate: Speech rate (0.5 = slow, 1.0 = normal, 2.0 = fast)
        
        Implementation: Web Speech API (JavaScript)
        """
        # JavaScript code to inject into Streamlit
        js_code = f"""
        <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance('{text}');
                utterance.lang = '{self.voice_map.get(self.language, "en-US")}';
                utterance.rate = {rate};
                
                // Play
                speechSynthesis.speak(utterance);
            }} else {{
                alert('Text-to-Speech not supported in this browser');
            }}
        }}
        
        // Auto-play if user clicked button
        speakText();
        </script>
        """
        
        return js_code
    
    def get_voice_commands_help(self) -> Dict[str, str]:
        """Get help text for voice commands"""
        if self.language == "sw":  # Swahili
            return {
                "soma injili": "Soma Injili ya leo",
                "soma masomo": "Soma masomo ya leo",
                "ombi la baba": "Omba Baba Yetu",
                "salamu maria": "Omba Salamu Maria",
                "ombi la rosary": "Omba Rosary",
                "tafuta kanisa": "Tafuta kanisa karibu",
                "misa lini": "Pata muda wa Misa",
                "msaada": "Onyesha msaada",
            }
        else:  # English
            return {
                "read gospel": "Read today's Gospel",
                "read readings": "Read today's readings",
                "pray our father": "Pray the Our Father",
                "pray hail mary": "Pray the Hail Mary",
                "pray rosary": "Pray the Rosary",
                "find church": "Find nearest church",
                "mass times": "Get Mass times",
                "help": "Show help",
            }
    
    def get_listen_button_js(self) -> str:
        """
        JavaScript code for voice recognition button
        
        Returns HTML/JS for Streamlit to inject
        """
        commands_help = self.get_voice_commands_help()
        commands_list = ", ".join([f'"{cmd}"' for cmd in commands_help.keys()])
        
        js_code = f"""
        <script>
        let recognition = null;
        
        function startListening() {{
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                alert('Voice recognition not supported in this browser. Try Chrome or Edge.');
                return;
            }}
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            recognition.lang = '{self.voice_map.get(self.language, "en-US")}';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            recognition.onstart = function() {{
                console.log('🎤 Listening...');
                document.getElementById('voice-status').textContent = '🎤 Listening...';
            }};
            
            recognition.onresult = function(event) {{
                const command = event.results[0][0].transcript.toLowerCase();
                console.log('Heard: ' + command);
                
                // Check if command matches known commands
                const knownCommands = [{commands_list}];
                const matched = knownCommands.find(cmd => command.includes(cmd));
                
                if (matched) {{
                    document.getElementById('voice-command').value = matched;
                    document.getElementById('voice-status').textContent = '✓ Command: ' + matched;
                }} else {{
                    document.getElementById('voice-status').textContent = '❌ Unknown command. Say "help" for list.';
                }}
            }};
            
            recognition.onerror = function(event) {{
                console.error('Speech recognition error:', event.error);
                document.getElementById('voice-status').textContent = '❌ Error: ' + event.error;
            }};
            
            recognition.onend = function() {{
                document.getElementById('voice-status').textContent = 'Click to speak again';
            }};
            
            recognition.start();
        }}
        
        function stopListening() {{
            if (recognition) {{
                recognition.stop();
            }}
        }}
        </script>
        
        <div style="padding: 20px; background: #f0f8ff; border-radius: 10px; text-align: center;">
            <button onclick="startListening()" style="font-size: 48px; background: none; border: none; cursor: pointer;">
                🎤
            </button>
            <p id="voice-status" style="margin-top: 10px; font-weight: bold;">
                Click microphone to speak
            </p>
            <input type="hidden" id="voice-command" />
        </div>
        """
        
        return js_code


class AudioLibrary:
    """
    Pre-recorded audio content library
    
    For high-quality audio where TTS isn't good enough:
    - Gospel readings (human voice)
    - Traditional prayers (sung/chanted)
    - Sunday homilies (priest recorded)
    - Catechism lessons
    """
    
    # Audio URLs (would be hosted on CDN)
    AUDIO_BASE_URL = "https://catholic-spiritual-os.s3.amazonaws.com/audio"
    
    PRAYERS = {
        "our_father_en": AudioContent(
            content_type="prayer",
            title="Our Father (English)",
            text="Our Father, who art in heaven...",
            audio_url=f"{AUDIO_BASE_URL}/prayers/our_father_en.mp3",
            language="en",
            duration_seconds=45,
        ),
        "our_father_sw": AudioContent(
            content_type="prayer",
            title="Baba Yetu (Swahili)",
            text="Baba yetu uliye mbinguni...",
            audio_url=f"{AUDIO_BASE_URL}/prayers/baba_yetu_sw.mp3",
            language="sw",
            duration_seconds=50,
        ),
        "our_father_lg": AudioContent(
            content_type="prayer",
            title="Kitaffe (Luganda)",
            text="Kitaffe aali mu ggulu...",
            audio_url=f"{AUDIO_BASE_URL}/prayers/kitaffe_lg.mp3",
            language="lg",
            duration_seconds=48,
        ),
        "hail_mary_en": AudioContent(
            content_type="prayer",
            title="Hail Mary (English)",
            text="Hail Mary, full of grace...",
            audio_url=f"{AUDIO_BASE_URL}/prayers/hail_mary_en.mp3",
            language="en",
            duration_seconds=30,
        ),
        "hail_mary_sw": AudioContent(
            content_type="prayer",
            title="Salamu Maria (Swahili)",
            text="Salamu Maria, umejaa neema...",
            audio_url=f"{AUDIO_BASE_URL}/prayers/salamu_maria_sw.mp3",
            language="sw",
            duration_seconds=32,
        ),
    }
    
    @classmethod
    def get_prayer_audio(cls, prayer_name: str, language: str) -> Optional[AudioContent]:
        """Get audio content for a prayer"""
        key = f"{prayer_name}_{language}"
        return cls.PRAYERS.get(key)
    
    @classmethod
    def get_audio_player_html(cls, audio: AudioContent) -> str:
        """Generate HTML audio player"""
        return f"""
        <div style="padding: 15px; background: #f9f9f9; border-radius: 8px; margin: 10px 0;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 32px;">🔊</div>
                <div style="flex: 1;">
                    <div style="font-weight: bold; margin-bottom: 5px;">{audio.title}</div>
                    <audio controls style="width: 100%;">
                        <source src="{audio.audio_url}" type="audio/mpeg">
                        Your browser does not support audio playback.
                    </audio>
                </div>
            </div>
            <div style="margin-top: 10px; padding: 10px; background: white; border-radius: 5px; font-style: italic; color: #555;">
                {audio.text[:100]}...
            </div>
        </div>
        """


class VoiceAccessibilityHelper:
    """
    Voice accessibility features for users with visual impairments or low literacy
    
    Features:
    - Screen reader optimization
    - High contrast voice UI
    - Large touch targets for voice buttons
    - Simple voice navigation
    """
    
    @staticmethod
    def get_voice_navigation_prompt(page_name: str) -> str:
        """Get voice prompt for page navigation"""
        prompts = {
            "home": "You are on the home page. Say 'daily prayers' to go to prayers, or 'find church' to locate a church.",
            "prayers": "Daily prayers page. Say 'our father' to pray the Our Father, or 'rosary' for the Rosary.",
            "gospel": "Today's Gospel page. Say 'read gospel' to hear it aloud.",
            "church_finder": "Find a church. Say 'near me' to find churches nearby, or say a city name.",
        }
        return prompts.get(page_name, "Say 'help' for available commands.")
    
    @staticmethod
    def get_large_voice_button_css() -> str:
        """CSS for large, touch-friendly voice buttons"""
        return """
        <style>
        .voice-button {
            width: 100px;
            height: 100px;
            font-size: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        
        .voice-button:hover {
            transform: scale(1.1);
        }
        
        .voice-button:active {
            transform: scale(0.95);
        }
        
        .voice-status {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            text-align: center;
        }
        </style>
        """


# DEMO USAGE

if __name__ == "__main__":
    # English voice interface
    voice_en = VoiceInterface(language="en")
    print("=== ENGLISH VOICE COMMANDS ===")
    for cmd, desc in voice_en.get_voice_commands_help().items():
        print(f"  {cmd}: {desc}")
    print()
    
    # Swahili voice interface
    voice_sw = VoiceInterface(language="sw")
    print("=== SWAHILI VOICE COMMANDS ===")
    for cmd, desc in voice_sw.get_voice_commands_help().items():
        print(f"  {cmd}: {desc}")
    print()
    
    # Audio library
    print("=== AVAILABLE AUDIO PRAYERS ===")
    for key, audio in AudioLibrary.PRAYERS.items():
        print(f"  {key}: {audio.title} ({audio.duration_seconds}s)")
