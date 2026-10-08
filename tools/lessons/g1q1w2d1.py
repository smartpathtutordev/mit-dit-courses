"""Grade 1 English · Q1 W2 D1 · Names of Places.

Source: LANG1Q1W2DAY1LESSON (Street Names and Landmarks, Colossians 3:23).
Objectives: learn the words barangay, street, scenery and discover; listen to
"Miko and the Streets of Barangay Masaya" and name the character, setting
and places; tell why a place has its name and talk about one's own barangay.
"""

LESSON = {
    "grade": 1, "quarter": 1, "week": 2, "day": 1,
    "title": "Names of Places",
    "source": "LANG1Q1W2DAY1LESSON — Street Names and Landmarks (Colossians 3:23)",
    "bg": "media/image1.jpg",
    "next": "../../DAY2/INTERACTIVE/index.html",
    "slides": [
        {
            "type": "cover", "pose": "waving.png", "goal": 1,
            "title": "Names of Places",
            "goals": ["Learn 4 place words", "Listen to Miko's story", "Tell why places have names"],
            "say": "Hello again, my friend! (pause) Welcome to Week Two! (pause) "
                   "Today we go for a walk. (pause) We learn why places have names!",
        },
        {
            "id": "words", "type": "cards", "pose": "pointing.png", "goal": 1,
            "title": "4 Place Words",
            "say": "Let us learn four words. (pause) Tap each picture. (pause) Say the word with me!",
            "yourTurn": "Tap each picture!",
            "items": [
                {"word": "barangay", "sub": "where we live", "img": "media/image28.jpg",
                 "say": "Barangay. (pause) A barangay is the place where we live."},
                {"word": "street", "sub": "kalye", "img": "media/image25.jpg",
                 "say": "Street. (pause) Kalye. (pause) We walk on the street."},
                {"word": "scenery", "sub": "what we see outside", "img": "media/image9.jpg",
                 "say": "Scenery. (pause) Scenery is what we see outside. (pause) Like trees and mountains!"},
                {"art": {"file": "media/art/discover.png", "prompt": "Miko (Filipino boy, 7, blue T-shirt, brown shorts) looking through a big magnifying glass at a colourful butterfly on a flower, amazed happy face."}, "word": "discover", "sub": "find something new", "img": "media/image2.jpg",
                 "say": "Discover. (pause) To discover is to find something new!"},
            ],
        },
        {
            "id": "find", "type": "pick", "pose": "thinking.png", "goal": 1,
            "title": "Listen and Tap!",
            "say": "Listen carefully. (pause) Tap the right picture!",
            "yourTurn": "Tap the right picture!",
            "rounds": [
                {"ask": "Tap: street", "askSay": "Where is the street? Tap it!",
                 "choices": [{"word": "street", "img": "media/image25.jpg", "ok": True},
                             {"word": "scenery", "img": "media/image9.jpg"},
                             {"word": "discover", "img": "media/image2.jpg"}]},
                {"ask": "Tap: barangay", "askSay": "Where is the barangay? Tap it!",
                 "choices": [{"word": "discover", "img": "media/image2.jpg"},
                             {"word": "barangay", "img": "media/image28.jpg", "ok": True},
                             {"word": "street", "img": "media/image25.jpg"}]},
            ],
        },
        {
            "id": "s1", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Miko and the Streets", "page": "Page 1", "img": "media/image28.jpg",
            "lines": ["This is Miko.", "He lives in Barangay Masaya.", "He goes for a walk."],
            "say": "Story time! (pause) This is Miko. (pause) He lives in Barangay Masaya. (pause) "
                   "Masaya means happy! (pause) One morning, Miko goes for a walk.",
        },
        {
            "id": "s2", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Miko and the Streets", "page": "Page 2", "img": "media/image13.jpg",
            "lines": ["Miko walks on Bayani Street.", "Bayani means hero.", "People tell stories of heroes here."],
            "say": "First, Miko walks on Bayani Street. (pause) Bayani means hero. (pause) "
                   "Here, people tell stories about heroes!",
        },
        {
            "id": "mid", "type": "pick", "pose": "raising_hand.png", "goal": 3,
            "title": "Quick! Bayani Means...",
            "say": "Quick question!",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "Bayani means...", "askSay": "Bayani Street. (pause) What does bayani mean?",
                 "choices": [{"word": "hero", "img": "media/image13.jpg", "ok": True}, {"word": "tree"}],
                 "yes": "Yes! Bayani means hero.", "yesSay": "Yes! Bayani means hero. (pause) The name tells us about the street!"},
            ],
        },
        {
            "id": "s3", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Miko and the Streets", "page": "Page 3", "img": "media/image30.jpg",
            "lines": ["Next, Miko walks on Likas Street.", "Likas means nature.", "It has many trees and plants!"],
            "say": "Next, Miko walks on Likas Street. (pause) Likas means nature. (pause) "
                   "Look! (pause) So many trees and plants!",
        },
        {
            "id": "s4", "type": "story", "pose": "holding_book.png", "goal": 2,
            "title": "Miko and the Streets", "page": "Page 4", "img": "media/image31.jpg",
            "lines": ["Last, Miko stands on the Bridge of Hope.", "He sees the river.", "He thinks of his dreams."],
            "say": "Last, Miko stands on the Bridge of Hope. (pause) He sees the river and the trees. "
                   "(pause) He thinks about his dreams.",
        },
        {
            "id": "story-check", "type": "pick", "pose": "raising_hand.png", "goal": 2,
            "title": "Think About the Story",
            "say": "Let us think about the story.",
            "yourTurn": "Tap your answer!",
            "rounds": [
                {"ask": "Who is in the story?", "askSay": "Who is in the story?",
                 "choices": [{"word": "Miko", "img": "media/image9.jpg", "ok": True}, {"word": "Turtle"}, {"word": "Pina"}],
                 "yes": "Yes! Miko!", "yesSay": "Yes! The story is about Miko."},
                {"ask": "Where does Miko live?", "askSay": "Where does Miko live?",
                 "choices": [{"word": "Barangay Masaya", "ok": True}, {"word": "a big city"}, {"word": "a boat"}],
                 "yes": "Yes! Barangay Masaya.", "yesSay": "Yes! Miko lives in Barangay Masaya."},
            ],
        },
        {
            "id": "order", "type": "order", "pose": "thinking.png", "goal": 2,
            "title": "Where Did Miko Go?",
            "say": "Where did Miko walk? (pause) Tap the places in order. (pause) First. (pause) Next. (pause) Last.",
            "yourTurn": "Tap where Miko went first!",
            "slots": ["First", "Next", "Last"],
            "items": [
                {"word": "Bayani Street", "img": "media/image13.jpg", "say": "First, Bayani Street."},
                {"word": "Likas Street", "img": "media/image30.jpg", "say": "Next, Likas Street."},
                {"word": "Bridge of Hope", "img": "media/image31.jpg", "say": "Last, the Bridge of Hope."},
            ],
            "ask": ["Where did Miko go first?", "Where did Miko go next?", "Where did Miko go last?"],
            "yes": "You followed Miko's walk!",
            "yesSay": "First, next, last! (pause) You followed Miko's walk!",
        },
        {
            "id": "why", "type": "pick", "pose": "pointing.png", "goal": 3,
            "title": "Why This Name?",
            "say": "A name can tell us about a place. (pause) Let us guess!",
            "yourTurn": "Tap the best name!",
            "rounds": [
                {"ask": "Many mango trees grow here. Name it...",
                 "askSay": "This street has many mango trees. (pause) What is a good name?",
                 "choices": [{"word": "Mango Street", "ok": True}, {"word": "Fish Street"}, {"word": "Car Street"}],
                 "yes": "Yes! Mango Street!", "yesSay": "Yes! Mango Street! (pause) The name tells us about the mango trees."},
                {"ask": "Likas means nature. Likas Street has...",
                 "askSay": "Likas means nature. (pause) What does Likas Street have?",
                 "choices": [{"word": "many trees", "img": "media/image30.jpg", "ok": True},
                             {"word": "many cars"}],
                 "yes": "Yes! Many trees!", "yesSay": "Yes! Likas Street has many trees and plants."},
            ],
        },
        {
            "id": "my-place", "type": "talk", "pose": "talking.png", "goal": 3,
            "title": "Tell Me About Your Place!",
            "img": "media/image28.jpg",
            "say": "Now, tell me about your place. (pause) What is the name of your barangay? (pause) "
                   "Say: I live in Barangay Masaya. (pause) Use your own barangay!",
            "yourTurn": "Say your barangay!",
            "frame": "I live in Barangay ____.",
            "example": {"label": "Miko says", "text": "I live in Barangay Masaya."},
        },
        {
            "id": "verse", "type": "verse", "pose": "praying.png",
            "verse": "Whatever you do, work at it with all your heart.", "ref": "Colossians 3:23",
            "meaning": "Do your best when you learn and help in your barangay.",
            "say": "Our Bible verse is, (pause) Whatever you do, work at it with all your heart. "
                   "(pause) That means, always do your best!",
            "verseSay": "Whatever you do, (pause) work at it with all your heart. (pause) Colossians three, verse twenty-three.",
        },
        {
            "id": "done", "type": "celebrate", "pose": "clapping.png",
            "title": "Great Exploring!",
            "recap": ["I know: barangay, street, scenery, discover.", "I followed Miko's walk.", "Names tell about places."],
            "say": "Hooray! (pause) You learned four place words. (pause) You followed Miko's walk. "
                   "(pause) And you know why places have names. (pause) See you tomorrow!",
        },
    ],
}
