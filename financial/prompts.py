unique_prompts = {
    "current_assets_2022": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract,calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to validate the following financial metrics from the company's balance sheet for the year 2022:

 

1. **Total current assets**: Accurately determine company's total CURRENT ASSETS for the year 2022. Validate if it is equal to {TotalCurrentAssets_2022}, if not update it to match the total current assets in the document.


 

2. **Breakdown of Total CURRENT ASSETS **: Decompose the total CURRENT ASSETS into the following 5 subcomponents. Ensure that the sum of these components equals the total CURRENT ASSETS:

** Cash: 

** Trade Receivables 

** Other (Non-Trade) Receivables

** Finished Goods

** Current Portion Of Prepaid And Deferred Assets



3. ** Validate the values for the 5 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical.

** Cash: {Cash_2022}

** Trade Receivables: {TradeReceivables_2022} 

** Other (Non-Trade) Receivables : {OtherNonTradeReceivables_2022}

** Finished Goods : {FinishedGoods_2022}

** Current Portion Of Prepaid And Deferred Assets : {CurrentPortionOfPrepaidAndDeferredAssets_2022}


  

 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING




 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total CURRENT ASSETS  and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes. If you have used Terminology Interpretation set that field to true else set it to false

OUTPUT FORMAT: only a JSON [without code block] and nothing else. JSON to be structured as follows:

{{
    "CurrentAssets": {{
        
        "Cash": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TradeReceivables": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherNonTradeReceivables": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "FinishedGoods": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfPrepaidAndDeferredAssets": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalCurrentAssets": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
    }}
}}
""",
    "current_assets_2023": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2023:

 

1. **Total current assets**: Accurately determine the company's total CURRENT ASSETS for the year 2023. Validate if it is equal to {TotalCurrentAssets_2023}, if not update it to match the total current assets in the document.

 

2. **Breakdown of Total CURRENT ASSETS **: Decompose the total CURRENT ASSETS into the following 5 subcomponents. Ensure that the sum of these components equals the total CURRENT ASSETS:

** Cash

** Trade Receivables  


** Other (Non-Trade) Receivables

** Finished Goods

** Current Portion Of Prepaid And Deferred Assets


3. ** Validate the values for the 5 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical.

** Cash: {Cash_2023}

** Trade Receivables: {TradeReceivables_2023} 

** Other (Non-Trade) Receivables : {OtherNonTradeReceivables_2023}

** Finished Goods : {FinishedGoods_2023}

** Current Portion Of Prepaid And Deferred Assets : {CurrentPortionOfPrepaidAndDeferredAssets_2023}





 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING

 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total CURRENT ASSETS  and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes. If you have used Terminology Interpretation set that field to true else set it to false

OUTPUT FORMAT: only a JSON [without code block] and nothing else. JSON to be structured as follows:

{{
    "CurrentAssets": {{
        
        "Cash": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TradeReceivables": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherNonTradeReceivables": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "FinishedGoods": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfPrepaidAndDeferredAssets": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalCurrentAssets": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
    }}
}}
""",
    "non_current_assets_2022": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2022:

 

1. **Total Non-Current Assets**: Accurately determine the company's total non-current assets for the year 2022. Validate if it is equal to {TotalNonCurrentAssets_2022}, if not update it to match the total non current assets in the document.


 

2. **Breakdown of Total Non-Current Assets**: Decompose the total non-current assets into the following eight subcomponents. Ensure that the sum of these components equals the total non-current assets:

   - **Construction In Progress**

   - **Machinery And Equipment** NOT COUNTING DEPRECIATION AND IMPAIRMENT (i.e. before deducting depreciation and impairment)

   - **Operating Leases**

   - **Accumulated Depreciation And Impairment** [negative value]

   - **long term portion of Derivative Assets**

   - **Non-Operating Non-Current Assets**

   - **Intangible Assets** NOT COUNTING AMORTIZATION AND IMPAIRMENT

   - **Accumulated Amortization And Impairment** [negative value]
   
   
3. ** Validate the values for the 8 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical.

 **Construction In Progress:  {ConstructionInProgress_2022}

 **Machinery And Equipment: {MachineryAndEquipment_2022}
 
 **Operating Leases: {OperatingLeases_2022}


 **Accumulated Depreciation And Impairment: {AccumulatedDepreciationAndImpairment_2022}

 **long term portion of Derivative Assets: {LongTermPortionOfDerivativeAssets_2022}
 
 **Non-Operating Non-Current Assets: {NonoperatingNoncurrentAssets_2022}


 **Intangible Assets: {IntangibleAssets_2022}
 
 **Accumulated Amortization And Impairment: {AccumulatedAmortizationAndImpairment_2022}

  



  

 

NOTE THAT MACHINERY AND EQUIPMENT SHOULD NOT INCLUDE CONSTRUCTION IN PROGRESS.

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total non-current assets and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block]  and nothing else. JSON to be structured as follows:


{{
    "NonCurrentAssets": {{
        "ConstructionInProgress": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "MachineryAndEquipment": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OperatingLeases": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "AccumulatedDepreciationAndImpairment": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDerivativeAssets": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "NonoperatingNoncurrentAssets": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "IntangibleAssets": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "AccumulatedAmortizationAndImpairment": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNonCurrentAssets": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        
    }}
}}


 """,
    "non_current_assets_2023": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2023:

 

1. **Total Non-Current Assets**: Accurately determine the company's total non-current assets for the year 2023.Validate if it is equal to {TotalNonCurrentAssets_2023}, if not update it to match the total non current assets in the document.

 

2. **Breakdown of Total Non-Current Assets**: Decompose the total non-current assets into the following eight subcomponents. Ensure that the sum of these components equals the total non-current assets:

   - **Construction In Progress**

   - **Machinery And Equipment** NOT COUNTING DEPRECIATION AND IMPAIRMENT (i.e. before deducting depreciation and impairment)

   - **Operating Leases**

   - **Accumulated Depreciation And Impairment** [negative value]

   - **long term portion of Derivative Assets**

   - **Non-Operating Non-Current Assets**

   - **Intangible Assets** NOT COUNTING AMORTIZATION AND IMPAIRMENT

   - **Accumulated Amortization And Impairment** [negative value]
   
   
   
3. ** Validate the values for the 8 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical.

 **Construction In Progress:  {ConstructionInProgress_2023}

 **Machinery And Equipment: {MachineryAndEquipment_2023}
 
 **Operating Leases: {OperatingLeases_2023}


 **Accumulated Depreciation And Impairment: {AccumulatedDepreciationAndImpairment_2023}

 **long term portion of Derivative Assets: {LongTermPortionOfDerivativeAssets_2023}
 
 **Non-Operating Non-Current Assets: {NonoperatingNoncurrentAssets_2023}


 **Intangible Assets: {IntangibleAssets_2023}
 
 **Accumulated Amortization And Impairment: {AccumulatedAmortizationAndImpairment_2023}






 

NOTE THAT MACHINERY AND EQUIPMENT SHOULD NOT INCLUDE CONSTRUCTION IN PROGRESS.

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total non-current assets and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block]  and nothing else. JSON to be structured as follows:


{{
    "NonCurrentAssets": {{
        "ConstructionInProgress": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "MachineryAndEquipment": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OperatingLeases": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "AccumulatedDepreciationAndImpairment": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDerivativeAssets": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "NonoperatingNoncurrentAssets": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "IntangibleAssets": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "AccumulatedAmortizationAndImpairment": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNonCurrentAssets": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        
    }}
}}


 """,
    "current_liabilities_2022": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2022:

 

1. **Total current liabilities**: Accurately determine the company's total CURRENT LIABILITIES for the year 2022.Validate if it is equal to {TotalCurrentLiabilities_2022}, if not update it to match the total current liabilities in the document.

 

2. **Breakdown of Total CURRENT LIABILITIES **: Decompose the total CURRENT LIABILITIES into the following 7 subcomponents. Ensure that the sum of these components equals the total CURRENT LIABILITIES:

   - **Short-Term Loans Payable**

   - **Current Portion Of Operating Lease Obligations**

   - **Trade Accounts Payable**

   - **Other Accruals**

   - **Other Taxes Payable**

   - **Income Taxes Payable**

   - **Current Portion Of Derivative Liabilities**
   
   
3. ** Validate the values for the 7 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical:

  - **Short-Term Loans Payable: {ShorttermLoansPayable_2022}

   - **Current Portion Of Operating Lease Obligations: {CurrentPortionOfOperatingLeaseObligations_2022}
   
   - **Trade Accounts Payable: {TradeAccountsPayable_2022}

   - **Other Accruals: {OtherAccruals_2022}

   - **Other Taxes Payable: {OtherTaxesPayable_2022}

   - **Income Taxes Payable: {IncomeTaxesPayable_2022}

   - **Current Portion Of Derivative Liabilities: {CurrentPortionOfDerivativeLiabilities_2022}
   



  

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING

 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total CURRENT LIABILTIES  and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block] and nothing else. JSON to be structured as follows:


{{
    "CurrentLiabilities": {{
        "ShorttermLoansPayable": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfOperatingLeaseObligations": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TradeAccountsPayable": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherAccruals": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherTaxesPayable": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "IncomeTaxesPayable": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfDerivativeLiabilities": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalCurrentLiabilities": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
    }}
}}

""",
    "current_liabilities_2023": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2023:

 

1. **Total current liabilities**: Accurately determine the company's total CURRENT LIABILITIES for the year 2023.Validate if it is equal to {TotalCurrentLiabilities_2023}, if not update it to match the total current liabilities in the document.

 

2. **Breakdown of Total CURRENT LIABILITIES **: Decompose the total CURRENT LIABILITIES into the following 7 subcomponents. Ensure that the sum of these components equals the total CURRENT LIABILITIES:

   - **Short-Term Loans Payable**

   - **Current Portion Of Operating Lease Obligations**

   - **Trade Accounts Payable**

   - **Other Accruals**

   - **Other Taxes Payable**

   - **Income Taxes Payable**

   - **Current Portion Of Derivative Liabilities**
   

3. ** Validate the values for the 7 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical:

  - **Short-Term Loans Payable: {ShorttermLoansPayable_2023}

   - **Current Portion Of Operating Lease Obligations: {CurrentPortionOfOperatingLeaseObligations_2023}
   
   - **Trade Accounts Payable: {TradeAccountsPayable_2023}

   - **Other Accruals: {OtherAccruals_2023}

   - **Other Taxes Payable: {OtherTaxesPayable_2023}

   - **Income Taxes Payable: {IncomeTaxesPayable_2023}

   - **Current Portion Of Derivative Liabilities: {CurrentPortionOfDerivativeLiabilities_2023}




 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING

 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total CURRENT LIABILTIES  and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block] and nothing else. JSON to be structured as follows:


{{
    "CurrentLiabilities": {{
        "ShorttermLoansPayable": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfOperatingLeaseObligations": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TradeAccountsPayable": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherAccruals": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherTaxesPayable": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "IncomeTaxesPayable": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfDerivativeLiabilities": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalCurrentLiabilities": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
    }}
}}

""",
    "non_current_liabilities_2022": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2022:

 

1. **Total non-current liabilities**: Accurately determine the company's total NON-CURRENT LIABILITIES for the year 2022.Validate if it is equal to {TotalNonCurrentLiabilities_2022}, if not update it to match the total non current liabilities in the document


 

2. **Breakdown of Total NON-CURRENT LIABILITIES **: Decompose the total NON-CURRENT LIABILITIES into the following 6 subcomponents. Ensure that the sum of these components equals the total NON-CURRENT LIABILITIES:

 - ** Long Term Bank Debt

- ** long term portion of Operating Lease Obligations

- ** Long Term Portion Of Derivative Liabilities

- ** Non Operating Non Current Liabilities (INCLUDING UNCATEGORISED NON CURRENT AND NON OPERATING LIABILITIES AND OBLIGATIONS)

- ** Long Term Portion Of Loans From Related Companies

- ** Long Term Portion Of Deferred Federal Income Tax


3. ** Validate the values for the 6 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical:

 - ** Long Term Bank Debt: {LongTermBankDebt_2022}

- ** long term portion of Operating Lease Obligations: {LongTermPortionOfOperatingLeaseObligations_2022}

- ** Long Term Portion Of Derivative Liabilities: {LongTermPortionOfDerivativeLiabilities_2022}

- ** Non Operating Non Current Liabilities: {NonOperatingNonCurrentLiabilities_2022}

- ** Long Term Portion Of Loans From Related Companies: {LongTermPortionOfLoansFromRelatedCompanies_2022}

- ** Long Term Portion Of Deferred Federal Income Tax: {LongTermPortionOfDeferredFederalIncomeTax_2022}




 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING

 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total NON-CURRENT LIABILTIES  and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block]  and nothing else. JSON to be structured as follows:



{{
    "NonCurrentLiabilities": {{
        "LongTermBankDebt": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfOperatingLeaseObligations": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDerivativeLiabilities": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "NonOperatingNonCurrentLiabilities": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfLoansFromRelatedCompanies": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDeferredFederalIncomeTax": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNonCurrentLiabilities": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
        
    }}
}}

""",
    "non_current_liabilities_2023": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract and calculate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2023:

 

1. **Total non-current liabilities**: Accurately determine the company's total NON-CURRENT LIABILITIES for the year 2023.Validate if it is equal to {TotalNonCurrentLiabilities_2023}, if not update it to match the total non current liabilities in the document

 

2. **Breakdown of Total NON-CURRENT LIABILITIES **: Decompose the total NON-CURRENT LIABILITIES into the following 6 subcomponents. Ensure that the sum of these components equals the total NON-CURRENT LIABILITIES:

 - ** Long Term Bank Debt

- ** long term portion of Operating Lease Obligations

- ** Long Term Portion Of Derivative Liabilities

- ** Non Operating Non Current Liabilities (INCLUDING UNCATEGORISED NON CURRENT AND NON OPERATING LIABILITIES AND OBLIGATIONS)

- ** Long Term Portion Of Loans From Related Companies

- ** Long Term Portion Of Deferred Federal Income Tax


3. ** Validate the values for the 6 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical:

 - ** Long Term Bank Debt: {LongTermBankDebt_2023}

- ** long term portion of Operating Lease Obligations: {LongTermPortionOfOperatingLeaseObligations_2023}

- ** Long Term Portion Of Derivative Liabilities: {LongTermPortionOfDerivativeLiabilities_2023}

- ** Non Operating Non Current Liabilities: {NonOperatingNonCurrentLiabilities_2023}

- ** Long Term Portion Of Loans From Related Companies: {LongTermPortionOfLoansFromRelatedCompanies_2023}

- ** Long Term Portion Of Deferred Federal Income Tax: {LongTermPortionOfDeferredFederalIncomeTax_2023}


 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING
 
 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total NON-CURRENT LIABILTIES  and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block]  and nothing else. JSON to be structured as follows:



{{
    "NonCurrentLiabilities": {{
        "LongTermBankDebt": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfOperatingLeaseObligations": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDerivativeLiabilities": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "NonOperatingNonCurrentLiabilities": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfLoansFromRelatedCompanies": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDeferredFederalIncomeTax": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNonCurrentLiabilities": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
        
    }}
}}

""",
    "net_worth_2022": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2022:

 

1. **Total net worth**: Accurately determine the company's total net worth for the year 2022.Validate if it is equal to {TotalNetWorth_2022}, if not update it to match the total net worth in the document

 

2. **Breakdown of Total net worth **: Decompose the TOTAL NET WORTH into the following 3 subcomponents. Ensure that the sum of these components equals the TOTAL NET WORTH:

** Common Stock

** Paid In Capital

** Retained Earnings

3. ** Validate the values for the 3 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical:

** Common Stock: {CommonStock_2022}

** Paid In Capital: {PaidInCapital_2022}

** Retained Earnings: {RetainedEarnings_2022}



 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING






 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total NET WORTH and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block]  and nothing else. JSON to be structured as follows:



{{
    "NetWorth": {{
        "CommonStock": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "PaidInCapital": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "RetainedEarnings": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNetWorth": {{
            "year": 2022,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
        
    }}
}}


""",
    "net_worth_2023": """**Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract, calculate and validate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year 2023:

 

1. **Total net worth**: Accurately determine the company's total net worth for the year 2023.Validate if it is equal to {TotalNetWorth_2023}, if not update it to match the total net worth in the document

 

2. **Breakdown of Total net worth **: Decompose the TOTAL NET WORTH into the following 3 subcomponents. Ensure that the sum of these components equals the TOTAL NET WORTH:

** Common Stock

** Paid In Capital

** Retained Earnings


3. ** Validate the values for the 3 subcomponents and update them if they are wrong. Ensure that you do not hallucinate while doing this. Accuracy is critical:

** Common Stock: {CommonStock_2023}

** Paid In Capital: {PaidInCapital_2023}

** Retained Earnings: {RetainedEarnings_2023}


 

IN GENERAL, THE ITEMS ARE ALL MUTUALLY EXCLUSIVE AND NON-OVERLAPPING



 

 

**Requirements**:

- **Terminology Interpretation**: Be aware that the terms used in the financial statements may not directly match the terms listed above. You must recognize equivalent terms or descriptions and accurately map them to the required categories.

- **Calculation and Derivation**: Some values may need to be derived through calculations based on the information provided in the financial statements or notes. You should perform these calculations accurately.

- **Expertise**: Leverage your expert knowledge in financial accounting to make informed decisions when interpreting and categorizing the data.

- **Accuracy**: It is crucial that you do not hallucinate or make assumptions beyond the provided data. If certain information is not explicitly stated or cannot be accurately derived, indicate that the information is unavailable.

 

**Output**: Provide the total NET WORTH and a detailed breakdown into the specified subcomponents, ensuring that all values are based on accurate interpretation and calculation of the data from the financial statements and notes.

OUTPUT FORMAT: only a JSON [without code block]  and nothing else. JSON to be structured as follows:



{{
    "NetWorth": {{
        "CommonStock": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "PaidInCapital": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "RetainedEarnings": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNetWorth": {{
            "year": 2023,
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
        
    }}
}}


"""
}
