# 🔍 TrustLens

### **Don't just trust it. Verify it.**

TrustLens is an AI-powered digital content verification agent designed to help users investigate online claims, screenshots, links, and videos using **AI analysis + live web search evidence**.

It helps users understand not only *what the evidence says*, but also **why a claim appears supported, contradicted, uncertain, or unsupported**.

---

## 🚨 Problem

False or misleading information can spread quickly through:

* 💬 WhatsApp forwards
* 📱 Social media posts
* 📰 News claims
* 💼 Job and financial offers
* 🛍️ Shopping-related claims
* 🎥 Viral videos
* 📸 Screenshots and edited posts

Simply searching the internet is often not enough. Users need a way to collect relevant information and understand how different sources relate to a claim.

---

## 💡 Solution

**TrustLens** combines an AI reasoning layer with live search data to create an explainable verification workflow.

Instead of returning only a simple **True / False** answer, TrustLens provides:

* 🟢 **Strongly Supported**
* 🔴 **Contradicted**
* 🟡 **Verification Needed**
* ⚪ **No Reliable Evidence Found**

It also explains:

* Why the result received that status
* What evidence was found
* Similar or related information
* Conflicting information
* Relevant sources

---

## ✨ Key Features

### 📝 Text Verification

Enter a factual claim and TrustLens extracts the main claim, generates relevant search queries, retrieves live information, and analyzes the evidence.

### 📷 Screenshot Analysis

Upload a screenshot and TrustLens identifies visible text, entities, dates, numbers, and the main factual claim for further verification.

### 🔗 Link Verification

Provide a URL and TrustLens analyzes the claim/context and retrieves relevant information from the web.

### 🎥 Video Analysis

Upload a video to analyze its visible content and identify observable signals that may indicate possible digital manipulation.

TrustLens does **not** automatically declare a video fake solely from visual appearance. It communicates uncertainty and limitations.

### 🔎 Live Evidence Retrieval

TrustLens uses live search data instead of relying only on static information.

### 🧩 Explainable Results

The goal is not just to provide a verdict, but to show **why** the result was reached.

---

## 🏗️ How It Works

```text
User Input
   │
   ├── Text
   ├── Screenshot
   ├── Link
   └── Video
        │
        ▼
   AI Content Understanding
        │
        ▼
   Claim Extraction
        │
        ▼
   Live Search via SerpApi
        │
        ├── Google Search
        ├── Google News
        └── YouTube Search
        │
        ▼
   Evidence Analysis
        │
        ▼
   Verification Status
        │
        ▼
   Explainable Report
        │
        ├── Why
        ├── Evidence
        ├── Similar Information
        ├── Conflicts
        └── Sources
```

---

## 🔍 SerpApi Integration

SerpApi is a **core part of TrustLens**, not a cosmetic integration.

TrustLens uses SerpApi to retrieve live search evidence relevant to the user's claim.

### SerpApi components used

| SerpApi Search    | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| 🔎 Google Search  | Retrieve relevant web pages and supporting information |
| 📰 Google News    | Find recent news coverage for news-related claims      |
| ▶️ YouTube Search | Find related video/context information                 |

The retrieved search results are then passed to the evidence-analysis layer to identify:

* Supporting information
* Contradictory information
* Similar information
* Missing or insufficient evidence

This allows TrustLens to use **current web information as an evidence layer** during verification.

---

## 🤖 AI Component

TrustLens uses the **Google Gemini API** for:

* Claim extraction
* Content understanding
* Screenshot analysis
* Evidence comparison
* Video analysis
* Explainable verification output

The AI layer works together with SerpApi:

```text
Gemini
   ↓
Understand the claim
   ↓
Generate search queries
   ↓
SerpApi
   ↓
Retrieve live evidence
   ↓
Gemini
   ↓
Compare and explain evidence
```

---

## 🛠️ Tech Stack

* 🐍 Python
* 🎈 Streamlit
* 🔍 SerpApi
* 🤖 Google Gemini API
* 🌐 GitHub
* ☁️ Streamlit Community Cloud

---

## 📁 Project Structure

```text
trustlens/
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
├── gemini_api.py
├── serpapi_api.py
├── verifier.py
├── media_analyzer.py
├── requirements.txt
└── README.md
```

> ⚠️ `secrets.toml` contains API credentials and should never be committed to a public repository.

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/SakshiPriya-a/trustlens.git
cd https://github.com/SakshiPriya-a/trustlens
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
SERPAPI_KEY = "your_serpapi_api_key"
```

⚠️ Never publish or commit your API keys.

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Security

API keys are stored using Streamlit secrets and are intentionally excluded from the public repository.

Do not expose:

* API keys
* Access tokens
* Passwords
* Private credentials

---

## ⚠️ Limitations

TrustLens is an evidence-assistance tool and should not be treated as an absolute authority.

In particular:

* Lack of search evidence does not automatically mean a claim is false.
* Multiple websites repeating the same information does not guarantee correctness.
* Video manipulation analysis is based on observable signals and may be inconclusive.
* Search results can change over time.
* Users should consult primary or official sources for high-stakes decisions.

---

## 🎯 Intended Use

TrustLens is designed for users who want to quickly investigate potentially misleading digital content and understand the evidence behind a claim.

Potential use cases include:

* News verification
* Viral social-media claims
* Government announcements
* Job-related claims
* Financial information
* Shopping claims
* Viral videos
* Online misinformation research

---

## 🚀 Future Improvements

Possible future improvements include:

* More specialized search sources
* Stronger source credibility analysis
* Improved media-forensics capabilities
* More detailed evidence mapping
* Additional search engines and verification signals
* Better multilingual claim verification

---

## 📌 Project Status

**Hackathon Prototype — SerpApi India Hackathon 2026**

Built as an AI-powered digital content verification agent using live search data from SerpApi.

---

### Made with ❤️ using AI + Search

**TrustLens — Don't just trust it. Verify it.**

