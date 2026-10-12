# DRP Platform — Digital Risk Protection
Digital Risk Protection Platform — Social &amp; App Monitoring. Detects fake social media profiles and impersonating mobile apps using multi-signal detection (fuzzy names, homoglyphs, logo pHash, publisher mismatch).  Built for HacXLerate 2026 Round 1 · Team BYTEBLAZE

---

## 🤝 AI Usage Disclosure

This project was built during HacXLerate 2026 (Round 1) by Team BYTEBLAZE.

**AI tools used:**
- **ChatGPT / Claude** — code scaffolding, boilerplate, debugging help, documentation
- **Groq (GPT-OSS 120B)** — LLM-powered threat summaries (a runtime feature, not dev-time)

**Human contributions:**
- Architecture design and system decisions
- Detection signal selection (homoglyph map, thresholds, weighting)
- Brand profile logic and false-positive exclusion strategy
- Testing, validation, and demo preparation
- All deployment and integration work

All AI-generated code was reviewed, tested, adapted, and understood by team members. Detection logic and product decisions were made by the team.

**Runtime AI (a product feature):**
The AI Threat Summary uses Groq's `openai/gpt-oss-120b` model to generate natural-language summaries of detected threats. This is a deliberate product feature — rules handle detection, AI handles explanation.
