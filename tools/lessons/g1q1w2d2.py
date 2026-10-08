"""Grade 1 English · Q1 W2 D2 · Listen, Follow, and Ask.

Source: LANG1Q1W2DAY2LESSON (Following Instructions & Asking Questions, Proverbs 22:6).
Objectives: follow one-step directions (Simon Says: stand, sit, bow, smile,
wave, clap); know the question words who / what / where; ask and answer
questions about the story "Katkat the Kitten".
"""

LESSON = {
    "grade": 1, "quarter": 1, "week": 2, "day": 2,
    "title": "Listen, Follow, and Ask",
    "source": "LANG1Q1W2DAY2LESSON — Following Instructions & Asking Questions (Proverbs 22:6)",
    "bg": "media/image1.jpg",
    "teacher": "KUYA",
    "next": "../../DAY3/INTERACTIVE/index.html",
    "slides": [
        {
            "type": "cover", "pose": "waving.png", "goal": 1,
            "title": "Listen, Follow, and Ask",
            "goals": ["Follow what I hear", "Use who, what, where", "Ask about a story"],
            "say": "Hello! I am Kuya Gas! (pause) Today you learn two big skills. "
                   "(pause) First, how to follow directions. (pause) Second, how to ask questions!",
        },
        {
            "id": "actions", "type": "cards", "pose": "pointing.png", "goal": 1,
            "title": "Action Words",
            "say": "These are action words. (pause) Tap each one. (pause) Then do the action!",
            "yourTurn": "Tap and do it!",
            "items": [
                {"word": "stand", "pose": "KUYA/introducing.png", "say": "Stand! (pause) Stand up tall."},
                {"word": "sit", "pose": "KUYA/sitting.png", "say": "Sit! (pause) Sit down."},
                {"word": "clap", "pose": "KUYA/clapping.png", "say": "Clap! (pause) Clap your hands."},
                {"word": "smile", "pose": "KUYA/laughing.png", "say": "Smile! (pause) Give a big smile."},
                {"word": "wave", "pose": "KUYA/waving.png", "say": "Wave! (pause) Wave hello."},
                {"word": "bow", "pose": "KUYA/praying.png", "say": "Bow! (pause) Bow your head."},
            ],
        },
        {
            "id": "simon-how", "type": "story", "pose": "talking.png", "goal": 1,
            "title": "How to Play Simon Says", "img": "media/image1.jpg",
            "lines": ["Hear \"Simon says\"? Do it!", "No \"Simon says\"? Stay still!"],
            "say": "Let us play Simon Says! (pause) If I say, Simon says, (pause) do the action. "
                   "(pause) If I do not say Simon says, (pause) stay still! (pause) Listen carefully!",
        },
        {
            "id": "simon", "type": "act", "simon": True, "pose": "clapping.png", "goal": 1,
            "title": "Simon Says!",
            "say": "Stand up! Ready? (pause) Listen to each one. (pause) Then tap what you did.",
            "yourTurn": "Listen, then tap!",
            "cmds": [
                {"word": "Stand!", "simon": True, "pose": "KUYA/introducing.png"},
                {"word": "Clap!", "simon": True, "pose": "KUYA/clapping.png"},
                {"word": "Smile!", "simon": False, "pose": "KUYA/laughing.png"},
                {"word": "Bow!", "simon": True, "pose": "KUYA/praying.png"},
                {"word": "Sit!", "simon": False, "pose": "KUYA/sitting.png"},
                {"word": "Wave!", "simon": True, "pose": "KUYA/waving.png"},
            ],
        },
        {
            "id": "qwords", "type": "cards", "pose": "raising_hand.png", "goal": 2,
            "title": "Question Words",
            "say": "Now, question words! (pause) We use them to ask. (pause) Tap each one.",
            "yourTurn": "Tap each word!",
            "items": [
                {"word": "Who?", "sub": "a person", "img": "media/q-who.jpg", "art": {"file": "media/art/q-who.png", "prompt": "Tala (Filipino girl, 6) pointing at her friend, a smiling boy waving hello, a big friendly question-mark shaped cloud above them (no letters)."},
                 "say": "Who. (pause) Who is for a person. (pause) Who is your friend?"},
                {"word": "What?", "sub": "a thing", "img": "media/q-what.jpg", "art": {"file": "media/art/q-what.png", "prompt": "A child’s hands holding up a shiny red toy ball with a little bell, the child looking at it curiously, a big friendly question-mark shaped cloud above (no letters)."},
                 "say": "What. (pause) What is for a thing. (pause) What is your toy?"},
                {"word": "Where?", "sub": "a place", "img": "media/q-where.jpg", "art": {"file": "media/art/q-where.png", "prompt": "Tala (Filipino girl, 6) with one hand above her eyes, looking far away at a small house and a tree on a path, as if searching for a place, a big friendly question-mark shaped cloud above (no letters)."},
                 "say": "Where. (pause) Where is for a place. (pause) Where is your school?"},
            ],
        },
        {
            "id": "qmatch", "type": "pick", "pose": "thinking.png", "goal": 2,
            "title": "Which Question Word?",
            "say": "Which question word do we use? (pause) Listen and tap!",
            "yourTurn": "Tap the question word!",
            "rounds": [
                {"ask": "For a PERSON, we ask...", "askSay": "When we ask about a person, we say...",
                 "choices": [{"word": "Who?", "ok": True}, {"word": "What?"}, {"word": "Where?"}],
                 "yes": "Yes! WHO is for a person.", "yesSay": "Yes! Who is for a person."},
                {"ask": "For a PLACE, we ask...", "askSay": "When we ask about a place, we say...",
                 "choices": [{"word": "Who?"}, {"word": "What?"}, {"word": "Where?", "ok": True}],
                 "yes": "Yes! WHERE is for a place.", "yesSay": "Yes! Where is for a place."},
                {"ask": "For a THING, we ask...", "askSay": "When we ask about a thing, we say...",
                 "choices": [{"word": "Who?"}, {"word": "What?", "ok": True}, {"word": "Where?"}],
                 "yes": "Yes! WHAT is for a thing.", "yesSay": "Yes! What is for a thing."},
            ],
        },
        {
            "id": "k1", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "Katkat the Kitten", "page": "Page 1", "img": "media/image16.jpg",
            "lines": ["Katkat is a little orange kitten.", "He lives near the beach."],
            "say": "Story time! (pause) Listen, and think of questions. (pause) "
                   "This is Katkat. (pause) He is a little orange kitten. (pause) He lives near the beach.",
        },
        {
            "id": "k2", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "Katkat the Kitten", "page": "Page 2", "img": "media/image30.jpg",
            "lines": ["Oh no! His ball is missing!", "Where is it?"],
            "say": "On Saturday morning, Katkat looks for his ball. (pause) His ball has a bell. "
                   "(pause) Oh no! (pause) It is missing! (pause) Where is it?",
        },
        {
            "id": "k3", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "Katkat the Kitten", "page": "Page 3", "img": "media/image31.jpg",
            "lines": ["A white kitten has the ball!", "She gives it back.", "Now they are friends!"],
            "say": "Katkat looks in the garden, near the mango tree. (pause) A white kitten has his ball! "
                   "(pause) She gives it back. (pause) Now they are friends!",
        },
        {
            "id": "ask-story", "type": "pick", "pose": "raising_hand.png", "goal": 3,
            "title": "Ask About the Story!",
            "say": "Let us ask questions about the story. (pause) Listen to each question!",
            "yourTurn": "Tap the answer!",
            "rounds": [
                {"ask": "WHO is the story about?", "askSay": "Who is the story about?",
                 "choices": [{"word": "Katkat", "img": "media/image16.jpg", "ok": True}, {"word": "Miko"}],
                 "yes": "Yes! Katkat the kitten.", "yesSay": "Yes! The story is about Katkat."},
                {"ask": "WHAT did Katkat lose?", "askSay": "What did Katkat lose?",
                 "choices": [{"word": "his hat"}, {"word": "his ball", "img": "media/image31.jpg", "ok": True}],
                 "yes": "Yes! His ball.", "yesSay": "Yes! He lost his ball with a bell."},
                {"ask": "WHERE did he find it?", "askSay": "Where did Katkat find his ball?",
                 "choices": [{"word": "in the garden", "img": "media/image19.jpg", "ok": True}, {"word": "in the sea"}],
                 "yes": "Yes! In the garden.", "yesSay": "Yes! In the garden, near the mango tree."},
            ],
        },
        {
            "id": "ask-friend", "type": "sentence", "pose": "talking.png", "goal": 2,
            "title": "Now YOU Ask a Question!",
            "say": "Now you ask! (pause) Tap a question. (pause) Then ask someone at home.",
            "yourTurn": "Tap a question and ask it!",
            "pre": "", "post": "",
            "options": [
                {"word": "Who is your best friend?"},
                {"word": "What is your favorite toy?"},
                {"word": "Where do you want to go?"},
            ],
        },
        {
            "id": "talk", "type": "talk", "pose": "talking.png", "goal": 2,
            "title": "Answer Like Katkat!",
            "say": "Now answer a question. (pause) What is your favorite toy? (pause) Say: My favorite toy is my ball.",
            "yourTurn": "Say your answer!",
            "frame": "My favorite toy is ____.",
            "example": {"label": "Katkat says", "text": "My favorite toy is my ball."},
        },
        {
            "id": "verse", "type": "verse", "pose": "praying.png",
            "verse": "Train up a child in the way he should go.", "ref": "Proverbs 22:6",
            "meaning": "We listen and follow good directions. That is how we grow!",
            "say": "Our Bible verse is, (pause) Train up a child in the way he should go. "
                   "(pause) We listen to our parents and teachers. (pause) That is how we grow!",
            "verseSay": "Train up a child in the way he should go. (pause) Proverbs twenty-two, verse six.",
        },
        {
            "id": "done", "type": "celebrate", "pose": "clapping.png",
            "title": "Super Listener!",
            "recap": ["I can follow directions.", "I know who, what, where.", "I can ask about a story."],
            "say": "Hooray! (pause) You followed directions. (pause) You learned who, what and where. "
                   "(pause) And you asked questions about Katkat. (pause) See you tomorrow!",
        },
    ],
}
