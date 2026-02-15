# ✝️ Catholic Spiritual OS

**A federated, mobile-first platform for the global Catholic Church**

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://catholicparishsteward.streamlit.app/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Live Demo**: https://catholicparishsteward.streamlit.app/

---

## 🌍 **What Is This?**

Catholic Spiritual OS is the first **Africa-designed, mobile-first, federated** platform serving the global Catholic Church.

**Unlike commercial parish software** (ParishStaq, OSV) designed for wealthy US parishes:
- ✅ **Works everywhere**: Westlands expat (4G) to Namugongo rural (2G)
- ✅ **Multi-modal access**: Web + Voice + SMS (even feature phones)
- ✅ **Federated architecture**: No central authority, parishes own their data
- ✅ **Offline-first**: Works without internet
- ✅ **Affordable**: $0-200/month vs $500-2000/month
- ✅ **Open source**: Trust + transparency

---

## 🚀 **Key Features (v0.3.0)**

### **For Individuals** (Personal Formation)
- **📖 Daily Mass Readings**: Full Gospel text with multi-source API (never fails)
- **🙏 Complete Prayer Library**: Our Father, Hail Mary, Rosary (EN/SW/LG)
- **📅 Liturgical Calendar**: Today's season, feast, saint of the day
- **🔊 Voice Interface**: Text-to-speech, audio prayers (oral culture support)
- **📱 Mobile-Optimized**: Touch-friendly, works on basic smartphones

### **For Parishes** (Community Coordination)
- **👥 Small Christian Communities (SCCs)**: 45,000+ communities in Kenya
- **👨‍🏫 Catechist Certification**: Track formation progress
- **💰 Stewardship & Giving**: Transparent financial tracking
- **📊 Admin Dashboard**: Member management, sacramental records
- **📥 Data Import/Export**: Free unlimited exports (no vendor lock-in)

### **For Global Church** (Universal Coordination)
- **🌍 Find a Catholic Church**: 200+ countries (Bhutan to Brazil)
- **🌐 Federated Parish Identity**: GeoHash + Phone (no fake Parish IDs)
- **🤝 Peer-to-Peer Coordination**: Direct parish networking
- **📲 SMS Bridge**: Feature phone access ($0.01/day, zero data)
- **🗣️ Multi-Language**: English, Swahili, Luganda, French, Spanish

### **For Context Sensitivity** (Everyone, Everywhere)
- **📡 Connection Detection**: Adapts to 4G/3G/2G/Offline
- **📱 Device Detection**: Smartphone to feature phone
- **🎯 Context-Aware UI**: Rich/poor, urban/rural, literate/oral
- **💾 Offline Cache**: Always works, even without internet

---

## 🎯 **Who Is This For?**

| User Type | Use Case | How It Helps |
|-----------|----------|--------------|
| **Westlands Expat (4G, iPhone)** | Needs Mass times when traveling | Full-featured app, find churches globally |
| **Namugongo Rural (2G, Nokia)** | Wants daily Gospel, can't afford data | SMS bridge ($0.01/day), audio prayers |
| **Low Literacy Elder** | Can't read well, wants to pray Rosary | Voice interface, audio-only mode |
| **Migrant Worker** | Filipino nurse in Saudi Arabia | Find Tagalog Mass, ethnic parish directory |
| **Parish Administrator** | Manages 500 families, tired of Excel | Import existing data, track sacraments |
| **Tourist in Bhutan** | Visiting Thimphu, needs Catholic Mass | Church finder → St. Mary's Church (7 parishes in Bhutan) |

---

## 📖 **Quick Start**

### **Try It Now** (No Installation)
Visit: https://catholicparishsteward.streamlit.app/

**Test These Features**:
1. **Page 12: Daily Prayers** → Complete Rosary in 3 languages
2. **Page 13: Find a Church** → Search "Bhutan" or "Namugongo"
3. **Page 09: Liturgy of the Day** → Today's Gospel with full text
4. **Page 01: Version Check** → Verify all features installed

### **Run Locally** (Developers)
```bash
# Clone repository
git clone https://github.com/gabrielmahia/catholic-network-tools.git
cd catholic-network-tools

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

**Requirements**:
- Python 3.11+
- Streamlit 1.28+
- Dependencies in `requirements.txt`

---

## 🏗️ **Architecture**

### **Five-Layer Nested System**

```
┌───────────────────────────────────────────────────────┐
│  E (RESILIENCE) — Crisis Response & Civic Action      │
│  ┌─────────────────────────────────────────────────┐  │
│  │  C (GLOBAL) — Federated Church Network          │  │
│  │  ┌───────────────────────────────────────────┐  │  │
│  │  │  B (DIOCESE) — Multi-Parish Governance    │  │  │
│  │  │  ┌─────────────────────────────────────┐  │  │  │
│  │  │  │  A (PARISH) — Community Coord       │  │  │  │
│  │  │  │  ┌───────────────────────────────┐  │  │  │  │
│  │  │  │  │  D (PERSONAL) — Formation     │  │  │  │  │
│  │  │  │  └───────────────────────────────┘  │  │  │  │
│  │  │  └─────────────────────────────────────┘  │  │  │
│  │  └───────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

**Follows Catholic Subsidiarity**: Decisions at lowest competent level  
**Federated, Not Centralized**: Parishes coordinate peer-to-peer

See: [WORLD_CLASS_FEATURES_SUMMARY.md](WORLD_CLASS_FEATURES_SUMMARY.md) for detailed architecture.

---

## 💡 **What Makes This Different?**

### **vs ParishSOFT / OSV** ($500-2000/month):

| Feature | Commercial Software | Catholic Spiritual OS |
|---------|-------------------|----------------------|
| **Price** | $500-2000/mo | **$0-200/mo** |
| **Africa Support** | ❌ No | **✅ Built for** |
| **Mobile-First** | ⚠️ Desktop-adapted | **✅ Native** |
| **Offline Mode** | ❌ No | **✅ Full** |
| **SMS Access** | ❌ No | **✅ Feature phones** |
| **Voice Interface** | ❌ No | **✅ Oral culture** |
| **Data Export** | ⚠️ Restricted | **✅ Free unlimited** |
| **Open Source** | ❌ No | **✅ Yes** |
| **Global Church Finder** | ❌ US-only | **✅ 200+ countries** |
| **Spiritual Content** | ❌ No | **✅ Prayers + Readings** |

### **vs Hallow / Laudate** (Personal prayer apps):
- ✅ **Parish coordination** (not just personal)
- ✅ **Global church directory** (find Mass anywhere)
- ✅ **Context-aware** (rich/poor adaptation)
- ✅ **Multi-modal** (web + voice + SMS)
- ✅ **Open source** (no subscription lock-in)

---

## 🔧 **Technical Stack**

**Frontend**: Streamlit (Python web framework)  
**Backend**: Python 3.11+  
**Database**: SQLite (demo), PostgreSQL (production roadmap)  
**Deployment**: Streamlit Cloud (auto-deploy from GitHub)

**APIs**:
- **Multi-source Gospel API**: USCCB, Universalis, Catholic Readings, iBreviary, local cache
- **Voice Interface**: Web Speech API (browser-native)
- **SMS Bridge**: Africa's Talking (Kenya/Uganda/Tanzania), Twilio (global)
- **Federated Identity**: GeoHash + Phone + Diocese (no central authority)

**Key Technologies**:
- **Context Detection**: navigator.connection, User-Agent, geolocation
- **Offline Support**: Service worker + IndexedDB (PWA roadmap)
- **Multi-Language**: i18n framework, community translations

---

## 📊 **Roadmap**

### **✅ Phase 1: COMPLETE** (v0.3.0)
- Multi-source Gospel API (bulletproof reliability)
- Federated parish identity (no fake IDs)
- Context-aware UI (adapts to user environment)
- Global church directory (200+ countries)
- Complete prayer library (3 languages)
- Voice interface (browser-based)
- SMS bridge architecture
- Mobile-responsive design

### **🔄 Phase 2: IN PROGRESS** (v0.4.0 - Next 2 Weeks)
- SMS production deployment (Africa's Talking webhook)
- Audio content library (record prayers in 3 languages)
- Offline PWA (service worker + IndexedDB)
- M-Pesa integration (Kenya mobile money)
- WhatsApp bot (message-based access)

### **📋 Phase 3: PLANNED** (v0.5.0 - Month 2)
- Full Swahili UI (not just prayers)
- Luganda UI
- Real PostgreSQL database (replace demo data)
- Claude AI integration (translation, homily helper, insights)
- Enhanced church directory (100K+ parishes via GCatholic integration)

---

## 🤝 **Contributing**

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas needing help**:
- **Translations**: Swahili, Luganda, French, Spanish UI
- **Audio content**: Record prayers in African languages
- **Parish data**: Verify church directory information
- **Testing**: Real-world usage feedback
- **Documentation**: Tutorials, guides

**Contributor License Agreement**: See [CLA.md](CLA.md)

---

## 📜 **License**

**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0**

- ✅ **View/Use**: Free for individuals, parishes, dioceses
- ✅ **Educational**: Use in catechesis, formation
- ❌ **Commercial**: Cannot resell without permission
- ❌ **Derivatives**: Cannot create modified versions without permission

See [LICENSE](LICENSE) for full terms.

**Why this license?**
- Protects against commercial exploitation
- Ensures original vision maintained
- Allows free use by Church communities
- Prevents vendor lock-in by competitors

**Want commercial use?** Contact: contact@aikungfu.dev

---

## 🔒 **Security**

**Reporting vulnerabilities**:
- **DO NOT** open public issues
- Email: contact@aikungfu.dev
- See [SECURITY.md](SECURITY.md) for details

**Privacy Principles**:
- **Personal data**: Full user control (opt-in sharing)
- **Parish data**: Owned by parish (free unlimited export)
- **Federated**: No central authority owns data
- **Offline-first**: Works without cloud dependency

---

## 📞 **Support & Contact**

**Live Demo**: https://catholicparishsteward.streamlit.app/  
**Repository**: https://github.com/gabrielmahia/catholic-network-tools  
**Email**: contact@aikungfu.dev

**Community**:
- [GitHub Issues](https://github.com/gabrielmahia/catholic-network-tools/issues) - Bug reports, feature requests
- [GitHub Discussions](https://github.com/gabrielmahia/catholic-network-tools/discussions) - Q&A, ideas
- Email - General inquiries, partnerships

---

## 📚 **Documentation**

**Essential Reading**:
- [WORLD_CLASS_FEATURES_SUMMARY.md](WORLD_CLASS_FEATURES_SUMMARY.md) - Complete feature documentation (comprehensive)
- [Docs/architecture/SYSTEM_OVERVIEW.md](Docs/architecture/SYSTEM_OVERVIEW.md) - Technical architecture
- [CHANGELOG.md](CHANGELOG.md) - Version history

**Governance**:
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [CLA.md](CLA.md) - Contributor agreement
- [SECURITY.md](SECURITY.md) - Security policy

**Archive**:
- [archive/](archive/) - Historical process documentation

---

## 🙏 **Acknowledgments**

**Built with**:
- **Streamlit** - Python web framework
- **Africa's Talking** - SMS infrastructure
- **USCCB / Universalis** - Liturgical data
- **GCatholic.org** - Global parish directory (future integration)
- **OpenResilience** - Federated architecture inspiration

**Special Thanks**:
- Catholic parishes in Kenya testing early versions
- Contributors providing translations
- Claude (Anthropic) for development assistance

---

## ✝️ **Mission**

> **"Ad maiorem Dei gloriam"** (For the greater glory of God)

**Our Vision**: A Catholic Church operating system that:
- Serves the **global majority** (not just wealthy parishes)
- Works for **everyone** (rich/poor, urban/rural, smartphone/feature phone)
- Respects **subsidiarity** (federated, not centralized)
- Maintains **data freedom** (parishes own their data)
- Enables **spiritual growth** (not just administration)
- Scales **globally** (200+ countries, 1.3B Catholics)

**This is the Church OS we deserve — built for the Church of the future: young, African, mobile-first, justice-oriented, and global.**

---

**Made with ❤️ for the global Catholic Church**

**Current Version**: v0.3.0 (February 2026)
