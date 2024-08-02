bl_info = {
    "name": "NLA Modifiers for Root Bone with Live Preview",
    "blender": (2, 80, 0),
    "category": "Animation",
    "description": "Transform location, rotation, and scale of root bone in selected NLA strip with live preview",
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import EnumProperty, FloatVectorProperty
from mathutils import Euler

# Store original keyframe values globally to keep track of untransformed states
original_keyframes = {}
current_transformations = {}

def store_original_keyframes(action, bone_name):
    """Store the original keyframe values to prevent accumulation."""
    if action.name not in original_keyframes:
        original_keyframes[action.name] = {}

    for fcurve in action.fcurves:
        if bone_name in fcurve.data_path:
            original_keyframes[action.name][(fcurve.data_path, fcurve.array_index)] = [
                keyframe.co[1] for keyframe in fcurve.keyframe_points
            ]

def apply_transform_to_bone(action, bone_name, location, rotation):
    """Apply transformation to a specific bone in the action."""
    if action.name not in original_keyframes:
        store_original_keyframes(action, bone_name)

    current_transformations[action.name] = {
        'location': location[:],
        'rotation': rotation[:]
    }

    for fcurve in action.fcurves:
        if bone_name in fcurve.data_path:
            orig_values = original_keyframes[action.name].get((fcurve.data_path, fcurve.array_index), [])
            for i, keyframe in enumerate(fcurve.keyframe_points):
                keyframe.co[1] = compute_new_keyframe_value(fcurve, orig_values[i], location, rotation)

def compute_new_keyframe_value(fcurve, orig_value, location, rotation):
    """Compute the new keyframe value based on transformations."""
    if 'location' in fcurve.data_path:
        return orig_value + location[fcurve.array_index]
    elif 'rotation_euler' in fcurve.data_path:
        # Adding the rotation in radians to the original value
        index = fcurve.array_index
        return orig_value + rotation[index]
    return orig_value

def update_transform(self, context):
    """Update handler to apply transformations in real-time to the selected NLA strip."""
    obj = context.object
    bone_name = context.scene.nla_mod_bone_name

    if obj is None or obj.type != 'ARMATURE' or obj.animation_data is None:
        return

    location = context.scene.nla_mod_location
    rotation = context.scene.nla_mod_rotation

    for track in obj.animation_data.nla_tracks:
        for strip in track.strips:
            if strip.select and strip.action:
                apply_transform_to_bone(strip.action, bone_name, location, rotation)

def get_bone_names(self, context):
    """Get a list of bone names for the dropdown menu."""
    obj = context.object
    if obj and obj.type == 'ARMATURE' and obj.data.bones:
        return [(bone.name, bone.name, "") for bone in obj.data.bones]
    return [("", "No Bones Available", "")]

class NLAMOD_OT_ApplyTransform(Operator):
    """Apply Transformation to Root Bone in Selected NLA Strip"""
    bl_idname = "nla_mod.apply_transform"
    bl_label = "Apply Transform"
    bl_options = {'REGISTER', 'UNDO'}

    location: FloatVectorProperty(name="Location", size=3, default=(0.0, 0.0, 0.0))
    rotation: FloatVectorProperty(name="Rotation (Radians)", size=3, default=(0.0, 0.0, 0.0), subtype='EULER')

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE' and obj.animation_data is not None

    def execute(self, context):
        update_transform(self, context)
        return {'FINISHED'}

class NLAMOD_OT_ResetTransform(Operator):
    """Reset Transformation Values"""
    bl_idname = "nla_mod.reset_transform"
    bl_label = "Reset Transform"

    def execute(self, context):
        context.scene.nla_mod_location = (0.0, 0.0, 0.0)
        context.scene.nla_mod_rotation = (0.0, 0.0, 0.0)
        return {'FINISHED'}

class NLA_PT_ModifiersPanel(Panel):
    """Creates a Panel in the NLA Editor Strip Tab"""
    bl_label = "Bone Transform Modifiers"
    bl_idname = "NLA_PT_modifiers_panel"
    bl_space_type = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Strip'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Bone Transformation")
        layout.prop(context.scene, "nla_mod_bone_name", text="Root Bone Name")
        layout.prop(context.scene, "nla_mod_location")
        layout.prop(context.scene, "nla_mod_rotation")
        layout.operator("nla_mod.reset_transform", text="Reset Transform", icon='FILE_REFRESH')

        obj = context.object
        if obj and obj.animation_data:
            for track in obj.animation_data.nla_tracks:
                for strip in track.strips:
                    if strip.select and strip.action:
                        current_transform = current_transformations.get(strip.action.name, {})
                        if current_transform:
                            layout.label(text=f"Current Transformation for {strip.action.name}:")
                            layout.label(text=f"  Location: {current_transform['location']}")
                            layout.label(text=f"  Rotation: {current_transform['rotation']}")

def register():
    bpy.utils.register_class(NLAMOD_OT_ApplyTransform)
    bpy.utils.register_class(NLAMOD_OT_ResetTransform)
    bpy.utils.register_class(NLA_PT_ModifiersPanel)

    bpy.types.Scene.nla_mod_bone_name = EnumProperty(
        name="Root Bone Name",
        description="Name of the root bone to transform",
        items=get_bone_names
    )

    bpy.types.Scene.nla_mod_location = FloatVectorProperty(
        name="Location",
        size=3,
        default=(0.0, 0.0, 0.0),
        description="Location transformation",
        update=update_transform
    )

    bpy.types.Scene.nla_mod_rotation = FloatVectorProperty(
        name="Rotation (Radians)",
        size=3,
        default=(0.0, 0.0, 0.0),
        description="Rotation transformation",
        subtype='EULER',
        unit='ROTATION',
        update=update_transform
    )

def unregister():
    bpy.utils.unregister_class(NLAMOD_OT_ApplyTransform)
    bpy.utils.unregister_class(NLAMOD_OT_ResetTransform)
    bpy.utils.unregister_class(NLA_PT_ModifiersPanel)

    del bpy.types.Scene.nla_mod_bone_name
    del bpy.types.Scene.nla_mod_location
    del bpy.types.Scene.nla_mod_rotation

if __name__ == "__main__":
    register()
