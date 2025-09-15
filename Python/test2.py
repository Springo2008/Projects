import numpy as np
import matplotlib.pyplot as plt

# sample the unit circle
thetas = np.linspace(-np.pi, np.pi, 201)
z_circle = np.exp(1j * thetas)
w_circle = z_circle ** (1j)  # principal branch used by numpy

# small grid in complex plane (avoid branch cut on negative real axis)
x = np.linspace(-2, 2, 41)
y = np.linspace(-2, 2, 41)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y
# avoid zeros and negative real axis where log has discontinuity; add tiny offset
Z += 1e-12
W = Z ** (1j)

fig, axes = plt.subplots(1, 2, figsize=(12,5))

# Left: original points (complex plane)
ax = axes[0]
ax.set_title("Original z-plane")
ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")
ax.set_aspect('equal')
ax.plot(z_circle.real, z_circle.imag, color='C0', label='unit circle')
ax.scatter((Z.real).ravel(), (Z.imag).ravel(), c=np.angle(Z).ravel(), cmap='hsv', s=8)
ax.legend()
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.grid(alpha=0.3)

# Right: images w = z^i (w-plane)
aw = axes[1]
aw.set_title("w-plane: w = z^i")
aw.set_xlabel("Re(w)")
aw.set_ylabel("Im(w)")
aw.set_aspect('equal')
# plot image of unit circle (these lie on the positive real axis)
aw.plot(w_circle.real, w_circle.imag, 'o', color='C1', label='image of unit circle')
# plot grid image colored by original angle to trace mapping
sc = aw.scatter(W.real.ravel(), W.imag.ravel(), c=np.angle(Z).ravel(), cmap='hsv', s=8)
aw.legend()
aw.grid(alpha=0.3)
fig.colorbar(sc, ax=aw, label='Arg(z) (color)')

plt.tight_layout()
plt.show()
