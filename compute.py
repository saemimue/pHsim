import numpy as np, pandas as pd, os, random
import pH_sim as p
import bokeh.plotting as plt
from bokeh.embed import components
from bokeh.palettes import Category10

psi = p.pH_calc()

def titrate(c_Ac, c_B, pKs_Ac, pKs_B, pKs_Tit):
    values = (c_Ac,  pKs_Ac, c_B, pKs_B, pKs_Tit)
    x, pH, a, b = psi.titration(values)
    print (len(x),len(pH))
    return x, pH

TOOLS = "reset, box_zoom, save, pan"
p = plt.figure(title="Acid/Base Titration Simulation",
        tools = TOOLS,
        toolbar_location = "above",
        x_axis_label = "increment",
        y_axis_label = "pH",
        plot_width = 500,
        plot_height = 500,
        )

def show(c_Ac, c_B, pKs_Ac, pKs_B, pKs_Tit,erase):
    global p
    if erase == "True":
        TOOLS = "reset, box_zoom, save, pan"
        p = plt.figure(title="Acid/Base Titration Simulation",
                tools = TOOLS,
                toolbar_location = "above",
                x_axis_label = "increment",
                y_axis_label = "pH",
                plot_width = 500,
                plot_height = 500,
                )
    col = random.choice(Category10[10])
    x, pH = titrate(c_Ac, c_B, pKs_Ac, pKs_B, pKs_Tit)
    p.line(x = x, y = pH,
            line_color=col,
            line_width=2,
            )
    p.circle(x, pH, color=col)
    script, div = components(p)
    head = """
    <link rel="stylesheet"
        href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.css"
        type="text/css" />
    <script type="text/javascript"
        src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.js">
    </script>
    <script type="text/javascript">
    Bokeh.set_log_level("info");
    </script>
    """
    return head, script, div


if __name__=='__main__':
    print("Used parameters were: c(Ac) = {}, c(B)= {} ,pKs(Ac) = {} "\
            "\npKs(B) = {}, pKs(Tit) = {}".format(
                c_Ac,
                C_B,
                pKs_Ac,
                pKs_B,
                pKs_Tit))
