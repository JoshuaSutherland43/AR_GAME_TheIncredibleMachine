# Vuforia Dataset + Frame Build Steps

## What Was Implemented In Project
- Added Unity Editor automation tool:
  - `Assets/Editor/MinimalARSetupTool.cs`
- Imported Vuforia package dataset:
  - `Assets/StreamingAssets/Vuforia/AR.dat`
  - `Assets/StreamingAssets/Vuforia/AR.xml`
- Target widths in dataset are `0.120000` meters (12 cm).
- Existing marker pages are ready for printing/upload:
  - `Docs/MarkerPages/`

## Run This In Unity
1. Open the project in Unity.
2. Wait for compile/import to finish.
3. Click menu:
   - `Tools > Minimal AR > Setup Markers + Prefabs + Scene`

This one action will:
- Rebuild prefabs:
  - `Assets/Prefabs/PF_FrameMachine.prefab`
  - `Assets/Prefabs/PF_Plank.prefab`
  - `Assets/Prefabs/PF_Cube.prefab`
  - `Assets/Prefabs/PF_Rope.prefab`
  - `Assets/Prefabs/PF_StartResetButton.prefab`
- Configure `SampleScene`:
  - Add interaction scripts on `ARCamera`
  - Ensure `GameSession` + `SessionManager`
  - Ensure image targets:
    - `frame_generator_img_target_01`
    - `object_spawner_plank_img_target_02`
    - `object_spawner_cube_img_target_03`
    - `object_spawner_rope_img_target_04`
    - `run_reset_button_img_target_05`
    - `spare_marker_img_target_06`
  - Apply width/aspect + dataset path
  - Add `VuforiaMarkerSpawner` on each target
  - Map spawn prefabs by target role

## Target Manager Step (Manual)
Uploading to Vuforia Target Manager cannot be completed offline from this workspace because it requires your account login and cloud export.

Do this:
1. If you receive a new Vuforia package, import or extract it.
2. Replace dataset files in `Assets/StreamingAssets/Vuforia/`.
3. Back in Unity, confirm each ImageTarget name matches exactly the AR dataset names above.
