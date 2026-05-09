import numpy as np
import matplotlib.pyplot as plt
from ripser import ripser

# ------------------------------------------------------------
# Dados: nuvem de pontos aproximadamente circular
# ------------------------------------------------------------
np.random.seed(4)

n = 40
theta = np.linspace(0, 2*np.pi, n, endpoint=False)

X = np.column_stack([
    np.cos(theta),
    np.sin(theta)
])

# Pequeno ruído para evitar simetria perfeita
X += 0.05*np.random.randn(n, 2)

# ------------------------------------------------------------
# Homologia persistente até dimensão 1
# ------------------------------------------------------------
result = ripser(X, maxdim=1)
dgms = result["dgms"]

H0 = dgms[0]
H1 = dgms[1]

# Para desenhar barras infinitas, escolhemos um corte visual
finite_deaths = np.concatenate([
    H0[np.isfinite(H0[:, 1]), 1],
    H1[np.isfinite(H1[:, 1]), 1]
])
xmax = max(finite_deaths) * 1.15

# ------------------------------------------------------------
# Figura com três painéis
# ------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))

# Painel A: nuvem de pontos
ax = axes[0]
ax.scatter(X[:, 0], X[:, 1], s=22)
ax.set_aspect("equal")
ax.set_title("(A) Nuvem de pontos")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

# Painel B: código de barras
ax = axes[1]
y = 0

# Barras de H0
for birth, death in H0:
    if np.isinf(death):
        death = xmax
    ax.plot([birth, death], [y, y], linewidth=1.6)
    y += 1

# Separador visual
ax.axhline(y + 0.5, linestyle="--", linewidth=0.8)
ax.text(xmax*0.98, y + 1.0, "$H_0$", ha="right", va="bottom")

y += 2

# Barras de H1
h1_start_y = y
for birth, death in H1:
    if np.isinf(death):
        death = xmax
    ax.plot([birth, death], [y, y], linewidth=2.2)
    y += 1

ax.text(xmax*0.98, h1_start_y + 0.3, "$H_1$", ha="right", va="bottom")

ax.set_xlim(0, xmax)
ax.set_ylim(-1, y + 1)
ax.set_title("(B) Código de barras")
ax.set_xlabel("parâmetro de escala")
ax.set_ylabel("classes")

# Painel C: diagrama de persistência
ax = axes[2]

# Diagonal
ax.plot([0, xmax], [0, xmax], linestyle="--", linewidth=1)

# Pontos H0 finitos
H0_finite = H0[np.isfinite(H0[:, 1])]
ax.scatter(H0_finite[:, 0], H0_finite[:, 1], s=22, label="$H_0$")

# Pontos H1 finitos
H1_finite = H1[np.isfinite(H1[:, 1])]
ax.scatter(H1_finite[:, 0], H1_finite[:, 1], s=35, label="$H_1$")

ax.set_xlim(0, xmax)
ax.set_ylim(0, xmax)
ax.set_aspect("equal")
ax.set_title("(C) Diagrama de persistência")
ax.set_xlabel("nascimento")
ax.set_ylabel("morte")
ax.legend(frameon=False)

plt.tight_layout()
plt.savefig("fig_barcode_diagrama_persistencia.png", dpi=300, bbox_inches="tight")
plt.show()