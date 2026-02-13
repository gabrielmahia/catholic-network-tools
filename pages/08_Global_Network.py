"""
Global Catholic Network - Federated Parish Coordination

NO CENTRAL AUTHORITY - parishes coordinate peer-to-peer based on:
- Geographic proximity (GeoHash)
- Shared justice campaigns
- Diocese coordination (optional)
- Resource sharing needs

Follows Catholic subsidiarity principle:
- Decisions at lowest competent level
- Parish → Diocese → National → Global
- Not centralized top-down
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.spiritual_os.federated_identity import (
    FederatedParishIdentity,
    GeoLocation,
    ContactInfo,
    DioceseRegistration,
    WESTLANDS_EXPAT_PARISH,
    NAMUGONGO_RURAL_PARISH,
)
from src.spiritual_os.church_directory import ChurchDirectory, DEMO_CHURCHES

st.set_page_config(
    page_title="Global Network | Catholic Spiritual OS",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Catholic Network")
st.caption("Federated parish coordination • No central authority • Subsidiarity principle")

# Context banner
st.info("""
**💡 Network Philosophy**: This system operates on **federated principles** — parishes coordinate 
peer-to-peer without requiring central authority. Like email domains or web servers, each parish 
is autonomous but can federate with others.
""")

st.divider()

# ============================================================================
# YOUR PARISH IDENTITY
# ============================================================================

st.header("🏘️ Your Parish Identity")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Federated Identity** means:
    - ✅ Your parish controls its own data
    - ✅ No "Parish ID" from central authority required
    - ✅ Self-asserted, community-verified
    - ✅ Can federate with others voluntarily
    
    **Identity Layers**:
    1. **Local** (Always): GeoHash + Phone + Name
    2. **Regional** (Optional): Diocese registration
    3. **Global** (Optional): Directory listing
    """)

with col2:
    # Demo parish selector
    demo_parish = st.selectbox(
        "View Demo Parish",
        ["St. Austin's (Westlands, Nairobi)", "St. Charles Lwanga (Namugongo, Uganda)"],
        key="demo_parish_selector"
    )
    
    parish = WESTLANDS_EXPAT_PARISH if "Westlands" in demo_parish else NAMUGONGO_RURAL_PARISH

# Display parish identity
with st.expander("📋 Parish Identity Card", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Parish Name", parish.name)
        st.caption(f"**Unique ID**: {parish.unique_id}")
        st.caption(f"**Display ID**: {parish.display_id}")
    
    with col2:
        st.metric("Primary Contact", parish.contact.phone)
        st.caption(f"**WhatsApp**: {'✅ Yes' if parish.contact.whatsapp else '❌ No'}")
        st.caption(f"**Location**: {parish.location.city}, {parish.location.country}")
    
    with col3:
        st.metric("Verification", parish.verification_level.value.replace('_', ' ').title())
        st.caption(f"**GeoHash**: {parish.location.geohash}")
        st.caption(f"**Established**: {parish.established}")

st.divider()

# ============================================================================
# NEARBY PARISHES (Geographic Discovery)
# ============================================================================

st.header("📍 Nearby Catholic Parishes")

st.markdown("""
**Geographic Discovery** via GeoHash:
- Find parishes within radius (5km, 10km, 50km)
- No central database required
- Works offline with cached data
- Privacy-preserving (location approximate)
""")

# Search radius
radius = st.slider("Search Radius (km)", min_value=5, max_value=100, value=20, step=5)

# Demo: Show nearby parishes
if demo_parish:
    st.info("""
    **📊 Demo Mode**: In production, this would query:
    1. Local cache (parishes you've synced with)
    2. Diocese directory (if connected)
    3. Global directory (GCatholic.org, crowdsourced)
    4. Peer broadcasts (nearby parishes announce themselves)
    """)
    
    # Show demo nearby parishes
    nearby = [
        {
            "name": "All Saints Cathedral",
            "distance": 12.3,
            "city": "Nairobi",
            "phone": "+254-722-234567",
            "whatsapp": True,
            "mass_languages": ["English", "Swahili", "French"],
        },
        {
            "name": "Holy Family Basilica",
            "distance": 15.7,
            "city": "Nairobi",
            "phone": "+254-722-345678",
            "whatsapp": True,
            "mass_languages": ["English", "Swahili"],
        },
    ]
    
    for p in nearby:
        with st.expander(f"⛪ {p['name']} — {p['distance']:.1f} km away"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Location**: {p['city']}")
                st.write(f"**Contact**: {p['phone']}")
                st.write(f"**WhatsApp**: {'✅' if p['whatsapp'] else '❌'}")
            with col2:
                st.write(f"**Mass Languages**: {', '.join(p['mass_languages'])}")
                if st.button(f"Connect with {p['name']}", key=f"connect_{p['name']}"):
                    st.success(f"✅ Connection request sent to {p['name']}")

st.divider()

# ============================================================================
# JUSTICE CAMPAIGN COORDINATION
# ============================================================================

st.header("⚖️ Justice Campaign Coordination")

st.markdown("""
**Peer-to-Peer Organization** (no central platform):
- Parishes self-organize via WhatsApp/Signal groups
- Diocese coordinates regionally (optional)
- Share impact data voluntarily
- No central authority required
""")

tabs = st.tabs(["Active Campaigns", "Start New Campaign", "Impact Tracking"])

with tabs[0]:
    st.subheader("🌍 Active Justice Campaigns")
    
    campaigns = [
        {
            "name": "Living Wage - East Africa",
            "parishes": 150,
            "volunteers": 2400,
            "workers_affected": 26000,
            "impact": "26% average wage increase",
            "coordinator": "Diocese of Nairobi Justice Office",
            "contact": "+254-722-456789 (WhatsApp)",
        },
        {
            "name": "Refugee Rights & Integration",
            "parishes": 89,
            "volunteers": 1200,
            "workers_affected": 12000,
            "impact": "Policy wins in 3 countries",
            "coordinator": "Kenya Conference of Catholic Bishops",
            "contact": "+254-722-567890 (WhatsApp)",
        },
    ]
    
    for campaign in campaigns:
        with st.expander(f"📢 {campaign['name']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Parishes Involved", campaign['parishes'])
                st.metric("Volunteers", campaign['volunteers'])
                st.metric("Workers Affected", f"{campaign['workers_affected']:,}")
            
            with col2:
                st.write(f"**Impact**: {campaign['impact']}")
                st.write(f"**Coordinator**: {campaign['coordinator']}")
                st.write(f"**Contact**: {campaign['contact']}")
                
                if st.button(f"Join Campaign", key=f"join_{campaign['name']}"):
                    st.success(f"✅ Joined {campaign['name']}! Coordinator will contact you.")

with tabs[1]:
    st.subheader("🚀 Start New Campaign")
    
    st.markdown("""
    **How to start a justice campaign**:
    1. **Define the issue** (living wage, housing, refugee rights, etc.)
    2. **Create WhatsApp/Signal group** for coordination
    3. **Recruit parishes** (start with nearby, then diocese)
    4. **Set goals & timeline**
    5. **Track impact** (workers helped, wages increased, policies changed)
    
    **No platform required** — use existing tools (WhatsApp, email, phone calls).
    """)
    
    with st.form("new_campaign"):
        campaign_name = st.text_input("Campaign Name", placeholder="e.g., Housing Justice - Nairobi")
        campaign_issue = st.selectbox(
            "Justice Issue",
            ["Living Wage", "Housing Justice", "Refugee Rights", "Environmental Justice", 
             "Healthcare Access", "Education Equity", "Prison Reform", "Other"]
        )
        campaign_goal = st.text_area("Campaign Goal", placeholder="What do you want to achieve?")
        campaign_contact = st.text_input("Coordinator Contact", placeholder="Your WhatsApp number")
        
        submitted = st.form_submit_button("🚀 Launch Campaign")
        
        if submitted:
            st.success(f"""
            ✅ **Campaign Created: {campaign_name}**
            
            **Next Steps**:
            1. Create WhatsApp group for coordination
            2. Invite nearby parishes to join
            3. Contact your diocese justice office
            4. Set first planning meeting
            
            **Coordinator**: {campaign_contact}
            """)

with tabs[2]:
    st.subheader("📊 Impact Tracking")
    
    st.markdown("""
    **Track and share impact voluntarily**:
    - Workers helped / wages increased
    - Policies changed / laws passed
    - Funds raised / services provided
    - Volunteers engaged / hours contributed
    
    **Transparency builds trust** — share what you can, when you can.
    """)
    
    with st.form("report_impact"):
        st.write("**Report Campaign Impact**")
        
        campaign_select = st.selectbox(
            "Campaign",
            ["Living Wage - East Africa", "Refugee Rights & Integration"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            workers_helped = st.number_input("Workers Helped", min_value=0, value=0, step=10)
            wage_increase = st.number_input("Avg Wage Increase (%)", min_value=0.0, value=0.0, step=0.1)
        
        with col2:
            volunteers = st.number_input("Volunteers Engaged", min_value=0, value=0, step=1)
            funds_raised = st.number_input("Funds Raised (USD)", min_value=0, value=0, step=100)
        
        impact_notes = st.text_area("Impact Notes", placeholder="Describe the impact...")
        
        submitted = st.form_submit_button("📤 Submit Impact Report")
        
        if submitted:
            st.success(f"""
            ✅ **Impact Report Submitted**
            
            Thank you for sharing! This data helps:
            - Other parishes learn from your work
            - Diocese understand regional impact
            - Donors see effectiveness
            - Global Church celebrate wins
            """)

st.divider()

# ============================================================================
# DIOCESE COORDINATION (Optional)
# ============================================================================

st.header("⛪ Diocese Coordination")

st.markdown("""
**Diocese-Level Aggregation** (optional):
- Parishes can register with their diocese
- Diocese coordinates regionally
- Share resources, campaigns, data
- Still federated (diocese doesn't control parishes)

**This is subsidiarity**: Local authority, voluntary coordination upward.
""")

diocese_connected = st.checkbox("Connected to Diocese", value=False)

if diocese_connected:
    st.success("""
    ✅ **Connected to Archdiocese of Nairobi**
    
    **Benefits**:
    - Regional campaign coordination
    - Shared resource directory
    - Diocese-wide announcements
    - Bishop accountability tracking
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Diocese Parishes", "127")
    with col2:
        st.metric("Active Campaigns", "8")
    with col3:
        st.metric("Total Volunteers", "15,000+")
else:
    st.info("""
    **Not connected to diocese?**
    
    You can still:
    - Connect with nearby parishes
    - Join justice campaigns
    - Share resources peer-to-peer
    
    Diocese connection is **optional**, not required.
    """)

st.divider()

# ============================================================================
# GLOBAL DIRECTORY
# ============================================================================

st.header("🌍 Global Catholic Directory")

st.markdown("""
**Find Catholic parishes anywhere**:
- 100,000+ parishes globally (goal)
- Crowdsourced + GCatholic.org integration
- Search by location, language, accessibility
- No central ownership required
""")

col1, col2 = st.columns(2)

with col1:
    search_country = st.text_input("Search Country", placeholder="Kenya, Uganda, Bhutan...")
    search_city = st.text_input("Search City", placeholder="Nairobi, Kampala, Thimphu...")

with col2:
    search_language = st.selectbox(
        "Mass Language",
        ["Any", "English", "Swahili", "Luganda", "Spanish", "French", "Latin", "Tagalog"]
    )
    
    if st.button("🔍 Search Global Directory", type="primary"):
        st.success("🔗 Redirecting to **Find a Church** page...")
        st.caption("(Page 13 in sidebar)")

# Quick stats
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Global Parishes", "100,000+", help="Goal for production")
with col2:
    st.metric("Countries", "200+")
with col3:
    st.metric("Languages", "50+")
with col4:
    st.metric("Catholics Served", "1.3B")

# Footer
st.divider()
st.caption("""
**🏗️ Architecture**: Federated, not centralized • **🗂️ Data**: Parishes own their data • 
**🔓 Open Source**: CC BY-NC-ND 4.0 • **⛪ Philosophy**: Subsidiarity principle
""")
