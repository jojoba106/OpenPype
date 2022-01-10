from Qt import QtWidgets, QtCore


class HelpButton(QtWidgets.QFrame):
    """Widget that catch left mouse click and can trigger a callback.

    Callback is defined by overriding `_mouse_release_callback`.
    """
    clicked = QtCore.Signal()

    def __init__(self, parent):
        super(HelpButton, self).__init__(parent)

        self._mouse_pressed = False
        self._mouse_hover = False

        self._label_variants = [
            "( ? )>  ",
            "( ? ) > ",
            "( ? )  >",
        ]
        self._default_variant = self._label_variants[0]
        self._variant_iterator = self._iter_over_variants()

        label = QtWidgets.QLabel(self._default_variant, self)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(label)

        variant_change_timer = QtCore.QTimer()
        variant_change_timer.setInterval(200)
        variant_change_timer.timeout.connect(self._on_update_variant)

        self._variant_change_timer = variant_change_timer
        self._label = label

    def _iter_over_variants(self):
        while True:
            for variant in self._label_variants:
                yield variant

    def _on_update_variant(self):
        if not self._mouse_hover:
            self._variant_change_timer.stop()
            self._label.setText(self._default_variant)
        else:
            variant = next(self._variant_iterator)
            self._label.setText(variant)

    def enterEvent(self, event):
        super().enterEvent(event)
        self._mouse_hover = True
        self._variant_change_timer.start()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._mouse_hover = False

    def _mouse_release_callback(self):
        self.clicked.emit()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_pressed = True
        super(HelpButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._mouse_pressed:
            self._mouse_pressed = False
            if self.rect().contains(event.pos()):
                self._mouse_release_callback()

        super(HelpButton, self).mouseReleaseEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        content_widget = QtWidgets.QWidget(self)

        left_side = QtWidgets.QWidget(content_widget)

        left_label = QtWidgets.QLabel("Left side", left_side)

        left_side_layout = QtWidgets.QVBoxLayout(left_side)
        left_side_layout.addWidget(left_label)

        ridght_side = QtWidgets.QWidget(content_widget)

        right_label = QtWidgets.QLabel("Right side", ridght_side)

        ridght_side_layout = QtWidgets.QVBoxLayout(ridght_side)
        ridght_side_layout.addWidget(right_label)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(left_side, 1)
        top_layout.addWidget(ridght_side, 1)

        close_btn = QtWidgets.QPushButton("Close", content_widget)

        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(close_btn, 0)

        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addLayout(top_layout, 1)
        content_layout.addLayout(bottom_layout, 0)

        help_widget = QtWidgets.QWidget(self)
        top_label = QtWidgets.QLabel("TOP", help_widget)
        bottom_label = QtWidgets.QLabel(
            "This is very very long label (inside).", help_widget
        )
        help_layout = QtWidgets.QVBoxLayout(help_widget)
        help_layout.setContentsMargins(0, 0, 0, 0)
        help_layout.addWidget(top_label, 0)
        help_layout.addWidget(bottom_label, 0)
        help_layout.addStretch(1)

        help_widget.setVisible(False)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(content_widget, 1)
        layout.addWidget(help_widget, 0)

        help_btn = HelpButton(self)

        help_btn.clicked.connect(self._on_help_btn)

        self._help_btn = help_btn
        self._help_widget = help_widget
        self._content_widget = content_widget

    def _on_help_btn(self):
        size = self.size()
        window_size = self.size()
        now_visible = self._help_widget.isVisible()
        if self._help_widget.isVisible():
            window_width = size.width() - self.layout().spacing()
            width = window_width - self._help_widget.width()

        else:
            window_width = size.width() + self.layout().spacing()
            width = window_width + self._help_widget.sizeHint().width()
        size.setWidth(width)
        window_size.setWidth(window_width)

        self.resize(window_size)
        self._help_widget.setVisible(not now_visible)
        QtWidgets.QApplication.processEvents()
        self.resize(size)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    app.exec_()
