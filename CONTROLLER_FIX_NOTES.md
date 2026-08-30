# Android gamepad input fix

This branch fixes two controller issues:

- Gamepad buttons and axes are tracked by `KeyboardController`, allowing continuous actions such as movement, strafing, turning and looking to use the existing gamepad defaults.
- Controller inputs captured by the existing Controls UI are routed into the gamepad binding map instead of being stored as keyboard bindings. Reassigning a controller key removes its previous gamepad assignment.

The existing 0.5 digital axis threshold is intentionally retained for this first validation build. True analogue look/turn behaviour can be addressed separately after device testing.
