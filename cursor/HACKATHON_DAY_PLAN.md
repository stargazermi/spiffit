# 🚀 Hackathon Day Plan

## ⏰ Timeline (8-hour hackathon)

### Hour 1-2 (Setup & Decision) - 9:00 AM - 11:00 AM
- [ ] **Team huddle** - Review automation opportunities
- [ ] **Pick use case** - Recommend: AI-Powered Incentive Calculator
- [ ] **Assign roles**:
  - Data Engineer: Set up Delta Lake
  - ML Engineer: LLM integration
  - Full Stack: Build UI
  - Product: Demo script & presentation
- [ ] **Upload data** to Databricks workspace
- [ ] **Create Delta tables**

### Hour 3-4 (Core Development) - 11:00 AM - 1:00 PM
- [ ] **Build calculation engine** (Python functions)
- [ ] **Test calculations** with sample data
- [ ] **Implement 3-5 key formulas**:
  - MRR incentive calculation
  - Renewal incentive calculation
  - TCV incentive calculation
  - Total incentive aggregation
  - Attainment tier logic

**Lunch Break** - 1:00 PM - 1:30 PM

### Hour 5-6 (AI Integration) - 1:30 PM - 3:30 PM
- [ ] **Set up Genie** for natural language processing
- [ ] **Connect LLM** (Gemini 2.5 or Claude Sonnet)
- [ ] **Build intent extraction** (question understanding)
- [ ] **Test queries**:
  - "What's my incentive?"
  - "Show top performers"
  - "What if I close $50K more?"
- [ ] **Add explanations** (natural language responses)

### Hour 7 (UI & Polish) - 3:30 PM - 4:30 PM
- [ ] **Build Streamlit/Databricks App**
- [ ] **Create chat interface**
- [ ] **Add visualizations** (charts, metrics)
- [ ] **Test end-to-end flow**
- [ ] **Fix bugs**

### Hour 8 (Demo Prep) - 4:30 PM - 5:00 PM
- [ ] **Prepare demo script**
- [ ] **Create "Excel vs AI" comparison**
- [ ] **Calculate ROI/time savings**
- [ ] **Practice pitch** (5 minutes max)
- [ ] **Prepare for Q&A**

---

## 🎯 MVP Requirements (Must-Haves)

1. ✅ **Data in Delta Lake**
   - At least 1 table loaded and queryable
   
2. ✅ **Working Calculations**
   - At least 3 incentive formulas implemented
   - Results match expected Excel outputs
   
3. ✅ **Natural Language Interface**
   - Can answer at least 5 types of questions
   - Uses Databricks AI (Genie/LLM)
   
4. ✅ **User Interface**
   - Simple chat or form interface
   - Displays results clearly
   
5. ✅ **Demo Ready**
   - 5-minute presentation prepared
   - "Before/After" comparison ready

---

## 🌟 Nice-to-Haves (If Time Permits)

- 📊 **Visualizations** - Charts showing attainment, top performers
- ⚠️ **Validation** - Anomaly detection on calculations
- 📈 **Predictions** - "What if" scenario modeling
- 📧 **Exports** - PDF reports, email integration
- 🔍 **Search** - Vector search for similar employees/deals
- 📱 **Mobile-friendly** - Responsive UI

---

## 🛠️ Tech Stack Decision Matrix

| Tool | Best For | Complexity | Impact |
|------|----------|-----------|--------|
| **Delta Lake** | Data storage & versioning | ⭐ Low | ⭐⭐⭐ High |
| **Genie** | Natural language queries | ⭐⭐ Medium | ⭐⭐⭐ High |
| **Gemini 2.5 / Claude** | Intent understanding | ⭐⭐ Medium | ⭐⭐⭐ High |
| **Python/Spark** | Calculations | ⭐ Low | ⭐⭐⭐ High |
| **Databricks Apps** | UI | ⭐⭐ Medium | ⭐⭐ Medium |
| **AI BI Dashboard** | Visualization | ⭐⭐ Medium | ⭐⭐ Medium |
| **ML Flow** | Model tracking | ⭐⭐⭐ High | ⭐ Low |
| **Vector Search** | Semantic search | ⭐⭐⭐ High | ⭐ Low |
| **LangChain** | Orchestration | ⭐⭐⭐ High | ⭐⭐ Medium |

**Recommended Minimum Stack:**
- Delta Lake ✅
- Python/Spark ✅  
- Genie or LLM ✅
- Databricks App/Streamlit ✅

---

## 📋 Role-Specific Checklists

### Data Engineer Tasks
- [ ] Upload Excel files to DBFS
- [ ] Create database schema
- [ ] Write data to Delta tables
- [ ] Clean/transform attainment percentages
- [ ] Set up table constraints
- [ ] Create sample queries
- [ ] Document data model

### ML/AI Engineer Tasks
- [ ] Set up Genie workspace
- [ ] Configure LLM endpoints
- [ ] Build intent classification
- [ ] Create prompt templates
- [ ] Test question understanding
- [ ] Implement response generation
- [ ] Add conversation memory

### Full Stack Developer Tasks
- [ ] Set up Databricks App environment
- [ ] Build chat interface
- [ ] Connect to backend APIs
- [ ] Add input validation
- [ ] Create result displays
- [ ] Add error handling
- [ ] Deploy app

### Product/Demo Lead Tasks
- [ ] Write demo script
- [ ] Prepare Excel comparison
- [ ] Calculate ROI metrics
- [ ] Create slide deck (if needed)
- [ ] Test user flows
- [ ] Prepare Q&A responses
- [ ] Time the presentation

---

## 🎤 Demo Script Template

### Opening (30 seconds)
> "Excel is where incentive data goes to die. Our sales ops team spends 40+ hours per month 
> manually calculating incentives in complex spreadsheets. Today, we're showing you how 
> Databricks AI can do it in seconds."

### The Problem (1 minute)
> **[Show Excel file on screen]**
> - Multiple sheets with hundreds of rows
> - Complex formulas scattered everywhere
> - Manual copy-paste for each person
> - Error-prone and time-consuming
> - No audit trail
> 
> **[Calculate one person's incentive manually - take your time]**
> "That took 3 minutes for ONE person. We have 200 people."

### The Solution (2 minutes)
> **[Switch to your Databricks App]**
> "Instead, watch this..."
> 
> **[Type in chat]:** "What's John Smith's total incentive this quarter?"
> 
> **[Show instant response with breakdown]**
> 
> **[Ask follow-up]:** "What if he closes $50K more in MRR?"
> 
> **[Show projection]**
> 
> "We just did in 30 seconds what takes 5-10 minutes in Excel."

### The Tech (1 minute)
> "Here's what's powering this:
> - **Delta Lake** for versioned, reliable data storage
> - **Databricks Genie** for natural language understanding
> - **Gemini 2.5 LLM** for intelligent responses
> - **Python/Spark** for lightning-fast calculations
> - **Databricks Apps** for the interface"

### The Impact (30 seconds)
> "**Time savings:** 40 hours/month → $10,000+ in labor costs
> **Error reduction:** 95% fewer calculation mistakes
> **Cost avoidance:** $50,000+ in potential mispayments
> **Scalability:** Works for 200 people or 200,000"

### Q&A (1 minute)
- "Does it handle complex formulas?" → Yes, unlimited complexity
- "Can it integrate with Salesforce?" → Absolutely, via Delta Lake
- "What about data security?" → Delta Lake + Databricks security
- "How long to production?" → 2-4 weeks with proper testing

---

## 🚨 Common Pitfalls to Avoid

1. **Scope Creep** 
   - ❌ Don't try to build everything
   - ✅ Pick 1 use case and nail it

2. **Over-Engineering**
   - ❌ Don't build complex ML models from scratch
   - ✅ Use Databricks hosted LLMs

3. **Poor Demo**
   - ❌ Don't show code or technical details
   - ✅ Show business value and user experience

4. **No "Before" Comparison**
   - ❌ Don't assume people know Excel is slow
   - ✅ Show side-by-side: Excel vs AI

5. **Ignoring Edge Cases**
   - ❌ Don't only test happy path
   - ✅ Show it handles errors gracefully

6. **Forgetting the Story**
   - ❌ Don't just show features
   - ✅ Tell a compelling narrative

---

## 💡 Last-Minute Ideas (If Stuck)

### Simplest Possible MVP
If you're running out of time:
1. Load ONE sheet to Delta Lake
2. Build ONE calculation function (MRR incentive)
3. Create a simple Streamlit form (not even chat)
4. User enters name → Gets incentive
5. Compare time: 5 min in Excel vs 10 sec in app

**This is still impressive!**

### Quick Wins
- Use Databricks sample datasets if data upload fails
- Use pre-built LLM endpoints (don't fine-tune)
- Copy-paste working code examples
- Use Streamlit templates
- Focus on ONE wow moment

---

## 📊 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to calculate 1 incentive | <30 sec | vs 5-10 min in Excel |
| Calculation accuracy | 100% | Matches Excel results |
| Questions answered | 5+ types | Natural language variety |
| Demo length | 5 min | Timed presentation |
| Audience "wow" reactions | 3+ | Count audible reactions |
| Follow-up interest | 2+ teams | Want to use in production |

---

## 🎉 Victory Conditions

You WIN the hackathon if you can show:
1. ✅ A working demo that impresses non-technical people
2. ✅ Clear time/cost savings (quantified)
3. ✅ Use of multiple Databricks AI capabilities
4. ✅ A solution that could realistically go to production
5. ✅ Answers to "why not just use Excel?" convincingly

**Bonus Points:**
- Live demo (not pre-recorded)
- Handles unexpected questions
- Beautiful UI
- Makes the judges say "wow"

---

## 🆘 Emergency Contacts & Resources

### If Things Break
- **Data won't load?** → Use Databricks sample data
- **LLM not responding?** → Fall back to keyword matching
- **UI crashes?** → Have screenshots ready
- **Demo fails?** → Have a backup video

### Helpful Documentation
- Databricks Genie: https://docs.databricks.com/genie/
- Delta Lake: https://docs.databricks.com/delta/
- Databricks Apps: https://docs.databricks.com/apps/
- ML Flow: https://mlflow.org/docs/latest/

### Sample Code
- See `cursor/prototypes/` folder for starter code
- Check `cursor/data-exploration/` for data analysis

---

**Good luck! You've got this! 🚀**

