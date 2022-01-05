import re

from Qt import QtCore, QtGui


class TasksModel(QtGui.QStandardItemModel):
    """Tasks model.

    Task model must have set context of asset documents.

    Items in model are based on 0-infinite asset documents. Always contain
    an interserction of context asset tasks. When no assets are in context
    them model is empty if 2 or more are in context assets that don't have
    tasks with same names then model is empty too.

    Args:
        controller (PublisherController): Controller which handles creation and
            publishing.
    """
    def __init__(self, controller):
        super(TasksModel, self).__init__()
        self._controller = controller
        self._items_by_name = {}
        self._asset_names = []
        self._task_names_by_asset_name = {}

    def set_asset_names(self, asset_names):
        """Set assets context."""
        self._asset_names = asset_names
        self.reset()

    @staticmethod
    def get_intersection_of_tasks(task_names_by_asset_name):
        """Calculate intersection of task names from passed data.

        Example:
        ```
        # Passed `task_names_by_asset_name`
        {
            "asset_1": ["compositing", "animation"],
            "asset_2": ["compositing", "editorial"]
        }
        ```
        Result:
        ```
        # Set
        {"compositing"}
        ```

        Args:
            task_names_by_asset_name (dict): Task names in iterable by parent.
        """
        tasks = None
        for task_names in task_names_by_asset_name.values():
            if tasks is None:
                tasks = set(task_names)
            else:
                tasks &= set(task_names)

            if not tasks:
                break
        return tasks or set()

    def is_task_name_valid(self, asset_name, task_name):
        """Is task name available for asset.

        Args:
            asset_name (str): Name of asset where should look for task.
            task_name (str): Name of task which should be available in asset's
                tasks.
        """
        task_names = self._task_names_by_asset_name.get(asset_name)
        if task_names and task_name in task_names:
            return True
        return False

    def reset(self):
        """Update model by current context."""
        if not self._asset_names:
            self._items_by_name = {}
            self._task_names_by_asset_name = {}
            self.clear()
            return

        task_names_by_asset_name = (
            self._controller.get_task_names_by_asset_names(self._asset_names)
        )
        self._task_names_by_asset_name = task_names_by_asset_name

        new_task_names = self.get_intersection_of_tasks(
            task_names_by_asset_name
        )
        old_task_names = set(self._items_by_name.keys())
        if new_task_names == old_task_names:
            return

        root_item = self.invisibleRootItem()
        for task_name in old_task_names:
            if task_name not in new_task_names:
                item = self._items_by_name.pop(task_name)
                root_item.removeRow(item.row())

        new_items = []
        for task_name in new_task_names:
            if task_name in self._items_by_name:
                continue

            item = QtGui.QStandardItem(task_name)
            self._items_by_name[task_name] = item
            new_items.append(item)
        root_item.appendRows(new_items)
