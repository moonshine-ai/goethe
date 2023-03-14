class Args:
  head_count: int = 8
  input_dimension: int = 512
  max_sequence_length: int = 2048
  max_batch_size: int = 32

  # TODO: get rid of this unneeded `self`
  @property
  def head_dimension(self) -> int:
    return Args.input_dimension // Args.head_count
