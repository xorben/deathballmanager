from dataclasses import dataclass, field


@dataclass(frozen=True)
class Implant:
    name: str
    tier: int
    modifiers: dict[str, int] = field(default_factory=dict)