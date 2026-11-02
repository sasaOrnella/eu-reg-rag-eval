"""Tracks API spend and stops the run when the budget cap is reached."""

from src.config import BUDGET_CAP_USD, PRICES_USD_PER_M_TOKENS


class BudgetExceeded(RuntimeError):
    pass


class CostTracker:
    def __init__(self, cap_usd: float = BUDGET_CAP_USD, prices: dict | None = None):
        self.cap_usd = cap_usd
        self.prices = prices if prices is not None else PRICES_USD_PER_M_TOKENS
        self.total_usd = 0.0
        self.log: list[dict] = []

    def add(self, model: str, input_tokens: int, output_tokens: int) -> float:
        if model not in self.prices:
            raise KeyError(f"No price configured for model '{model}'. Edit src/config.py.")
        p = self.prices[model]
        cost = (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
        self.total_usd += cost
        self.log.append({"model": model, "in": input_tokens, "out": output_tokens, "usd": cost})
        if self.total_usd > self.cap_usd:
            raise BudgetExceeded(f"Spent ${self.total_usd:.2f}, cap is ${self.cap_usd:.2f}")
        return cost
