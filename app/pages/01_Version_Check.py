"""
Version Check - Verify which version is deployed

This page displays the current version and features.
Use this to confirm deployment succeeded.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Version Check | Catholic Spiritual OS",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Version & Deployment Check")

st.markdown("""
This page helps verify which version of Catholic Spiritual OS is currently deployed.
""")

# Version info
st.header("📊 Current Version")

VERSION = "0.3.0"
BUILD_DATE = "2026-02-13"
COMMIT = "b030b30 (PR #5: World-class features)"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Version", VERSION)

with col2:
    st.metric("Build Date", BUILD_DATE)

with col3:
    st.metric("Commit", COMMIT[:8])

# Feature detection
st.header("✅ Feature Detection")

features = {}

# Check if new modules exist
try:
    from src.spiritual_os.mass_readings import MassReadingsAPI
    features['Mass Readings API'] = '✅ INSTALLED'
except ImportError:
    features['Mass Readings API'] = '❌ MISSING (v0.3.0 feature)'

try:
    from src.spiritual_os.prayers import PrayerLibrary
    features['Prayer Library'] = '✅ INSTALLED'
except ImportError:
    features['Prayer Library'] = '❌ MISSING (v0.3.0 feature)'

try:
    from src.spiritual_os.church_directory import ChurchDirectory
    features['Church Directory'] = '✅ INSTALLED'
except ImportError:
    features['Church Directory'] = '❌ MISSING (v0.3.0 feature)'

try:
    from src.spiritual_os.utils.data_io import DataImporter
    features['Data Import/Export'] = '✅ INSTALLED'
except ImportError:
    features['Data Import/Export'] = '❌ MISSING (v0.3.0 feature)'

try:
    from src.spiritual_os.ui.mobile_css import inject_mobile_css
    features['Mobile CSS'] = '✅ INSTALLED'
except ImportError:
    features['Mobile CSS'] = '❌ MISSING (v0.3.0 feature)'

# Display results
for feature, status in features.items():
    if '✅' in status:
        st.success(f"{feature}: {status}")
    else:
        st.error(f"{feature}: {status}")

# Check new pages exist
st.header("📄 Page Detection")

pages_dir = Path(__file__).parent
expected_pages = {
    '12_Daily_Prayers.py': 'v0.3.0 - Complete prayer library',
    '13_Find_a_Church.py': 'v0.3.0 - Global church directory',
}

for page_file, description in expected_pages.items():
    page_path = pages_dir / page_file
    if page_path.exists():
        st.success(f"✅ {page_file}: {description}")
    else:
        st.error(f"❌ {page_file} NOT FOUND - Deployment incomplete!")

# System info
st.header("🖥️ System Information")

import platform
import sys

st.code(f"""
Python Version: {sys.version.split()[0]}
Platform: {platform.platform()}
Architecture: {platform.machine()}
Deployment Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
""")

# Diagnosis
st.header("🔧 Deployment Status")

all_features = all('✅' in status for status in features.values())
all_pages = all((pages_dir / page).exists() for page in expected_pages.keys())

if all_features and all_pages:
    st.success("""
    ✅ **DEPLOYMENT SUCCESSFUL!**
    
    All v0.3.0 features are installed and working.
    
    New features available:
    - Page 12: Daily Prayers (complete Catholic prayer library)
    - Page 13: Find a Church (global directory)
    - Page 09: Enhanced with Mass readings
    - Admin: Data import/export
    - Mobile-responsive CSS
    """)
else:
    st.error("""
    ❌ **DEPLOYMENT INCOMPLETE!**
    
    Some v0.3.0 features are missing. This means:
    - Streamlit Cloud didn't deploy latest code
    - You're looking at old version (pre-PR #5)
    - Need to trigger manual redeploy
    
    **Action**: Go to Streamlit dashboard and click "Reboot app"
    """)

st.divider()

# Help section
with st.expander("🆘 Troubleshooting Guide"):
    st.markdown("""
    ### If Features Are Missing:
    
    1. **Check GitHub**: https://github.com/gabrielmahia/catholic-network-tools/commits/main
       - Top commit should be "trigger: force Streamlit Cloud redeploy"
       - If not, code isn't merged
    
    2. **Check Streamlit Dashboard**: https://share.streamlit.io/
       - Sign in
       - Find your app
       - Click "Reboot app"
       - Wait 2-3 minutes
    
    3. **Hard Refresh Browser**:
       - Windows/Linux: Ctrl + Shift + R
       - Mac: Cmd + Shift + R
       - Or try incognito window
    
    4. **Check Build Logs**:
       - Dashboard → Your app → Logs
       - Look for errors
       - Share with developer
    
    5. **Nuclear Option**:
       - Delete app in Streamlit dashboard
       - Create new deployment
       - Connect to gabrielmahia/catholic-network-tools
       - Branch: main
       - Deploy fresh
    """)

st.markdown("---")
st.caption("Catholic Spiritual OS | Version Check Page | v0.3.0")
