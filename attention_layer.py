from typing import Optional
import torch
from misc import identity
# TODO: reimplement these layers
from fairscale.nn.model_parallel.layers import ParallelEmbedding, RowParallelLinear, ColumnParallelLinear
# TODO: look into this class
import fairscale.nn.model_parallel.initialize as fs_init
from torch import Tensor
from args import Args

class AttentionLayer(torch.nn.Module):
  def __init__(self, args: Args):
    self._args = args
    self._local_heads_count = args.head_count // fs_init.get_model_parallel_world_size()
    # $W_i^Q \in \mathbb R^{d_\mathrm{model} \times d_k}$
    self._wq = ColumnParallelLinear(
      args.input_dimension,
      args.head_count * self.head_dimension,
      bias = False,
      gather_output = False,
      init_method = identity
    )

    # W_i^K \in R^{d_\mathrm{model} \times d_k}$
    self._wk = ColumnParallelLinear(
      args.input_dimension,
      args.head_count * self.head_dimension,
      bias = False,
      gather_output = False,
      init_method = identity
    )
    # W_i^V \in R^{d_\mathrm{model} \times d_k}$
    self._wv = ColumnParallelLinear(
      args.input_dimension,
      args.head_count * self.head_dimension,
      bias = False,
      gather_output = False,
      init_method = identity
    )

    # W^O \in R^{hd_v \times d_\mathrm{model}}$
    self._wo = RowParallelLinear(
      args.head_count * self.head_dimension,
      args.input_dimension,
      bias = False,
      input_is_parallel = True,
      init_method = identity
    )
  # freqs refers to the frequencies generated by $PE_{(pos, 2i)} = \sin{(\frac{pos}{10000^{2i/d_\mathrm{model}}})}
  # mask is those values that correspond to illegal connections, in order to preserve the auto-regressive property
  def forward(self, x: Tensor, start_position: int, freqs: Tensor, mask: Optional[Tensor]):
    batch_size, sequence_length = x.shape
    # get the x_q, x_k, x_v projection values from the parameter matrices
    xq, xk, xv = self._wq(x), self._wk(x), self._wv(x)
    # TODO: what do these lines do?
    # Appears to reshape the projection values into the batch size without changing the tensor size in memory
    # Why can't we store these in memory in the desired shape by default? This is done on every forward pass??
    xq, xk, xv = [ projection_value.view(batch_size, sequence_length, self.n_local_heads) for projection_value in [ xq, xk, xv] ]
    raise NotImplementedError("AttentionLayer.forward(...) is unimplemented.")




    