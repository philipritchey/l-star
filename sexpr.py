class sexpr:
  def __init__(self, name: str):
    self.name: str = name
    self.left: sexpr = None
    self.right: sexpr = None

  def __str__(self) -> str:
    if not self.left:
      return f"{self.name}"
    if not self.right:
      return f"({self.name} {self.left})"
    return f"({self.name} {self.left} {self.right})"

  def __eq__(self, other) -> bool:
    return str(self) == str(other)

