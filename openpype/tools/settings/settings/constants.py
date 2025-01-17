from Qt import QtCore


DEFAULT_PROJECT_LABEL = "< Default >"
PROJECT_NAME_ROLE = QtCore.Qt.UserRole + 1
PROJECT_IS_ACTIVE_ROLE = QtCore.Qt.UserRole + 2
PROJECT_IS_SELECTED_ROLE = QtCore.Qt.UserRole + 3


__all__ = (
    "DEFAULT_PROJECT_LABEL",

    "PROJECT_NAME_ROLE",
    "PROJECT_IS_ACTIVE_ROLE",
    "PROJECT_IS_SELECTED_ROLE"
)
