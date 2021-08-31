import tkinter
import math

##### 'CALCULATE' BUTTON #####

def calc_button_clicked():

    # Value for the radio button selection
    choice = selection.get()

    # Regardless of radio selection, convert the input to perimeter side 1 for all calculations
    # Use a string version of perimeter for text displays. Use a float version for calculations

    # If Sides radio button selected:
    if choice == 1:
        peri_float_1 = abs(float(side_input_1.get().replace(',', '')))
        peri_float_2 = abs(float(side_input_2.get().replace(',', '')))

    # If Perimeter radio button is selected:
    elif choice == 2:
        peri_float_1 = abs(float(perimeter_input.get().replace(',', ''))) / 4
        peri_float_2 = peri_float_1
        
    # If Area radio button selected:
    elif choice == 3:
        peri_float_1 = math.sqrt(abs(float(area_input.get().replace(',', ''))))
        peri_float_2 = peri_float_1

    # String calculations for all parameters. Use perimeter to calculate all values. Set decimal precision
    # to whatever user specifies in input
    precision = decimal_input.get()
    side_input_1.delete(0, 'end')
    side_input_1.insert(0, f'{peri_float_1:,.{precision}f}')
    side_input_2.delete(0, 'end')
    side_input_2.insert(0, f'{peri_float_2:,.{precision}f}')
    perimeter_input.delete(0, 'end')
    perimeter_input.insert(0, f'{2 * (peri_float_1 + peri_float_2):,.{precision}f}')
    area_input.delete(0, 'end')
    area_input.insert(0, f'{peri_float_1 * peri_float_2:,.{precision}f}')

    # Clear the canvas. This will allow for any previous shapes to be removed.
    # Then redraw the axes and origin coordinates
    canvas.delete('all')
    draw_axes()

    # Set the perimeter strings to match the float equivalents with decimal precision
    peri_str_1 = f'{peri_float_1:,.{precision}f}'
    peri_str_2 = f'{peri_float_2:,.{precision}f}'



    ##### SCALING #####
    
    # Only perform scaling if both sides are not 0
    if peri_float_1 != 0 and peri_float_2 != 0:

        # If both sides are equal
        if peri_float_1 == peri_float_2:

            # If side 1 is < 200 or > 600, scale accordingly
            if peri_float_1 < 200:
                draw_coords(peri_float_1 / 2)
                peri_float_1 = 200
                peri_float_2 = 200
            elif peri_float_1 > 600:
                draw_coords(peri_float_1 / 2)
                peri_float_1 = 600
                peri_float_2 = 600
            else:
                draw_coords()

        #  If both sides are not equal
        else:

            # Create boolean so that the correct side is scaled. This is because, in some cases, a side will be
            # less than 200 but the other side will be more than 600, meaning both scales would be applicable.
            # In this case, only one (the latter vertical side) will scale.
            scale_horizontal = False
            scale_vertical = False

            # If side 1 is < side 2
            if peri_float_1 < peri_float_2:

                # If side 1 is < 200, enable horizontal scaling
                if peri_float_1 < 200:
                    original_x = peri_float_1
                    original_y = peri_float_2
                    ratio = peri_float_2 / peri_float_1
                    peri_float_1 = 200
                    peri_float_2 = 200 * ratio
                    scale_horizontal = True

                # If side 2 is > 600, enable vertical scaling.
                # Disable horizontal scaling, if any
                if peri_float_2 > 600:
                    # Only scale the original_y value if horizontal scaling has not
                    # been activated
                    if not scale_horizontal:
                        original_y = peri_float_2
                    ratio = peri_float_2 / 600
                    peri_float_2 = 600
                    peri_float_1 /= ratio
                    scale_horizontal = False
                    scale_vertical = True

            # Else, if side 2 is > side 1
            elif peri_float_2 < peri_float_1:

                # If side 2 is > 600, enable vertical scaling
                if peri_float_2 < 200:
                    original_x = peri_float_1
                    original_y = peri_float_2
                    ratio = peri_float_1 / peri_float_2
                    peri_float_2 = 200
                    peri_float_1 = 200 * ratio
                    scale_vertical = True

                # If side 1 is < 200, enable horizontal scaling
                # Disable vertical scaling, if any
                if peri_float_1 > 600:
                    # Only scale the original_x value if vertical scaling has not
                    # been activated
                    if not scale_vertical:
                        original_x = peri_float_1
                    ratio = peri_float_1 / 600
                    peri_float_1 = 600
                    peri_float_2 /= ratio
                    scale_horizontal = True
                    scale_vertical = False

            # If either scaling is enabled (and only one can be enabled), draw rectangle and scale
            # accordingly. Else, draw rectangle with default scale (meaning both sides are: 200 <= x <= 600)
            if scale_horizontal:
                draw_coords(original_x / 2)
            elif scale_vertical:
                draw_coords(original_y / 2)
            else:
                draw_coords()

    # Draw the rectangle using perimeters. Perimeters must not be 0.
    # Send rectangle to lowest layer of canvas so axes are visible over it
    if peri_float_1 != 0 and peri_float_2 != 0:
        rect = canvas.create_rectangle(canvas_width / 2 - peri_float_1 / 2, canvas_height / 2 - peri_float_2 / 2, \
                                  canvas_width / 2 + peri_float_1 / 2, canvas_height / 2 + peri_float_2 / 2, \
                                  fill = 'lime green', outline = 'black')
        canvas.tag_lower(rect)
        
        # Draw the text for the x/y coordinates of perimeter tuples (starting bottom-right, running counter-clockwise)
        # Remove the commas in order for numbers to be accepted as floats, then re-add commas in strings for readability
        # Set precision based on user's precision input
        canvas.create_text(canvas_width / 2 + peri_float_1 / 2 + 5, canvas_height / 2 + peri_float_2 / 2 + 10, anchor = tkinter.NW, \
                           text = '(' + ('{:,.{p}f}'.format(float(peri_str_1.replace(',', '')) / 2, p = precision)) + ', -' \
                           + ('{:,.{p}f}'.format(float(peri_str_2.replace(',', '')) / 2, p = precision))+ ')', fill = 'gray')
        canvas.create_text(canvas_width / 2 + peri_float_1 / 2 + 5, canvas_height / 2 - peri_float_2 / 2 - 10, anchor = tkinter.SW, \
                           text = '(' + ('{:,.{p}f}'.format(float(peri_str_1.replace(',', '')) / 2, p = precision)) + ', ' \
                           + ('{:,.{p}f}'.format(float(peri_str_2.replace(',', '')) / 2, p = precision)) + ')', fill = 'gray')
        canvas.create_text(canvas_width / 2 - peri_float_1 / 2 - 5, canvas_height / 2 - peri_float_2 / 2 - 10, anchor = tkinter.SE, \
                           text = '(-' + ('{:,.{p}f}'.format(float(peri_str_1.replace(',', '')) / 2, p = precision)) + ', ' \
                           + ('{:,.{p}f}'.format(float(peri_str_2.replace(',', '')) / 2, p = precision)) + ')', fill = 'gray')
        canvas.create_text(canvas_width / 2 - peri_float_1 / 2 - 5, canvas_height / 2 + peri_float_2 / 2 + 10, anchor = tkinter.NE, \
                           text = '(-' + ('{:,.{p}f}'.format(float(peri_str_1.replace(',', '')) / 2, p = precision)) + ', -' \
                           + ('{:,.{p}f}'.format(float(peri_str_2.replace(',', '')) / 2, p = precision)) + ')', fill = 'gray')

    canvas.pack()



##### 'CLEAR' BUTTON #####

def clear_button_clicked():

    # Clear all values. Re-draw axes and coordinates
    canvas.delete('all')
    selection.set(1)
    side_input_1.delete(0, 'end')
    side_input_1.insert(0, '0')
    side_input_2.delete(0, 'end')
    side_input_2.insert(0, '0')
    perimeter_input.delete(0, 'end')
    perimeter_input.insert(0, '0')
    area_input.delete(0, 'end')
    area_input.insert(0, '0')
    decimal_input.delete(0, 'end')
    decimal_input.insert(0, '2')
    draw_axes()
    draw_coords(100)



##### DRAW AXES, ORIGIN COORDINATES, GRIDLINE MARKERS #####

def draw_axes():
    
    # Draw axes and origin coordinates
    canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, width = 1, fill='black')
    canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, width = 1, fill='black')
    canvas.create_text(canvas_width / 2 + 5, canvas_height / 2 + 10, anchor = tkinter.W, text = '(0, 0)')

    # Draw gridline markers
    x_gridlines = canvas_width / 8
    y_gridlines = canvas_height / 8
    for num in range(7):
        canvas.create_line(x_gridlines, canvas_height / 2 - 10, \
                           x_gridlines, canvas_height / 2 + 10, fill = 'black')
        canvas.create_line(canvas_width / 2 - 10, y_gridlines, \
                           canvas_width / 2 + 10, y_gridlines, fill = 'black')
        x_gridlines += canvas_width / 8
        y_gridlines += canvas_height / 8



##### DRAW GRID COORDINATES #####

def draw_coords(length = 100):

    # If (side / 2) is <= 100, rightmost coordinate will be 3 * (side / 2). Otherwise, coordinate will be
    # the current set side / 2. This will allow coordinates to adapt to side size
    if length <= 100:
        grid_val = length * 3
    else:
        grid_val = length

    # x/y coordinates will be set to increments that 1/8 the size of the canvas
    grid_x_position = canvas_width - canvas_width / 8
    grid_y_position = 0 + canvas_height / 8

    # Set precision to current decimal input
    precision = decimal_input.get()

    # Run loop 7 times (skipping the middle coordinate), drawing the coordinates on screen. Then increment
    # the grid values accordingly 
    for num in range(7):
        if num != 3:
            canvas.create_text(grid_x_position, canvas_height / 2 + 20, text = f'{grid_val:,.{precision}f}')
            canvas.create_text(canvas_width / 2 + 30, grid_y_position, text = f'{grid_val:,.{precision}f}')
        grid_x_position -= canvas_width / 8
        grid_y_position += canvas_height / 8
        if length <= 100:
            grid_val -= length
        else:
            grid_val -= length / 3



##### MAIN FUNCTION #####
            
# Create main window. Set to full screen. Place window on top
window = tkinter.Toplevel()
window.geometry('%dx%d' % (window.winfo_screenwidth(), window.winfo_screenheight()))

# Set canvas width/height constants
canvas_width = 800
canvas_height = 800

# Create top frame & canvas, and bottom frame & button canvas
top_frame = tkinter.Frame(window, width = canvas_width, height = 1000)
top_frame.pack(side = 'top', pady = 10)
canvas = tkinter.Canvas(top_frame, width = canvas_width, height = canvas_height, bg = 'white', \
                        highlightbackground = 'black', highlightthickness = 1)
canvas.pack()
bottom_frame = tkinter.Frame(window, width = canvas_width, height = 100)
bottom_frame.pack(side = 'top', pady = 10)
bottom_frame.pack_propagate(0)
button_canvas = tkinter.Canvas(bottom_frame, width = canvas_width, height = 100, bg = 'lavender', \
                               highlightbackground = 'black', highlightthickness = 1)
button_canvas.pack()

# Draw default axes and default coordinates
draw_axes()



##### RADIO BUTTONS #####

selection = tkinter.IntVar()
selection.set(1)

selection_sides = tkinter.Radiobutton(bottom_frame, text = 'Sides', variable = selection, value = 1, bg = 'lavender')
selection_perimeter = tkinter.Radiobutton(bottom_frame, text = 'Perimeter', variable = selection, value = 2, bg = 'lavender')
selection_area = tkinter.Radiobutton(bottom_frame, text = 'Area', variable = selection, value = 3, bg = 'lavender')

selection_sides.place(x = 200, y = 15)
selection_perimeter.place(x = 200, y = 45)
selection_area.place(x = 200, y = 65)



##### USER INPUT AND BUTTONS #####

side_input_1 = tkinter.Entry(bottom_frame, width = 17, justify = 'right')
side_input_2 = tkinter.Entry(bottom_frame, width = 17, justify = 'right')
perimeter_input = tkinter.Entry(bottom_frame, width = 17, justify = 'right')
area_input = tkinter.Entry(bottom_frame, width = 17, justify = 'right')

# Insert a 0 in the user_input box. This will prevent error if user clicks 'Calculate' with a null value
side_input_1.insert(0, '0')
side_input_2.insert(0, '0')
perimeter_input.insert(0, '0')
area_input.insert(0, '0')

side_label_1 = tkinter.Label(bottom_frame, text = 'x: ', bg = 'lavender')
side_label_2 = tkinter.Label(bottom_frame, text = 'y: ', bg = 'lavender')
side_label_1.place(x = canvas_width  / 2 - 70, y = 10)
side_label_2.place(x = canvas_width  / 2 - 70, y = 30)
side_input_1.place(x = canvas_width / 2 - 50, y = 10)
side_input_2.place(x = canvas_width / 2 - 50, y = 30)
perimeter_input.place(x = canvas_width / 2 - 50, y = 50)
area_input.place(x = canvas_width / 2 - 50, y = 70)

# 'Calculate' button
calc_button = tkinter.Button(bottom_frame, text = 'Calculate', command = calc_button_clicked, height = 3, width = 8)
calc_button.place(x = canvas_width / 2 + 75, y = 20)

# 'Clear all' button
clear_button = tkinter.Button(bottom_frame, text = 'Clear all', command = clear_button_clicked, height = 3, width = 8)
clear_button.place(x = canvas_width / 2 + 150, y = 20)

# 'Back' button
back_button = tkinter.Button(bottom_frame, text = 'Back', command = lambda : window.destroy(), height = 3, width = 8)
back_button.place(x = 10, y = 20)

# Decimal precision input
decimal_label = tkinter.Label(bottom_frame, text = 'Dec. precision: ', bg = 'lavender')
decimal_label.place(x = canvas_width - 150, y = 10)
decimal_input = tkinter.Entry(bottom_frame, width = 5, justify = 'right')
decimal_input.insert(0, '2')
decimal_input.place(x = canvas_width - 50, y = 10)

# Draw default axes and default coordinates
draw_axes()
draw_coords(100)

# Run tkinter main loop
tkinter.mainloop()

