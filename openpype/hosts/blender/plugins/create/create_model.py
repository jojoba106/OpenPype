"""Create a model asset."""

import bpy

from avalon import api
from openpype.hosts.blender.api import plugin, lib, ops
from openpype.hosts.blender.api.pipeline import MODEL_TASK_NAME


class CreateModel(plugin.Creator):
    """Polygonal static geometry"""

    name = "modelMain"
    label = "Model"
    family = "model"
    icon = "cube"

    def process(self):
        """ Run the creator on Blender main thread"""
        mti = ops.MainThreadItem(self._process)
        ops.execute_in_main_thread(mti)

    def _process(self):

        # get info from data and create name value
        asset = self.data["asset"]
        subset = self.data["subset"]
        #name = plugin.asset_name(asset, subset)

        name = MODEL_TASK_NAME
        # Get Instance Container or create it if it does not exist
        instance = bpy.data.collections.get(name)
        if not instance:
            instance = bpy.data.collections.new(name=name)
            bpy.context.scene.collection.children.link(instance)

        #add custum property on the instance with the data
        self.data['task'] = api.Session.get('AVALON_TASK')
        lib.imprint(instance, self.data)

        # Add selected objects to instance
        if (self.options or {}).get("useSelection"):
            selected = lib.get_selection()
            for obj in selected:
                instance.objects.link(obj)
                bpy.context.scene.collection.objects.unlink(obj)
        return instance
