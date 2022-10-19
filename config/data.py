from dataclasses import dataclass, field
import yaml


@dataclass
class DataLoader():
    path: str = "./config.yaml"
    data: dict = field(init=False)

    def load_data(self):
        with open(self.path) as f:
            self.data = yaml.safe_load(f)
        return self.data
