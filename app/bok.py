from datetime import datetime


from bokeh.layouts import gridplot
from bokeh.plotting import ColumnDataSource, figure, curdoc
import controllers
import dao

arduinoEndpoint = dao.ArduinoDAO("Arduino Data Access Object")
arduinoController = controllers.ArduinoController(arduinoEndpoint)

# LIGHT
light_cds = ColumnDataSource({'x': [], 'y': []})
light_plot = figure(name="light",
                    y_axis_label='lumens',
                    x_axis_type="datetime",
                    width=700,
                    plot_height=225)

light_plot.x_range.follow = "end"
light_plot.x_range.follow_interval = 600000     # 10 minutes
light_plot.x_range.range_padding = 0

light_plot.line(x='x', y='y', source=light_cds, line_width=3, line_color='khaki', line_join='bevel')
light_plot.circle(x='x', y='y', source=light_cds, size=4, fill_color='khaki', line_color='khaki')


# TEMPERATURE
temp_cds = ColumnDataSource({'x': [], 'y': []})
temp_plot = figure(name="temperature",
                   y_axis_label='Farenheit',
                   x_axis_type="datetime",
                   width=700,
                   plot_height=225,
                   x_range=light_plot.x_range)

temp_plot.line(x='x', y='y', source=temp_cds, line_width=3, line_color='red', line_join='bevel')
temp_plot.circle(x='x', y='y', source=temp_cds, size=4, fill_color='red', line_color='red')


# MOISTURE
moisture_cds = ColumnDataSource({'x': [], 'y': []})
moisture_plot = figure(name="moisture",
                       y_axis_label='drops',
                       x_axis_type="datetime",
                       width=700,
                       plot_height=225,
                       x_range=light_plot.x_range)

moisture_plot.line(x='x', y='y', source=moisture_cds, line_width=3, line_color='blue', line_join='bevel')
moisture_plot.circle(x='x', y='y', source=moisture_cds, size=4, fill_color='blue', line_color='blue')


plot = gridplot([[light_plot], [temp_plot], [moisture_plot]], merge_tools=True)


def update():
    now = datetime.now()
    now = now.replace(microsecond=0)
    light_lvl, temp_lvl, moisture_lvl = None, None, None
    x = next(iter(arduinoController.readArduino()))
    light_lvl = {'x': [now], 'y': [x.illuminance]}
    temp_lvl = {'x': [now], 'y': [x.temperature['f']]}
    moisture_lvl = {'x': [now], 'y': [x.soilMoisture]}

    light_cds.stream(light_lvl)
    temp_cds.stream(temp_lvl)
    moisture_cds.stream(moisture_lvl)


# show the results
curdoc().add_periodic_callback(update, 1000)
curdoc().add_root(plot)
