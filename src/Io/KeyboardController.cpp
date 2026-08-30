#include "KeyboardController.h"

#include <cmath>

#include "Library/Platform/Interface/PlatformEvents.h"

namespace {
// Match the digital threshold used by GameWindowHandler for the first controller validation build.
constexpr float GAMEPAD_AXIS_THRESHOLD = 0.5f;
}

KeyboardController::KeyboardController()
    : PlatformEventFilter({
          EVENT_KEY_PRESS,
          EVENT_KEY_RELEASE,
          EVENT_GAMEPAD_KEY_PRESS,
          EVENT_GAMEPAD_KEY_RELEASE,
          EVENT_GAMEPAD_AXIS
      }) {}

bool KeyboardController::isKeyPressedThisFrame(PlatformKey key) const {
    if (key == PlatformKey::KEY_NONE)
        return false;

    return _isKeyPressedThisFrame[key];
}

bool KeyboardController::isKeyDownThisFrame(PlatformKey key) const {
    if (key == PlatformKey::KEY_NONE)
        return false;

    return _isKeyDown[key] || _isKeyPressedThisFrame[key];
}

void KeyboardController::setKeyState(PlatformKey key, bool isDown) {
    if (key == PlatformKey::KEY_NONE)
        return;

    if (isDown) {
        if (!_isKeyDown[key])
            _isKeyPressedThisFrame[key] = true;
        _isKeyDown[key] = true;
    } else {
        _isKeyDown[key] = false;
    }
}

bool KeyboardController::keyPressEvent(const PlatformKeyEvent *event) {
    setKeyState(event->key, true);
    return false;
}

bool KeyboardController::keyReleaseEvent(const PlatformKeyEvent *event) {
    setKeyState(event->key, false);
    return false;
}

bool KeyboardController::gamepadKeyPressEvent(const PlatformGamepadKeyEvent *event) {
    setKeyState(event->key, true);
    return false;
}

bool KeyboardController::gamepadKeyReleaseEvent(const PlatformGamepadKeyEvent *event) {
    setKeyState(event->key, false);
    return false;
}

bool KeyboardController::gamepadAxisEvent(const PlatformGamepadAxisEvent *event) {
    PlatformKey positiveKey = event->axis;
    PlatformKey negativeKey = PlatformKey::KEY_NONE;

    switch (event->axis) {
    case PlatformKey::KEY_GAMEPAD_LEFTSTICK_RIGHT:
        negativeKey = PlatformKey::KEY_GAMEPAD_LEFTSTICK_LEFT;
        break;
    case PlatformKey::KEY_GAMEPAD_RIGHTSTICK_RIGHT:
        negativeKey = PlatformKey::KEY_GAMEPAD_RIGHTSTICK_LEFT;
        break;
    case PlatformKey::KEY_GAMEPAD_LEFTSTICK_DOWN:
        negativeKey = PlatformKey::KEY_GAMEPAD_LEFTSTICK_UP;
        break;
    case PlatformKey::KEY_GAMEPAD_RIGHTSTICK_DOWN:
        negativeKey = PlatformKey::KEY_GAMEPAD_RIGHTSTICK_UP;
        break;
    default:
        break;
    }

    if (negativeKey != PlatformKey::KEY_NONE) {
        setKeyState(positiveKey, event->value >= GAMEPAD_AXIS_THRESHOLD);
        setKeyState(negativeKey, event->value <= -GAMEPAD_AXIS_THRESHOLD);
    } else {
        // Triggers are one-directional axes.
        setKeyState(positiveKey, std::abs(event->value) >= GAMEPAD_AXIS_THRESHOLD);
    }

    return false;
}

void KeyboardController::processMessages(PlatformEventHandler *eventHandler) {
    _isKeyPressedThisFrame.fill(false);
    ProxyEventLoop::processMessages(eventHandler);
}

void KeyboardController::reset() {
    _isKeyDown.fill(false);
    _isKeyPressedThisFrame.fill(false);
}
