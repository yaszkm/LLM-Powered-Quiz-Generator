import os
import torch
import spaces
import json
from transformers import AutoTokenizer, pipeline
from huggingface_hub import login
from dotenv import load_dotenv
import gradio as gr
from transformers import Pipeline
from typing import List, Dict, Union

from config import *
from ui import *

@spaces.GPU()
def initialize_model_and_tokenizer() -> Pipeline:
    load_dotenv()
    login(token=os.getenv("HUGGING_FACE_ACCESS_TOKEN"))

    is_cuda_available = torch.cuda.is_available()
    print(f"Is CUDA available: {is_cuda_available}")
    # print(f"CUDA device: {torch.cuda.get_device_name(torch.cuda.current_device())}")

    model = "microsoft/Phi-3-mini-4k-instruct"
    device=0 # if is_cuda_available else -1
    tokenizer = AutoTokenizer.from_pretrained(model)

    pipe = pipeline(
        "text-generation",
        model=model,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device=device,
        tokenizer=tokenizer,
    )

    return pipe


def get_prompt(quiz_type: str, topic: str, standard_difficulty: str, difficulty_description: str, style: str, 
               style_description: str, num_questions: int, json_format: str) -> str:
    prompt_template = QUIZ_PROMPT_CONTENT_MAP.get(quiz_type, QUIZ_PROMPT_CONTENT_MAP["Trivia"])

    return prompt_template.format(
        topic=topic,
        standard_difficulty=standard_difficulty,
        difficulty_description=difficulty_description,
        style=style,
        style_description=style_description, 
        num_questions=num_questions, 
        json_format=json_format
    )


def generate_prompt(quiz_type: str, topic: str, difficulty: str, style: str, num_questions: int) -> List[Dict]:
    json_format = QUIZ_TYPE_IN_JSON.get(quiz_type, QUIZ_TYPE_IN_JSON["Trivia"])
    style_description = STYLE_DESCRIPTIONS.get(style, "Casual")
    standard_difficulty = DIFFICULTY_INFO[difficulty]["label"]
    difficulty_description = DIFFICULTY_INFO[difficulty]["description"]
    content = get_prompt(
        quiz_type=quiz_type,
        topic=topic,
        standard_difficulty=standard_difficulty,
        difficulty_description=difficulty_description,
        style=style,
        style_description=style_description, 
        num_questions=num_questions, 
        json_format=json_format
    )

    return [{
        "role": "system",
        "content": content
    }]


def generate_quiz(pipe: Pipeline, quiz_type: str, topic: str, difficulty: str, style: str, num_questions: int,
                  max_tokens: int = MAX_NEW_TOKENS, temp: float = TEMP) -> str:
    prompt = generate_prompt(quiz_type, topic, difficulty, style, num_questions)
    generation_args: Dict[str, Union[int, bool, float]] = {
        "max_new_tokens": max_tokens,
        "return_full_text": False,
        "temperature": temp,
        "do_sample": True,
    }

    result = pipe(prompt, **generation_args)

    return result[0]['generated_text'][8:-3].strip() if 'generated_text' in result[0] else "Error generating quiz."


def generate_and_display(quiz_type: str, topic: str, difficulty: str, style: str, num_questions: int) -> tuple:
    json_data = generate_quiz(initialize_model_and_tokenizer(), quiz_type, topic, difficulty, style, num_questions)
    quiz_data = json.loads(json_data)
    processing_message = " "

    print(quiz_data)

    return quiz_data, quiz_data, processing_message


def clear_quiz() -> tuple[None, None, str]:
    
    return None, None, ""

with gr.Blocks(css=CSS) as demo:
    raw_output = gr.JSON(visible=False)

    gr.Markdown("# Quizpresso")
    gr.Markdown("## Customized Quiz Generator!")

    with gr.Row():
        quiz_type = gr.Dropdown(label="Quiz Type", choices=VALID_TYPES, value=DEFAULT_TYPE)
        quiz_topic = gr.Dropdown(label="Topic", choices=VALID_TOPICS, value=DEFAULT_TOPIC)
        quiz_difficulty = gr.Dropdown(label="Difficulty", choices=VALID_DIFFICULTIES, value=DEFAULT_DIFFICULTY)
        response_style = gr.Dropdown(label="Vibe", choices=VALID_STYLES, value=DEFAULT_STYLE)
        num_questions = gr.Slider(label="Number of Questions", minimum=1, maximum=10, value=DEFAULT_NUM_QUESTIONS, step=1)
        generate_button = gr.Button("Challenge Accepted")

    @gr.render(inputs=raw_output)
    def show_questions(data) -> None:
        if data:
            gr.Markdown("#### " + data["intro"])
            for i, q in enumerate(data["questions"]):
                question_text = q.get("q", "")
                options = q.get("opt", [])
                answer = q["ans"]

                with gr.Row():
                    gr.Markdown("### " + question_text)

                with gr.Row():
                    buttons = generate_button_row(options, f"row_{i}", correct_button_index=answer)
                    gr.Markdown(" ")

            gr.Markdown("#### " + data["outro"])

    with gr.Column():
        status_message = gr.Markdown()

    with gr.Column():
        formatted_json = gr.JSON(label="JSON", visible=False)

    generate_button.click(
        fn=clear_quiz,
        inputs=[],
        outputs=[raw_output, formatted_json, status_message],
        queue=True
    )

    generate_button.click(
        fn=generate_and_display,
        inputs=[quiz_type, quiz_topic, quiz_difficulty, response_style, num_questions],
        outputs=[raw_output, formatted_json, status_message],
        queue=True
    )

demo.launch()
