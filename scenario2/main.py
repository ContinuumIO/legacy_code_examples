from os.path import dirname, join

import numpy as np
import scipy.fftpack as ftp
import pandas as pd
import fwrapper

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBox, VBoxForm
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.sampledata.movies_data import movie_path

axis_map = {
    "Time": "x",
    "Signal": "y",
}

# Create Input controls
signal = TextInput(title="Add your signal here!")
noise = Slider(title="Noise added to signal", start=0, end=10, value=0, step=1)
t_axis = Select(title="Time", options=sorted({"Time": "x"}), value="Time")
f_axis = Select(title="Frequency", options=sorted({"Frequency": "f"}), value="Frequency")
y_axis = Select(title="Signal", options=sorted({"Signal": "y"}), value="Signal")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], dft=[], f=[], color=[]))

hover = HoverTool(tooltips=[
    ("Time","@x"),
    ("Signal", "@y"),
])

hover2 = HoverTool(tooltips=[
    ("Frequency","@f"),
    ("Signal", "@dft"),
])


p = Figure(plot_height=400, plot_width=800, title="", toolbar_location=None, tools=[hover])
p.line(x="x", y="y", source=source, color="blue")
p.circle(x="x", y="y", source=source, color="blue")

dftp = Figure(plot_height=400, plot_width=800, title="", toolbar_location=None, tools=[hover2])
dftp.line(x="f", y="dft", source=source, color="green")

def acquire_signal_and_dft():
    txt = signal.value
    nse = noise.value
    size = 200
    x = np.linspace(0, 4, size)
    dt = x[1] - x[0]

    y = np.zeros(size)
    F = np.zeros(size)
    w = np.zeros(size)

    if nse:
        some_noise = float(nse)*np.random.random_sample(size)
        y += some_noise

    if txt:
        #Put y in existence
        txt = 'z = ' + txt
        cur_locs = locals()
        cur_globals = globals()
        exec(txt, cur_globals, cur_locs)
        y = y + cur_locs['z']
        #scipyF = np.abs(ftp.rfft(y))
        Freal, Fimg = fwrapper.dft(y, np.zeros(size), size)
        F = np.abs(extract_real_dft(Freal, Fimg))
        w = ftp.rfftfreq(size, dt)

    plt_df = pd.DataFrame(data={"x":x, "y":y, 'dft':F, 'f':w, "color":['blue']*size})
    return plt_df

def update(attrname, old, new):
    df = acquire_signal_and_dft()
    x_name = axis_map[t_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = t_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title = "Signal" 
    source.data = dict(
        x=df.x,
        y=df.y,
        dft=df.dft,
        f=df.f,
    )

def extract_real_dft(freal, fimg):
    N = freal.shape[0] # N is even
    ans = np.zeros(N)
    if N % 2 == 0: # N is even
        real_idx = np.array(range(0,N//2 + 1))
        img_idx = np.array(range(1,N//2))

        ans_idx_real = np.array([0] + list(range(1,N,2)))
        ans_idx_img = np.array(range(2,N-1,2))
    else:
        real_idx = np.array(range(0,N//2 + 1))
        img_idx = np.array(range(1,N//2 + 1))

        ans_idx_real = np.array([0] + list(range(1,N,2)))
        ans_idx_img = np.array(range(2,N+1,2))

    ans[ans_idx_real] = freal[real_idx]
    ans[ans_idx_img] = fimg[img_idx]
    return ans




controls = [signal, noise]
for control in controls:
    control.on_change('value', update)

inputs = HBox(VBoxForm(*controls), width=300)

plots = VBox(p, dftp)

update(None, None, None) # initial load of the data

curdoc().add_root(HBox(inputs, plots, width=1100))
