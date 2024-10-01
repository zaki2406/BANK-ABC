import json

d='''{
    "CurrentAssets": {
        "Cash": {
            "year": 2023,
            "value": "194.2",
            "TerminologyInterpretation": "Cash and cash equivalents",
            "CalculationRequired": "false"
        },
        "TradeReceivables": {
            "year": 2023,
            "value": "10.4",
            "TerminologyInterpretation": "Trade receivables",
            "CalculationRequired": "false"
        },
        "OtherNonTradeReceivables": {
            "year": 2023,
            "value": "31.5",
            "TerminologyInterpretation": "Other receivables",
            "CalculationRequired": "false"
        },
        "FinishedGoods": {
            "year": 2023,
            "value": "33.5",
            "TerminologyInterpretation": "Inventories",
            "CalculationRequired": "false"
        },
        "CurrentPortionOfPrepaidAndDeferredAssets": {
            "year": 2023,
            "value": "9.6",
            "TerminologyInterpretation": "Prepayments",
            "CalculationRequired": "false"
        },
        "TotalCurrentAssets": {
            "year": 2023,
            "value": "280.0",
            "TerminologyInterpretation": "Total current assets",
            "CalculationRequired": "false"
        }
    }
}'''
data = json.loads(d)
for key in data:
    print(f"Top-level key: {key}")
    sub_dict = data[key]
    for sub_key in sub_dict:
        print(f"  Sub-key: {sub_key}")
        print(f"    Content: {sub_dict[sub_key]}")


import json

# Sample JSON data
data = {
    "CurrentAssets": {
        "Cash": {
            "year": 2022,
            "value": "65.6",
            "TerminologyInterpretation": "false",
            "CalculationRequired": "false"
        },
        "TradeReceivables": {
            "year": 2022,
            "value": "6.4",
            "TerminologyInterpretation": "false",
            "CalculationRequired": "frealse"
        },
        "OtherNonTradeReceivables": {
            "year": 2022,
            "value": "9.1",
            "TerminologyInterpretation": "false",
            "CalculationRequired": "false"
        },
        "FinishedGoods": {
            "year": 2022,
            "value": "11.5",
            "TerminologyInterpretation": "true",
            "CalculationRequired": "false"
        },
        "CurrentPortionOfPrepaidAndDeferredAssets": {
            "year": 2022,
            "value": "2.4",
            "TerminologyInterpretation": "true",
            "CalculationRequired": "false"
        },
        "TotalCurrentAssets": {
            "year": 2022,
            "value": "95.0",
            "TerminologyInterpretation": "true",
            "CalculationRequired": "true"
        }
    }
}

# Keys to include in the sum
keys_to_sum = [
    "Cash",
    "TradeReceivables",
    "OtherNonTradeReceivables",
    "FinishedGoods",
    "CurrentPortionOfPrepaidAndDeferredAssets"
]

# Calculate the sum
total = sum(float(data["CurrentAssets"][key]["value"]) for key in keys_to_sum if key in data["CurrentAssets"])

print("Total:", total)


