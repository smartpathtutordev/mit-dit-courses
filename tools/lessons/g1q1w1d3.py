"""Grade 1 English · Q1 W1 D3 · Songs and Stories.

Source: LANG1Q1W1DAY3NARRATIONSCRIPT (Nursery Rhymes and Stories, Exodus 20:12).
Objectives: sing a song and name vegetables, sing and move, listen to two
stories and tell what they teach (be kind and patient, help at home).
"""

LESSON = {
    "grade": 1, "quarter": 1, "week": 1, "day": 3,
    "title": "Songs and Stories",
    "source": "LANG1Q1W1DAY3NARRATIONSCRIPT — Nursery Rhymes and Stories (Exodus 20:12)",
    "bg": "media/image1.jpg",
    "next": "../../DAY4/INTERACTIVE/index.html",
    "slides": [
        {
            "type": "cover", "pose": "waving.png", "goal": 1,
            "title": "Songs and Stories",
            "goals": ["Sing and name vegetables", "Sing and move my body", "Listen to two stories"],
            "say": "Good morning, my friend! (pause) Yesterday we got ready for school. (pause) "
                   "Today we sing songs. (pause) And we listen to stories!",
        },
        {
            "id": "kubo", "type": "story", "pose": "pointing.png", "goal": 1,
            "title": "Bahay Kubo", "img": "media/image44.jpg",
            "lines": ["This is a bahay kubo.", "It is a small house.", "It has a big garden!"],
            "say": "Look at this little house. (pause) It is a bahay kubo. (pause) It is a small house. "
                   "(pause) Look all around it. (pause) It has a big garden with many vegetables!",
        },
        {
            "id": "veg", "type": "cards", "pose": "showing.png", "goal": 1,
            "title": "Vegetables in the Garden",
            "say": "Let us meet some vegetables! (pause) Tap each one. (pause) Say its name with me.",
            "yourTurn": "Tap each vegetable!",
            "items": [
                {"word": "pechay", "sub": "a leafy vegetable", "img": "media/image37.png",
                 "say": "Pechay. (pause) It has big green leaves!"},
                {"word": "bawang", "sub": "garlic", "img": "media/image41.png",
                 "say": "Bawang. (pause) In English, garlic. (pause) It is white!"},
                {"word": "luya", "sub": "ginger", "img": "media/image42.png",
                 "say": "Luya. (pause) In English, ginger. (pause) It is brown and bumpy!"},
            ],
        },
        {
            "id": "song", "type": "chant", "pose": "clapping.png", "goal": 1,
            "title": "Let Us Sing: Bahay Kubo", "img": "media/image44.jpg",
            "say": "Now let us sing! (pause) Tap a line to hear it. (pause) Or tap the big button to sing it all. "
                   "(pause) Listen for bawang and luya!",
            "yourTurn": "Tap a line and sing!",
            "allLabel": "Sing it all!",
            "lines": [
                {"text": "Bahay kubo, kahit munti,"},
                {"text": "ang halaman doon ay sari-sari."},
                {"text": "Singkamas at talong, sigarilyas at mani,"},
                {"text": "sibuyas, kamatis, bawang at luya!"},
            ],
        },
        {
            "id": "find-veg", "type": "pick", "pose": "thinking.png", "goal": 1,
            "title": "Find the Vegetable!",
            "say": "Can you find the vegetables? (pause) Listen. (pause) Then tap!",
            "yourTurn": "Tap the vegetable!",
            "rounds": [
                {"ask": "Tap the garlic!", "askSay": "Where is the garlic? The bawang?",
                 "choices": [{"word": "pechay", "img": "media/image37.png"},
                             {"word": "bawang", "img": "media/image41.png", "ok": True},
                             {"word": "luya", "img": "media/image42.png"}]},
                {"ask": "Tap the ginger!", "askSay": "Where is the ginger? The luya?",
                 "choices": [{"word": "luya", "img": "media/image42.png", "ok": True},
                             {"word": "bawang", "img": "media/image41.png"},
                             {"word": "pechay", "img": "media/image37.png"}]},
                {"ask": "Tap the pechay!", "askSay": "Where is the pechay? The one with green leaves?",
                 "choices": [{"word": "bawang", "img": "media/image41.png"},
                             {"word": "luya", "img": "media/image42.png"},
                             {"word": "pechay", "img": "media/image37.png", "ok": True}]},
            ],
        },
        {
            "id": "move", "type": "act", "pose": "clapping.png", "goal": 2,
            "title": "Sing and Move!",
            "say": "Please stand up! (pause) Let us sing and move. (pause) Touch each part of your body with me!",
            "yourTurn": "Touch it, then tap!",
            "cmds": [
                {"word": "Touch your feet!", "sub": "paa", "img": "../../DAY4/INTERACTIVE/media/body-feet.jpg", "art": {"file": "../../DAY4/INTERACTIVE/media/art/body-feet.png", "prompt": "Tala (Filipino girl, 6) standing and pointing down to her two FEET in white sneakers. That body part is gently highlighted with a soft yellow glow. Full body, front view."},
                 "say": "Paa! (pause) Touch your feet!"},
                {"word": "Touch your knees!", "sub": "tuhod", "img": "../../DAY4/INTERACTIVE/media/body-knees.jpg", "art": {"file": "../../DAY4/INTERACTIVE/media/art/body-knees.png", "prompt": "Tala (Filipino girl, 6) bending forward and touching both KNEES with her hands. That body part is gently highlighted with a soft yellow glow. Full body, front view."},
                 "say": "Tuhod! (pause) Touch your knees!"},
                {"word": "Touch your shoulders!", "sub": "balikat", "img": "../../DAY4/INTERACTIVE/media/body-shoulders.jpg", "art": {"file": "../../DAY4/INTERACTIVE/media/art/body-shoulders.png", "prompt": "Tala (Filipino girl, 6) touching both SHOULDERS with her hands, arms crossed. That body part is gently highlighted with a soft yellow glow. Full body, front view."},
                 "say": "Balikat! (pause) Touch your shoulders!"},
                {"word": "Touch your head!", "sub": "ulo", "img": "../../DAY4/INTERACTIVE/media/body-head.jpg", "art": {"file": "../../DAY4/INTERACTIVE/media/art/body-head.png", "prompt": "Tala (Filipino girl, 6) touching the top of her HEAD with both hands. That body part is gently highlighted with a soft yellow glow. Full body, front view."},
                 "say": "Ulo! (pause) Touch your head!"},
            ],
        },
        {
            "id": "t1", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "The Turtle and the Monkey", "page": "Page 1", "img": "media/image11.jpg", "art": {"file": "media/art/turtle-monkey-split.png", "prompt": "A friendly green turtle and a cheeky brown monkey in a sunny Filipino garden, cutting a young banana plant into two parts: the monkey proudly holds the leafy top, the turtle holds the bottom part with roots.", "scene": True},
            "lines": ["Turtle and Monkey find a banana plant.", "They cut it in two."],
            "say": "Story time! (pause) This is Turtle. (pause) And this is Monkey. (pause) "
                   "They find a banana plant. (pause) They cut it in two. (pause) Monkey takes the top. Turtle takes the bottom.",
        },
        {
            "id": "t2", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "The Turtle and the Monkey", "page": "Page 2", "img": "media/image13.jpg",
            "lines": ["Turtle plants it and waters it.", "It grows bananas!"],
            "say": "Monkey laughs at Turtle. (pause) But Turtle plants it. (pause) She waters it every day. "
                   "(pause) It grows tall. (pause) It grows bananas! (pause) Turtle is kind and patient.",
        },
        {
            "id": "t-check", "type": "pick", "pose": "raising_hand.png", "goal": 3,
            "title": "Think About the Story",
            "say": "Let us think about the story.",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "Who was patient?", "askSay": "Who was kind and patient?",
                 "choices": [{"word": "Turtle", "ok": True}, {"word": "Monkey"}],
                 "yes": "Yes! Turtle was patient.", "yesSay": "Yes! Turtle was kind and patient. (pause) And she got bananas!"},
            ],
        },
        {
            "id": "p1", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "The Legend of the Pineapple", "page": "Page 1", "img": "media/image17.jpg", "art": {"file": "media/art/pina-kitchen.png", "prompt": "Inside a cosy nipa-hut kitchen: little girl Pina (age 7, long black hair, simple dress) pouting with arms crossed, while her tired, sick mother rests on a bamboo bed holding her forehead. Clay pot and wooden spoon on the table.", "scene": True},
            "lines": ["Pina did not help her mother.", "\"I cannot find it!\" she said."],
            "say": "Here is another story. (pause) This is Pina. (pause) Her mother was sick. (pause) "
                   "She asked Pina to help. (pause) But Pina said, I cannot find it! (pause) She did not even look.",
        },
        {
            "id": "p2", "type": "story", "pose": "holding_book.png", "goal": 3,
            "title": "The Legend of the Pineapple", "page": "Page 2", "img": "media/panel-b1.jpg", "art": {"file": "media/art/pineapple-garden.png", "prompt": "A small garden beside the doorway of a nipa hut, one big golden pineapple plant growing there, the pineapple covered in many little eyes, with a soft magical sparkle around it. Gentle and not scary.", "scene": True},
            "lines": ["A new fruit grew in the garden.", "It had many, many eyes!"],
            "say": "The next day, Pina was gone. (pause) A new fruit grew in the garden. (pause) "
                   "It had many, many eyes! (pause) It is the pineapple. (pause) The pinya!",
        },
        {
            "id": "p-check", "type": "pick", "pose": "raising_hand.png", "goal": 3,
            "title": "What Does the Story Teach?",
            "say": "What does the story teach us?",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "What should we do at home?", "askSay": "What should we do at home?",
                 "choices": [{"word": "Help!", "ok": True}, {"word": "Do not help."}],
                 "yes": "Yes! We help at home.", "yesSay": "Yes! We help at home. (pause) Every little help is a big help!"},
            ],
        },
        {
            "id": "like", "type": "sentence", "pose": "point_self.png", "goal": 3,
            "title": "Which story did you like?",
            "say": "Which story did you like? (pause) Tap one. (pause) Then say it with me.",
            "yourTurn": "Tap one and say it!",
            "pre": "I like the story about the", "post": ".",
            "options": [
                {"word": "turtle", "img": "media/image13.jpg"},
                {"art": {"file": "media/art/pineapple-garden.png", "prompt": "A small garden beside the doorway of a nipa hut, one big golden pineapple plant growing there, the pineapple covered in many little eyes, with a soft magical sparkle around it. Gentle and not scary.", "scene": True}, "word": "pineapple", "img": "media/panel-b1.jpg"},
            ],
        },
        {
            "id": "verse", "type": "verse", "pose": "praying.png",
            "verse": "Honor your father and your mother.", "ref": "Exodus 20:12",
            "meaning": "Be kind like Turtle. Help at home, not like Pina.",
            "say": "Our Bible verse is, (pause) Honor your father and your mother. (pause) "
                   "We honor them when we help at home.",
            "verseSay": "Honor your father and your mother. (pause) Exodus twenty, verse twelve.",
        },
        {
            "id": "done", "type": "celebrate", "pose": "clapping.png",
            "title": "Great Singing and Listening!",
            "recap": ["I sang Bahay Kubo.", "I sang and moved my body.", "Be kind. Help at home."],
            "say": "Hooray! (pause) You sang Bahay Kubo. (pause) You moved your body. (pause) "
                   "And you listened to two stories. (pause) See you tomorrow!",
        },
    ],
}
