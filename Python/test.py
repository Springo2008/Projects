import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# points to visualize: some vectors in the plane
pts = np.array([
    1+0j, 0.6+0.8j, -0.7+0.3j, -0.4-0.9j, 0.2-0.6j
])
rotated = 1j * pts  # multiply by i

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_aspect('equal')
ax.set_title("Multiplication by e^{iθ} (animation) — final θ = π/2 is multiplication by i")

# plot original points as arrows
orig_arrows = []
for z in pts:
    arr = ax.arrow(0, 0, z.real, z.imag, head_width=0.05, length_includes_head=True, color='C0', alpha=0.8)
    orig_arrows.append(arr)
# placeholders for rotated arrows
rot_plots = []
for _ in pts:
    p, = ax.plot([], [], 'o', color='C1')
    rot_plots.append(p)

def update(frame):
    theta = (frame / 120) * (np.pi/2)  # 0 -> π/2
    rot = np.exp(1j * theta) * pts
    for p, z in zip(rot_plots, rot):
        p.set_data(z.real, z.imag)
    ax.set_xlabel(f'θ = {theta:.3f} rad')
    return rot_plots

anim = FuncAnimation(fig, update, frames=121, interval=30, blit=False)
# To display in Jupyter: from IPython.display import HTML; HTML(anim.to_jshtml())
# To save (requires ffmpeg or imagemagick): anim.save('rotate_by_i.gif', writer='imagemagick', fps=30)
plt.show()