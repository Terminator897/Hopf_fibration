import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons



t_fiber = np.linspace(0, 2*np.pi, 500)
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]

fig = plt.figure(figsize=(14, 7))


ax_s2 = fig.add_subplot(121, projection='3d')
ax_s2.set_title("@LyudmilaSutotskaya")
x_s2 = np.cos(u) * np.sin(v)
y_s2 = np.sin(u) * np.sin(v)
z_s2 = np.cos(v)
ax_s2.plot_wireframe(x_s2, y_s2, z_s2, color='black', alpha=0.7, linewidth=0.5)
point_s2, = ax_s2.plot([0], [0], [1], 'ro', markersize=8, label='Точка отношения z1/z2')


ax_3d = fig.add_subplot(122, projection='3d')
ax_3d.set_title("Расслоение Хопфа")
limit = 4
ax_3d.set_xlim(-limit, limit)
ax_3d.set_ylim(-limit, limit)
ax_3d.set_zlim(-limit, limit)
ax_3d.set_axis_off()

fiber_line, = ax_3d.plot([], [], [], color='red', linewidth=3)
torus_lines = [ax_3d.plot([], [], [], color='blue', alpha=0.55, linewidth=1)[0] for _ in range(12)]

def get_hopf_fiber(theta, phi, family=1):
   

    denom = 1 - np.sin(theta) * np.sin(t_fiber)
    
    x = (np.cos(theta) * np.cos(phi + family * t_fiber)) / denom
    y = (np.cos(theta) * np.sin(phi + family * t_fiber)) / denom
    z = (np.sin(theta) * np.cos(t_fiber)) / denom
    return x, y, z


ax_theta = plt.axes([0.25, 0.1, 0.5, 0.03])
ax_phi   = plt.axes([0.25, 0.06, 0.5, 0.03])
ax_fam   = plt.axes([0.05, 0.4, 0.1, 0.15]) 

slider_theta = Slider(ax_theta, 'Широта θ', 0.01, np.pi-0.01, valinit=np.pi/4)
slider_phi   = Slider(ax_phi, 'Долгота φ', 0, 2*np.pi, valinit=0)
radio_fam = RadioButtons(ax_fam, ('Семейство A', 'Семейство B'))

def update(val):
    theta = slider_theta.val
    phi = slider_phi.val
    # vibor zakrutochki)
    fam_val = 1 if radio_fam.set_active == 'Семейство A' else -1
    if radio_fam.value_selected == 'Семейство B': fam_val = -1
    else: fam_val = 1
    
    
    ps_x = np.sin(theta) * np.cos(phi)
    ps_y = np.sin(theta) * np.sin(phi)
    ps_z = np.cos(theta)
    point_s2.set_data([ps_x], [ps_y])
    point_s2.set_3d_properties([ps_z])
    


    fx, fy, fz = get_hopf_fiber(theta, phi, family=fam_val)
    fiber_line.set_data(fx, fy)
    fiber_line.set_3d_properties(fz)
    
    
    phis = np.linspace(0, 2*np.pi, len(torus_lines), endpoint=False)
    for i, p in enumerate(phis):
        tx, ty, tz = get_hopf_fiber(theta, p, family=fam_val)
        torus_lines[i].set_data(tx, ty)
        torus_lines[i].set_3d_properties(tz)
    
    fig.canvas.draw_idle()

slider_theta.on_changed(update)
slider_phi.on_changed(update)
radio_fam.on_clicked(update)


update(None)
plt.show()