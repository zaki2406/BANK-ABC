original_promts=[''' **Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract and calculate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year  {year1}:

 

1. **Total current assets**: Accurately determine the company's total CURRENT ASSETS for the year {year1}.

 

2. **Breakdown of Total CURRENT ASSETS **: Decompose the total CURRENT ASSETS into the following 5 subcomponents. Ensure that the sum of these components equals the total CURRENT ASSETS:

** Cash

** Trade Receivables

** Other (Non-Trade) Receivables

** Finished Goods

** Current Portion Of Prepaid And Deferred Assets

  

 

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
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TradeReceivables": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherNonTradeReceivables": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "FinishedGoods": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfPrepaidAndDeferredAssets": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalCurrentAssets": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
    }}
}}
''',''' **Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract and calculate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year {year1}:

 

1. **Total current liabilities**: Accurately determine the company's total CURRENT LIABILITIES for the year {year1}.

 

2. **Breakdown of Total CURRENT LIABILITIES **: Decompose the total CURRENT LIABILITIES into the following 7 subcomponents. Ensure that the sum of these components equals the total CURRENT LIABILITIES:

   - **Short-Term Loans Payable**

   - **Current Portion Of Operating Lease Obligations**

   - **Trade Accounts Payable**

   - **Other Accruals**

   - **Other Taxes Payable**

   - **Income Taxes Payable**

   - **Current Portion Of Derivative Liabilities**

 

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
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfOperatingLeaseObligations": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TradeAccountsPayable": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherAccruals": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OtherTaxesPayable": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "IncomeTaxesPayable": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "CurrentPortionOfDerivativeLiabilities": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalCurrentLiabilities": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
    }}
}}

 ''',''' **Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract and calculate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year {year1}:

 

1. **Total Non-Current Assets**: Accurately determine the company's total non-current assets for the year {year1}.

 

2. **Breakdown of Total Non-Current Assets**: Decompose the total non-current assets into the following eight subcomponents. Ensure that the sum of these components equals the total non-current assets:

   - **Construction In Progress**

   - **Machinery And Equipment** NOT COUNTING DEPRECIATION AND IMPAIRMENT (i.e. before deducting depreciation and impairment)

   - **Operating Leases**

   - **Accumulated Depreciation And Impairment** [negative value]

   - **long term portion of Derivative Assets**

   - **Non-Operating Non-Current Assets**

   - **Intangible Assets** NOT COUNTING AMORTIZATION AND IMPAIRMENT

   - **Accumulated Amortization And Impairment** [negative value]

 

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
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "MachineryAndEquipment": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "OperatingLeases": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "AccumulatedDepreciationAndImpairment": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDerivativeAssets": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "NonoperatingNoncurrentAssets": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "IntangibleAssets": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "AccumulatedAmortizationAndImpairment": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNonCurrentAssets": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        
    }}
}}


  ''',''' **Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract and calculate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year {year1}:

 

1. **Total non-current liabilities**: Accurately determine the company's total NON-CURRENT LIABILITIES for the year {year1}.

 

2. **Breakdown of Total NON-CURRENT LIABILITIES **: Decompose the total NON-CURRENT LIABILITIES into the following 6 subcomponents. Ensure that the sum of these components equals the total NON-CURRENT LIABILITIES:

 - ** Long Term Bank Debt

- ** long term portion of Operating Lease Obligations

- ** Long Term Portion Of Derivative Liabilities

- ** Non Operating Non Current Liabilities (INCLUDING UNCATEGORISED NON CURRENT AND NON OPERATING LIABILITIES AND OBLIGATIONS)

- ** Long Term Portion Of Loans From Related Companies

- ** Long Term Portion Of Deferred Federal Income Tax

 

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
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfOperatingLeaseObligations": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDerivativeLiabilities": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "NonOperatingNonCurrentLiabilities": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfLoansFromRelatedCompanies": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "LongTermPortionOfDeferredFederalIncomeTax": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNonCurrentLiabilities": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
        
    }}
}}

''',''' **Role**: You are an expert financial analyst and accountant with specialized knowledge in financial statement analysis and financial accounting. Your task is to accurately extract and calculate specific financial values from a company's financial statements and the accompanying notes.

 

**Task**: Your primary responsibility is to determine the following financial metrics from the company's balance sheet for the year {year1}:

 

1. **Total net worth**: Accurately determine the company's total net worth for the year {year1}.

 

2. **Breakdown of Total net worth **: Decompose the TOTAL NET WORTH into the following 3 subcomponents. Ensure that the sum of these components equals the TOTAL NET WORTH:

** Common Stock

** Paid In Capital

** Retained Earnings

 

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
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "PaidInCapital": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "RetainedEarnings": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }},
        "TotalNetWorth": {{
            "year": {year1},
            "value": "<value>",
            "TerminologyInterpretation": "<true/false>",
            "CalculationRequired": "<true/false>"
        }}
        
        
    }}
}}


''']