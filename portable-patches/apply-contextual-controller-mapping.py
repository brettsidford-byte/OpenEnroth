from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"Expected source block not found in {path}: {old[:80]!r}")
    p.write_text(text.replace(old, new, 1))


replace("src/GUI/UI/UIGame.cpp",
        '#include "Io/InputEnumFunctions.h"\n#include "Io/Mouse.h"',
        '#include "Io/InputEnumFunctions.h"\n#include "Io/InputActionContexts.h"\n#include "Io/Mouse.h"')
replace("src/GUI/UI/UIGame.cpp",
        '    curr_key_map = keyboardActionMapping->currentKeybindings(KEYBINDINGS_CONFIGURABLE);',
        '    curr_key_map = keyboardActionMapping->currentGamepadKeybindings(KEYBINDINGS_ALL);')
replace("src/GUI/UI/UIGame.cpp",
        '                if (x.first != y.first && x.second == y.second) {',
        '                if (x.first != y.first && x.second != PlatformKey::KEY_NONE && x.second == y.second &&\n                    inputActionsShareContext(x.first, y.first)) {')
replace("src/GUI/UI/UIGame.cpp",
'''    int base_controls_offset = 0;
    if (KeyboardPageNum == 1) {
        render->DrawQuad2D(game_ui_options_controls[3], {19, 302});
    } else {
        base_controls_offset = 14;
        render->DrawQuad2D(game_ui_options_controls[4], {127, 302});
    }

    for (int i = 0; i < 7; ++i) {
        InputAction action1 = (InputAction)(base_controls_offset + i);
        DrawText(assets->pFontLucida.get(), {23, 142 + i * 21}, ui_gamemenu_keys_action_name_color, GetDisplayName(action1), pGUIWindow_CurrentMenu->frameRect);
        DrawText(assets->pFontLucida.get(), {127, 142 + i * 21}, GameMenuUI_GetKeyBindingColor(action1), GetDisplayName(curr_key_map[action1]), pGUIWindow_CurrentMenu->frameRect);

        int j = i + 7;
        InputAction action2 = (InputAction)(base_controls_offset + j);
        DrawText(assets->pFontLucida.get(), {247, 142 + i * 21}, ui_gamemenu_keys_action_name_color, GetDisplayName(action2), pGUIWindow_CurrentMenu->frameRect);
        DrawText(assets->pFontLucida.get(), {350, 142 + i * 21}, GameMenuUI_GetKeyBindingColor(action2), GetDisplayName(curr_key_map[action2]), pGUIWindow_CurrentMenu->frameRect);
    }''',
'''    const InputActionPage &page = inputActionPage(KeyboardPageNum);

    DrawText(assets->pFontLucida.get(), {20, 306}, ui_gamemenu_keys_action_name_color, "< PREV", pGUIWindow_CurrentMenu->frameRect);
    DrawText(assets->pFontLucida.get(), {150, 306}, ui_gamemenu_keys_action_name_color, "NEXT >", pGUIWindow_CurrentMenu->frameRect);
    DrawText(assets->pFontLucida.get(), {190, 118}, ui_gamemenu_keys_action_name_color, page.title, pGUIWindow_CurrentMenu->frameRect);

    for (int row = 0; row < static_cast<int>(page.count); ++row) {
        InputAction action = page.actions[row];
        int column = row / 7;
        int line = row % 7;
        int actionX = column == 0 ? 23 : 247;
        int keyX = column == 0 ? 127 : 350;
        int y = 142 + line * 21;
        DrawText(assets->pFontLucida.get(), {actionX, y}, ui_gamemenu_keys_action_name_color, GetDisplayName(action), pGUIWindow_CurrentMenu->frameRect);
        DrawText(assets->pFontLucida.get(), {keyX, y}, GameMenuUI_GetKeyBindingColor(action), GetDisplayName(curr_key_map[action]), pGUIWindow_CurrentMenu->frameRect);
    }''')

replace("src/Application/GameMenu.cpp",
        '#include "Io/InputEnums.h"\n#include "Io/KeyboardInputHandler.h"',
        '#include "Io/InputEnums.h"\n#include "Io/InputActionContexts.h"\n#include "Io/KeyboardInputHandler.h"')
replace("src/Application/GameMenu.cpp",
'''                    currently_selected_action_for_binding = (InputAction)param;
                    if (KeyboardPageNum != 1)
                        currently_selected_action_for_binding = (InputAction)(param + 14);
                    keyboardInputHandler->StartTextInput(TextInputType::Text, 1, pGUIWindow_CurrentMenu.get());''',
'''                    currently_selected_action_for_binding = inputActionForBindingRow(KeyboardPageNum, param);
                    if (currently_selected_action_for_binding == INPUT_ACTION_INVALID) {
                        pAudioPlayer->playUISound(SOUND_error);
                        continue;
                    }
                    keyboardInputHandler->StartTextInput(TextInputType::Text, 1, pGUIWindow_CurrentMenu.get());''')
replace("src/Application/GameMenu.cpp",
        '                curr_key_map = keyboardActionMapping->defaultKeybindings(KEYBINDINGS_CONFIGURABLE);',
        '                curr_key_map = keyboardActionMapping->defaultGamepadKeybindings(KEYBINDINGS_ALL);')
replace("src/Application/GameMenu.cpp",
'''            case UIMSG_SelectKeyPage1:
                KeyboardPageNum = 1;
                continue;
            case UIMSG_SelectKeyPage2:
                KeyboardPageNum = 2;
                continue;''',
'''            case UIMSG_SelectKeyPage1:
                KeyboardPageNum--;
                if (KeyboardPageNum < 1)
                    KeyboardPageNum = static_cast<int>(kInputActionPages.size());
                continue;
            case UIMSG_SelectKeyPage2:
                KeyboardPageNum++;
                if (KeyboardPageNum > static_cast<int>(kInputActionPages.size()))
                    KeyboardPageNum = 1;
                continue;''')

replace("src/Io/KeyboardActionMapping.h",
'''    [[nodiscard]] Keybindings currentKeybindings(KeybindingsQuery query) const;
    [[nodiscard]] Keybindings defaultKeybindings(KeybindingsQuery query) const;
    void applyKeybindings''',
'''    [[nodiscard]] Keybindings currentKeybindings(KeybindingsQuery query) const;
    [[nodiscard]] Keybindings defaultKeybindings(KeybindingsQuery query) const;
    [[nodiscard]] Keybindings currentGamepadKeybindings(KeybindingsQuery query) const;
    [[nodiscard]] Keybindings defaultGamepadKeybindings(KeybindingsQuery query) const;
    void applyKeybindings''')
replace("src/Io/KeyboardActionMapping.cpp",
        '#include "InputEnumFunctions.h"',
        '#include "InputEnumFunctions.h"\n#include "InputActionContexts.h"')
replace("src/Io/KeyboardActionMapping.cpp",
'''void Io::KeyboardActionMapping::applyKeybindings(const Io::Keybindings &keybindings) {''',
'''Io::Keybindings Io::KeyboardActionMapping::currentGamepadKeybindings(KeybindingsQuery query) const {
    Io::Keybindings result;
    for (const auto &[inputAction, configEntry] : _gamepadEntryByInputAction)
        if (query == KEYBINDINGS_ALL || (query == KEYBINDINGS_CONFIGURABLE && allConfigurableInputActions().contains(inputAction)))
            result.emplace(inputAction, configEntry->value());
    return result;
}

Io::Keybindings Io::KeyboardActionMapping::defaultGamepadKeybindings(KeybindingsQuery query) const {
    Io::Keybindings result;
    for (const auto &[inputAction, configEntry] : _gamepadEntryByInputAction)
        if (query == KEYBINDINGS_ALL || (query == KEYBINDINGS_CONFIGURABLE && allConfigurableInputActions().contains(inputAction)))
            result.emplace(inputAction, configEntry->defaultValue());
    return result;
}

void Io::KeyboardActionMapping::applyKeybindings(const Io::Keybindings &keybindings) {''')
replace("src/Io/KeyboardActionMapping.cpp",
'''            if (otherAction != inputAction && otherEntry->value() == key)
                otherEntry->setValue(PlatformKey::KEY_NONE);''',
'''            if (otherAction != inputAction && otherEntry->value() == key &&
                inputActionsShareContext(inputAction, otherAction))
                otherEntry->setValue(PlatformKey::KEY_NONE);''')

replace("src/Application/GameConfig.h",
'''        Key Escape = {this, INPUT_ACTION_ESCAPE, "escape", PlatformKey::KEY_GAMEPAD_B, "Escape key."};
        Key ToggleWindowMode = {this, INPUT_ACTION_TOGGLE_WINDOW_MODE, "toggle_window_mode", PlatformKey::KEY_NONE, "Toggle window mode key."};''',
'''        Key Escape = {this, INPUT_ACTION_ESCAPE, "escape", PlatformKey::KEY_GAMEPAD_B, "Escape key."};
        Key ToggleMouseLook = {this, INPUT_ACTION_TOGGLE_MOUSE_LOOK, "toggle_mouse_look", PlatformKey::KEY_NONE, "Toggle mouse look key."};
        Key ToggleWindowMode = {this, INPUT_ACTION_TOGGLE_WINDOW_MODE, "toggle_window_mode", PlatformKey::KEY_NONE, "Toggle window mode key."};
        Key ArcomagePlayCard = {this, INPUT_ACTION_ARCOMAGE_PLAY_CARD, "arcomage_play", PlatformKey::KEY_GAMEPAD_A, "Play currently selected card."};
        Key ArcomageDiscard = {this, INPUT_ACTION_ARCOMAGE_DISCARD, "arcomage_discard", PlatformKey::KEY_GAMEPAD_Y, "Discard currently selected card."};
        Key ArcomageLeft = {this, INPUT_ACTION_ARCOMAGE_LEFT, "arcomage_left", PlatformKey::KEY_GAMEPAD_LEFT, "Select next card to left."};
        Key ArcomageRight = {this, INPUT_ACTION_ARCOMAGE_RIGHT, "arcomage_right", PlatformKey::KEY_GAMEPAD_RIGHT, "Select next card to right."};''')

print("Contextual controller mapping changes applied successfully")
