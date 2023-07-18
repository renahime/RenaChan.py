from dataclasses import dataclass,field

@dataclass
class Session:
    data: dict = field(default_factory=dict)
    is_active: bool = False
    start_time: int = 0

    def get_stats(self):
        return "hi"

    def get_weekly(self):
        return "hi"
