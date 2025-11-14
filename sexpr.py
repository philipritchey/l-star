from typing import Any

class sexpr:
  def __init__(self, name: str):
    self.name: str = name
    self.left: sexpr | None
    self.right: sexpr | None

  def __str__(self) -> str:
    if self.left is None:
      return f"{self.name}"
    if self.right is None:
      return f"({self.name} {self.left})"
    return f"({self.name} {self.left} {self.right})"

  def __eq__(self, other: Any) -> bool:
    return str(self) == str(other)
