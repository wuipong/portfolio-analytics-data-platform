import os
import json
# COMMENT: in Databricks environment，use dbrx / langchain to integrate
# from langchain_community.llms import Databricks
# from langchain.prompts import PromptTemplate

class AIAssetEnricher:
    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        # COMMENT: use Databricks Secrets API Key
        self.api_key = os.getenv("AI_API_KEY")

    def extract_bond_covenants(self, pdf_text):
        """
        use LLM to extract bond detail from PDF
        """
        prompt = f"""
        Extract the following attributes from the provided bond prospectus text:
        1. Call Date (YYYY-MM-DD)
        2. Change of Control Clause (True/False)
        3. Dividend Restriction (Description)

        Text: {pdf_text[:2000]}  # 僅取前 2000 字作為示例
        Return as JSON.
        """
        
        # Simulate return
        # COMMENT: production environment will call llm.invoke(prompt)
        mock_ai_response = {
            "call_date": "2028-06-15",
            "change_of_control": True,
            "dividend_restriction": "Cannot exceed 50% of net income"
        }
        
        return mock_ai_response

    def enrich_asset_metadata(self, holdings_df):
        """
        Insert data capture by AI into existing portofolio DataFrame
        """
        print("[AI Step] Running NLP extraction for unstructured bond attributes...")
        
        # Demo here only
        # in production environment iterate by ISIN
        holdings_df['ai_extracted_call_date'] = "2028-06-15"
        holdings_df['has_change_of_control'] = True
        
        # COMMENT: In Databricks, use Pandas UDF parallel handle ISIN
        # enriched_df = holdings_df.withColumn("ai_data", ai_udf(col("prospectus_text")))
        
        print("✅ AI Enrichment complete: Unstructured attributes merged.")
        return holdings_df

if __name__ == "__main__":
    sample_text = "The issuer has the option to call the bonds on June 15, 2028..."
    enricher = AIAssetEnricher()
    result = enricher.extract_bond_covenants(sample_text)
    print(f"AI Extracted Data: {json.dumps(result, indent=2)}")
