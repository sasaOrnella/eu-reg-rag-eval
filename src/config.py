"""Project-wide settings.

Fill in the prices from your API provider's pricing page before running experiments.
Prices change, so always check the official page. Unit: USD per 1M tokens.
"""

PRICES_USD_PER_M_TOKENS = {
    # "model-name": {"input": 0.0, "output": 0.0},
    "example-model": {"input": 0.0, "output": 0.0},  # TODO(you): replace with real values
}

BUDGET_CAP_USD = 40.0  # hard cap for the whole experiment series; adjust deliberately
