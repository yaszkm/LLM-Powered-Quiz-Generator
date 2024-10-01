import gradio as gr
from typing import Dict, List

def update_buttons(clicked_button: str, is_correct: bool, buttons: List[str]):
    updates = {}

    for button in buttons:
        if button == clicked_button:
            updates[button] = gr.update(
                value=(button.value + " 🎉") if is_correct else button.value,
                interactive=False,
                elem_classes="btn-answer " + ("btn-correct" if is_correct else "btn-wrong")
            )
        else:
            if is_correct:
                updates[button] = gr.update(interactive=False)
            else:
                updates[button] = gr.update()

    return updates


def generate_button_row(options: List[str], row_id: str, correct_button_index: int):
    buttons: List[gr.Button] = []
    button_labels = options

    for i, label in enumerate(button_labels):
        button = gr.Button(label, elem_id=f"{row_id}_btn_{i}")
        buttons.append(button)

    def handle_button_click(clicked_button_label: str):
        clicked_button = next(button for button in buttons if button.value == clicked_button_label)
        is_correct = buttons.index(clicked_button) == correct_button_index
        updates = update_buttons(clicked_button, is_correct, buttons)
        return [updates[button] for button in buttons]

    for button in buttons:
        button.click(fn=handle_button_click, inputs=[button], outputs=buttons)

    return buttons
    