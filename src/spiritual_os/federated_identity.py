"""
Federated Parish Identity System

CRITICAL: There is NO universal Catholic Parish ID system!

The Catholic Church operates as a federation:
- Diocese level: Local authority
- Parish level: Self-governed under diocese
- Global level: Loose coordination, no central registry

This module implements federated identity inspired by:
- Email (local authority, global federation)
- Web domains (self-asserted, DNS-verified)
- DID (Decentralized Identifiers)

IDENTITY STRATEGY:
1. GeoHash (always works, globally unique for location)
2. Contact (phone/WhatsApp - how people actually find parishes in Africa)
3. Diocese code (local registry)
4. Optional global listings (GCatholic, Vatican)

NO CENTRAL AUTHORITY REQUIRED
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
import hashlib
import geohash2  # pip install geohash2


class IdentityLevel(Enum):
    """Levels of identity verification"""
    SELF_ASSERTED = "self_asserted"      # Parish claims identity
    COMMUNITY_VERIFIED = "community"      # Local community confirms
    DIOCESE_REGISTERED = "diocese"        # Diocese officially recognizes
    GLOBAL_LISTED = "global"              # In global directories (GCatholic, Vatican)


@dataclass
class GeoLocation:
    """Geographic location of parish"""
    latitude: float
    longitude: float
    geohash: str = ""  # 7 chars = ~150m precision, 8 = ~19m
    address: str = ""
    city: str = ""
    region: str = ""  # State/Province
    country: str = ""
    
    def __post_init__(self):
        if not self.geohash:
            # Generate geohash from coordinates
            self.geohash = geohash2.encode(self.latitude, self.longitude, precision=7)
    
    @property
    def geohash_short(self) -> str:
        """Short geohash for display"""
        return self.geohash[:5]
    
    def distance_to(self, other: 'GeoLocation') -> float:
        """Approximate distance in km (Haversine formula)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth radius in km
        
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(other.latitude), radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c


@dataclass
class ContactInfo:
    """How to actually reach the parish"""
    # Primary identifiers in Africa
    phone: str                          # "+254-722-123456"
    whatsapp: bool = False              # Is phone also WhatsApp?
    
    # Optional Western identifiers
    email: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    
    # SMS shortcode (if registered)
    sms_shortcode: Optional[str] = None  # "40404"
    
    def __str__(self):
        return self.phone + (" (WhatsApp)" if self.whatsapp else "")


@dataclass
class DioceseRegistration:
    """Registration at diocese level"""
    diocese_name: str                   # "Archdiocese of Nairobi"
    diocese_code: str                   # "NAI" (3-letter code)
    parish_number: str                  # "042" (within diocese)
    registration_date: str              # ISO format
    bishop: Optional[str] = None
    
    @property
    def full_code(self) -> str:
        """Full diocese-parish code"""
        return f"{self.diocese_code}-{self.parish_number}"


@dataclass
class GlobalListings:
    """Optional listings in global directories"""
    gcatholic_id: Optional[str] = None       # GCatholic.org ID
    vatican_annuario: Optional[str] = None   # Vatican Annuario Pontificio
    catholic_hierarchy: Optional[str] = None  # Catholic-Hierarchy.org
    
    def is_globally_listed(self) -> bool:
        """Is parish in any global directory?"""
        return any([self.gcatholic_id, self.vatican_annuario, self.catholic_hierarchy])


@dataclass
class FederatedParishIdentity:
    """
    Federated Parish Identity - No Central Authority Required
    
    Identity is built from multiple layers:
    1. LOCAL: Name + Location + Contact (always present)
    2. REGIONAL: Diocese registration (optional but common)
    3. GLOBAL: International directories (optional)
    
    Like email: local authority (@gmail.com decides who gets addresses)
    Diocese: local authority (decides parish codes)
    Global: optional federation (can list in GCatholic if desired)
    """
    
    # LAYER 1: Local Identity (REQUIRED)
    name: str                           # "St. Austin's Parish"
    location: GeoLocation               # GPS + address
    contact: ContactInfo                # Phone/WhatsApp/email
    established: str                    # ISO date
    
    # LAYER 2: Regional Identity (OPTIONAL but common)
    diocese: Optional[DioceseRegistration] = None
    
    # LAYER 3: Global Identity (OPTIONAL)
    global_listings: GlobalListings = field(default_factory=GlobalListings)
    
    # LAYER 4: National Identity (varies by country)
    national_registration: Optional[str] = None  # Kenya NGO #, US EIN, etc.
    
    # Self-Sovereign Identity (future: blockchain)
    did: Optional[str] = None           # "did:parish:nairobi:staustin"
    
    # Verification level
    verification_level: IdentityLevel = IdentityLevel.SELF_ASSERTED
    
    # Metadata
    languages: List[str] = field(default_factory=list)
    patron_saint: Optional[str] = None
    
    @property
    def unique_id(self) -> str:
        """
        Generate unique identifier WITHOUT central authority
        
        Strategy: Hash of location + contact + name
        This is self-generated but globally unique (collision probability ~0)
        """
        components = [
            self.name.lower().strip(),
            self.location.geohash,
            self.contact.phone,
            self.established[:4],  # Year only
        ]
        
        combined = "|".join(components)
        hash_obj = hashlib.sha256(combined.encode())
        
        # Return first 12 chars (base58 encoded)
        # Example: "s21yf9A2k4Nm"
        return hash_obj.hexdigest()[:12]
    
    @property
    def display_id(self) -> str:
        """Human-readable identifier for display"""
        if self.diocese:
            # Use diocese code if available
            return f"{self.diocese.full_code} ({self.location.geohash_short})"
        else:
            # Fallback to geohash + country
            return f"{self.location.country}:{self.location.geohash_short}"
    
    @property
    def primary_identifier(self) -> str:
        """What to use in practice? Phone number!"""
        return self.contact.phone
    
    def verify_with_diocese(self, diocese_code: str, parish_number: str):
        """Upgrade verification level when diocese confirms"""
        self.verification_level = IdentityLevel.DIOCESE_REGISTERED
    
    def list_globally(self, directory: str, listing_id: str):
        """Add to global directory"""
        if directory == "gcatholic":
            self.global_listings.gcatholic_id = listing_id
        elif directory == "vatican":
            self.global_listings.vatican_annuario = listing_id
        elif directory == "catholic-hierarchy":
            self.global_listings.catholic_hierarchy = listing_id
        
        if self.global_listings.is_globally_listed():
            self.verification_level = IdentityLevel.GLOBAL_LISTED
    
    def to_dict(self) -> Dict:
        """Export for JSON/API"""
        return {
            "name": self.name,
            "unique_id": self.unique_id,
            "display_id": self.display_id,
            "location": {
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
                "geohash": self.location.geohash,
                "address": self.location.address,
                "city": self.location.city,
                "country": self.location.country,
            },
            "contact": {
                "phone": self.contact.phone,
                "whatsapp": self.contact.whatsapp,
                "email": self.contact.email,
                "website": self.contact.website,
            },
            "diocese": {
                "name": self.diocese.diocese_name,
                "code": self.diocese.full_code,
            } if self.diocese else None,
            "global_listings": {
                "gcatholic": self.global_listings.gcatholic_id,
                "vatican": self.global_listings.vatican_annuario,
            } if self.global_listings.is_globally_listed() else None,
            "verification": self.verification_level.value,
        }


# EXAMPLES

WESTLANDS_EXPAT_PARISH = FederatedParishIdentity(
    name="St. Austin's Parish",
    location=GeoLocation(
        latitude=-1.2667,
        longitude=36.8000,
        address="Muthithi Road, Westlands",
        city="Nairobi",
        region="Nairobi County",
        country="Kenya",
    ),
    contact=ContactInfo(
        phone="+254-722-123456",
        whatsapp=True,
        email="staustin@nairobi.catholic.ke",
        website="https://staustin.or.ke",
    ),
    established="1995-03-15",
    diocese=DioceseRegistration(
        diocese_name="Archdiocese of Nairobi",
        diocese_code="NAI",
        parish_number="042",
        registration_date="1995-03-15",
        bishop="Archbishop Philip Anyolo",
    ),
    global_listings=GlobalListings(
        gcatholic_id="NAI042",
    ),
    national_registration="NGO/2024/123456",  # Kenya NGO registration
    languages=["English", "Swahili"],
    patron_saint="St. Augustine of Hippo",
    verification_level=IdentityLevel.DIOCESE_REGISTERED,
)

NAMUGONGO_RURAL_PARISH = FederatedParishIdentity(
    name="St. Charles Lwanga Parish",
    location=GeoLocation(
        latitude=0.3667,
        longitude=32.6500,
        address="Namugongo Road",
        city="Namugongo",
        region="Wakiso District",
        country="Uganda",
    ),
    contact=ContactInfo(
        phone="+256-772-123456",
        whatsapp=True,
        email=None,  # No email (rural)
        website=None,
    ),
    established="1982-06-03",
    diocese=DioceseRegistration(
        diocese_name="Archdiocese of Kampala",
        diocese_code="KLA",
        parish_number="087",
        registration_date="1982-06-03",
        bishop="Archbishop Paul Ssemogerere",
    ),
    languages=["Luganda", "English"],
    patron_saint="St. Charles Lwanga (Uganda Martyr)",
    verification_level=IdentityLevel.DIOCESE_REGISTERED,
)


# DEMO: How to use

if __name__ == "__main__":
    # Westlands expat parish
    print("=== WESTLANDS EXPAT PARISH ===")
    print(f"Name: {WESTLANDS_EXPAT_PARISH.name}")
    print(f"Unique ID: {WESTLANDS_EXPAT_PARISH.unique_id}")
    print(f"Display ID: {WESTLANDS_EXPAT_PARISH.display_id}")
    print(f"Primary Contact: {WESTLANDS_EXPAT_PARISH.primary_identifier}")
    print(f"Verification: {WESTLANDS_EXPAT_PARISH.verification_level.value}")
    print()
    
    # Namugongo rural parish
    print("=== NAMUGONGO RURAL PARISH ===")
    print(f"Name: {NAMUGONGO_RURAL_PARISH.name}")
    print(f"Unique ID: {NAMUGONGO_RURAL_PARISH.unique_id}")
    print(f"Display ID: {NAMUGONGO_RURAL_PARISH.display_id}")
    print(f"Primary Contact: {NAMUGONGO_RURAL_PARISH.primary_identifier}")
    print(f"Verification: {NAMUGONGO_RURAL_PARISH.verification_level.value}")
    print()
    
    # Distance between parishes
    distance = WESTLANDS_EXPAT_PARISH.location.distance_to(NAMUGONGO_RURAL_PARISH.location)
    print(f"Distance: {distance:.1f} km")
