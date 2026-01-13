# 🏗️ System Architecture & Design

**Document Version**: 1.0  
**Last Updated**: January 13, 2026  
**Target Audience**: Developers & Architects

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Frontend Architecture](#frontend-architecture)
5. [Backend Architecture](#backend-architecture)
6. [Integration Points](#integration-points)
7. [Deployment Architecture](#deployment-architecture)
8. [Scalability & Performance](#scalability--performance)

---

## System Overview

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER LAYER                               │
│  (Browser - Desktop, Tablet, Mobile - All Major Browsers)       │
└────────────────┬────────────────────────────────┬────────────────┘
                 │                                 │
         ┌───────▼──────────┐           ┌────────▼────────┐
         │   FRONTEND       │           │   STANDALONE    │
         │   SERVER         │           │   TAROT READER  │
         │                  │           │                 │
         │  - HTML/CSS/JS   │           │  - Client-side  │
         │  - Static files  │           │  - 78-card deck │
         │  - Index         │           │  - Spread logic │
         │  - Courses       │           │  - Animations   │
         │  - Community     │           │  - No backend   │
         │  - Checkout      │           │  - Portable     │
         └────────┬─────────┘           └────────┬────────┘
                  │                               │
                  └───────────┬───────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  OPTIONAL: API     │
                    │  INTEGRATION       │
                    │                    │
                    │ - Web2 Gateway     │
                    │ - Analytics        │
                    │ - Auth Services    │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼─────┐        ┌────▼──────┐     ┌────▼──────┐
    │  ICP       │        │ External  │     │ Analytics │
    │  Canister  │        │ Services  │     │ Service   │
    │            │        │           │     │           │
    │ - Tarot    │        │ - Payment │     │ - GA4     │
    │ - Ledger   │        │ - Auth    │     │ - Events  │
    │ - Assets   │        │ - Email   │     │           │
    └────────────┘        └───────────┘     └───────────┘
```

---

## Component Architecture

### Frontend Components

```
FRONTEND/
├── index.html
│   ├── Navigation Header
│   ├── Hero Section
│   ├── Courses Overview
│   ├── Call-to-Action
│   └── Footer
│
├── pages/modulo-1.html (Course 1)
│   ├── Course Header
│   ├── Module Content
│   ├── Lesson Sections
│   ├── Progress Tracker
│   └── Enroll Button
│
├── pages/modulo-2.html (Course 2)
│   └── [Same structure as Module 1]
│
├── pages/modulo-3.html (Course 3)
│   └── [Same structure as Module 1]
│
├── pages/circulo.html (Community)
│   ├── Community Header
│   ├── Member Portal
│   ├── Discussion Threads
│   ├── Shared Readings
│   └── Member Directory
│
├── pages/checkout.html (Payment)
│   ├── Order Summary
│   ├── Bundle Selection
│   ├── Form Validation
│   ├── Payment Integration
│   └── Confirmation
│
└── tarot-reader.html (Standalone)
    ├── Deck Display
    ├── Spread Selection
    ├── Card Drawing Logic
    ├── Interpretation Display
    ├── History/Favorites
    └── Export/Share
```

### Shared Frontend Systems

```
FRONTEND SYSTEMS
│
├── Styling (CSS)
│   ├── Global Styles
│   ├── Color Schemes
│   │   ├── Light Mode (#f5f5f0 bg, #2c2c2c text)
│   │   └── Dark Mode (inverted)
│   ├── Responsive Breakpoints
│   │   ├── Mobile: < 768px
│   │   ├── Tablet: 768px - 1024px
│   │   └── Desktop: > 1024px
│   ├── Animations
│   │   ├── Card draws (600-1000ms)
│   │   ├── Fade transitions (300ms)
│   │   └── Smooth scrolls
│   └── Accessibility
│       ├── High contrast mode
│       ├── Focus indicators (2px gold outline)
│       └── Reduced motion support
│
├── JavaScript Modules
│   ├── DOM Manipulation
│   ├── Event Handling
│   ├── Form Validation
│   ├── Dark Mode Toggle
│   ├── Mobile Menu Handler
│   ├── Tarot Logic
│   │   ├── Deck generation
│   │   ├── Card shuffling
│   │   ├── Spread algorithms
│   │   └── Interpretation mapping
│   └── Analytics Tracking
│
└── Utilities
    ├── Helper Functions
    ├── Validation Rules
    ├── Format/Parse Utilities
    └── Storage Management
```

### Backend Components

```
BACKEND CANISTER STRUCTURE
│
├── main.mo (Entry Point)
│   ├── Canister State Management
│   ├── Message Handling
│   ├── Async Operations
│   └── HTTP Interface
│
├── Tarot Module
│   ├── data.mo
│   │   ├── Full 78-card deck data
│   │   ├── Card names (Major/Minor Arcana)
│   │   ├── Card descriptions
│   │   ├── Interpretations (upright/reversed)
│   │   └── Card imagery references
│   │
│   ├── lib.mo
│   │   ├── shuffle() - Deck shuffling algorithm
│   │   ├── draw(count) - Draw N cards
│   │   ├── spread(type) - Generate spreads
│   │   │   ├── 1-card (daily)
│   │   │   ├── 3-card (past/present/future)
│   │   │   └── 10-card (celtic cross)
│   │   ├── interpret(card) - Get interpretation
│   │   └── getReadingHistory() - Query readings
│   │
│   └── types.mo
│       ├── Card type definition
│       ├── Spread type definition
│       ├── Reading type definition
│       └── Result types
│
├── Ledger Module
│   ├── lib.mo
│   │   ├── recordTransaction()
│   │   ├── getBalance()
│   │   ├── transferFunds()
│   │   └── getHistory()
│   │
│   └── types.mo
│       ├── Transaction type
│       ├── Account type
│       └── Balance type
│
├── Assets Module
│   ├── lib.mo
│   │   ├── storeAsset()
│   │   ├── retrieveAsset()
│   │   ├── getAssetMetadata()
│   │   └── deleteAsset()
│   │
│   └── types.mo
│       ├── Asset type
│       └── Metadata type
│
├── Http Module
│   ├── lib.mo
│   │   ├── handleRequest()
│   │   ├── parseQuery()
│   │   ├── buildResponse()
│   │   └── errorHandling()
│   │
│   └── types.mo
│       ├── HttpRequest type
│       └── HttpResponse type
│
└── Configuration
    ├── dfx.json - Canister settings
    ├── canister_ids.json - Deployed addresses
    ├── vessel.dhall - Dependency versions
    └── .env - Environment variables
```

---

## Data Flow

### 1. **User Navigation Flow**

```
User Visit → index.html
              ├─ Check dark mode preference (localStorage)
              ├─ Load CSS (light/dark theme)
              ├─ Load JavaScript modules
              ├─ Initialize event listeners
              ├─ Render navigation
              └─ Render homepage content

User Click → Course Link
              ├─ Load modulo-X.html
              ├─ Check localStorage for enrollment status
              ├─ Display course content
              ├─ Enable/disable enrollment button
              └─ Track page view (GA4)
```

### 2. **Tarot Reading Flow**

```
User Open → tarot-reader.html
            ├─ Initialize 78-card deck (client-side)
            ├─ Display deck controls
            └─ Ready for interaction

User Select Spread → 3-Card
                     ├─ Execute shuffle algorithm
                     ├─ Animate card draw (600ms)
                     ├─ Display 3 cards with positions
                     ├─ Fetch interpretations (from embedded data)
                     ├─ Display meaning & guidance
                     ├─ Offer save/share options
                     └─ Update reading history (localStorage)
```

### 3. **Checkout Flow**

```
User Select → Course Bundle
              ├─ Display bundle details & pricing
              ├─ Validate form inputs
              ├─ Calculate total
              └─ Ready for payment

User Proceed → Payment
               ├─ Collect payment info
               ├─ Validate form (client-side)
               ├─ Send to payment gateway
               ├─ Await confirmation
               ├─ Record enrollment
               ├─ Send confirmation email
               └─ Redirect to course
```

### 4. **Backend Processing Flow**

```
Frontend Request → HTTP API (main.mo)
                   ├─ Parse request
                   ├─ Route to appropriate module
                   │  ├─ Tarot module
                   │  ├─ Ledger module
                   │  ├─ Assets module
                   │  └─ Http module
                   ├─ Process logic
                   ├─ Return response (JSON)
                   └─ Frontend handles response
```

---

## Frontend Architecture

### Layered Architecture

```
PRESENTATION LAYER
│ HTML - Structure & Content
│
APPLICATION LAYER
│ JavaScript - Business Logic
│ ├─ Validation
│ ├─ Calculations
│ ├─ Event Handling
│ └─ State Management (localStorage)
│
STYLING LAYER
│ CSS - Visual Design
│ ├─ Layout
│ ├─ Colors & Typography
│ ├─ Animations
│ └─ Responsive Design
│
DATA LAYER
│ Storage - Persistence
│ ├─ localStorage (client-side)
│ ├─ sessionStorage (temporary)
│ └─ Optional: Backend API
```

### Modular JavaScript Structure (Recommended)

```javascript
// modules/tarotReader.js
export class TarotReader {
  constructor(deckData) { ... }
  shuffle() { ... }
  drawCards(count) { ... }
  getSpread(type) { ... }
  interpret(card) { ... }
}

// modules/validation.js
export function validateEmail(email) { ... }
export function validateForm(formData) { ... }

// modules/darkMode.js
export class DarkModeToggle {
  constructor() { ... }
  toggle() { ... }
  detect() { ... }
  save() { ... }
}

// modules/mobileMenu.js
export class MobileMenu {
  constructor() { ... }
  open() { ... }
  close() { ... }
}

// modules/analytics.js
export function trackEvent(eventName, data) { ... }
export function trackPageView(page) { ... }
```

### CSS Architecture (BEM Methodology)

```css
/* Block: Card */
.card { }
.card__image { }
.card__title { }
.card__description { }
.card--flipped { }

/* Block: Button */
.button { }
.button__text { }
.button--primary { }
.button--secondary { }
.button:focus-visible { }

/* State: Dark Mode */
[data-theme="dark"] .card { }
[data-theme="dark"] .button { }
```

---

## Backend Architecture

### Motoko Canister Structure

```motoko
// main.mo
import Tarot from "./Tarot/lib";
import Ledger from "./Ledger/lib";
import Assets from "./Assets/lib";
import Http from "./Http/lib";

actor EscolaDoOraculo {
  // State
  private var readings : [Reading] = [];
  private var users : [User] = [];
  
  // Public update functions
  public func requestReading(spreadType : Text) : async Reading { }
  public func enrollCourse(courseId : Text, payment : Nat) : async Enrollment { }
  public func recordTransaction(tx : Transaction) : async Result { }
  
  // Public query functions
  public query func getReading(id : Text) : async ?Reading { }
  public query func getCourseContent(id : Text) : async Course { }
  public query func getUserHistory(userId : Text) : async [Reading] { }
  
  // HTTP handler
  public func http_request(req : Http.HttpRequest) : async Http.HttpResponse { }
}
```

### State Management

```
Canister State
├── Readings Database
│   ├── reading_id
│   ├── user_id
│   ├── timestamp
│   ├── spread_type
│   ├── cards_drawn
│   └── interpretation
│
├── Enrollments Database
│   ├── enrollment_id
│   ├── user_id
│   ├── course_id
│   ├── enrollment_date
│   └── completion_status
│
├── Ledger
│   ├── account_id
│   ├── balance
│   ├── transaction_history
│   └── last_updated
│
└── Assets Storage
    ├── asset_id
    ├── asset_data
    ├── metadata
    └── access_control
```

---

## Integration Points

### 1. **Payment Gateway Integration**
```
Frontend (checkout.html)
    ↓ (Payment details)
External Payment Service (Stripe/PayPal/etc)
    ↓ (Confirmation)
Webhook → Backend (main.mo)
    ↓ (Validate & record)
Ledger Module
    ↓ (Store transaction)
Response → Frontend
    ↓ (Confirmation & enrollment)
Course Access Granted
```

### 2. **Email Service Integration**
```
User Enrolls → Checkout Complete
    ↓
Backend Records Enrollment
    ↓
Trigger Email Service
    ↓
Send Confirmation Email
    ↓
Send Welcome Email with Course Link
```

### 3. **Analytics Integration (GA4)**
```
User Event → JavaScript Event Tracker
    ↓
Send to GA4
    ↓
Analytics Dashboard Updated
    ↓
Reports & Insights Available
```

### 4. **Authentication (Future)**
```
User Login → Authentication Service
    ↓
Verify Credentials
    ↓
Issue JWT/Session Token
    ↓
Frontend Stores Token
    ↓
Use Token for API Requests
```

---

## Deployment Architecture

### Frontend Deployment Options

```
GitHub → (GitHub Actions CI/CD)
  ↓
  ├─ Option 1: GitHub Pages (Static)
  ├─ Option 2: Vercel (Optimized)
  ├─ Option 3: Netlify (Optimized)
  ├─ Option 4: ICP Canister (Decentralized)
  └─ Option 5: Traditional Server (AWS/Azure/GCP)
```

### Backend Deployment

```
Local Development
    ↓ (dfx start)
Local Replica
    ↓ (dfx deploy)
IC Mainnet
    ↓
Canister ID: [Your Canister ID]
    ↓
HTTP Interface Available
    ↓
Permanent, Decentralized Storage
```

---

## Scalability & Performance

### Frontend Performance

| Metric          | Target     | Method                                  |
| --------------- | ---------- | --------------------------------------- |
| **Page Load**   | < 2s       | CSS optimization, image compression     |
| **Tarot Draw**  | 600-1000ms | Intentional animation delay             |
| **Interaction** | < 100ms    | Debounced events, efficient DOM queries |
| **Bundle Size** | < 200KB    | No external dependencies                |
| **Mobile**      | 320px - 4K | Responsive CSS, flexible layout         |

### Backend Scalability

| Aspect                  | Approach               | Benefit                   |
| ----------------------- | ---------------------- | ------------------------- |
| **State Growth**        | Stable Canister Memory | Persistent across updates |
| **Concurrent Requests** | ICP Message Queue      | Automatic load balancing  |
| **Data Retrieval**      | Indexed Queries        | Fast lookups              |
| **Cost Model**          | Cycles-based           | Predictable pricing       |

### Caching Strategy

```
Browser Cache (HTTP Headers)
├─ Static assets: 1 year
├─ HTML pages: 1 day
├─ API responses: 1 hour
└─ Dynamic content: No cache

Local Storage (Client-Side)
├─ Dark mode preference
├─ Reading history
├─ User preferences
└─ Session data

Backend Cache (Optional)
├─ Frequently accessed cards
├─ Course content
└─ User enrollment status
```

---

## Security Architecture

### Frontend Security

```
Input Validation
├─ Client-side validation (UX)
└─ Server-side validation (Security)

Content Security Policy (CSP)
├─ No inline scripts
├─ Only HTTPS resources
└─ X-Frame-Options headers

HTTPS/SSL
└─ All traffic encrypted
```

### Backend Security

```
Canister Isolation
├─ Separate state per canister
└─ No cross-canister vulnerabilities

Message Authentication
├─ IC certificates
└─ Caller verification

Data Encryption
├─ At-rest (canister state)
└─ In-transit (IC network)
```

---

## Future Architectural Enhancements

1. **Microservices**: Split backend into separate canisters
2. **Database**: Introduce stable structures for persistence
3. **Caching Layer**: Add Redis for performance
4. **CDN**: Global content delivery
5. **Message Queue**: Async job processing
6. **Monitoring**: Comprehensive logging & alerting

---

**Version**: 1.0  
**Last Updated**: January 13, 2026  
**Next Review**: March 15, 2026
