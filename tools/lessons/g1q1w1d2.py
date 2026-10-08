"""Grade 1 English · Q1 W1 D2 · Getting Ready for School.

Source: LANG1Q1W1DAY2NARRATIONSCRIPT (DepEd lesson, Exodus 20:12).
Objectives follow the source: morning-routine words, a story told in order
(first / next / last), and talking about the child's own morning.
"""

LESSON = {
    "grade": 1, "quarter": 1, "week": 1, "day": 2,
    "title": "Getting Ready for School",
    "source": "LANG1Q1W1DAY2NARRATIONSCRIPT — Preparing for School (Exodus 20:12)",
    "bg": "media/image1.jpg",
    "next": "../../DAY3/INTERACTIVE/index.html",
    "slides": [
        {
            "type": "cover", "pose": "waving.png", "goal": 1,
            "title": "Getting Ready for School",
            "goals": ["Say 5 morning words", "Tell a story in order", "Talk about MY morning"],
            "say": "Good morning, my friend! (pause) I am Tala. (pause) Yesterday we talked about you and your family. "
                   "(pause) Today, we get ready for school!",
        },
        {
            "id": "words", "type": "cards", "pose": "pointing.png", "goal": 1,
            "title": "5 Morning Words",
            "say": "Every morning, we do five things. (pause) Listen. (pause) Then tap each picture and say the words with me!",
            "yourTurn": "Your turn! Tap each picture!",
            "items": [
                {"art": {"file": "media/art/wake-up.png", "prompt": "Tala (Filipino girl, 6) sitting up in her bed, stretching both arms high and yawning, morning sunlight on her face."}, "word": "wake up", "img": "media/image1.jpg", "say": "Wake up. (pause) We open our eyes."},
                {"word": "take a bath", "img": "media/image4.jpg", "say": "Take a bath. (pause) We use soap and water."},
                {"art": {"file": "media/art/get-dressed.png", "prompt": "Tala (Filipino girl, 6) putting on her Filipino public-school uniform: buttoning a white blouse, blue skirt, school bag beside her."}, "word": "get dressed", "img": "media/image5.jpg", "say": "Get dressed. (pause) We put on our clothes."},
                {"word": "eat breakfast", "img": "media/image7.jpg", "say": "Eat breakfast. (pause) Our first food of the day."},
                {"word": "brush teeth", "img": "media/image8.jpg", "say": "Brush your teeth. (pause) Clean and shiny!"},
            ],
        },
        {
            "id": "act", "type": "act", "pose": "clapping.png", "goal": 1,
            "title": "Show Me! Act It Out!",
            "say": "Let us play! (pause) Stand up. (pause) I say the words. (pause) You act them out!",
            "yourTurn": "Act it out, then tap!",
            "cmds": [
                {"word": "Wake up!", "sub": "Stretch your arms.", "img": "media/image1.jpg",
                 "say": "Wake up! (pause) Stretch your arms up high!"},
                {"word": "Take a bath!", "sub": "Scrub, scrub, scrub.", "img": "media/image4.jpg",
                 "say": "Take a bath! (pause) Scrub, scrub, scrub!"},
                {"word": "Get dressed!", "sub": "Button your shirt.", "img": "media/image5.jpg",
                 "say": "Get dressed! (pause) Button your shirt."},
                {"word": "Eat breakfast!", "sub": "Yum, yum!", "img": "media/image7.jpg",
                 "say": "Eat breakfast! (pause) Yum, yum!"},
                {"word": "Brush your teeth!", "sub": "Up and down.", "img": "media/image8.jpg",
                 "say": "Brush your teeth! (pause) Up and down, up and down."},
            ],
        },
        {
            "id": "find", "type": "pick", "pose": "thinking.png", "goal": 1,
            "title": "Listen and Tap!",
            "say": "Now, listen carefully. (pause) I say a word. (pause) You tap the right picture.",
            "yourTurn": "Tap the right picture!",
            "rounds": [
                {"ask": "Tap: brush teeth", "askSay": "Where is brush teeth? Tap it!",
                 "choices": [{"word": "wake up", "img": "media/image1.jpg"},
                             {"word": "brush teeth", "img": "media/image8.jpg", "ok": True},
                             {"word": "get dressed", "img": "media/image5.jpg"}]},
                {"ask": "Tap: eat breakfast", "askSay": "Where is eat breakfast? Tap it!",
                 "choices": [{"word": "eat breakfast", "img": "media/image7.jpg", "ok": True},
                             {"word": "take a bath", "img": "media/image4.jpg"},
                             {"word": "brush teeth", "img": "media/image8.jpg"}]},
                {"ask": "Tap: take a bath", "askSay": "Where is take a bath? Tap it!",
                 "choices": [{"word": "get dressed", "img": "media/image5.jpg"},
                             {"word": "wake up", "img": "media/image1.jpg"},
                             {"word": "take a bath", "img": "media/image4.jpg", "ok": True}]},
            ],
        },
        {
            "id": "story1", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Story: Before Going to School", "page": "Page 1",
            "img": "media/image5.jpg", "art": {"file": "media/art/story-wake-up.png", "prompt": "Sunrise in a Filipino family bedroom with two beds: Tala (6) and her little brother Bunso (5) waking up and stretching, a rooster crowing on the window sill outside.", "scene": True},
            "lines": ["This is Tala and Bunso.", "They wake up early.", "It is time for school!"],
            "say": "Story time! (pause) Our story is called, Before Going to School. (pause) "
                   "This is Tala and Bunso. (pause) They wake up early. (pause) It is time for school!",
        },
        {
            "id": "story2", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Story: Before Going to School", "page": "Page 2",
            "img": "media/image30.jpg",
            "lines": ["They take a bath.", "They get dressed.", "They eat breakfast."],
            "say": "Nanay says, hurry up! (pause) They take a bath. (pause) They get dressed. (pause) They eat breakfast. "
                   "(pause) Then they brush their teeth.",
        },
        {
            "id": "mid", "type": "pick", "pose": "raising_hand.png", "goal": 2,
            "title": "Quick! What Did They Do?",
            "say": "Quick question!",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "After the bath, they...", "askSay": "After the bath, what did they do?",
                 "choices": [{"word": "went to sleep", "img": "media/image1.jpg"},
                             {"word": "got dressed", "img": "media/image5.jpg", "ok": True}],
                 "yes": "Yes! They got dressed.", "yesSay": "Yes! They got dressed for school. (pause) Let us see what happens next!"},
            ],
        },
        {
            "id": "story3", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Story: Before Going to School", "page": "Page 3",
            "img": "media/image18.png",
            "lines": ["Oh no!", "The pencil is missing!", "The crayons are missing!"],
            "say": "But wait. (pause) Oh no! (pause) Bunso's pencil is missing! (pause) Tala's crayons are missing! "
                   "(pause) Where can they be?",
        },
        {
            "id": "story4", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Story: Before Going to School", "page": "Page 4",
            "img": "media/image20.png",
            "lines": ["Nanay helps them look.", "Under the bed!", "Thank you, Nanay!"],
            "say": "Nanay says, I will help you look. (pause) They look here. They look there. (pause) "
                   "Look! Under the bed! (pause) Thank you, Nanay!",
        },
        {
            "id": "order", "type": "order", "pose": "thinking.png", "goal": 2,
            "title": "What Happened First?",
            "say": "What happened in the story? (pause) Tap the pictures in order. (pause) First. (pause) Next. (pause) Last.",
            "yourTurn": "Tap what happened first!",
            "slots": ["First", "Next", "Last"],
            "items": [
                {"word": "They got ready.", "img": "media/image30.jpg", "say": "First, they got ready for school."},
                {"word": "Things were missing.", "img": "media/image18.png", "say": "Next, the pencil and crayons were missing."},
                {"word": "They found them!", "img": "media/under-bed.jpg", "say": "Last, they found them under the bed!"},
            ],
            "ask": ["What happened first?", "What happened next?", "What happened last?"],
            "yes": "First, next, last. You did it!",
            "yesSay": "First, next, last! (pause) You told the whole story!",
        },
        {
            "id": "who", "type": "pick", "pose": "raising_hand.png", "goal": 2,
            "title": "Think About the Story",
            "say": "Let us think about the story.",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "Who helped them look?", "askSay": "Who helped Tala and Bunso look for their things?",
                 "choices": [{"word": "Nanay", "pose": "NANAY/waving.png", "ok": True},
                             {"word": "Kuya", "pose": "KUYA/waving.png"},
                             {"word": "Ate", "pose": "ATE/waving.png"}],
                 "yes": "Yes! Nanay helped them.", "yesSay": "Yes! Nanay helped them. (pause) Our family helps us."},
                {"ask": "Where were the things?", "askSay": "Where were the pencil and crayons?",
                 "choices": [{"word": "in the bag"}, {"word": "under the bed", "ok": True}, {"word": "on the table"}],
                 "yes": "Yes! Under the bed!", "yesSay": "Yes! They were under the bed!"},
            ],
        },
        {
            "id": "my-morning", "type": "sentence", "pose": "point_self.png", "goal": 3,
            "title": "What do YOU do in the morning?",
            "say": "Now, let us talk about you! (pause) What do you do in the morning? (pause) Tap one. Then say it with me.",
            "yourTurn": "Tap one and say it!",
            "pre": "In the morning, I", "post": ".",
            "options": [
                {"word": "wake up", "img": "media/image1.jpg"},
                {"word": "take a bath", "img": "media/image4.jpg"},
                {"word": "eat breakfast", "img": "media/image7.jpg"},
                {"word": "brush my teeth", "img": "media/image8.jpg"},
            ],
        },
        {
            "id": "talk", "type": "talk", "pose": "talking.png", "goal": 3,
            "title": "Your Turn to Talk!",
            "say": "Tell me about your morning. (pause) Say: First, I wake up. (pause) Next, I eat breakfast. (pause) Your turn!",
            "yourTurn": "Say it out loud!",
            "frame": "First, I ____. Next, I ____.",
            "example": {"label": "Tala says", "text": "First, I wake up. Next, I eat breakfast."},
        },
        {
            "id": "verse", "type": "verse", "pose": "praying.png",
            "verse": "Honor your father and your mother.", "ref": "Exodus 20:12",
            "meaning": "Listen to Nanay and Tatay. Say thank you when they help you.",
            "say": "Our Bible verse is, (pause) Honor your father and your mother. (pause) "
                   "Honor means we listen to them. (pause) And we say thank you, like Tala and Bunso!",
            "verseSay": "Honor your father and your mother. (pause) Exodus twenty, verse twelve.",
        },
        {
            "id": "done", "type": "celebrate", "pose": "clapping.png",
            "title": "You Are Ready for School!",
            "recap": ["I know 5 morning words.", "I can tell first, next, last.", "I can talk about my morning."],
            "say": "Hooray! (pause) You learned five morning words. (pause) You told the story in order. "
                   "(pause) And you talked about your morning. (pause) See you tomorrow!",
        },
    ],
}
