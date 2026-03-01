from dataclasses import dataclass


@dataclass(frozen=True)
class TransitionRequest:
    source: str
    target_top: object
    target_sub: object
    reason: str