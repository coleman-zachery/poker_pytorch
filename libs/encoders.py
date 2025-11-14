from libs.constants import RANKS, SUITS
import torch
import torch.nn as nn
import torch.nn.functional as F

class CardEncoder(nn.Module):
    def __init__(self, ranks=len(RANKS), suits=len(SUITS), rank_dim=8, suit_dim=4, output_dim=16):
        super().__init__()
        self.rank_emb = nn.Embedding(ranks, rank_dim)
        self.suit_emb = nn.Embedding(suits, suit_dim)
        self.fc = nn.Linear(suit_dim + rank_dim, output_dim)

    def forward(self, card_tensor):
        rank_tensor = card_tensor[:, 0]
        suit_tensor = card_tensor[:, 1]
        rank_emb = self.rank_emb(rank_tensor)
        suit_emb = self.suit_emb(suit_tensor)
        combined = torch.cat((rank_emb, suit_emb), dim=-1)
        output = self.fc(combined)
        return output

class PokerHandClassifier(nn.Module):
    def __init__(self, input_dim=16, hidden_dim=32, num_classes=11):
        super().__init__()
        self.fc1 = nn.Linear(input_dim * 5, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, hand_tensor):
        batch_size = hand_tensor.size(0)
        hand_flat = hand_tensor.view(batch_size, -1)
        x = F.relu(self.fc1(hand_flat))
        output = self.fc2(x)
        return output

################################################################
################################################################

class PokerHandClassifier_WithAttention(nn.Module):
    def __init__(self, input_dim=16, hidden_dim=32, num_classes=11, num_heads=4):
        super().__init__()
        # self-attention layer lets cards "interact"
        self.attn = nn.MultiheadAttention(embed_dim=input_dim, num_heads=num_heads, batch_first=True)
        
        # optional feedforward layer after attention
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, hand_tensor):
        # hand_tensor: (batch, num_cards, input_dim)
        attn_output, _ = self.attn(hand_tensor, hand_tensor, hand_tensor)
        
        # permutation-invariant pooling (mean or sum)
        pooled = attn_output.mean(dim=1)  # (batch, input_dim)
        
        x = F.relu(self.fc1(pooled))
        output = self.fc2(x)
        return output

################################################################
################################################################

class PokerHandClassifier_SelfAttention(nn.Module):
    def __init__(self, input_dim=16, hidden_dim=32, num_classes=11, num_heads=4, num_layers=2):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.MultiheadAttention(embed_dim=input_dim, num_heads=num_heads, batch_first=True)
            for _ in range(num_layers)
        ])
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, hand_tensor):
        x = hand_tensor
        for attn in self.layers:
            attn_out, _ = attn(x, x, x)
            x = x + attn_out  # residual connection
        pooled = x.mean(dim=1)
        x = F.relu(self.fc1(pooled))
        return self.fc2(x)

################################################################
################################################################

class AttentionPooling(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.attn = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        # x: (batch, num_cards, input_dim)
        attn_scores = self.attn(x)                 # (batch, num_cards, 1)
        attn_weights = torch.softmax(attn_scores, dim=1)
        pooled = torch.sum(attn_weights * x, dim=1)  # weighted sum (batch, input_dim)
        return pooled

class PokerHandClassifier_AttentionPooling(nn.Module):
    def __init__(self, input_dim=16, hidden_dim=32, num_classes=11):
        super().__init__()
        self.pool = AttentionPooling(input_dim, hidden_dim)
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, hand_tensor):
        pooled = self.pool(hand_tensor)
        x = F.relu(self.fc1(pooled))
        return self.fc2(x)

################################################################
################################################################

class SAB(nn.Module):
    def __init__(self, dim_in, dim_out, num_heads=4):
        super().__init__()
        self.mha = nn.MultiheadAttention(embed_dim=dim_out, num_heads=num_heads, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(dim_out, dim_out * 2),
            nn.ReLU(),
            nn.Linear(dim_out * 2, dim_out),
        )
        self.ln1 = nn.LayerNorm(dim_out)
        self.ln2 = nn.LayerNorm(dim_out)
        self.proj = nn.Linear(dim_in, dim_out) if dim_in != dim_out else nn.Identity()

    def forward(self, x):
        # Project to match MHA input dimension if necessary
        x_proj = self.proj(x)
        attn_out, _ = self.mha(x_proj, x_proj, x_proj)
        x = self.ln1(x_proj + attn_out)
        ff_out = self.fc(x)
        return self.ln2(x + ff_out)

class PMA(nn.Module):
    def __init__(self, dim, num_heads=4, num_seeds=1):
        super().__init__()
        self.seed_vectors = nn.Parameter(torch.randn(num_seeds, dim))
        self.mha = nn.MultiheadAttention(embed_dim=dim, num_heads=num_heads, batch_first=True)

    def forward(self, x):
        batch_size = x.size(0)
        seed = self.seed_vectors.unsqueeze(0).repeat(batch_size, 1, 1)  # (B, num_seeds, dim)
        out, _ = self.mha(seed, x, x)
        return out  # (B, num_seeds, dim)

class PokerHandClassifier_SetTransformer(nn.Module):
    def __init__(self, input_dim=16, dim_hidden=32, num_heads=4, num_classes=11):
        super().__init__()
        self.sab1 = SAB(input_dim, dim_hidden, num_heads)
        self.sab2 = SAB(dim_hidden, dim_hidden, num_heads)
        self.pma = PMA(dim_hidden, num_heads, num_seeds=1)
        self.fc = nn.Sequential(
            nn.Linear(dim_hidden, dim_hidden),
            nn.ReLU(),
            nn.Linear(dim_hidden, num_classes),
        )

    def forward(self, hand_tensor):
        # hand_tensor: (batch, num_cards, input_dim)
        x = self.sab1(hand_tensor)
        x = self.sab2(x)
        x = self.pma(x).squeeze(1)  # (batch, dim_hidden)
        return self.fc(x)