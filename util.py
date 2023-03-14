from typing import Tuple
from torch import Tensor
import torch

def apply_rotary_embedding(query_vector: Tensor, key_vector: Tensor, frequency_cis: Tensor) -> Tuple[Tensor, Tensor]:
  "Applies rotary embeddings to the query and key vectors, which are then used in the subsequent dot product attention computation. The rotary embeddings add a positional encoding to the query and key vectors, allowing the model to better capture the relative position of tokens in the sequence."

  # reshape the key and query vectors into complex-valued tensors (i.e. those where the last dimension represents the real and imaginary parts of each elements), as alternating values are real and complex respectively.
  query_vector_ = torch.view_as_complex(query_vector.float().reshape(*query_vector.shape[:-1], -1, 2))
  key_vector_ = torch.view_as_complex(key_vector.float().reshape(*key_vector.shape[:-1], -1, 2))
  # reshape the frequencies to match the dimensions of query_vector_ and key_vector_
  frequency_cis_ = frequency_cis.view(*[ d if i == 1 or i == frequency_cis.ndim - 1 else 1 for i, d in enumerate(frequency_cis.shape)])
  
  # apply rotary embedding
  query_vector_ = torch.view_as_real(query_vector_ * frequency_cis_).flatten(3)
  key_vector_ = torch.view_as_real(key_vector_ * frequency_cis_).flatten(3)
  # retype the tenors
  query_vector_ = query_vector.type_as(query_vector)
  key_vector_ = key_vector.type_as(key_vector)
  return (query_vector_, key_vector_)


