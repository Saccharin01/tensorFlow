from dataclasses import dataclass
import json

@dataclass
class UserInput:
  region : str
  image: str