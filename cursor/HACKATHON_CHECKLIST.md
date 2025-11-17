# 🎯 Hackathon Day Checklist

## Before You Start (Morning Setup)

### Team Preparation
- [ ] Print or bookmark `cursor/QUICK_START.md`
- [ ] Print or bookmark `cursor/HACKATHON_DAY_PLAN.md`
- [ ] Assign team roles:
  - [ ] Data Engineer (Delta Lake setup)
  - [ ] ML/AI Engineer (LLM integration)
  - [ ] Full Stack Dev (UI)
  - [ ] Product/Demo Lead (Presentation)
- [ ] Set up Databricks workspace access for all team members
- [ ] Test screen sharing / presentation setup

### Data & Environment
- [ ] Upload Excel files to Databricks:
  - [ ] `AE Ethernet Incentive Data.xlsx`
  - [ ] `Voice_Incentive_data.xlsx`
- [ ] Create notebooks folder in Databricks
- [ ] Upload `cursor/prototypes/01_load_data_to_delta.py`
- [ ] Upload `cursor/prototypes/02_incentive_calculator.py`
- [ ] Test running the scripts
- [ ] Verify Delta tables are created

---

## Hour 1-2: Foundation (9:00 AM - 11:00 AM)

### Data Engineer Tasks
- [ ] Run `01_load_data_to_delta.py` successfully
- [ ] Verify all 5 Delta tables created:
  - [ ] `incentives.ae_performance`
  - [ ] `incentives.ae_opportunities`
  - [ ] `incentives.ae_lit_buildings`
  - [ ] `incentives.voice_activations`
  - [ ] `incentives.voice_orders`
- [ ] Test sample queries
- [ ] Document table schemas

### Team Decision
- [ ] Review 3 use case options in `cursor/automation-ideas/use-cases.md`
- [ ] Vote on which to build (recommend #1)
- [ ] Review implementation plan
- [ ] Create shared task board/document

---

## Hour 3-4: Core Development (11:00 AM - 1:00 PM)

### ML/AI Engineer Tasks
- [ ] Test basic IncentiveCalculator class
- [ ] Implement MRR incentive calculation
- [ ] Implement Renewal incentive calculation
- [ ] Implement TCV incentive calculation
- [ ] Implement Total incentive calculation
- [ ] Test with 3-5 sample AE names
- [ ] Document calculation logic

### Full Stack Tasks
- [ ] Set up Databricks App environment
- [ ] Create basic Streamlit structure
- [ ] Design UI mockup
- [ ] Plan component structure

### Product Tasks
- [ ] Identify 5-10 demo questions to support
- [ ] Write demo script draft
- [ ] Start slide deck (if needed)
- [ ] Gather competitive examples (Excel screenshots)

---

## LUNCH BREAK (1:00 PM - 1:30 PM)
- [ ] Order food
- [ ] Quick team sync - are we on track?
- [ ] Adjust plan if needed

---

## Hour 5-6: AI Integration (1:30 PM - 3:30 PM)

### ML/AI Engineer Tasks
- [ ] Set up Genie or LLM endpoint
- [ ] Create prompt templates for:
  - [ ] Intent classification
  - [ ] Parameter extraction
  - [ ] Response generation
- [ ] Build question understanding logic
- [ ] Test 5 different question types:
  - [ ] "What's [name]'s incentive?"
  - [ ] "Show top performers"
  - [ ] "What if I close $X more?"
  - [ ] "How am I tracking?"
  - [ ] "Who's in Platinum tier?"
- [ ] Add natural language explanations

### Full Stack Tasks
- [ ] Connect UI to calculation engine
- [ ] Build chat interface
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test end-to-end flow

### Product Tasks
- [ ] Calculate ROI metrics:
  - [ ] Time savings
  - [ ] Cost savings
  - [ ] Error reduction
- [ ] Prepare "Excel way" demo
- [ ] Take screenshots
- [ ] Write comparison talking points

---

## Hour 7: Polish & Testing (3:30 PM - 4:30 PM)

### Everyone
- [ ] Full end-to-end testing
- [ ] Fix critical bugs
- [ ] Add any quick wins:
  - [ ] Better formatting
  - [ ] Charts/visualizations
  - [ ] More example questions
- [ ] Deploy to final environment
- [ ] Get deployment URL

### Demo Prep
- [ ] Test demo flow 3 times
- [ ] Identify backup plans if things break
- [ ] Take screenshots as fallback
- [ ] Record video as fallback (optional)

---

## Hour 8: Final Prep (4:30 PM - 5:00 PM)

### Demo Lead Tasks
- [ ] Finalize 5-minute pitch
- [ ] Practice pitch 2-3 times
- [ ] Time it (must be under 5 min!)
- [ ] Prepare Q&A responses:
  - [ ] "Can this handle complex formulas?"
  - [ ] "What about data security?"
  - [ ] "How long to production?"
  - [ ] "Can it integrate with other systems?"
- [ ] Have backup demo ready (screenshots/video)

### Team Tasks
- [ ] Clean up code (remove debugging statements)
- [ ] Add code comments
- [ ] Create architecture diagram (if time)
- [ ] Commit code to GitHub
- [ ] Update README with results

### Final Checks
- [ ] Demo works on presentation computer
- [ ] Internet connection stable
- [ ] Backup plan ready
- [ ] Team roles clear for demo
- [ ] Everyone knows their part

---

## Demo Time! (Presentation)

### Setup (2 minutes before)
- [ ] Open Excel file
- [ ] Open your Databricks App
- [ ] Close all other windows
- [ ] Test audio/screen share
- [ ] Have water handy

### During Demo (5 minutes)
- [ ] Opening hook (30 sec)
- [ ] Show the problem (1 min)
- [ ] Show your solution (2 min)
- [ ] Explain the tech (1 min)
- [ ] State the impact (30 sec)

### After Demo
- [ ] Answer questions confidently
- [ ] Note feedback
- [ ] Exchange contact info with interested judges
- [ ] Celebrate! 🎉

---

## Post-Hackathon

### If You Win 🏆
- [ ] Celebrate with team!
- [ ] Schedule follow-up meeting
- [ ] Plan next steps:
  - [ ] Production deployment timeline
  - [ ] Security review
  - [ ] User testing
  - [ ] Additional features

### Regardless of Outcome
- [ ] Thank your team
- [ ] Document lessons learned
- [ ] Save all work to GitHub
- [ ] Share demo video internally
- [ ] Consider productionizing anyway!

---

## Emergency Contacts

### If Tech Breaks
- **Data won't load?** → Use sample/demo data
- **LLM not working?** → Fall back to keyword matching
- **UI crashes?** → Use screenshots
- **Everything fails?** → Show video/slides

### If Running Behind
- **Hour 2:** Skip optional features
- **Hour 4:** Use simpler UI (form instead of chat)
- **Hour 6:** Skip visualizations
- **Hour 8:** Focus on ONE perfect demo flow

---

## Success Criteria

You're ready to present if you can answer YES to:
- [ ] Can you calculate at least ONE incentive metric?
- [ ] Can it handle natural language questions?
- [ ] Does it work faster than Excel?
- [ ] Can you quantify the time/cost savings?
- [ ] Can you demo it smoothly in 5 minutes?

**If YES to all → You're ready to win! 🚀**

---

## Confidence Boosters

Remember:
- ✅ You have 400+ lines of starter code
- ✅ You have detailed implementation plans
- ✅ You have real data analyzed
- ✅ You have a clear business case
- ✅ You have a winning demo script

**You've got this! 💪**

