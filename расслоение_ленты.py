import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


t0 = 0.0
azim0 = 45
elev0 = 20

u_curve = np.linspace(0, 4*np.pi, 800)   
v_strip = np.linspace(-1, 1, 60)

fig = plt.figure(figsize=(10, 6))

ax3d = fig.add_subplot(111, projection='3d')
ax3d.set_title("Лента Мёбиуса и слой")
ax3d.set_box_aspect([1, 1, 0.5])
ax3d.view_init(elev=elev0, azim=azim0)
ax3d.set_axis_off()

U, V = np.meshgrid(np.linspace(0, 2*np.pi, 300), v_strip)

X = (1 + (V/2)*np.cos(U/2)) * np.cos(U)
Y = (1 + (V/2)*np.cos(U/2)) * np.sin(U)
Z = (V/2) * np.sin(U/2)

ax3d.plot_surface(X, Y, Z, color='lightgray', alpha=0.75, linewidth=0)

def mobius_curve(t):
    v0 = 2*t - 1
    x = (1 + (v0/2)*np.cos(u_curve/2)) * np.cos(u_curve)
    y = (1 + (v0/2)*np.cos(u_curve/2)) * np.sin(u_curve)
    z = (v0/2) * np.sin(u_curve/2)
    return x, y, z

x, y, z = mobius_curve(t0)
curve, = ax3d.plot(x, y, z, color='red', linewidth=2)

t_text = fig.text(0.5, 0.20, f"t = {t0:.3f}", ha='center', fontsize=12)
nik_text = fig.text(0.5, 0.25, "@LyudmilaSutotskaya", ha='center', fontsize=12)

ax_t = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_azim = plt.axes([0.2, 0.11, 0.6, 0.03])
ax_elev = plt.axes([0.2, 0.07, 0.6, 0.03])

slider_t = Slider(ax_t, 't', 0.0, 1.0, valinit=t0)
slider_azim = Slider(ax_azim, 'azim', 0, 360, valinit=azim0)
slider_elev = Slider(ax_elev, 'elev', -90, 90, valinit=elev0)

def update(val):
    t = slider_t.val
    azim = slider_azim.val
    elev = slider_elev.val

    x, y, z = mobius_curve(t)
    curve.set_data(x, y)
    curve.set_3d_properties(z)

    ax3d.view_init(elev=elev, azim=azim)

    t_text.set_text(f"t = {t:.3f}")
    fig.canvas.draw_idle()

slider_t.on_changed(update)
slider_azim.on_changed(update)
slider_elev.on_changed(update)

plt.subplots_adjust(bottom=0.18)
plt.show()
