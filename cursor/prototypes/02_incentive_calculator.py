"""
Starter Code: Incentive Calculator Functions
This replaces Excel formulas with Python logic
"""

from pyspark.sql.functions import col, when, lit
from pyspark.sql import DataFrame
from typing import Dict, List, Optional
import json


class IncentiveCalculator:
    """
    Core incentive calculation engine
    Replaces complex Excel formulas with clean Python code
    """
    
    def __init__(self, spark_session):
        self.spark = spark_session
        self._load_data()
    
    def _load_data(self):
        """Load data from Delta tables"""
        self.ae_performance = self.spark.table("incentives.ae_performance")
        self.ae_opportunities = self.spark.table("incentives.ae_opportunities")
        self.voice_activations = self.spark.table("incentives.voice_activations")
        
    # ========================================================================
    # MRR INCENTIVE CALCULATIONS
    # ========================================================================
    
    def calculate_mrr_incentive(self, ae_name: str) -> Dict:
        """
        Calculate MRR-based incentive for a specific AE
        
        Replaces Excel formula:
        =IF(MRR_Attainment >= 120%, Budget * 20%, 
           IF(MRR_Attainment >= 100%, Budget * 15%,
           IF(MRR_Attainment >= 80%, Budget * 10%, Budget * 5%)))
        
        Args:
            ae_name: Name of the Account Executive
            
        Returns:
            Dictionary with incentive breakdown and explanation
        """
        # Get AE record
        ae_record = self.ae_performance.filter(col("ae_name") == ae_name).first()
        
        if ae_record is None:
            return {
                "error": f"AE '{ae_name}' not found",
                "available_aes": self._get_all_ae_names()[:10]  # Show first 10
            }
        
        # Extract values
        budget = float(ae_record["mrr_budget"])
        actual = float(ae_record["mrr_actual"])
        attainment_pct = float(ae_record["mrr_attainment_pct"]) * 100
        
        # Calculate tier and payout
        if attainment_pct >= 120:
            tier = "Platinum"
            payout_pct = 0.20
            payout = budget * payout_pct
        elif attainment_pct >= 100:
            tier = "Gold"
            payout_pct = 0.15
            payout = budget * payout_pct
        elif attainment_pct >= 80:
            tier = "Silver"
            payout_pct = 0.10
            payout = budget * payout_pct
        else:
            tier = "Bronze"
            payout_pct = 0.05
            payout = budget * payout_pct
        
        return {
            "ae_name": ae_name,
            "metric": "MRR",
            "budget": budget,
            "actual": actual,
            "attainment_pct": attainment_pct,
            "incentive_tier": tier,
            "payout_pct": payout_pct * 100,
            "payout": payout,
            "explanation": (
                f"{ae_name} achieved {attainment_pct:.1f}% MRR attainment "
                f"(${actual:,.2f} actual vs ${budget:,.2f} budget), "
                f"earning {tier} tier with a ${payout:,.2f} incentive "
                f"({payout_pct*100:.0f}% of budget)."
            )
        }
    
    # ========================================================================
    # RENEWAL INCENTIVE CALCULATIONS
    # ========================================================================
    
    def calculate_renewal_incentive(self, ae_name: str) -> Dict:
        """
        Calculate Renewal-based incentive
        Similar structure to MRR but with different thresholds
        """
        ae_record = self.ae_performance.filter(col("ae_name") == ae_name).first()
        
        if ae_record is None:
            return {"error": f"AE '{ae_name}' not found"}
        
        budget = float(ae_record["renewal_budget"])
        actual = float(ae_record["renewal_actual"])
        attainment_pct = float(ae_record["renewal_attainment_pct"]) * 100
        
        # Different tier structure for renewals
        if attainment_pct >= 110:
            tier = "Platinum"
            payout_pct = 0.18
        elif attainment_pct >= 100:
            tier = "Gold"
            payout_pct = 0.12
        elif attainment_pct >= 85:
            tier = "Silver"
            payout_pct = 0.08
        else:
            tier = "Bronze"
            payout_pct = 0.03
        
        payout = budget * payout_pct
        
        return {
            "ae_name": ae_name,
            "metric": "Renewal",
            "budget": budget,
            "actual": actual,
            "attainment_pct": attainment_pct,
            "incentive_tier": tier,
            "payout_pct": payout_pct * 100,
            "payout": payout,
            "explanation": (
                f"{ae_name} achieved {attainment_pct:.1f}% renewal attainment, "
                f"earning {tier} tier with a ${payout:,.2f} incentive."
            )
        }
    
    # ========================================================================
    # TCV INCENTIVE CALCULATIONS
    # ========================================================================
    
    def calculate_tcv_incentive(self, ae_name: str) -> Dict:
        """Calculate Total Contract Value incentive"""
        ae_record = self.ae_performance.filter(col("ae_name") == ae_name).first()
        
        if ae_record is None:
            return {"error": f"AE '{ae_name}' not found"}
        
        budget = float(ae_record["tcv_budget"])
        actual = float(ae_record["tcv_actual"])
        attainment_pct = float(ae_record["tcv_attainment_pct"]) * 100
        
        if attainment_pct >= 115:
            tier = "Platinum"
            payout_pct = 0.16
        elif attainment_pct >= 100:
            tier = "Gold"
            payout_pct = 0.12
        elif attainment_pct >= 80:
            tier = "Silver"
            payout_pct = 0.08
        else:
            tier = "Bronze"
            payout_pct = 0.04
        
        payout = budget * payout_pct
        
        return {
            "ae_name": ae_name,
            "metric": "TCV",
            "budget": budget,
            "actual": actual,
            "attainment_pct": attainment_pct,
            "incentive_tier": tier,
            "payout_pct": payout_pct * 100,
            "payout": payout,
            "explanation": (
                f"{ae_name} achieved {attainment_pct:.1f}% TCV attainment, "
                f"earning {tier} tier with a ${payout:,.2f} incentive."
            )
        }
    
    # ========================================================================
    # TOTAL INCENTIVE CALCULATIONS
    # ========================================================================
    
    def calculate_total_incentive(self, ae_name: str) -> Dict:
        """
        Calculate total incentive across all categories
        This is what users want most often!
        """
        mrr = self.calculate_mrr_incentive(ae_name)
        if "error" in mrr:
            return mrr
        
        renewal = self.calculate_renewal_incentive(ae_name)
        tcv = self.calculate_tcv_incentive(ae_name)
        
        total_payout = mrr["payout"] + renewal["payout"] + tcv["payout"]
        
        return {
            "ae_name": ae_name,
            "total_payout": total_payout,
            "breakdown": {
                "mrr": {
                    "attainment": mrr["attainment_pct"],
                    "tier": mrr["incentive_tier"],
                    "payout": mrr["payout"]
                },
                "renewal": {
                    "attainment": renewal["attainment_pct"],
                    "tier": renewal["incentive_tier"],
                    "payout": renewal["payout"]
                },
                "tcv": {
                    "attainment": tcv["attainment_pct"],
                    "tier": tcv["incentive_tier"],
                    "payout": tcv["payout"]
                }
            },
            "summary": (
                f"💰 Total Incentive for {ae_name}: ${total_payout:,.2f}\n\n"
                f"Breakdown:\n"
                f"• MRR ({mrr['incentive_tier']}): ${mrr['payout']:,.2f} "
                f"({mrr['attainment_pct']:.1f}% attainment)\n"
                f"• Renewal ({renewal['incentive_tier']}): ${renewal['payout']:,.2f} "
                f"({renewal['attainment_pct']:.1f}% attainment)\n"
                f"• TCV ({tcv['incentive_tier']}): ${tcv['payout']:,.2f} "
                f"({tcv['attainment_pct']:.1f}% attainment)"
            )
        }
    
    # ========================================================================
    # WHAT-IF SCENARIO MODELING
    # ========================================================================
    
    def calculate_what_if_scenario(self, ae_name: str, additional_mrr: float) -> Dict:
        """
        Answer: "What if I close $50K more in MRR?"
        This is IMPOSSIBLE to do easily in Excel!
        """
        # Get current state
        current = self.calculate_total_incentive(ae_name)
        if "error" in current:
            return current
        
        # Get current values
        ae_record = self.ae_performance.filter(col("ae_name") == ae_name).first()
        current_budget = float(ae_record["mrr_budget"])
        current_actual = float(ae_record["mrr_actual"])
        
        # Calculate new scenario
        new_actual = current_actual + additional_mrr
        new_attainment_pct = (new_actual / current_budget) * 100
        
        # Determine new tier
        if new_attainment_pct >= 120:
            new_tier = "Platinum"
            new_payout_pct = 0.20
        elif new_attainment_pct >= 100:
            new_tier = "Gold"
            new_payout_pct = 0.15
        elif new_attainment_pct >= 80:
            new_tier = "Silver"
            new_payout_pct = 0.10
        else:
            new_tier = "Bronze"
            new_payout_pct = 0.05
        
        new_mrr_payout = current_budget * new_payout_pct
        
        # Calculate delta
        current_mrr_payout = current["breakdown"]["mrr"]["payout"]
        payout_increase = new_mrr_payout - current_mrr_payout
        
        return {
            "ae_name": ae_name,
            "scenario": f"Add ${additional_mrr:,.2f} to MRR",
            "current": {
                "mrr_actual": current_actual,
                "attainment_pct": current["breakdown"]["mrr"]["attainment"],
                "tier": current["breakdown"]["mrr"]["tier"],
                "mrr_payout": current_mrr_payout,
                "total_payout": current["total_payout"]
            },
            "projected": {
                "mrr_actual": new_actual,
                "attainment_pct": new_attainment_pct,
                "tier": new_tier,
                "mrr_payout": new_mrr_payout,
                "total_payout": current["total_payout"] - current_mrr_payout + new_mrr_payout
            },
            "impact": {
                "payout_increase": payout_increase,
                "tier_change": current["breakdown"]["mrr"]["tier"] != new_tier,
                "worth_it": payout_increase > 0
            },
            "explanation": (
                f"📈 Scenario Analysis for {ae_name}:\n\n"
                f"If you close an additional ${additional_mrr:,.2f} in MRR:\n"
                f"• Your MRR attainment would increase from "
                f"{current['breakdown']['mrr']['attainment']:.1f}% to {new_attainment_pct:.1f}%\n"
                f"• Your tier would {'change from ' + current['breakdown']['mrr']['tier'] + ' to ' + new_tier if current['breakdown']['mrr']['tier'] != new_tier else 'remain ' + new_tier}\n"
                f"• Your MRR incentive would increase by ${payout_increase:,.2f}\n"
                f"• Your total payout would be ${current['total_payout'] - current_mrr_payout + new_mrr_payout:,.2f}\n\n"
                f"{'🎯 This would boost your tier! Great opportunity!' if current['breakdown']['mrr']['tier'] != new_tier else '💡 Keep pushing to reach the next tier!'}"
            )
        }
    
    # ========================================================================
    # RANKING & LEADERBOARD FUNCTIONS
    # ========================================================================
    
    def get_top_performers(self, metric: str = "mrr", limit: int = 10) -> Dict:
        """
        Get top performers by metric
        Great for leaderboards!
        """
        metric_map = {
            "mrr": ("mrr_attainment_pct", "MRR"),
            "renewal": ("renewal_attainment_pct", "Renewal"),
            "tcv": ("tcv_attainment_pct", "TCV"),
            "ethernet": ("ethernet_attainment_pct", "Ethernet")
        }
        
        if metric.lower() not in metric_map:
            return {"error": f"Invalid metric. Choose from: {', '.join(metric_map.keys())}"}
        
        col_name, display_name = metric_map[metric.lower()]
        
        top_performers = self.ae_performance \
            .select("ae_name", "region", col_name) \
            .orderBy(col(col_name).desc()) \
            .limit(limit) \
            .collect()
        
        results = []
        for rank, performer in enumerate(top_performers, 1):
            results.append({
                "rank": rank,
                "ae_name": performer["ae_name"],
                "region": performer["region"],
                "attainment_pct": float(performer[col_name]) * 100
            })
        
        return {
            "metric": display_name,
            "top_performers": results,
            "summary": (
                f"🏆 Top {limit} Performers by {display_name} Attainment:\n\n" +
                "\n".join([
                    f"{p['rank']}. {p['ae_name']} ({p['region']}) - {p['attainment_pct']:.1f}%"
                    for p in results
                ])
            )
        }
    
    def get_regional_performance(self, region: Optional[str] = None) -> Dict:
        """Get performance summary by region"""
        if region:
            df = self.ae_performance.filter(col("region") == region)
        else:
            df = self.ae_performance
        
        summary = df.groupBy("region").agg({
            "mrr_attainment_pct": "avg",
            "renewal_attainment_pct": "avg",
            "tcv_attainment_pct": "avg",
            "ae_name": "count"
        }).collect()
        
        results = []
        for row in summary:
            results.append({
                "region": row["region"],
                "ae_count": row["count(ae_name)"],
                "avg_mrr_attainment": float(row["avg(mrr_attainment_pct)"]) * 100,
                "avg_renewal_attainment": float(row["avg(renewal_attainment_pct)"]) * 100,
                "avg_tcv_attainment": float(row["avg(tcv_attainment_pct)"]) * 100
            })
        
        return {"regional_summary": results}
    
    # ========================================================================
    # HELPER FUNCTIONS
    # ========================================================================
    
    def _get_all_ae_names(self) -> List[str]:
        """Get list of all AE names"""
        return [row["ae_name"] for row in self.ae_performance.select("ae_name").distinct().collect()]
    
    def search_ae(self, partial_name: str) -> List[str]:
        """Search for AEs by partial name match"""
        all_names = self._get_all_ae_names()
        return [name for name in all_names if partial_name.lower() in name.lower()]


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder.appName("IncentiveCalculator").getOrCreate()
    calculator = IncentiveCalculator(spark)
    
    print("="*80)
    print("INCENTIVE CALCULATOR - EXAMPLE USAGE")
    print("="*80)
    
    # Example 1: Calculate single metric incentive
    print("\n1. Calculate MRR Incentive:")
    print("-" * 80)
    result = calculator.calculate_mrr_incentive("John Smith")
    print(json.dumps(result, indent=2, default=str))
    
    # Example 2: Calculate total incentive
    print("\n2. Calculate Total Incentive:")
    print("-" * 80)
    result = calculator.calculate_total_incentive("John Smith")
    print(result["summary"])
    
    # Example 3: What-if scenario
    print("\n3. What-If Scenario (+$50K MRR):")
    print("-" * 80)
    result = calculator.calculate_what_if_scenario("John Smith", 50000)
    print(result["explanation"])
    
    # Example 4: Top performers
    print("\n4. Top 5 MRR Performers:")
    print("-" * 80)
    result = calculator.get_top_performers("mrr", limit=5)
    print(result["summary"])
    
    # Example 5: Search AEs
    print("\n5. Search for AEs named 'Smith':")
    print("-" * 80)
    results = calculator.search_ae("Smith")
    print(f"Found {len(results)} matches: {results}")
    
    print("\n" + "="*80)
    print("✅ Calculator is working! Ready for AI integration!")
    print("="*80)

