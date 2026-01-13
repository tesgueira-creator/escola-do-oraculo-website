# 📁 Complete File Structure Reference

**Document Version**: 2.0  
**Last Updated**: January 13, 2026  
**Last Reorganized**: January 13, 2026

---

## Quick Navigation

- [Root Level Files](#root-level-files)
- [Frontend Structure](#frontend-structure)
- [Backend Structure](#backend-structure)
- [Documentation Structure](#documentation-structure)
- [Scripts & Utilities](#scripts--utilities)
- [File Descriptions](#file-descriptions)
- [Quick File Finder](#quick-file-finder)

---

## Root Level Files

```
escola-do-oraculo-website/
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── .venv/                         # Python virtual environment (optional)
│
├── README.md                      # Main project README
├── PROJECT_OVERVIEW.md            # Project context & overview
├── ARCHITECTURE.md                # System architecture document
├── FILE_STRUCTURE.md              # This file
├── TECHNICAL_STACK.md             # Technology documentation
│
├── frontend/                      # ✨ Web interface (7 pages + assets)
├── backend/                       # 🔗 Motoko/ICP backend (5 modules)
├── docs/                          # 📚 Project documentation (7 files)
└── scripts/                       # 🛠️ Build & setup scripts (1 file)
```

---

## Frontend Structure

```
frontend/
├── 📄 index.html                  # [1] Homepage - Main entry point
│                                  #    ├─ Navigation header
│                                  #    ├─ Hero section with CTA
│                                  #    ├─ 3-course cards overview
│                                  #    ├─ Community portal preview
│                                  #    ├─ Featured readings
│                                  #    └─ Footer
│
├── 📄 tarot-reader.html           # [2] Standalone tarot reader
│                                  #    ├─ 78-card deck
│                                  #    ├─ Spread selection
│                                  #    ├─ Card drawing interface
│                                  #    ├─ Interpretation display
│                                  #    ├─ Reading history
│                                  #    └─ Export/share options
│
├── 📄 test-forms.html             # [3] Testing & demonstration page
│                                  #    ├─ Form validation demo
│                                  #    ├─ Error message testing
│                                  #    ├─ Component showcase
│                                  #    └─ Accessibility testing
│
├── pages/                         # Course & feature pages
│   ├── 📄 modulo-1.html          # [4] Module 1: A Base do Oráculo
│   │                              #    ├─ Foundation course content
│   │                              #    ├─ Lesson sections (5-7)
│   │                              #    ├─ Learning objectives
│   │                              #    ├─ Exercises
│   │                              #    ├─ Module 1 image banner
│   │                              #    └─ Enroll button
│   │
│   ├── 📄 modulo-2.html          # [5] Module 2: O Método Kally
│   │                              #    ├─ Methodology course content
│   │                              #    ├─ Lesson sections (5-7)
│   │                              #    ├─ Technique demonstrations
│   │                              #    ├─ Practical exercises
│   │                              #    ├─ Module 2 image banner
│   │                              #    └─ Enroll button
│   │
│   ├── 📄 modulo-3.html          # [6] Module 3: Profissionalização
│   │                              #    ├─ Professionalization content
│   │                              #    ├─ Advanced topics (5-7)
│   │                              #    ├─ Business guidance
│   │                              #    ├─ Portfolio building
│   │                              #    ├─ Module 3 image banner
│   │                              #    └─ Enroll button
│   │
│   ├── 📄 circulo.html           # [7] Círculo do Oráculo (Community)
│   │                              #    ├─ Community portal intro
│   │                              #    ├─ Member login
│   │                              #    ├─ Discussion forums
│   │                              #    ├─ Shared readings feed
│   │                              #    ├─ Member profiles
│   │                              #    └─ Events calendar
│   │
│   └── 📄 checkout.html          # [8] Checkout/Enrollment
│                                  #    ├─ Bundle selection
│                                  #    ├─ Order summary
│                                  #    ├─ Form validation
│                                  #    ├─ Payment integration points
│                                  #    ├─ Billing information
│                                  #    └─ Confirmation handling
│
├── css/                           # Stylesheets folder (for organization)
│                                  # ℹ️ Currently embedded in HTML files
│                                  # 🎨 Recommended: Extract to style.css
│
├── js/                            # JavaScript modules folder (for organization)
│                                  # ℹ️ Currently embedded in HTML files
│                                  # 💻 Recommended: Extract to modules:
│                                  #    ├─ tarotReader.js
│                                  #    ├─ validation.js
│                                  #    ├─ darkMode.js
│                                  #    ├─ mobileMenu.js
│                                  #    └─ analytics.js
│
├── assets/                        # Static assets
│   ├── images/                    # Course & content images
│   │   ├── 📷 modulo-1.png       # Module 1 banner image
│   │   ├── 📷 modulo-2.png       # Module 2 banner image
│   │   └── 📷 modulo-3.png       # Module 3 banner image
│   │
│   └── icons/                     # Favicon & icon files
│       ├── 🔗 favicon.ico        # Browser tab icon (.ico format)
│       └── 🔗 favicon.svg        # Browser tab icon (.svg format)
│
└── README.md                      # Frontend documentation
                                   # ℹ️ Explains frontend architecture
                                   # 📖 Development guidelines
                                   # 🚀 How to run locally

```

### Frontend Statistics

| Item                            | Count  | Status           |
| ------------------------------- | ------ | ---------------- |
| **HTML Pages**                  | 8      | ✅ All functional |
| **Images**                      | 3 PNG  | ✅ Optimized      |
| **Icons**                       | 2      | ✅ Both formats   |
| **Lines of Code (HTML/CSS/JS)** | ~3,500 | ✅ Optimized      |
| **External Dependencies**       | 0      | ✅ Pure vanilla   |

---

## Backend Structure

```
backend/                           # ICP/Motoko smart contracts
├── 📄 dfx.json                   # DFX configuration file
│                                  # ├─ Canister definitions
│                                  # ├─ Network settings
│                                  # ├─ Build configurations
│                                  # └─ Local replica settings
│
├── 📄 canister_ids.json          # Deployed canister identifiers
│                                  # ├─ Local canister IDs
│                                  # ├─ Production canister IDs
│                                  # └─ IC mainnet addresses
│
├── 📄 vessel.dhall               # Motoko dependency file
│                                  # ├─ Package management
│                                  # ├─ Version specifications
│                                  # └─ Dependency resolution
│
├── 📄 README.md                  # Backend documentation
│                                  # ├─ Setup instructions
│                                  # ├─ API documentation
│                                  # ├─ Testing guide
│                                  # └─ Deployment guide
│
├── src/                           # Source code
│   ├── 📄 main.mo                # [1] Main canister entry point
│   │                              #    ├─ Actor definition
│   │                              #    ├─ State management
│   │                              #    ├─ Message handlers
│   │                              #    ├─ Update functions
│   │                              #    ├─ Query functions
│   │                              #    └─ HTTP interface
│   │
│   ├── Tarot/                     # [2] Tarot module (card logic)
│   │   ├── 📄 lib.mo             # Tarot algorithms
│   │   │                          # ├─ shuffle()
│   │   │                          # ├─ drawCards(n)
│   │   │                          # ├─ getSpread(type)
│   │   │                          # ├─ interpret(card)
│   │   │                          # └─ getReadingHistory()
│   │   │
│   │   ├── 📄 data.mo            # 78-card deck data
│   │   │                          # ├─ Card definitions (78)
│   │   │                          # ├─ Card names
│   │   │                          # ├─ Descriptions
│   │   │                          # ├─ Interpretations
│   │   │                          # │  ├─ Upright meaning
│   │   │                          # │  ├─ Reversed meaning
│   │   │                          # │  └─ Guidance
│   │   │                          # └─ Imagery references
│   │   │
│   │   └── 📄 types.mo           # Type definitions
│   │                              # ├─ Card type
│   │                              # ├─ Spread type
│   │                              # ├─ Reading type
│   │                              # ├─ Interpretation type
│   │                              # └─ Result types
│   │
│   ├── Ledger/                    # [3] Ledger module (transactions)
│   │   ├── 📄 lib.mo             # Ledger functions
│   │   │                          # ├─ recordTransaction()
│   │   │                          # ├─ getBalance()
│   │   │                          # ├─ transferFunds()
│   │   │                          # ├─ getHistory()
│   │   │                          # └─ validateTransaction()
│   │   │
│   │   └── 📄 types.mo           # Ledger types
│   │                              # ├─ Transaction type
│   │                              # ├─ Account type
│   │                              # └─ Balance type
│   │
│   ├── Assets/                    # [4] Assets module (storage)
│   │   ├── 📄 lib.mo             # Asset management
│   │   │                          # ├─ storeAsset()
│   │   │                          # ├─ retrieveAsset()
│   │   │                          # ├─ getAssetMetadata()
│   │   │                          # ├─ deleteAsset()
│   │   │                          # └─ listAssets()
│   │   │
│   │   └── 📄 types.mo           # Asset types
│   │                              # ├─ Asset type
│   │                              # └─ Metadata type
│   │
│   ├── Http/                      # [5] HTTP module (Web2 gateway)
│   │   ├── 📄 lib.mo             # HTTP handling
│   │   │                          # ├─ handleRequest()
│   │   │                          # ├─ parseQuery()
│   │   │                          # ├─ buildResponse()
│   │   │                          # ├─ errorHandling()
│   │   │                          # └─ corsHeaders()
│   │   │
│   │   └── 📄 types.mo           # HTTP types
│   │                              # ├─ HttpRequest type
│   │                              # └─ HttpResponse type
│   │
│   └── .gitkeep                   # (Git folder marker)
│
├── art/                           # Design & graphics assets
│                                  # ├─ Logo files
│                                  # ├─ Brand assets
│                                  # ├─ UI mockups
│                                  # └─ Card artwork references
│
└── .gitkeep                       # (Git folder marker)

```

### Backend Statistics

| Item                 | Count | Status          |
| -------------------- | ----- | --------------- |
| **Motoko Files**     | 13    | ✅ Functional    |
| **Modules**          | 5     | ✅ Organized     |
| **Card Definitions** | 78    | ✅ Complete      |
| **Type Definitions** | 12+   | ✅ Comprehensive |
| **HTTP Endpoints**   | 4+    | ✅ RESTful       |

---

## Documentation Structure

```
docs/                              # Project documentation
├── 📄 ACCESSIBILITY_AUDIT.md     # [1] WCAG 2.1 Compliance Report
│                                  # ├─ Audit summary
│                                  # ├─ Detailed findings
│                                  # ├─ Compliance checklist
│                                  # ├─ Color contrast analysis
│                                  # ├─ Keyboard navigation tests
│                                  # ├─ Screen reader compatibility
│                                  # └─ Recommendations
│
├── 📄 IMPROVEMENTS.md            # [2] Enhancement Roadmap
│                                  # ├─ Planned features
│                                  # ├─ Bug fixes
│                                  # ├─ Performance optimizations
│                                  # ├─ Priority levels
│                                  # ├─ Resource estimates
│                                  # └─ Dependencies
│
├── 📄 IMPROVEMENTS_SUMMARY.md    # [3] Completed Improvements
│                                  # ├─ 12 improvements tracked
│                                  # ├─ 8 completed (67%)
│                                  # ├─ Implementation details
│                                  # ├─ Before/after comparisons
│                                  # ├─ Impact assessment
│                                  # └─ Testing results
│
├── 📄 IMPROVEMENTS_SHOWCASE.md   # [4] Feature Showcase
│                                  # ├─ Visual demonstrations
│                                  # ├─ Code examples
│                                  # ├─ Screenshots
│                                  # ├─ User testimonials
│                                  # └─ Performance metrics
│
├── 📄 EXECUTION_REPORT.md        # [5] Project Execution Details
│                                  # ├─ Timeline
│                                  # ├─ Milestones achieved
│                                  # ├─ Team contributions
│                                  # ├─ Budget tracking
│                                  # ├─ Risk management
│                                  # └─ Lessons learned
│
├── 📄 SETUP_GOOGLE_ANALYTICS_AND_WHATSAPP.md  # [6] Integration Guide
│                                  # ├─ GA4 setup steps
│                                  # ├─ WhatsApp integration
│                                  # ├─ API keys management
│                                  # ├─ Event tracking
│                                  # └─ Troubleshooting
│
├── 📄 SPIRITUAL_ENHANCEMENTS.md  # [7] Spiritual Features
│                                  # ├─ Spiritual philosophy
│                                  # ├─ Card meanings depth
│                                  # ├─ Interpretation guidance
│                                  # ├─ Ritual recommendations
│                                  # └─ Community practices
│
└── README.md                      # Documentation index
                                   # ├─ Document guide
                                   # ├─ Search index
                                   # └─ Quick links
```

### Documentation Statistics

| Document                               | Pages   | Words       | Purpose      |
| -------------------------------------- | ------- | ----------- | ------------ |
| ACCESSIBILITY_AUDIT.md                 | ~20     | 5,000+      | Compliance   |
| IMPROVEMENTS.md                        | ~15     | 4,000+      | Roadmap      |
| IMPROVEMENTS_SUMMARY.md                | ~12     | 3,500+      | Status       |
| IMPROVEMENTS_SHOWCASE.md               | ~10     | 3,000+      | Marketing    |
| EXECUTION_REPORT.md                    | ~15     | 4,000+      | Project mgmt |
| SETUP_GOOGLE_ANALYTICS_AND_WHATSAPP.md | ~8      | 2,500+      | Integration  |
| SPIRITUAL_ENHANCEMENTS.md              | ~12     | 3,500+      | Content      |
| **TOTAL**                              | **~92** | **~26,000** | **Complete** |

---

## Scripts & Utilities

```
scripts/                           # Build & setup scripts
└── 📄 setup-git.bat              # Git initialization script
                                   # ├─ Git configuration
                                   # ├─ Repository setup
                                   # ├─ Hook installation
                                   # ├─ Branch initialization
                                   # └─ Remote configuration
```

---

## File Descriptions

### Core HTML Files (frontend/)

| File                  | Lines | Purpose          | Key Sections                |
| --------------------- | ----- | ---------------- | --------------------------- |
| **index.html**        | ~300  | Homepage         | Hero, Courses, CTA, Footer  |
| **tarot-reader.html** | ~400  | Standalone tarot | Deck, Spreads, Readings     |
| **test-forms.html**   | ~250  | Testing          | Form components, validation |
| **modulo-1.html**     | ~350  | Course 1         | Lessons, exercises, content |
| **modulo-2.html**     | ~350  | Course 2         | Lessons, exercises, content |
| **modulo-3.html**     | ~350  | Course 3         | Lessons, exercises, content |
| **circulo.html**      | ~300  | Community        | Portal, forums, profiles    |
| **checkout.html**     | ~280  | Enrollment       | Forms, payment, validation  |

### Backend Motoko Files (backend/src/)

| File                | Lines | Purpose       | Exports                     |
| ------------------- | ----- | ------------- | --------------------------- |
| **main.mo**         | ~200  | Entry point   | Actor, message handlers     |
| **Tarot/lib.mo**    | ~150  | Tarot logic   | Functions (5)               |
| **Tarot/data.mo**   | ~800  | Card data     | 78 cards, full descriptions |
| **Tarot/types.mo**  | ~80   | Type defs     | Card, Spread, Reading types |
| **Ledger/lib.mo**   | ~120  | Ledger ops    | Transaction functions       |
| **Ledger/types.mo** | ~60   | Ledger types  | Account, Balance types      |
| **Assets/lib.mo**   | ~100  | Asset mgmt    | Storage functions           |
| **Assets/types.mo** | ~50   | Asset types   | Asset, Metadata types       |
| **Http/lib.mo**     | ~80   | HTTP handling | Request/response            |
| **Http/types.mo**   | ~40   | HTTP types    | Request, Response types     |

---

## Quick File Finder

### By Purpose

**🎓 Educational Content**
- `frontend/pages/modulo-1.html` - Foundation
- `frontend/pages/modulo-2.html` - Methodology
- `frontend/pages/modulo-3.html` - Professionalization

**🃏 Tarot Functionality**
- `frontend/tarot-reader.html` - Standalone reader
- `backend/src/Tarot/data.mo` - Card definitions
- `backend/src/Tarot/lib.mo` - Reading algorithms

**💰 Payments & Enrollment**
- `frontend/pages/checkout.html` - Enrollment interface
- `backend/src/Ledger/lib.mo` - Transaction processing

**👥 Community**
- `frontend/pages/circulo.html` - Community portal
- `backend/src/Http/lib.mo` - API endpoints

**🎨 Design & Assets**
- `frontend/assets/images/modulo-*.png` - Course images
- `frontend/assets/icons/favicon.*` - Favicon files
- `backend/art/` - Design assets

**📚 Documentation**
- `PROJECT_OVERVIEW.md` - High-level overview
- `ARCHITECTURE.md` - System design
- `FILE_STRUCTURE.md` - This file (file mapping)
- `docs/ACCESSIBILITY_AUDIT.md` - Compliance report
- `docs/IMPROVEMENTS.md` - Feature roadmap

### By Technology

**HTML5**
- `frontend/*.html` - All 8 pages

**CSS3**
- Embedded in HTML files (light/dark themes)
- Responsive, ~1500 lines total

**JavaScript (ES6+)**
- Embedded in HTML files
- Vanilla JS, no frameworks
- ~2000 lines total

**Motoko**
- `backend/src/**/*.mo` - 13 files
- ~2000 lines total

**Configuration**
- `backend/dfx.json`
- `backend/canister_ids.json`
- `backend/vessel.dhall`
- `.gitignore`

### By Audience

**End Users**
- `frontend/pages/modulo-*.html`
- `frontend/pages/circulo.html`
- `frontend/pages/checkout.html`
- `frontend/tarot-reader.html`

**Frontend Developers**
- `frontend/**/*.html`
- `PROJECT_OVERVIEW.md`
- `ARCHITECTURE.md`
- `FILE_STRUCTURE.md`

**Backend Developers**
- `backend/src/**/*.mo`
- `backend/dfx.json`
- `backend/README.md`

**Project Managers**
- `PROJECT_OVERVIEW.md`
- `docs/EXECUTION_REPORT.md`
- `docs/IMPROVEMENTS.md`
- `docs/IMPROVEMENTS_SUMMARY.md`

**QA/Accessibility**
- `docs/ACCESSIBILITY_AUDIT.md`
- `frontend/test-forms.html`
- `ARCHITECTURE.md`

---

## File Organization Recommendations

### Current Status
✅ **Well-organized** with:
- Clear separation of frontend/backend
- Organized documentation
- Logical module structure

### Suggested Future Improvements

**Frontend**
```
frontend/
├── css/
│   ├── base.css          # Global styles
│   ├── themes.css        # Light/dark mode
│   ├── responsive.css    # Media queries
│   ├── animations.css    # Transitions
│   └── accessibility.css # A11y styles
│
└── js/
    ├── tarotReader.js
    ├── validation.js
    ├── darkMode.js
    ├── mobileMenu.js
    ├── analytics.js
    └── main.js           # Init all modules
```

**Backend**
```
backend/
├── tests/               # Unit tests
├── scripts/             # Build scripts
└── docs/                # API docs
```

---

## File Size Reference

| Category            | Size   | Notes                                        |
| ------------------- | ------ | -------------------------------------------- |
| **Frontend HTML**   | ~2.5MB | All images included inline or referenced     |
| **Frontend CSS/JS** | ~500KB | Embedded in HTML (future extraction: ~200KB) |
| **Backend Motoko**  | ~150KB | Optimized, no external deps                  |
| **Documentation**   | ~2MB   | All markdown files                           |
| **Git History**     | ~50MB  | Repository commits                           |
| **Total Project**   | ~55MB  | Compressed                                   |

---

**Version**: 2.0  
**Last Updated**: January 13, 2026  
**Structure Reorganized**: January 13, 2026  
**Next Review**: February 15, 2026
