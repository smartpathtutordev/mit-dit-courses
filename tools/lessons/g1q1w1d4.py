"""Grade 1 English · Q1 W1 D4 · My Body, Many Languages.

Source: LANG1Q1W1DAY4NARRATIONSCRIPT (Body Parts and Language Diversity, Exodus 20:12).
Objectives: name body parts (English, with the Filipino word), follow
"touch your ___" directions, and know that different Philippine languages
use different words for the same thing, and every language is beautiful.
"""

LESSON = {
    "grade": 1, "quarter": 1, "week": 1, "day": 4,
    "title": "My Body, Many Languages",
    "source": "LANG1Q1W1DAY4NARRATIONSCRIPT — Body Parts and Language Diversity (Exodus 20:12)",
    "bg": "media/image1.jpg",
    "next": "../../../WEEK2/DAY1/INTERACTIVE/index.html",
    "slides": [
        {
            "type": "cover", "pose": "waving.png", "goal": 1,
            "title": "My Body, Many Languages",
            "goals": ["Name parts of my body", "Play Touch Your Body", "Learn: many languages!"],
            "say": "Good morning, my friend! (pause) This is the last day of our first week. "
                   "(pause) Today we learn the parts of our body. (pause) And I have a surprise for you!",
        },
        {
            "id": "face", "type": "cards", "pose": "pointing.png", "goal": 1,
            "title": "My Head and Face",
            "say": "Let us learn five words. (pause) Tap each picture. (pause) Then touch that part of your face!",
            "yourTurn": "Tap each picture!",
            "items": [
                {"word": "head", "sub": "ulo", "img": "media/body-head.jpg", "art": {"file": "media/art/body-head.png", "prompt": "Tala (Filipino girl, 6) touching the top of her HEAD with both hands. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Head. (pause) Ulo. (pause) Touch your head!"},
                {"word": "eyes", "sub": "mata", "img": "media/body-eyes.jpg", "art": {"file": "media/art/body-eyes.png", "prompt": "Tala (Filipino girl, 6) pointing to her two EYES, eyes wide open and sparkling. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Eyes. (pause) Mata. (pause) Blink your eyes!"},
                {"word": "ears", "sub": "tenga", "img": "media/body-ears.jpg", "art": {"file": "media/art/body-ears.png", "prompt": "Tala (Filipino girl, 6) cupping one hand behind her EAR as if listening. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Ears. (pause) Tenga. (pause) Touch your ears!"},
                {"word": "nose", "sub": "ilong", "img": "media/body-nose.jpg", "art": {"file": "media/art/body-nose.png", "prompt": "Tala (Filipino girl, 6) touching the tip of her NOSE with one finger. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Nose. (pause) Ilong. (pause) Touch your nose!"},
                {"word": "mouth", "sub": "bibig", "img": "media/body-mouth.jpg", "art": {"file": "media/art/body-mouth.png", "prompt": "Tala (Filipino girl, 6) pointing to her MOUTH with a big open smile. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Mouth. (pause) Bibig. (pause) Smile with your mouth!"},
            ],
        },
        {
            "id": "body", "type": "cards", "pose": "showing.png", "goal": 1,
            "title": "My Body",
            "say": "Now five more words! (pause) Tap each picture. (pause) Then move that part of your body!",
            "yourTurn": "Tap each picture!",
            "items": [
                {"word": "shoulders", "sub": "balikat", "img": "media/body-shoulders.jpg", "art": {"file": "media/art/body-shoulders.png", "prompt": "Tala (Filipino girl, 6) touching both SHOULDERS with her hands, arms crossed. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},
                 "say": "Shoulders. (pause) Balikat. (pause) Touch your shoulders!"},
                {"word": "hands", "sub": "kamay", "img": "media/body-hands.jpg", "art": {"file": "media/art/body-hands.png", "prompt": "Tala (Filipino girl, 6) holding up both open HANDS, palms facing us, fingers spread. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Hands. (pause) Kamay. (pause) Clap your hands!"},
                {"word": "tummy", "sub": "tiyan", "img": "media/body-tummy.jpg", "art": {"file": "media/art/body-tummy.png", "prompt": "Tala (Filipino girl, 6) patting her TUMMY with both hands, happy face. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Tummy. (pause) Tiyan. (pause) Pat your tummy!"},
                {"word": "knees", "sub": "tuhod", "img": "media/body-knees.jpg", "art": {"file": "media/art/body-knees.png", "prompt": "Tala (Filipino girl, 6) bending forward and touching both KNEES with her hands. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Knees. (pause) Tuhod. (pause) Touch your knees!"},
                {"word": "feet", "sub": "paa", "img": "media/body-feet.jpg", "art": {"file": "media/art/body-feet.png", "prompt": "Tala (Filipino girl, 6) standing and pointing down to her two FEET in white sneakers. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "say": "Feet. (pause) Paa. (pause) Stamp your feet!"},
            ],
        },
        {
            "id": "song", "type": "chant", "pose": "clapping.png", "goal": 1,
            "title": "Sing and Touch!",
            "img": "media/image8.jpg",
            "say": "Let us sing! (pause) Stand up. (pause) Touch each part as you sing!",
            "yourTurn": "Sing and touch!",
            "allLabel": "Sing it all!",
            "lines": [
                {"text": "Head, shoulders, knees and feet,", "say": "Head, shoulders, knees and feet!"},
                {"text": "knees and feet!", "say": "Knees and feet!"},
                {"text": "Eyes and ears and mouth and nose,", "say": "Eyes and ears and mouth and nose!"},
                {"text": "Paa, tuhod, balikat, ulo!", "say": "Paa, tuhod, balikat, ulo!"},
            ],
        },
        {
            "id": "touch", "type": "act", "pose": "clapping.png", "goal": 2,
            "title": "Touch Your Body!",
            "say": "Let us play a game! (pause) I say a word. (pause) You touch that part. (pause) Ready?",
            "yourTurn": "Touch it, then tap!",
            "cmds": [
                {"word": "Touch your head!", "img": "media/body-head.jpg", "art": {"file": "media/art/body-head.png", "prompt": "Tala (Filipino girl, 6) touching the top of her HEAD with both hands. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                {"word": "Touch your feet!", "img": "media/body-feet.jpg", "art": {"file": "media/art/body-feet.png", "prompt": "Tala (Filipino girl, 6) standing and pointing down to her two FEET in white sneakers. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                {"word": "Blink your eyes!", "img": "media/body-eyes.jpg", "art": {"file": "media/art/body-eyes.png", "prompt": "Tala (Filipino girl, 6) pointing to her two EYES, eyes wide open and sparkling. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                {"word": "Touch your knees!", "img": "media/body-knees.jpg", "art": {"file": "media/art/body-knees.png", "prompt": "Tala (Filipino girl, 6) bending forward and touching both KNEES with her hands. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                {"word": "Pat your tummy!", "img": "media/body-tummy.jpg", "art": {"file": "media/art/body-tummy.png", "prompt": "Tala (Filipino girl, 6) patting her TUMMY with both hands, happy face. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                {"word": "Touch your ears!", "img": "media/body-ears.jpg", "art": {"file": "media/art/body-ears.png", "prompt": "Tala (Filipino girl, 6) cupping one hand behind her EAR as if listening. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
            ],
        },
        {
            "id": "find", "type": "pick", "pose": "thinking.png", "goal": 1,
            "title": "Listen and Tap!",
            "say": "Listen carefully. (pause) Tap the right picture!",
            "yourTurn": "Tap the right picture!",
            "rounds": [
                {"ask": "Tap the nose!", "askSay": "Where is the nose? Tap it!",
                 "choices": [{"word": "nose", "img": "media/body-nose.jpg", "art": {"file": "media/art/body-nose.png", "prompt": "Tala (Filipino girl, 6) touching the tip of her NOSE with one finger. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "ok": True},
                             {"word": "ears", "img": "media/body-ears.jpg", "art": {"file": "media/art/body-ears.png", "prompt": "Tala (Filipino girl, 6) cupping one hand behind her EAR as if listening. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                             {"word": "hands", "img": "media/body-hands.jpg", "art": {"file": "media/art/body-hands.png", "prompt": "Tala (Filipino girl, 6) holding up both open HANDS, palms facing us, fingers spread. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},}]},
                {"ask": "Tap the hands!", "askSay": "Where are the hands? Tap them!",
                 "choices": [{"word": "feet", "img": "media/body-feet.jpg", "art": {"file": "media/art/body-feet.png", "prompt": "Tala (Filipino girl, 6) standing and pointing down to her two FEET in white sneakers. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                             {"word": "hands", "img": "media/body-hands.jpg", "art": {"file": "media/art/body-hands.png", "prompt": "Tala (Filipino girl, 6) holding up both open HANDS, palms facing us, fingers spread. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "ok": True},
                             {"word": "eyes", "img": "media/body-eyes.jpg", "art": {"file": "media/art/body-eyes.png", "prompt": "Tala (Filipino girl, 6) pointing to her two EYES, eyes wide open and sparkling. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},}]},
                {"ask": "Tap the knees!", "askSay": "Where are the knees? Tap them!",
                 "choices": [{"word": "shoulders", "img": "media/body-shoulders.jpg", "art": {"file": "media/art/body-shoulders.png", "prompt": "Tala (Filipino girl, 6) touching both SHOULDERS with her hands, arms crossed. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                             {"word": "mouth", "img": "media/body-mouth.jpg", "art": {"file": "media/art/body-mouth.png", "prompt": "Tala (Filipino girl, 6) pointing to her MOUTH with a big open smile. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},},
                             {"word": "knees", "img": "media/body-knees.jpg", "art": {"file": "media/art/body-knees.png", "prompt": "Tala (Filipino girl, 6) bending forward and touching both KNEES with her hands. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "ok": True}]},
            ],
        },
        {
            "id": "langs", "type": "langs", "pose": "showing.png", "goal": 3,
            "title": "Different Words, Same Meaning!",
            "img": "media/body-ears.jpg", "art": {"file": "media/art/body-ears.png", "prompt": "Tala (Filipino girl, 6) cupping one hand behind her EAR as if listening. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "meaning": "They all mean EARS!",
            "say": "Here is my surprise! (pause) Our country has many languages. (pause) "
                   "Listen to the word for ears. (pause) Tap each card!",
            "yourTurn": "Tap each word!",
            "items": [
                {"lang": "Tagalog", "word": "tenga", "say": "In Tagalog, we say tenga."},
                {"lang": "Cebuano", "word": "dalunggan", "say": "In Cebuano, they say dalunggan."},
                {"lang": "Ilocano", "word": "lapayag", "say": "In Ilocano, they say lapayag."},
                {"lang": "Kapampangan", "word": "balugbug", "say": "In Kapampangan, they say balugbug."},
            ],
        },
        {
            "id": "same", "type": "pick", "pose": "raising_hand.png", "goal": 3,
            "title": "Think About It!",
            "say": "Let us think!",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "Tenga, dalunggan, lapayag. They all mean...",
                 "askSay": "Tenga. Dalunggan. Lapayag. (pause) What do they all mean?",
                 "choices": [{"word": "ears", "img": "media/body-ears.jpg", "art": {"file": "media/art/body-ears.png", "prompt": "Tala (Filipino girl, 6) cupping one hand behind her EAR as if listening. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."}, "ok": True},
                             {"word": "nose", "img": "media/body-nose.jpg", "art": {"file": "media/art/body-nose.png", "prompt": "Tala (Filipino girl, 6) touching the tip of her NOSE with one finger. That body part is gently highlighted with a soft yellow glow so a child can see which body part it is. Full body, front view."},}],
                 "yes": "Yes! Different words, same meaning!",
                 "yesSay": "Yes! They all mean ears. (pause) Different words. Same meaning!"},
                {"ask": "A friend says a different word. We...",
                 "askSay": "Your friend uses a different word. (pause) What do we do?",
                 "choices": [{"word": "listen", "ok": True}, {"word": "laugh"}],
                 "yes": "Yes! We listen and learn.",
                 "yesSay": "Yes! We listen. (pause) We say, teach me your word!"},
            ],
        },
        {
            "id": "home-word", "type": "talk", "pose": "talking.png", "goal": 3,
            "title": "What Do You Say at Home?",
            "img": "media/image18.jpg",
            "say": "What language do you speak at home? (pause) What do you call your ears at home? (pause) "
                   "Say: At home, I say tenga. (pause) Use your own word!",
            "yourTurn": "Say your word!",
            "frame": "At home, I say ____.",
            "example": {"label": "Tala says", "text": "At home, I say tenga."},
        },
        {
            "id": "beautiful", "type": "story", "pose": "hugging.png", "goal": 3,
            "title": "All Languages Are Beautiful", "img": "media/image18.jpg",
            "lines": ["Our country has many languages.", "Every language is beautiful.", "Your language is beautiful too!"],
            "say": "Look at our country, the Philippines. (pause) People speak many languages. (pause) "
                   "Every language is beautiful. (pause) And your language is beautiful too!",
        },
        {
            "id": "verse", "type": "verse", "pose": "praying.png",
            "verse": "Honor your father and your mother.", "ref": "Exodus 20:12",
            "meaning": "Our family teaches us our first words. Say thank you!",
            "say": "Our Bible verse is, (pause) Honor your father and your mother. (pause) "
                   "They taught us our first words. (pause) Let us thank them!",
            "verseSay": "Honor your father and your mother. (pause) Exodus twenty, verse twelve.",
        },
        {
            "id": "done", "type": "celebrate", "pose": "clapping.png",
            "title": "You Finished Week 1!",
            "recap": ["I can name parts of my body.", "I can follow: touch your head!", "Every language is beautiful."],
            "say": "Congratulations! (pause) You finished Week One! (pause) You can name the parts of your body. "
                   "(pause) And you know every language is beautiful. (pause) See you next week!",
        },
    ],
}
