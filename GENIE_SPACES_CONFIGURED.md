# ✅ Genie Spaces Configured!

Your Genie spaces are set up and ready to use in the `dlk-hackathon` workspace.

## 📋 Space IDs

| Space Name | Purpose | Space ID |
|------------|---------|----------|
| **spg-mocking-bird-sales** | Sales performance data | `01f0c403c3cf184e9b7f1f6c9ee45905` |
| **spg-mocking-bird-analytics** | SPIFF winners & rankings | `01f0c404048613b3b494b1a64a1bca84` |
| **spg-mocking-bird-market** | Competitor intelligence | `01f0c4043acf19dc936c37fd2a8bced3` |

## 🔗 Direct Links

- [Sales Space](https://dbc-4a93b454-f17b.cloud.databricks.com/genie/spaces/01f0c403c3cf184e9b7f1f6c9ee45905)
- [Analytics Space](https://dbc-4a93b454-f17b.cloud.databricks.com/genie/spaces/01f0c404048613b3b494b1a64a1bca84)
- [Market Space](https://dbc-4a93b454-f17b.cloud.databricks.com/genie/spaces/01f0c4043acf19dc936c37fd2a8bced3)

## ✅ What's Already Configured

### Streamlit App (`streamlit/spiffit-ai-calculator/`)
- ✅ `app.yaml` - Space IDs configured for Databricks deployment
- ✅ `env.example` - Template file with all space IDs for local testing

### Data Tables (`hackathon.hackathon_spiffit`)
- ✅ `sales_performance` - Connected to sales space
- ✅ `spiff_winners` - Connected to analytics space  
- ✅ `competitor_spiffs` - Connected to market space

## 🚀 Ready to Test!

### Test in Genie UI
Go to each space and try these queries:

**Sales Space:**
```
Who are the top performers?
What's John Smith's attainment percentage?
Show me all deals closed
```

**Analytics Space:**
```
Who won the most SPIFFs?
Show total earnings by person
Who ranks #1 in Double MRR program?
```

**Market Space:**
```
What are competitors offering in December?
Show the highest paying programs
What's Competitor A doing?
```

### Test Locally with Streamlit
```bash
cd streamlit/spiffit-ai-calculator

# Copy env file
cp env.example .env

# Run the app
streamlit run app.py --server.port 8000
```

### Deploy to Databricks
The `app.yaml` is already configured - just push to Git and create a Databricks App!

---

**🎉 You're all set for the hackathon!**

