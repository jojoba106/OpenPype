import pyblish.api
import bpy
from openpype.hosts.blender.plugins.load.load_model import BlendModelLoader
from openpype.hosts.blender.plugins.load.load_rig import BlendRigLoader
from openpype.hosts.blender.plugins.load.load_layout_blend import BlendLayoutLoader

from openpype.hosts.blender.api import plugin

from openpype.hosts.blender.api.workio import save_file
from openpype.hosts.blender.api.pipeline import (
    AVALON_CONTAINERS,
    AVALON_PROPERTY,
    AVALON_CONTAINER_ID,
)
from avalon import io


class UpdateAvalonProperty(
    pyblish.api.InstancePlugin,
):
    """Update Avalon Property with representation"""

    order = pyblish.api.IntegratorOrder + 0.05
    label = "Update Avalon Property"
    optional = False
    hosts = ["blender"]
    families = ["animation", "model", "rig", "action", "layout"]

    def process(self, instance):

        from openpype.lib import version_up

        asset = instance.data["anatomyData"]["asset"]
        family = instance.data["anatomyData"]["family"]
        version = int(instance.data["anatomyData"]["version"])
        libpath = ""
        # Get representation from the db
        representation = io.find_one(
            {
                "context.asset": asset,
                "context.family": family,
                "context.version": version,
                "context.ext": "blend",
            }
        )
        context = {"representation": representation}
        if family == "model":
            blend_model_loader = BlendModelLoader(context=context)
            blend_model_loader.update_avalon_property(representation=representation)
        elif "rig":
            blend_rig_loader = BlendRigLoader(context=context)
            blend_rig_loader.update_avalon_property(representation=representation)
        elif "layout":
            blend_layout_loader = BlendLayoutLoader(context=context)
            blend_layout_loader.update_avalon_property(representation=representation)

        # Get the filepath of the publish
        filepath = str(representation["data"]["path"])

        # Get the filepath of the publish
        save_file(filepath, copy=False)

        # Overwrite the publish file
        self.log.info(" %s updated.", filepath)
