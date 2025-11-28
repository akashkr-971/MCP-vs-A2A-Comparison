import json
import random
from pathlib import Path

def generate_dataset(
    num_cases: int = 30,
    min_length: int = 5,
    max_length: int = 20,
    min_value: int = 1,
    max_value: int = 500
):
    """
    Generate a list of numeric arrays for analysis.
    This will be used by BOTH MCP and A2A experiments.
    """
    random.seed(42)  # so MCP and A2A see the exact same data
    dataset = []

    for _ in range(num_cases):
        length = random.randint(min_length, max_length)
        numbers = [random.randint(min_value, max_value) for _ in range(length)]
        dataset.append(numbers)

    return dataset


def main():
    data = generate_dataset()
    output_path = Path("common_dataset.json")
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Dataset generated and saved to {output_path.resolve()}")


if __name__ == "__main__":
    main()
