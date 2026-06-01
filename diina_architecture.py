python
import torch
import torch.nn as nn
import torch.nn.functional as F
‌
class DynamicInhibitionModule(nn.Module):
"""
DIINA Core: Mimics Bilingual Inhibitory Control.
Calculates a gate (gamma) to suppress noise in low-resource data.
"""
def __init__(self, hidden_size):
super(DynamicInhibitionModule, self).__init__()
self.W_gamma = nn.Linear(hidden_size, 1)
self.V_gamma = nn.Linear(hidden_size, 1)
self.bias_gamma = nn.Parameter(torch.zeros(1))
self.sigmoid = nn.Sigmoid()
‌
def forward(self, rep_i, rep_j):
# rep_i: Query representation, rep_j: Key representation
# Implementing gamma_ij = sigma(W*h_i + V*h_j + b)
wq = self.W_gamma(rep_i).unsqueeze(2)  # (batch, seq_len, 1, 1)
vk = self.V_gamma(rep_j).unsqueeze(1)  # (batch, 1, seq_len, 1)
‌
combined = wq + vk + self.bias_gamma
gamma_ij = self.sigmoid(combined).squeeze(-1) # (batch, seq_len, seq_len)
return gamma_ij
‌
class DIINAMultiHeadAttention(nn.Module):
def __init__(self, hidden_size, num_heads):
super(DIINAMultiHeadAttention, self).__init__()
self.num_heads = num_heads
self.head_dim = hidden_size // num_heads
self.scale = self.head_dim ** -0.5
‌
self.q_linear = nn.Linear(hidden_size, hidden_size)
self.k_linear = nn.Linear(hidden_size, hidden_size)
self.v_linear = nn.Linear(hidden_size, hidden_size)
self.out_linear = nn.Linear(hidden_size, hidden_size)
‌
# Dynamic Inhibition Module for each head
self.inhibition_module = DynamicInhibitionModule(self.head_dim)
‌
def forward(self, x):
batch_size, seq_len, hidden_size = x.size()
‌
# 1. Linear projections
q = self.q_linear(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
k = self.k_linear(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
v = self.v_linear(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
‌
# 2. Standard Attention Scores
attn_scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale
alpha_ij = F.softmax(attn_scores, dim=-1)
‌
# 3. Apply Dynamic Inhibition (The DIINA Innovation)
# We compute the gate based on Q and K of each head
# Reshaping to match the pairwise computation in the module
inhibited_outputs = []
for i in range(self.num_heads):
q_head = q[:, i, :, :]
k_head = k[:, i, :, :]
v_head = v[:, i, :, :]
‌
# Compute gamma gate for this head
gamma_ij = self.inhibition_module(q_head, k_head)
‌
# alpha'_ij = gamma_ij * alpha_ij
inhibited_alpha = gamma_ij * alpha_ij[:, i, :, :]
‌
# Compute final head output
head_out = torch.matmul(inhibited_alpha, v_head)
inhibited_outputs.append(head_out)
‌
# 4. Concatenate and Project
out = torch.cat(inhibited_outputs, dim=-1)
return self.out_linear(out)
‌
# Example Usage for Yoruba NLP Task:
# model = DIINAMultiHeadAttention(hidden_size=768, num_heads=12)
# input_tokens = torch.randn(32, 128, 768) # (Batch, Seq_Len, Hidden)
# output = model(input_tokens)
