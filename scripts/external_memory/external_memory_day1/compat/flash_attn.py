"""Lightweight flash-attn compatibility shim for feasibility experiments.

This module implements the small subset of the flash-attn API that
Matrix-Game-2 uses during inference. It falls back to PyTorch scaled dot
product attention so we can validate the pipeline on machines without the
flash-attn wheel.
"""

from __future__ import annotations

from typing import Iterable

import torch
import torch.nn.functional as F


def _match_kv_heads(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    if q.shape[2] == k.shape[2]:
        return k, v
    if q.shape[2] % k.shape[2] != 0:
        raise ValueError(
            f"Incompatible head counts: q={q.shape[2]}, k={k.shape[2]}"
        )
    repeat = q.shape[2] // k.shape[2]
    return k.repeat_interleave(repeat, dim=2), v.repeat_interleave(repeat, dim=2)


def _as_cu_list(cu_seqlens: torch.Tensor | Iterable[int]) -> list[int]:
    if isinstance(cu_seqlens, torch.Tensor):
        return [int(x) for x in cu_seqlens.detach().cpu().tolist()]
    return [int(x) for x in cu_seqlens]


def flash_attn_func(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    dropout_p: float = 0.0,
    softmax_scale: float | None = None,
    causal: bool = False,
    window_size=(-1, -1),
    deterministic: bool = False,
    **_: object,
) -> torch.Tensor:
    del window_size, deterministic
    k, v = _match_kv_heads(q, k, v)

    q_t = q.permute(0, 2, 1, 3)
    k_t = k.permute(0, 2, 1, 3)
    v_t = v.permute(0, 2, 1, 3)
    scale = softmax_scale if softmax_scale is not None else None

    out = F.scaled_dot_product_attention(
        q_t,
        k_t,
        v_t,
        attn_mask=None,
        dropout_p=dropout_p,
        is_causal=causal,
        scale=scale,
    )
    return out.permute(0, 2, 1, 3).contiguous()


def flash_attn_varlen_func(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    cu_seqlens_q,
    cu_seqlens_k,
    max_seqlen_q: int,
    max_seqlen_k: int,
    dropout_p: float = 0.0,
    softmax_scale: float | None = None,
    causal: bool = False,
    window_size=(-1, -1),
    deterministic: bool = False,
    **_: object,
) -> torch.Tensor:
    del max_seqlen_q, max_seqlen_k, window_size, deterministic
    q_offsets = _as_cu_list(cu_seqlens_q)
    k_offsets = _as_cu_list(cu_seqlens_k)

    outputs = []
    for i in range(len(q_offsets) - 1):
        q_start, q_end = q_offsets[i], q_offsets[i + 1]
        k_start, k_end = k_offsets[i], k_offsets[i + 1]
        q_i = q[q_start:q_end].unsqueeze(0)
        k_i = k[k_start:k_end].unsqueeze(0)
        v_i = v[k_start:k_end].unsqueeze(0)
        out_i = flash_attn_func(
            q_i,
            k_i,
            v_i,
            dropout_p=dropout_p,
            softmax_scale=softmax_scale,
            causal=causal,
        )
        outputs.append(out_i.squeeze(0))

    return torch.cat(outputs, dim=0)
