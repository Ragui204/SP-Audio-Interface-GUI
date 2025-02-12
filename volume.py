from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QDial,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QFrame,
    QSpacerItem
)
from PyQt5.QtCore import Qt


def add_volume_controls(layout):
    """
    Adds volume controls and other plugin controls to the layout.
    """
    main_layout = QHBoxLayout()  # Use QHBoxLayout for horizontal arrangement
    main_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
    
    # Reverb
# In the add_volume_controls function

    # Reverb
    reverb_layout = QVBoxLayout()

    # Create a container widget for the reverb box
    reverb_container = QWidget()
    reverb_container.setStyleSheet("background-color: #555;")  # Example color: dark gray

    # Add the reverb layout to the container
    reverb_container.setLayout(reverb_layout)

    reverb_label = QLabel("Reverb")
    reverb_label.setAlignment(Qt.AlignCenter)
    reverb_layout.addWidget(reverb_label)
    reverb_layout.addItem(QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))
    reverb_grid = QGridLayout()
    add_plugin(reverb_grid, "Decay", 0, 0)
    add_plugin(reverb_grid, "Size", 0, 1)
    add_plugin(reverb_grid, "Mix", 0, 2)
    add_plugin(reverb_grid, "Color", 1, 0)
    add_plugin(reverb_grid, "Mod", 1, 1)
    add_plugin(reverb_grid, "Speed", 1, 2)
    reverb_layout.addLayout(reverb_grid)

    # Add the reverb container to the main layout
    main_layout.addWidget(reverb_container)  # Add reverb first
    main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))      

    # Add divider
    divider = QFrame()
    divider.setFrameShape(QFrame.VLine)
    divider.setFrameShadow(QFrame.Sunken)
    main_layout.addWidget(divider)

    # Volume Controls
    volume_layout = QVBoxLayout()
    volume_layout.setAlignment(Qt.AlignCenter)

    # Create a container widget for the volume box
    volume_container = QWidget()
    volume_container.setStyleSheet("background-color: #555;")  # Example color: dark gray
    volume_container.setLayout(volume_layout)  # Add the volume layout to the container

    volume_label = QLabel("Volume")
    volume_label.setAlignment(Qt.AlignCenter)
    volume_knob = QDial()
    volume_knob.setFixedSize(300, 300)
    #volume_knob.setMaximum(300)
    #volume_knob.setValue(50)
    volume_knob.setNotchesVisible(True)
    volume_layout.addWidget(volume_label)
    volume_layout.addWidget(volume_knob)

    # Add the volume container to the main layout
    main_layout.addWidget(volume_container)  # Add volume in the middle
    main_layout.addItem(QSpacerItem(0,0, QSizePolicy.Fixed, QSizePolicy.Minimum))

    # Add divider
    divider = QFrame()
    divider.setFrameShape(QFrame.VLine)
    divider.setFrameShadow(QFrame.Sunken)
    divider.setLineWidth(0)  # Set the line width to 5 pixels
    main_layout.addWidget(divider)

    # Delay
    delay_layout = QVBoxLayout()

    # Create a container widget for the delay box
    delay_container = QWidget()
    delay_container.setStyleSheet("background-color: #555;")  # Example color: dark gray
    delay_container.setLayout(delay_layout)  # Add the delay layout to the container

    delay_label = QLabel("Delay")
    delay_label.setAlignment(Qt.AlignCenter)
    delay_layout.addWidget(delay_label)
    delay_layout.addItem(QSpacerItem(50, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))
    delay_grid = QGridLayout()
    add_plugin(delay_grid, "Time", 0, 0)
    add_plugin(delay_grid, "Feedback", 0, 1)
    add_plugin(delay_grid, "Mix", 0, 2)
    add_plugin(delay_grid, "Color", 1, 0)
    add_plugin(delay_grid, "Mod", 1, 1)
    delay_layout.addLayout(delay_grid)

    # Add the delay container to the main layout
    main_layout.addWidget(delay_container)  # Add delay last

    layout.addLayout(main_layout)
    layout.setAlignment(main_layout, Qt.AlignTop | Qt.AlignRight)


def add_plugin(layout, name, row, col):
    """Helper function to add a plugin with dial knob"""
    vbox = QVBoxLayout()
    label = QLabel(name)
    label.setAlignment(Qt.AlignCenter)
    dial = QDial()
    dial.setFixedSize(200, 270)
    dial.setMinimum(0)
    dial.setMaximum(100)
    dial.setValue(50)
    dial.setNotchesVisible(True)

    # Add shadow effect using stylesheet
    dial.setStyleSheet("""
        QDial {
            border: 5px solid #5c5c5c;  /* Add a border for better visibility */
            border-radius: 50px;  /* Adjust border-radius as needed */
        }
        QDial::handle {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                              stop:0 #ffffff, stop:1 #c0c0c0);  /* Light gray gradient */
            border: 1px solid #5c5c5c;
            width: 20px;
            height: 20px;
            margin: -5px 0;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #888888;  /* Add a drop shadow */
        }
    """)

    vbox.addWidget(label)
    vbox.addWidget(dial)
    layout.addLayout(vbox, row, col)