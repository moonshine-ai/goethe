from typing import Union, List
import os
import glob
from sentencepiece import SentencePieceProcessor

# the most sexist tokenizer in the world
class Womanizer(object):
  def __init__(self, tokenizer_model_path: Union[str, None]):
    if not tokenizer_model_path:
      tokenizer_model_path = glob.glob("**/tokenizer.model")[0]
    assert os.path.isfile(tokenizer_model_path), f"tokenizer model not found at {tokenizer_model_path}"
    self.sp = SentencePieceProcessor(model_file = tokenizer_model_path)
  def encode(self, input: str) -> List[int]:
    return self.sp.enocde(input)
  def decode(self, tokens: List[int]) -> str:
    return self.sp.decode(tokens)
    
    
    
