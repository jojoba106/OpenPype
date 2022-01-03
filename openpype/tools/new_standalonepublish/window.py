from Qt import QtWidgets, QtGui, QtCore

import avalon.api
from avalon.api import AvalonMongoDB
from openpype.hosts.new_standalonepublisher import (
    api as new_standalonepublisher
)

from openpype.tools.publisher import PublisherWindow
from openpype.tools.utils.constants import PROJECT_NAME_ROLE
from openpype.tools.utils.models import (
    ProjectModel,
    ProjectSortFilterProxy
)


class StandaloneOverlayWidget(QtWidgets.QFrame):
    def __init__(self, publisher_window):
        super(StandaloneOverlayWidget, self).__init__(publisher_window)
        self.setObjectName("OverlayFrame")

        # Care about parent changes of size
        publisher_window.installEventFilter(self)

        # Create db connection for projects model
        dbcon = AvalonMongoDB()
        dbcon.install()

        header_label = QtWidgets.QLabel("Select project", self)
        # Create project models and view
        projects_model = ProjectModel(dbcon)
        projects_proxy = ProjectSortFilterProxy()
        projects_proxy.setSourceModel(projects_model)

        projects_view = QtWidgets.QListView(self)
        projects_view.setModel(projects_proxy)
        projects_view.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        confirm_btn = QtWidgets.QPushButton("Choose", self)
        btns_layout = QtWidgets.QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(confirm_btn, 0)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(header_label, 0, 1, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(projects_view, 1, 1)
        layout.addLayout(btns_layout, 2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)

        projects_view.doubleClicked.connect(self._on_double_click)
        confirm_btn.clicked.connect(self._on_confirm_click)

        self._projects_view = projects_view
        self._projects_model = projects_model
        self._confirm_btn = confirm_btn

        self._publisher_window = publisher_window

    def eventFilter(self, obj, event):
        if isinstance(event, QtGui.QResizeEvent):
            self._resize_to_parent_size()
        return False

    def _resize_to_parent_size(self):
        self.resize(
            self._publisher_window.width(),
            self._publisher_window.height()
        )

    def showEvent(self, event):
        self._projects_model.refresh()
        super(StandaloneOverlayWidget, self).showEvent(event)

    def _on_double_click(self):
        self.set_selected_project()

    def _on_confirm_click(self):
        self.set_selected_project()

    def set_selected_project(self):
        index = self._projects_view.currentIndex()

        project_name = index.data(PROJECT_NAME_ROLE)
        if not project_name:
            return

        new_standalonepublisher.save_project_name(project_name)
        self.setVisible(False)
        self._publisher_window.removeEventFilter(self)
        self._publisher_window.reset()


def main():
    avalon.api.install(new_standalonepublisher)

    app = QtWidgets.QApplication([])
    window = PublisherWindow(reset_on_show=False)
    overlay_widget = StandaloneOverlayWidget(window)
    window.show()
    app.exec_()
