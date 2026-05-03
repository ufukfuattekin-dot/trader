"""Compute entry, stop loss, and take-profit using ATR-based volatility stops."""


def calculate_levels(signal, risk_reward=2.0, atr_multiplier=2.0):
    entry = signal["price"]
    stop = entry - (signal["atr"] * atr_multiplier)
    risk = entry - stop
    target = entry + (risk * risk_reward)

    return {
        **signal,
        "entry": entry,
        "stop_loss": stop,
        "take_profit": target,
        "stop_pct": ((stop - entry) / entry) * 100,
        "target_pct": ((target - entry) / entry) * 100,
        "risk_reward": risk_reward,
    }


def apply_risk(signals, risk_reward=2.0, atr_multiplier=2.0):
    return [calculate_levels(s, risk_reward, atr_multiplier) for s in signals]
