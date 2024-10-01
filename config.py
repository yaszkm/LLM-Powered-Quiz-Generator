MAX_NEW_TOKENS = 800
TEMP = 0.1

VALID_TOPICS = sorted(["Mobile Apps", "Music", "Movies", "Animals", "Video Games", "Art", "Food", "Geography",
                       "History", "Space", "Literature", "Math", "Environment", "Mythology", "Philosophy",
                       "Pop Culture", "Sports", "Technology", "Science"])

VALID_STYLES = sorted(["Casual", "Formal", "Pirate", "Shakespearean", "Bro Speak", "Fairy Tale",
                       "Gamer Lingo", "Emojis", "Teenager", "Silly", "Exaggerated", "Superhero", "Minimalist"])

VALID_DIFFICULTIES = (["Piece of Cake", "Getting Spicy", "Brain Buster", "Mastermind Mode", "Legendary"])

DEFAULT_TOPIC = VALID_TOPICS[17]
DEFAULT_DIFFICULTY = VALID_DIFFICULTIES[2]
DEFAULT_STYLE = VALID_STYLES[2]
DEFAULT_NUM_QUESTIONS = 5

DIFFICULTY_INFO = {
    "Piece of Cake": {
        "label": "Extremely Easy",
        "description": "Kindergarten to elementary school level - very simple and basic questions."
    },
    "Getting Spicy": {
        "label": "Easy",
        "description": "Middle school to high school level - moderate questions that require some thought."
    },
    "Brain Buster": {
        "label": "Medium",
        "description": "Bachelor's degree level - more challenging questions that test in-depth knowledge."
    },
    "Mastermind Mode": {
        "label": "Hard",
        "description": "Master's degree level - highly challenging questions requiring advanced understanding."
    },
    "Legendary": {
        "label": "Extremely Hard",
        "description": "Expert or PhD level - extremely difficult questions for specialists or those with extensive expertise."
    }
}

QUIZ_TYPE_IN_JSON = {
    "Trivia": """```json{
        "intro": "Your introductory text here",
            "questions": [{
            "q": "Question", 
            "opt": array of 4 answer options,
            "ans": answer index as integer
            // Repeat as necessary
        }],
        "outro": "Your concluding text here"
    }```""",
    "What Am I?": """```json{
        "intro": "Your introductory text here",
        "questions": [{
            "q": "What am I? Description", 
            "opt": array of 4 answer options,
            "ans": answer index as integer
            // Repeat as necessary
        }],
        "outro": "Your concluding text here"
    }```""",
    "Scale Battle": """```json{
        "intro": "Your introductory text here",
        "questions": [{
            "q": "Which of the following has more/less <attribute>?", 
            "opt": array of 2 answer options,
            "ans": answer index as integer
            // Repeat as necessary
        }],
        "outro": "Your concluding text here"
    }```""",
    "Fact or Fiction": """```json{
        "intro": "Your introductory text here",
            "questions": [{
            "q": "Statement", 
            "opt": ["True", "False"],  // or ["Fact", "Fiction"]
            "ans": answer index as integer
            // Repeat as necessary
        }],
        "outro": "Your concluding text here"
    }```"""
}

STYLE_DESCRIPTIONS = {
    "Casual": "Just chill and relaxed — talk like you're with a friend over coffee, keeping it real.",
    "Formal": "A polished and respectful tone — use complete sentences, no slang, fit for professional settings.",
    "Pirate": "Arrr! Playful and exaggerated — nautical terms and old-timey speak, full of adventure and fun!",
    "Shakespearean": "Hark, good sir! Employ thou's finest language, rich with thy poetic flair and noble speech. Speak as if thou art on the grand stage, with lofty and profound words. Pray, keep it regal and timeless!",
    "Bro Speak": "Alright, bro, here's the lowdown: Use slang, stay hyped, and chat like you're with your best bud. Just keep it real and have a blast, ya feel?",
    "Fairy Tale": "Once upon a time — whimsical and imaginative, full of fairy tale magic and moral lessons.",
    "Gamer Lingo": "GG, fam! Use gaming slang and abbreviations like you're right in the middle of a match. Just keep it hype and in-game!",
    "Emojis": "Express with emojis 😊 — colorful and fun, use many emojis to show feelings and actions 🎉👍.",
    "Teenager": "OMG! Totally chill — full of current slang and abbreviations, like texting with friends.",
    "Silly": "Goofy and zany — everything's a bit wacky and exaggerated, like a cartoon come to life.",
    "Exaggerated": "Larger than life — every detail is blown up to epic proportions, with flair and drama.",
    "Superhero": "Heroic and epic — adventures with superpowers andt high-stakes action, just like your favorite comic book.",
    "Minimalist": "Simple and sleek — everything pared down to the essentials, clear and no-nonsense."
}

QUIZ_PROMPT_CONTENT_MAP = {
    "Trivia": """
        You are hosting a trivia game show, similar to "Who Wants to Be a Millionaire?"
        A {topic} manner is described as: {style_description}
        Use that {style} manner of speech to generate a fun introduction, an engaging outro,
        and {num_questions} trivia questions about {topic}. Do not repeat the same question. Ensure all questions are unique.
        The question should be at a {standard_difficulty} difficulty level.
        This difficulty level corresponds to what can be described as: {difficulty_description}
        Questions should be phrased in the {style} manner as well. Each question has 4 options with only one correct answer.
        Provide information based only on verified facts.
        The answer key must be a numeric index (0-3) indicating the correct option.
        Provide everything in the following JSON format: {json_format}
    """,
    "What Am I?": """
        You are hosting a "What Am I?" game show.
        A {style} manner is described as: {style_description}
        Use that {style} manner of speech to generate a fun introduction, an engaging outro,
        and {num_questions} descriptions related to {topic}.
        Do not repeat the same description. Ensure all descriptions are unique.
        The question should be at a {standard_difficulty} difficulty level.
        This difficulty level corresponds to what can be described as: {difficulty_description}
        Questions should be phrased in the {style} manner as well. Each question has 4 options with only one correct answer. 
        Provide information based only on verified facts.
        Do not add letters or prefixes in front of the options.
        The answer key must be a numeric index (0-3) indicating the correct option.
        Provide everything in the following JSON format: {json_format}
    """,
    "Scale Battle": """
        You are hosting a "Scale Battle" game show.
        In this game, contestants compare two options based on a certain attribute (e.g., size, quantity, distance).
        A {style} manner is described as: {style_description}
        Use that {style} manner of speech to generate a fun introduction, an engaging outro,
        and {num_questions} questions related to {topic}. Do not repeat the same question. Ensure all questions are unique.
        The question should be at a {standard_difficulty} difficulty level.
        This difficulty level corresponds to what can be described as: {difficulty_description}
        Questions should be phrased in the {style} manner as well. Each question should present 2 options for comparison and ask which option has more or less of the specified attribute.
        Provide information based only on verified facts.
        The answer key must be a numeric index (0-1) indicating the correct option.
        Provide everything in the following JSON format: {json_format}
    """,
    "Fact or Fiction": """
        You are hosting a "Fact or Fiction" game show.
        A {style} manner is described as: {style_description}
        Use that {style} manner of speech to generate a fun introduction, an engaging outro,
        and {num_questions} statements that are either true (fact) or false (fiction) about {topic}.
        Use the {style} manner and phrase each statements as as a declarative sentence.
        Do not repeat the same statement. Ensure all statements are unique.
        The difficulty level ({standard_difficulty}) of these statements corresponds to what can be described as: {difficulty_description}
        Each statement has 2 options ("True" and "False"; or "Fact" and "Fiction") with only one of them being correct.
        Provide information based only on verified facts.
        The answer key must be a numeric index (0-1) indicating the correct option.
        Provide everything in the following JSON format: {json_format}
    """
}

VALID_TYPES = list(QUIZ_PROMPT_CONTENT_MAP.keys())
DEFAULT_TYPE = VALID_TYPES[0]

CSS = """
    .question {
        font-weight: normal;
    }
    .btn-answer {
        color: white;
    }
    .btn-correct {
        background-image: none;
        background-color: green;
    }
    .btn-wrong {
        background-image: none;
        background-color: red;
    }
"""
