# Streamlit Apps

This folder contains separate Streamlit applications for the hackathon.

## 📁 Apps

### 1. **spiffit-hello/**
Simple "Hello World" app to test Databricks Apps deployment.

- **Purpose:** Test deployment workflow
- **Files:** `app.py`, `app.yaml`, `requirements.txt`
- **Deploy Path:** `streamlit/spiffit-hello/`

[See app README](spiffit-hello/README.md)

---

### 2. **spiffit-ai-calculator/**
AI-powered incentive calculator with natural language interface.

- **Purpose:** Main hackathon app (or starting point)
- **Files:** 
  - `app.py` - Main Streamlit app
  - `ai_helper.py` - AI/LLM integration
  - `query_parser.py` - Query parsing
  - `app.yaml`, `requirements.txt`
- **Deploy Path:** `streamlit/spiffit-ai-calculator/`

[See app README](spiffit-ai-calculator/README.md)

---

## 🚀 Quick Start

### Test Locally
```bash
# Hello World
cd streamlit/spiffit-hello
pip install -r requirements.txt
streamlit run app.py --server.port 8000

# AI Calculator
cd streamlit/spiffit-ai-calculator
pip install -r requirements.txt
streamlit run app.py --server.port 8000
```

### Deploy to Databricks

1. **Push to Git:**
```bash
git add streamlit/
git commit -m "Add Streamlit apps"
git push origin main
```

2. **In Databricks:**
- Go to **Apps**
- Click **Create App**
- **Source:** Your repo (`spiffit`)
- **Path:** Select `streamlit/spiffit-hello/` or `streamlit/spiffit-ai-calculator/`
- **Deploy!**

---

## 📚 Additional Resources

- **AI Integration Guide:** `../docs/ai_integration_guide.md` - Detailed steps for Hour 5-6
- **Genie Setup Guide:** `../docs/GENIE_SETUP.md`
- **Create Genie Spaces:** `../docs/CREATE_GENIE_SPACES_GUIDE.md`
- **Autonomous Agent Guide:** `../docs/AUTONOMOUS_SPIFF_AGENT.md`
- **SQL Setup:** `../sql/` - Mock data creation scripts
- **Calculator Code:** `../cursor/prototypes/02_incentive_calculator.py`
- **Implementation Plans:** `../cursor/automation-ideas/implementation-plans/`

---

## 🎯 Folder Structure

```
streamlit/
├── README.md (this file - app overview)
│
├── spiffit-hello/
│   ├── app.py
│   ├── app.yaml
│   ├── requirements.txt
│   └── README.md
│
└── spiffit-ai-calculator/
    ├── app.py
    ├── ai_helper.py
    ├── query_parser.py
    ├── spiff_agent.py
    ├── spiff_agent_app.py
    ├── app.yaml
    ├── requirements.txt
    └── README.md

📁 Documentation and SQL scripts are now at root level:
   ../docs/     - All guides and documentation
   ../sql/      - Mock data SQL scripts
```

---

**Ready to build! 🚀**

