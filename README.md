Below is a README file for the Blender add-on code provided. This README includes an overview, installation instructions, usage details, and additional notes to help users understand and utilize the add-on effectively.

---

# NLA Modifiers for Root Bone with Live Preview

This Blender add-on allows users to transform the location, rotation, and scale of the root bone in selected NLA strips with a live preview. It provides a user-friendly interface to apply transformations to armature actions in the NLA Editor, maintaining original keyframe values for non-destructive editing.

## Features

- **Live Preview:** Apply transformations to the root bone in real-time for the selected NLA strip.
- **Non-destructive Editing:** Store original keyframe values to prevent accumulation and allow easy resetting.
- **User Interface:** Intuitive panel in the NLA Editor for easy access to transformation controls.
- **Reset Functionality:** Quickly reset transformations to their default states.

## Installation

1. **Download the Add-on:**
   - Copy the add-on script to a file named `nla_modifiers.py`.

2. **Install the Add-on in Blender:**
   - Open Blender and go to `Edit` > `Preferences`.
   - In the Preferences window, go to the `Add-ons` tab.
   - Click `Install...` and select the `nla_modifiers.py` file.
   - Enable the add-on by checking the box next to `NLA Modifiers for Root Bone with Live Preview`.

3. **Save Preferences (Optional):**
   - Click `Save Preferences` to keep the add-on enabled when restarting Blender.

## Usage

1. **Open the NLA Editor:**
   - Switch to the NLA Editor in the Blender interface.

2. **Select an NLA Strip:**
   - Ensure that your armature object has animation data with NLA strips.
   - Select the desired NLA strip where you want to apply transformations.

3. **Access the Add-on Panel:**
   - Open the `Bone Transform Modifiers` panel located in the sidebar of the NLA Editor.

4. **Select the Root Bone:**
   - Choose the root bone from the dropdown menu labeled `Root Bone Name`.

5. **Apply Transformations:**
   - Adjust the `Location` and `Rotation` fields to apply transformations.
   - The changes will be previewed live in the 3D view.

6. **Reset Transformations:**
   - Click the `Reset Transform` button to revert transformations to their initial state.

## Code Overview

### Main Components

- **Operators:**
  - `NLAMOD_OT_ApplyTransform`: Applies transformations to the selected NLA strip.
  - `NLAMOD_OT_ResetTransform`: Resets transformation values to defaults.

- **Panel:**
  - `NLA_PT_ModifiersPanel`: Provides the UI in the NLA Editor for interacting with the add-on.

- **Utility Functions:**
  - `store_original_keyframes()`: Saves original keyframe values for non-destructive editing.
  - `apply_transform_to_bone()`: Applies specified transformations to the bone in the action.
  - `compute_new_keyframe_value()`: Computes new keyframe values based on transformations.
  - `create_keyframes_if_missing()`: Ensures keyframes exist for location and rotation.

- **Properties:**
  - `nla_mod_bone_name`: Dropdown to select the root bone.
  - `nla_mod_location`: Float vector property to input location transformations.
  - `nla_mod_rotation`: Float vector property to input rotation transformations.

## Additional Notes

- This add-on is designed for Blender 2.80 and later.
- The add-on assumes that the user has a basic understanding of Blender's NLA Editor and armature animation.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to modify the README as needed, especially if you plan to expand the add-on's functionality or provide more detailed instructions.
