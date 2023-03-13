class Args:
  head_count: int = 8
  input_dimension: int = 512

  # TODO: get rid of this unneeded `self`
  @property
  def head_dimension(self) -> int:
    return Args.input_dimension // Args.head_count
