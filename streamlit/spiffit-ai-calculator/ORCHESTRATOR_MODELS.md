# 🤖 Orchestrator Model Guide

## What is the Orchestrator?

The **Agent Brain (Orchestrator)** is the LLM that:
- **Routes queries** → Decides which Genie spaces/tools to call
- **Synthesizes results** → Combines answers from multiple sources
- **Reasons** → Determines the best strategy for each question

---

## ✅ Current Models (Hardcoded)

The dropdown currently shows 4 models:

```python
[
    "databricks-meta-llama-3-1-70b-instruct",
    "databricks-dbrx-instruct", 
    "anthropic-claude-3-sonnet",
    "openai-gpt-4"
]
```

**⚠️ IMPORTANT:** These are **examples**. They may not exist in your workspace!

---

## 🔍 How to Find Available Models

### Option 1: Run the PowerShell Script

```powershell
.\list-serving-endpoints.ps1
```

This will show:
- ✅ All serving endpoints in your workspace
- 🎯 Which ones are suitable for orchestration
- 📊 Their status (READY, NOT_READY, etc.)

### Option 2: Databricks CLI

```bash
databricks serving-endpoints list --profile dlk-hackathon
```

### Option 3: Databricks UI

1. Go to your workspace
2. Click **Compute** → **Serving**
3. Look for Foundation Model endpoints

---

## 📦 Typical Foundation Model Endpoints

If your workspace has Foundation Model API enabled, you might see:

### **Meta Llama Models:**
- `databricks-meta-llama-3-1-405b-instruct` (🔥 most powerful)
- `databricks-meta-llama-3-1-70b-instruct` (⚡ fast + capable)
- `databricks-meta-llama-3-1-8b-instruct` (💰 cheapest)
- `databricks-meta-llama-3-70b-instruct` (Llama 3)

### **Databricks Models:**
- `databricks-dbrx-instruct` (Databricks' own model)
- `databricks-mixtral-8x7b-instruct` (Mixture of Experts)

### **Third-Party Models:**
- `anthropic-claude-3-5-sonnet` (Claude 3.5)
- `anthropic-claude-3-sonnet` (Claude 3)
- `anthropic-claude-3-haiku` (Fast + cheap)
- `openai-gpt-4o` (GPT-4 Omni)
- `openai-gpt-4` (GPT-4)
- `openai-gpt-3.5-turbo` (Cheapest)
- `mistralai-mixtral-8x22b-instruct` (Mistral large)
- `mistralai-mistral-large` (Mistral)

---

## 🎯 **Recommended Models for Orchestration**

For **smart routing** (which Genie to call?), you need:
- ✅ Strong reasoning capabilities
- ✅ Good JSON output
- ✅ Fast response time (<2s)
- ✅ Cost-effective (many queries)

### **Tier 1: Best Overall** 🏆
```
databricks-meta-llama-3-1-70b-instruct
```
- ✅ Excellent reasoning
- ✅ Fast (<1s)
- ✅ Good balance cost/performance
- ✅ **RECOMMENDED for hackathon**

### **Tier 2: Premium (if budget allows)** 💎
```
anthropic-claude-3-5-sonnet
openai-gpt-4o
databricks-meta-llama-3-1-405b-instruct
```
- ✅ Best reasoning
- ⚠️ Higher cost
- ⚠️ Slightly slower

### **Tier 3: Budget-Friendly** 💰
```
databricks-meta-llama-3-1-8b-instruct
anthropic-claude-3-haiku
openai-gpt-3.5-turbo
```
- ✅ Very fast
- ✅ Lowest cost
- ⚠️ Less reliable reasoning

---

## 🔧 How to Update the Model List

### Step 1: Check What's Available

Run:
```powershell
.\list-serving-endpoints.ps1
```

### Step 2: Update `app.py`

Edit lines 193-198:

```python
model_choice = st.selectbox(
    "🤖 Agent Brain (Orchestrator)",
    [
        # Add ONLY models that exist in YOUR workspace!
        "databricks-meta-llama-3-1-70b-instruct",  # ⭐ Recommended
        "databricks-meta-llama-3-1-405b-instruct", # Most powerful
        "databricks-dbrx-instruct",                # Databricks native
        "anthropic-claude-3-5-sonnet",             # Claude latest
        "anthropic-claude-3-haiku",                # Fast + cheap
        "openai-gpt-4o",                           # GPT-4 Omni
        "databricks-meta-llama-3-1-8b-instruct",   # Budget option
    ],
    help="Which LLM the multi-agent uses for routing & synthesis"
)
```

### Step 3: Test

Test that the endpoint exists:

```python
# In troubleshooting tab, it will show if the model fails
```

---

## 🐛 Common Errors

### **Error: Serving endpoint not found**

```
databricks.sdk.errors.platform.ResourceDoesNotExist: 
Serving endpoint 'openai-gpt-4' not found
```

**Solution:** That model doesn't exist in your workspace. Remove it from the list or create the endpoint.

### **Error: Permission denied**

```
PermissionDenied: User not authorized to query serving endpoint
```

**Solution:** Check your user permissions for the serving endpoint.

---

## 📊 Performance Tips

### **For Hackathon Demo:**
- ✅ Use **`databricks-meta-llama-3-1-70b-instruct`** (default)
- ✅ Fast + reliable
- ✅ Good reasoning for multi-agent routing

### **For Production:**
- 🎯 Start with **Llama 3.1 70B**
- 📊 Monitor token usage + cost
- ⚡ Consider **Claude 3 Haiku** for high-volume routing (cheaper)
- 💎 Use **GPT-4o** or **Claude 3.5 Sonnet** for synthesis (better quality)

### **Strategy: Hybrid Models**

You could use DIFFERENT models for:
- **Routing** (fast/cheap): Llama 8B or Claude Haiku
- **Synthesis** (quality): GPT-4o or Claude 3.5 Sonnet

---

## 🚀 Next Steps

1. **Run the script:** `.\list-serving-endpoints.ps1`
2. **See what you have** in your workspace
3. **Update the dropdown** with available models
4. **Test** with different models to compare quality
5. **Pick the best** for your use case!

---

## 💡 Pro Tips

- 🎯 **For demos:** Use the most powerful model (impress judges!)
- 💰 **For production:** Balance cost vs quality
- ⚡ **For speed:** Smaller models (8B) are 3-5x faster
- 🔬 **For accuracy:** Larger models (70B+) reason better

---

**🎸 When in doubt... Llama 3.1 70B will Spiff It! 🎸**

