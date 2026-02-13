"""
Mass Readings API Integration - Multi-Source with Cascading Fallback

Provides actual Scripture text for daily Mass readings with enterprise reliability.

ARCHITECTURE:
- Multiple data sources with automatic failover
- Local caching for offline access
- Source priority based on reliability + completeness
- No single point of failure

Data sources (in priority order):
1. USCCB (United States Conference of Catholic Bishops) - Official US source
2. Universalis (universalis.com) - Global liturgy resource
3. Catholic Readings API (daily-mass-readings.org) - Community maintained
4. iBreviary (ibreviary.org) - Mobile-first API
5. Local cache (sqlite) - Works completely offline

Context awareness:
- Westlands expat (4G) → Fetches from all sources, rich content
- Namugongo rural (2G) → Cached content, minimal bandwidth
- Offline mode → Local cache only
"""

import requests
from datetime import date, datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
from pathlib import Path
import json


class LiturgicalCycle(Enum):
    """Liturgical year cycle"""
    YEAR_A = "A"
    YEAR_B = "B"
    YEAR_C = "C"


class ReadingType(Enum):
    """Types of Mass readings"""
    FIRST_READING = "first_reading"
    PSALM = "psalm"
    SECOND_READING = "second_reading"
    GOSPEL = "gospel"
    ALLELUIA = "alleluia"


class SourcePriority(Enum):
    """Priority level for data sources"""
    PRIMARY = 1      # Official Catholic sources
    SECONDARY = 2    # Reliable community sources
    TERTIARY = 3     # Backup sources
    FALLBACK = 4     # Last resort
    OFFLINE = 5      # Local cache only


@dataclass
class DataSource:
    """Configuration for a Gospel data source"""
    name: str
    base_url: str
    priority: SourcePriority
    timeout: int = 10
    requires_auth: bool = False
    active: bool = True
    
    def __repr__(self):
        return f"<Source: {self.name} (Priority {self.priority.value})>"


@dataclass
class Reading:
    """Individual Scripture reading"""
    type: ReadingType
    citation: str  # e.g., "John 3:16-21"
    text: str  # Full text of the reading
    audio_url: Optional[str] = None  # Link to audio version
    source: str = "unknown"  # Which API provided this


@dataclass
class MassReadings:
    """Complete set of readings for a liturgical day"""
    date: date
    liturgical_title: str  # e.g., "7th Sunday in Ordinary Time"
    liturgical_cycle: LiturgicalCycle
    season: str
    color: str
    
    first_reading: Reading
    psalm: Reading
    second_reading: Optional[Reading]  # Not present on weekdays
    gospel: Reading
    alleluia: Optional[Reading]
    
    reflections: List[str] = field(default_factory=list)
    saint_of_day: Optional[str] = None
    source: str = "unknown"  # Which source provided this data
    cached: bool = False  # Was this from cache?


class MassReadingsAPI:
    """
    Multi-Source Gospel API with Cascading Fallback
    
    Reliability through redundancy:
    1. Try primary sources (official Catholic APIs)
    2. Fall back to secondary sources (community maintained)
    3. Use tertiary sources (broader Christian APIs)
    4. Return cached data (always available offline)
    
    Context-aware:
    - Slow connection: Skip heavy sources, use cache
    - Fast connection: Try all sources, cache result
    - Offline: Cache only
    """
    
    # Define all available data sources
    SOURCES = [
        DataSource(
            name="USCCB",
            base_url="https://bible.usccb.org/api/readings",
            priority=SourcePriority.PRIMARY,
            timeout=10,
        ),
        DataSource(
            name="Universalis",
            base_url="https://universalis.com/api",
            priority=SourcePriority.PRIMARY,
            timeout=10,
        ),
        DataSource(
            name="Catholic Readings",
            base_url="https://api.daily-mass-readings.org/readings",
            priority=SourcePriority.SECONDARY,
            timeout=8,
        ),
        DataSource(
            name="iBreviary",
            base_url="https://www.ibreviary.org/api",
            priority=SourcePriority.SECONDARY,
            timeout=8,
        ),
        DataSource(
            name="Local Cache",
            base_url="sqlite:///mass_readings_cache.db",
            priority=SourcePriority.OFFLINE,
            timeout=1,
        ),
    ]
    
    # Fallback for demo/testing
    DEMO_API = "https://api.daily-mass-readings.org"
    
    @classmethod
    def get_today(cls, connection_speed: str = "fast") -> Optional[MassReadings]:
        """
        Get Mass readings for today
        
        Args:
            connection_speed: "fast" (4G+), "medium" (3G), "slow" (2G), "offline"
        """
        return cls.get_readings(date.today(), connection_speed)
    
    @classmethod
    def get_readings(
        cls, 
        target_date: date,
        connection_speed: str = "fast"
    ) -> Optional[MassReadings]:
        """
        Get Mass readings with multi-source fallback
        
        Strategy:
        1. Fast connection (4G+): Try all sources in priority order
        2. Medium connection (3G): Skip tertiary sources, use primary + cache
        3. Slow connection (2G): Cache first, then try one primary source
        4. Offline: Cache only
        
        Returns complete readings with full Scripture text.
        Falls back gracefully if API unavailable.
        """
        
        # Check cache first for slow/offline connections
        if connection_speed in ["slow", "offline"]:
            cached = cls._get_from_cache(target_date)
            if cached:
                return cached
            
            if connection_speed == "offline":
                # Offline: cache only
                return cls._get_fallback_readings(target_date)
        
        # Determine which sources to try based on connection
        sources_to_try = cls._filter_sources_by_connection(connection_speed)
        
        # Try each source in priority order
        for source in sources_to_try:
            if not source.active:
                continue
            
            try:
                if source.name == "Local Cache":
                    result = cls._get_from_cache(target_date)
                else:
                    result = cls._fetch_from_source(source, target_date)
                
                if result:
                    # Success! Cache it for offline use
                    cls._cache_readings(result)
                    return result
                    
            except Exception as e:
                print(f"Source {source.name} failed: {e}")
                continue  # Try next source
        
        # All sources failed → return cached or minimal fallback
        cached = cls._get_from_cache(target_date)
        if cached:
            return cached
        
        return cls._get_fallback_readings(target_date)
    
    @classmethod
    def _filter_sources_by_connection(cls, speed: str) -> List[DataSource]:
        """Filter sources based on connection speed"""
        
        if speed == "fast":
            # Try all sources
            return sorted(cls.SOURCES, key=lambda s: s.priority.value)
        
        elif speed == "medium":
            # Skip tertiary, use primary + secondary + cache
            return [s for s in cls.SOURCES 
                   if s.priority in [SourcePriority.PRIMARY, 
                                    SourcePriority.SECONDARY,
                                    SourcePriority.OFFLINE]]
        
        elif speed == "slow":
            # Cache first, then one primary source
            cache = [s for s in cls.SOURCES if s.priority == SourcePriority.OFFLINE]
            primary = [s for s in cls.SOURCES if s.priority == SourcePriority.PRIMARY][:1]
            return cache + primary
        
        else:  # offline
            # Cache only
            return [s for s in cls.SOURCES if s.priority == SourcePriority.OFFLINE]
    
    @classmethod
    def _fetch_from_source(
        cls,
        source: DataSource,
        target_date: date
    ) -> Optional[MassReadings]:
        """Fetch readings from a specific source"""
        
        try:
            # Format URL based on source
            if source.name == "Catholic Readings":
                url = f"{source.base_url}/{target_date.isoformat()}"
            elif source.name == "USCCB":
                url = f"{source.base_url}/{target_date.strftime('%m%d%y')}"
            elif source.name == "Universalis":
                url = f"{source.base_url}/mass/{target_date.isoformat()}"
            elif source.name == "iBreviary":
                url = f"{source.base_url}/readings/{target_date.isoformat()}"
            else:
                # Fallback format
                url = f"{cls.DEMO_API}/readings/{target_date.isoformat()}"
            
            response = requests.get(url, timeout=source.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response (format varies by source)
            readings = cls._parse_response(data, target_date, source.name)
            
            if readings:
                readings.source = source.name
                readings.cached = False
                return readings
            
        except requests.RequestException as e:
            print(f"Network error from {source.name}: {e}")
            return None
        except Exception as e:
            print(f"Parse error from {source.name}: {e}")
            return None
    
    @classmethod
    def _parse_response(
        cls,
        data: Dict[str, Any],
        target_date: date,
        source_name: str
    ) -> Optional[MassReadings]:
        """Parse API response (handles different formats)"""
        """Parse API response (handles different formats from different sources)"""
        
        try:
            # Extract readings (format varies by source)
            first_reading = Reading(
                type=ReadingType.FIRST_READING,
                citation=data.get("first_reading", {}).get("citation", ""),
                text=data.get("first_reading", {}).get("text", ""),
                source=source_name
            )
            
            psalm = Reading(
                type=ReadingType.PSALM,
                citation=data.get("psalm", {}).get("citation", ""),
                text=data.get("psalm", {}).get("text", ""),
                source=source_name
            )
            
            # Second reading (only on Sundays/Solemnities)
            second_reading = None
            if "second_reading" in data and data["second_reading"]:
                second_reading = Reading(
                    type=ReadingType.SECOND_READING,
                    citation=data.get("second_reading", {}).get("citation", ""),
                    text=data.get("second_reading", {}).get("text", ""),
                    source=source_name
                )
            
            gospel = Reading(
                type=ReadingType.GOSPEL,
                citation=data.get("gospel", {}).get("citation", ""),
                text=data.get("gospel", {}).get("text", ""),
                source=source_name
            )
            
            # Alleluia
            alleluia = None
            if "alleluia" in data:
                alleluia = Reading(
                    type=ReadingType.ALLELUIA,
                    citation=data.get("alleluia", {}).get("citation", ""),
                    text=data.get("alleluia", {}).get("text", ""),
                    source=source_name
                )
            
            # Determine liturgical cycle (simplified)
            year = target_date.year
            cycle_map = {0: LiturgicalCycle.YEAR_A, 1: LiturgicalCycle.YEAR_B, 2: LiturgicalCycle.YEAR_C}
            cycle = cycle_map[year % 3]
            
            return MassReadings(
                date=target_date,
                liturgical_title=data.get("title", ""),
                liturgical_cycle=cycle,
                season=data.get("season", "ordinary"),
                color=data.get("color", "green"),
                first_reading=first_reading,
                psalm=psalm,
                second_reading=second_reading,
                gospel=gospel,
                alleluia=alleluia,
                reflections=data.get("reflections", []),
                saint_of_day=data.get("saint", None),
                source=source_name,
                cached=False
            )
        except Exception as e:
            print(f"Error parsing {source_name} response: {e}")
            return None
    
    @classmethod
    def _cache_readings(cls, readings: MassReadings) -> None:
        """Cache readings to local storage for offline use"""
        # Simple JSON file cache for now
        # In production: use SQLite or IndexedDB
        try:
            cache_dir = Path.home() / ".catholic_spiritual_os" / "cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            cache_file = cache_dir / f"readings_{readings.date.isoformat()}.json"
            
            # Convert to dict
            cache_data = {
                "date": readings.date.isoformat(),
                "liturgical_title": readings.liturgical_title,
                "liturgical_cycle": readings.liturgical_cycle.value,
                "season": readings.season,
                "color": readings.color,
                "first_reading": {
                    "citation": readings.first_reading.citation,
                    "text": readings.first_reading.text,
                },
                "psalm": {
                    "citation": readings.psalm.citation,
                    "text": readings.psalm.text,
                },
                "second_reading": {
                    "citation": readings.second_reading.citation if readings.second_reading else "",
                    "text": readings.second_reading.text if readings.second_reading else "",
                } if readings.second_reading else None,
                "gospel": {
                    "citation": readings.gospel.citation,
                    "text": readings.gospel.text,
                },
                "alleluia": {
                    "text": readings.alleluia.text,
                } if readings.alleluia else None,
                "reflections": readings.reflections,
                "saint_of_day": readings.saint_of_day,
                "source": readings.source,
                "cached_at": datetime.now().isoformat(),
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            print(f"Cache write failed: {e}")
            # Non-critical, continue
    
    @classmethod
    def _get_from_cache(cls, target_date: date) -> Optional[MassReadings]:
        """Retrieve readings from local cache"""
        try:
            cache_file = Path.home() / ".catholic_spiritual_os" / "cache" / f"readings_{target_date.isoformat()}.json"
            
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            # Reconstruct MassReadings object
            cycle_map = {"A": LiturgicalCycle.YEAR_A, "B": LiturgicalCycle.YEAR_B, "C": LiturgicalCycle.YEAR_C}
            
            readings = MassReadings(
                date=date.fromisoformat(data["date"]),
                liturgical_title=data["liturgical_title"],
                liturgical_cycle=cycle_map[data["liturgical_cycle"]],
                season=data["season"],
                color=data["color"],
                first_reading=Reading(
                    type=ReadingType.FIRST_READING,
                    citation=data["first_reading"]["citation"],
                    text=data["first_reading"]["text"],
                    source="cache"
                ),
                psalm=Reading(
                    type=ReadingType.PSALM,
                    citation=data["psalm"]["citation"],
                    text=data["psalm"]["text"],
                    source="cache"
                ),
                second_reading=Reading(
                    type=ReadingType.SECOND_READING,
                    citation=data["second_reading"]["citation"],
                    text=data["second_reading"]["text"],
                    source="cache"
                ) if data.get("second_reading") else None,
                gospel=Reading(
                    type=ReadingType.GOSPEL,
                    citation=data["gospel"]["citation"],
                    text=data["gospel"]["text"],
                    source="cache"
                ),
                alleluia=Reading(
                    type=ReadingType.ALLELUIA,
                    citation="",
                    text=data["alleluia"]["text"],
                    source="cache"
                ) if data.get("alleluia") else None,
                reflections=data.get("reflections", []),
                saint_of_day=data.get("saint_of_day"),
                source="Local Cache",
                cached=True
            )
            
            return readings
            
        except Exception as e:
            print(f"Cache read failed: {e}")
            return None
        
        # Extract readings
        first_reading = Reading(
            type=ReadingType.FIRST_READING,
            citation=data.get("first_reading", {}).get("citation", ""),
            text=data.get("first_reading", {}).get("text", "")
        )
        
        psalm = Reading(
            type=ReadingType.PSALM,
            citation=data.get("psalm", {}).get("citation", ""),
            text=data.get("psalm", {}).get("text", "")
        )
        
        # Second reading (only on Sundays/Solemnities)
        second_reading = None
        if "second_reading" in data and data["second_reading"]:
            second_reading = Reading(
                type=ReadingType.SECOND_READING,
                citation=data.get("second_reading", {}).get("citation", ""),
                text=data.get("second_reading", {}).get("text", "")
            )
        
        gospel = Reading(
            type=ReadingType.GOSPEL,
            citation=data.get("gospel", {}).get("citation", ""),
            text=data.get("gospel", {}).get("text", "")
        )
        
        # Alleluia
        alleluia = None
        if "alleluia" in data:
            alleluia = Reading(
                type=ReadingType.ALLELUIA,
                citation=data.get("alleluia", {}).get("citation", ""),
                text=data.get("alleluia", {}).get("text", "")
            )
        
        # Determine liturgical cycle (simplified)
        year = target_date.year
        cycle_map = {0: LiturgicalCycle.YEAR_A, 1: LiturgicalCycle.YEAR_B, 2: LiturgicalCycle.YEAR_C}
        cycle = cycle_map[year % 3]
        
        return MassReadings(
            date=target_date,
            liturgical_title=data.get("title", ""),
            liturgical_cycle=cycle,
            season=data.get("season", "ordinary"),
            color=data.get("color", "green"),
            first_reading=first_reading,
            psalm=psalm,
            second_reading=second_reading,
            gospel=gospel,
            alleluia=alleluia,
            reflections=data.get("reflections", []),
            saint_of_day=data.get("saint", None)
        )
    
    @classmethod
    def _get_fallback_readings(cls, target_date: date) -> MassReadings:
        """
        Fallback readings when API unavailable
        
        Provides citations only, not full text.
        In production, this should load from cached/offline database.
        """
        
        # Simplified fallback - just provides structure
        return MassReadings(
            date=target_date,
            liturgical_title="Mass Readings",
            liturgical_cycle=LiturgicalCycle.YEAR_A,
            season="ordinary",
            color="green",
            first_reading=Reading(
                type=ReadingType.FIRST_READING,
                citation="See parish missal",
                text="Mass readings unavailable offline. Please check parish missal or visit USCCB.org when online."
            ),
            psalm=Reading(
                type=ReadingType.PSALM,
                citation="See parish missal",
                text="Psalm unavailable offline."
            ),
            second_reading=None,
            gospel=Reading(
                type=ReadingType.GOSPEL,
                citation="See parish missal",
                text="Gospel reading unavailable offline. Please check parish missal or visit USCCB.org when online."
            ),
            alleluia=None,
            reflections=[],
            saint_of_day=None
        )
    
    @classmethod
    def get_sunday_readings_for_month(cls, year: int, month: int) -> List[MassReadings]:
        """
        Get all Sunday readings for a given month
        
        Useful for parish bulletin planning.
        """
        from calendar import monthrange
        
        readings = []
        _, last_day = monthrange(year, month)
        
        for day in range(1, last_day + 1):
            target_date = date(year, month, day)
            
            # Only Sundays (weekday 6)
            if target_date.weekday() == 6:
                reading = cls.get_readings(target_date)
                if reading:
                    readings.append(reading)
        
        return readings


# Demo usage
if __name__ == "__main__":
    today = MassReadingsAPI.get_today()
    if today:
        print(f"Mass Readings for {today.date}")
        print(f"Liturgical Title: {today.liturgical_title}")
        print(f"Season: {today.season} (Cycle {today.liturgical_cycle.value})")
        print(f"\n--- GOSPEL ---")
        print(f"{today.gospel.citation}")
        print(today.gospel.text[:200] + "..." if len(today.gospel.text) > 200 else today.gospel.text)
