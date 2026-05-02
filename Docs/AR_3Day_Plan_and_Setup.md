# AR "Incredible Machine" 3-Day Plan (Vuforia + Unity)

## Recommended Stack
- Keep `Vuforia` for this submission.
- Reason: this project is already configured for Vuforia image targets, and your requirement is marker cards on paper.
- You can migrate to AR Foundation later, but changing stack now increases risk.

## Delivery Plan (Incremental)
### Day 1: Stable core loop
- Keep one image target for the frame anchor (`img_target_frame`).
- Spawn one large frame (2m x 0.75m x 4m scene layout) with:
  - ball spawner at top
  - basket at lower-left
- Add session flow:
  - green button = start attempt
  - red button = reset to pre-run arrangement
- Confirm one-ball attempt end-to-end.

### Day 2: Interaction and object cards
- Add three object cards (plank / rope / cube markers).
- Each marker spawns a manipulable object into world space.
- Enable one-tap interaction:
  - hover highlight
  - tap to pick up
  - move object by moving phone
  - tap again to place
- Add jerk gesture toggle:
  - quick forward-back flick enters rotation mode
  - quick forward-back flick exits rotation mode

### Day 3: Tuning and polish
- Tune jerk thresholds and cooldown on real phone.
- Tune collider sizes and physics materials for ball reliability.
- Add fail timeout and test resets repeatedly.
- Optimize performance:
  - disable expensive shadows
  - keep rigidbody count low
  - simplify meshes/colliders
- Record demo and keep a fallback scene.

## Scripts Added in This Project
- `Assets/Scripts/Game/Interaction/WorldTapInteractor.cs`
- `Assets/Scripts/Game/Interaction/SelectableObject.cs`
- `Assets/Scripts/Game/Interaction/BoxOutlineVisual.cs`
- `Assets/Scripts/Game/Input/JerkRotationToggle.cs`
- `Assets/Scripts/Game/Gameplay/SessionManager.cs`
- `Assets/Scripts/Game/Gameplay/BallSpawner.cs`
- `Assets/Scripts/Game/Gameplay/Ball.cs`
- `Assets/Scripts/Game/Gameplay/BasketGoal.cs`
- `Assets/Scripts/Game/Gameplay/WorldStartResetButton.cs`
- `Assets/Scripts/Game/Markers/VuforiaMarkerSpawner.cs`

## Unity Scene Wiring (Do This Next)
1. Camera rig
- On `ARCamera`, add:
  - `JerkRotationToggle`
  - `WorldTapInteractor`
- In `WorldTapInteractor`, assign:
  - `Ar Camera` = `ARCamera`
  - `Jerk Toggle` = the `JerkRotationToggle` you just added

2. Start/reset flow
- Create an empty object `GameSession`.
- Add `SessionManager`.
- Assign:
  - `Ball Spawner` = your frame's spawner object with `BallSpawner`
  - `Basket Goal` = basket trigger object with `BasketGoal`
  - `Start Reset Button` = world button object with `WorldStartResetButton`
- On your button object:
  - add collider
  - add `WorldStartResetButton`
  - assign its renderer

3. Movable objects
- For each object player can move, add:
  - collider
  - `SelectableObject`
  - rigidbody (recommended for physics pieces)
- `BoxOutlineVisual` is auto-added by `SelectableObject` if missing.

4. Marker-driven spawning
- For each image target (`IT_Frame`, `IT_PlankCard`, `IT_RopeCard`, `IT_CubeCard`, `IT_StartCard`), add:
  - `VuforiaMarkerSpawner`
- Configure each spawner:
  - `Spawn Prefab` = what this card should create
  - `Spawn Only Once` = true
  - `Detach From Marker After Spawn` = true
  - set local offset so spawned object does not overlap paper

## Marker Image Guide (Paper Pages)
- Use distinct, high-detail, non-repeating images (photos/illustrations with many corners and contrast).
- Avoid:
  - large plain areas
  - repeated patterns
  - glossy paper glare
  - motion blur prints
- Print recommendations:
  - matte paper
  - minimum ~12 cm wide target image
  - keep flat and well-lit
- Keep each card visually different from others.

## How To Add New Pages/Markers in Vuforia
1. Open Vuforia Target Manager (web).
2. Create one database for this project (or reuse existing `ClassExampleTargets`).
3. Add each page image as an `Image Target` with real-world width.
4. Download Unity package/database (`.dat` + `.xml`) for your project.
5. Put files into `Assets/StreamingAssets/Vuforia/`.
6. In Unity, create an `ImageTarget` GameObject for each new marker.
7. Set each target's name to match your database entry.
8. Attach `VuforiaMarkerSpawner` and assign spawn prefab per marker.

## Gesture Tuning Notes
- Jerk detection is in `JerkRotationToggle`.
- Key fields:
  - `Forward Threshold`
  - `Backward Threshold`
  - `Max Reversal Time Seconds`
  - `Cooldown Seconds`
- To reduce accidental triggers while walking:
  - increase thresholds
  - reduce reversal time window
  - keep cooldown >= 0.4s
