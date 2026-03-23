from __future__ import annotations

from typing import Any

import pandas as pd

from vaiiixbr.config import Settings
from vaiiixbr.risk import RiskManager


class PaperTrader:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.risk = RiskManager(settings)
        self.position: dict[str, Any] | None = None
        self.cash = settings.paper_initial_cash
        self.equity = settings.paper_initial_cash

    def step(self, prepared: pd.DataFrame, signal: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
        last = prepared.iloc[-1]
        timestamp = str(prepared.index[-1])
        event = "aguardando"
        closed_trade = None

        if self.position is None and signal.get("decision") == "compra":
            plan = self.risk.build_long_plan(float(last["close"]), float(last["atr"]), self.cash)
            if plan:
                self.position = {
                    "entry_time": timestamp,
                    "entry": plan.entry,
                    "stop": plan.stop,
                    "target": plan.target,
                    "quantity": plan.quantity,
                    "score": signal.get("long_score", 0),
                }
                event = "paper_buy"
        elif self.position is not None:
            low = float(last["low"])
            high = float(last["high"])
            if low <= float(self.position["stop"]):
                exit_price = float(self.position["stop"])
                outcome = "stop"
            elif high >= float(self.position["target"]):
                exit_price = float(self.position["target"])
                outcome = "target"
            else:
                exit_price = None
                outcome = "holding"

            if exit_price is not None:
                pnl = (exit_price - float(self.position["entry"])) * float(self.position["quantity"])
                self.cash += pnl
                self.equity = self.cash
                closed_trade = {
                    "entry_time": self.position["entry_time"],
                    "exit_time": timestamp,
                    "entry_price": float(self.position["entry"]),
                    "exit_price": exit_price,
                    "stop_price": float(self.position["stop"]),
                    "target_price": float(self.position["target"]),
                    "quantity": float(self.position["quantity"]),
                    "pnl": pnl,
                    "outcome": outcome,
                    "score": int(self.position["score"]),
                }
                self.position = None
                event = f"paper_exit_{outcome}"
            else:
                mtm = (float(last["close"]) - float(self.position["entry"])) * float(self.position["quantity"])
                self.equity = self.cash + mtm
                event = "paper_holding"

        state = {
            "paper_event": event,
            "paper_cash": round(self.cash, 2),
            "paper_equity": round(self.equity, 2),
            "paper_in_position": self.position is not None,
        }
        return state, closed_trade
