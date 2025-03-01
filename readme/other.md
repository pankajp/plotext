# Other Plots
- [Error Plot](https://github.com/piccolomo/plotext/blob/master/readme/other.md#error-plot)
- [Event Plot](https://github.com/piccolomo/plotext/blob/master/readme/other.md#event-plot)
- [Extra Line Plot](https://github.com/piccolomo/plotext/blob/master/readme/other.md#estra-line-plot)
- [Text Plot](https://github.com/piccolomo/plotext/blob/master/readme/other.md#text-plot)

[Main Guide](https://github.com/piccolomo/plotext#guide)


## Error Plot
To plot data with error bars, along both the `x` and `y` axes use the `error()` function as in this example:

```python
import plotext as plt
from random import random 
l = 20
n = 1
ye = [random() * n for i in range(l)]; xe = [random() * n for i in range(l)]
y = plt.sin(length = l); 
plt.error(y, xerr = xe, yerr = ye)
plt.title('Error Plot')
plt.show()
```
or directly on terminal:
```console
python3 -c "import plotext as plt; plt.clf();  from random import random; l = 20; n = 1; ye = [random() * n for i in range(l)]; xe = [random() * n for i in range(l)]; y = plt.sin(length = l); plt.error(y, xerr = xe, yerr = ye); plt.title('Error Plot'); plt.show();"
```
![datetime](https://raw.githubusercontent.com/piccolomo/plotext/master/data/error.png)
- Optionally also the x coordinates could be provided,
- the documentation of the `error()` function can be accessed with `doc.error()`.

[Main Guide](https://github.com/piccolomo/plotext#guide), [Other Plots](https://github.com/piccolomo/plotext/blob/master/readme/other.md)


## Event Plot
To signal the timing of certain events, `eventplot()` function could be of use. Here is an example:

```python
import plotext as plt
from random import randint
from datetime import datetime, timedelta

plt.date_form("H:M") # also "H" looks ok

times = [datetime(2022, 3, 27, randint(0, 23), randint(0, 59), randint(0, 59)) for i in range(100)] # A random list of times during the day
times = plt.datetimes_to_string(times)

plt.plotsize(None, 20) # Set the height you prefer or comment for maximum size 

plt.eventplot(times)

plt.show()
```
or directly on terminal:
```console
python3 -c "import plotext as plt; from random import randint; from datetime import datetime, timedelta; plt.date_form('H:M'); times = [datetime(2022, 3, 27, randint(0, 23), randint(0, 59), randint(0, 59)) for i in range(100)]; times = plt.datetimes_to_string(times); plt.plotsize(None, 20); plt.eventplot(times); plt.show()"
```

![datetime](https://raw.githubusercontent.com/piccolomo/plotext/master/data/eventplot.png)

The documentation of the `eventplot()` function can be accessed with `doc.eventplot()`.

[Main Guide](https://github.com/piccolomo/plotext#guide), [Other Plots](https://github.com/piccolomo/plotext/blob/master/readme/other.md)


## Extra Line Plot
To plot extra vertical or horizontal lines use the functions `horizontal_line()` - `hline()` in short - and `vertical_line()` - `vline()` in short.

```python
import plotext as plt
y = plt.sin() 
plt.scatter(y)
plt.title("Extra Lines")
plt.vline(100, "magenta")
plt.hline(0.5, "blue+")
plt.plotsize(100, 30)
plt.show()
```
or directly on terminal:
```console
python3 -c "import plotext as plt; y = plt.sin(); plt.scatter(y); plt.title('Extra Lines'); plt.vline(100, 'magenta'); plt.hline(0.5, 'blue+'); plt.plotsize(100, 30); plt.show()"
```

![datetime](https://raw.githubusercontent.com/piccolomo/plotext/master/data/extralines.png)

- Note that `vertical_line()` and `horizontal_line()` accept as coordinates numbers, date/time strings or bar labels, if the plot allows it,
- The documentation of the `vertical_line()` and `horizontal_line()` functions can be accessed with `doc.vertical_line()` and `doc.horizontal_line()`.

[Main Guide](https://github.com/piccolomo/plotext#guide), [Other Plots](https://github.com/piccolomo/plotext/blob/master/readme/other.md)


## Text Plot
To add text to a plot use the `text()` function. Here is how to use it for a labelled bar plot:
 
```python
import plotext as plt

pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
percentages = [14, 36, 11, 8, 7, 4]

plt.bar(pizzas, percentages)
plt.title("Labelled Bar Plot using Text()")

[plt.text(pizzas[i], x = pizzas[i], y = percentages[i] + 1.5, alignment = 'center', color = 'red') for i in range(len(pizzas))]
plt.ylim(0, 38)
plt.plotsize(100, 30)
plt.show()
```

or directly on terminal:
```console
python3 -c "import plotext as plt; pizzas = ['Sausage', 'Pepperoni', 'Mushrooms', 'Cheese', 'Chicken', 'Beef']; percentages = [14, 36, 11, 8, 7, 4]; plt.bar(pizzas, percentages); plt.title('Labelled Bar Plot using Text()'); [plt.text(pizzas[i], x = pizzas[i], y = percentages[i] + 1.5, alignment = 'center', color = 'red') for i in range(len(pizzas))]; plt.ylim(0, 38); plt.plotsize(100, 30); plt.show()"
```

![datetime](https://raw.githubusercontent.com/piccolomo/plotext/master/data/labelled-bar.png)

- note that `text()` accepts as coordinates numbers, date/time strings or bar labels, if the plot allows it,
- the full documentation of the `text()` function can be accessed with `doc.text()`.

[Main Guide](https://github.com/piccolomo/plotext#guide), [Other Plots](https://github.com/piccolomo/plotext/blob/master/readme/other.md)
