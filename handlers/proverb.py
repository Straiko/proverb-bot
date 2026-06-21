import json
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from services.database import Database
from services.ai_matcher import AIMatcher
from config import Config

router = Router()

CATEGORIES = [
    {"id": 1, "name": "мудрость", "emoji": "🧠"},
    {"id": 2, "name": "любовь", "emoji": "❤️"},
    {"id": 3, "name": "работа", "emoji": "💼"},
    {"id": 4, "name": "дружба", "emoji": "🤝"},
    {"id": 5, "name": "семья", "emoji": "👨‍👩‍👧‍👦"},
    {"id": 6, "name": "деньги", "emoji": "💰"},
    {"id": 7, "name": "удача", "emoji": "🍀"},
    {"id": 8, "name": "здоровье", "emoji": "💪"},
    {"id": 9, "name": "лень", "emoji": "😴"},
    {"id": 10, "name": "терпение", "emoji": "⏳"},
    {"id": 11, "name": "ум", "emoji": "🎓"},
    {"id": 12, "name": "правда", "emoji": "⚖️"},
    {"id": 13, "name": "трусость", "emoji": "🦁"},
    {"id": 14, "name": "зависть", "emoji": "👀"},
    {"id": 15, "name": "учёба", "emoji": "📚"},
]

PROVERBS = [
    # === МУДРОСТЬ ===
    {"id": 1, "text": "Не откладывай на завтра то, что можешь сделать сегодня.", "category_id": 1},
    {"id": 2, "text": "Семь раз отмерь, один раз отрежь.", "category_id": 1},
    {"id": 3, "text": "Голова без ума — как фонарь без свечи.", "category_id": 1},
    {"id": 4, "text": "Одна ласточка весны не делает.", "category_id": 1},
    {"id": 5, "text": "Ум — хорошо, а два лучше.", "category_id": 1},
    {"id": 6, "text": "Что посеешь, то и пожнёшь.", "category_id": 1},
    {"id": 7, "text": "Язык до Киева доведёт.", "category_id": 1},
    {"id": 8, "text": "Не всё то золото, что блестит.", "category_id": 1},
    {"id": 9, "text": "Правда глаза колет.", "category_id": 1},
    {"id": 10, "text": "Не спи — смотри, не зевай — слушай.", "category_id": 1},
    {"id": 11, "text": "Одна голова хорошо, а две лучше.", "category_id": 1},
    {"id": 12, "text": "Не всё коту масленица.", "category_id": 1},
    {"id": 13, "text": "В тесноте, да не в обиде.", "category_id": 1},
    {"id": 14, "text": "Мудрость приходит с опытом.", "category_id": 1},
    {"id": 15, "text": "Знание — сила.", "category_id": 1},

    # === ЛЮБОВЬ ===
    {"id": 16, "text": "Любовь зла, полюбишь и козла.", "category_id": 2},
    {"id": 17, "text": "Влюблённому всё не спится.", "category_id": 2},
    {"id": 18, "text": "Сердцу не прикажешь.", "category_id": 2},
    {"id": 19, "text": "Любовь — не картошка, не выбросишь из огорода.", "category_id": 2},
    {"id": 20, "text": "Где любовь, там и Бог.", "category_id": 2},
    {"id": 21, "text": "С глаз долой — из сердца вон.", "category_id": 2},
    {"id": 22, "text": "Милые бранятся — только тешатся.", "category_id": 2},
    {"id": 23, "text": "Любишь кататься — люби и саночки возить.", "category_id": 2},
    {"id": 24, "text": "Любовь не пожар, а загорится — не потушишь.", "category_id": 2},
    {"id": 25, "text": "Милый не злодей, а иссушил до костей.", "category_id": 2},
    {"id": 26, "text": "От любви до ненависти — один шаг.", "category_id": 2},
    {"id": 27, "text": "Старая любовь не забывается.", "category_id": 2},
    {"id": 28, "text": "С милым рай и в шалаше.", "category_id": 2},
    {"id": 29, "text": "Любовь слепа.", "category_id": 2},
    {"id": 30, "text": "Без любимого и мир постыл.", "category_id": 2},

    # === РАБОТА ===
    {"id": 31, "text": "Без труда не вытащишь и рыбку из пруда.", "category_id": 3},
    {"id": 32, "text": "Под лежачий камень вода не течёт.", "category_id": 3},
    {"id": 33, "text": "Хочешь есть калачи — не сиди на печи.", "category_id": 3},
    {"id": 34, "text": "Работа — не волк, в лес не убежит.", "category_id": 3},
    {"id": 35, "text": "Труд кормит, а лень портит.", "category_id": 3},
    {"id": 36, "text": "Кто не работает, тот не ест.", "category_id": 3},
    {"id": 37, "text": "Дело мастера боится.", "category_id": 3},
    {"id": 38, "text": "Кто рано встаёт, тому Бог подаёт.", "category_id": 3},
    {"id": 39, "text": "Терпение и труд всё перетрут.", "category_id": 3},
    {"id": 40, "text": "С молитвой в устах, с работой в руках.", "category_id": 3},
    {"id": 41, "text": "Не откладывай на завтра то, что можешь сделать сегодня.", "category_id": 3},
    {"id": 42, "text": "Дело учит, и мучит, и кормит.", "category_id": 3},
    {"id": 43, "text": "Конец — делу венец.", "category_id": 3},
    {"id": 44, "text": "Работа в руках плесневеет.", "category_id": 3},
    {"id": 45, "text": "Скоро сказка сказывается, да не скоро дело делается.", "category_id": 3},

    # === ДРУЖБА ===
    {"id": 46, "text": "Друг познаётся в беде.", "category_id": 4},
    {"id": 47, "text": "Один в поле не воин.", "category_id": 4},
    {"id": 48, "text": "Старый друг лучше новых двух.", "category_id": 4},
    {"id": 49, "text": "Не имей сто рублей, а имей сто друзей.", "category_id": 4},
    {"id": 50, "text": "Друзья познаются в беде.", "category_id": 4},
    {"id": 51, "text": "В беде дружок познаётся.", "category_id": 4},
    {"id": 52, "text": "Друг за друга стоять — и врага одолеть.", "category_id": 4},
    {"id": 53, "text": "Без друга на душе вьюга.", "category_id": 4},
    {"id": 54, "text": "Верный друг — лучше тысячи слуг.", "category_id": 4},
    {"id": 55, "text": "Друга ищи, а найдешь — береги.", "category_id": 4},

    # === СЕМЬЯ ===
    {"id": 56, "text": "В семье союз, так и дом не разрушится.", "category_id": 5},
    {"id": 57, "text": "Семья — крепость, пока в ней любовь.", "category_id": 5},
    {"id": 58, "text": "В гостях хорошо, а дома лучше.", "category_id": 5},
    {"id": 59, "text": "Дитя — цветок жизни.", "category_id": 5},
    {"id": 60, "text": "Дома и стены помогают.", "category_id": 5},
    {"id": 61, "text": "Своя хатка — что родная матка.", "category_id": 5},
    {"id": 62, "text": "Всякому мила своя сторона.", "category_id": 5},
    {"id": 63, "text": "Дома все споро, а вчуже житье хуже.", "category_id": 5},
    {"id": 64, "text": "Родная землица и во сне снится.", "category_id": 5},
    {"id": 65, "text": "В родном углу все по нутру.", "category_id": 5},

    # === ДЕНЬГИ ===
    {"id": 66, "text": "Деньги не пахнут.", "category_id": 6},
    {"id": 67, "text": "Деньги — не всё, но без них — ничего.", "category_id": 6},
    {"id": 68, "text": "Грех да беда, кому нет и холода.", "category_id": 6},
    {"id": 69, "text": "Мал золотник, да дорог.", "category_id": 6},
    {"id": 70, "text": "Голь на выдумки хитра.", "category_id": 6},
    {"id": 71, "text": "Дарёному коню в зубы не смотрят.", "category_id": 6},
    {"id": 72, "text": "На чужой каравай рот не разевай.", "category_id": 6},
    {"id": 73, "text": "Деньга лежит, а шкура дрожит.", "category_id": 6},
    {"id": 74, "text": "У скупого и в Крещенье льду не выпросишь.", "category_id": 6},
    {"id": 75, "text": "Добрый хозяин — господин деньгам, а плохой — слуга.", "category_id": 6},

    # === УДАЧА ===
    {"id": 76, "text": "На бога надейся, а сам не плошай.", "category_id": 7},
    {"id": 77, "text": "Везёт тому, кто ждёт.", "category_id": 7},
    {"id": 78, "text": "Счастье любит тишину.", "category_id": 7},
    {"id": 79, "text": "Кто ищет, тот найдёт.", "category_id": 7},
    {"id": 80, "text": "Лучше синица в руках, чем журавль в небе.", "category_id": 7},
    {"id": 81, "text": "Волков бояться — в лес не ходить.", "category_id": 7},
    {"id": 82, "text": "Кто не рискует, тот не пьёт шампанского.", "category_id": 7},
    {"id": 83, "text": "Фортуна улыбается храбрым.", "category_id": 7},
    {"id": 84, "text": "Удача — это когда机会呈现在准备好的人面前.", "category_id": 7},
    {"id": 85, "text": "Пока гром не грянет, мужик не перекрестится.", "category_id": 7},

    # === ЗДОРОВЬЕ ===
    {"id": 86, "text": "Здоровье — дороже золота.", "category_id": 8},
    {"id": 87, "text": "Болен — лечись, а здоров берегись.", "category_id": 8},
    {"id": 88, "text": "Движение — жизнь.", "category_id": 8},
    {"id": 89, "text": "В здоровом теле — здоровый дух.", "category_id": 8},
    {"id": 90, "text": "Бережёного Бог бережёт.", "category_id": 8},
    {"id": 91, "text": "Здоровье — богатство, а болезнь — нищета.", "category_id": 8},
    {"id": 92, "text": "Чистота — здоровье.", "category_id": 8},
    {"id": 93, "text": "Свежий воздух и вода — лучшие лекарства.", "category_id": 8},
    {"id": 94, "text": "Ешь простую пищу — будешь здоров.", "category_id": 8},
    {"id": 95, "text": "Сон — лучшее лекарство.", "category_id": 8},

    # === ЛЕНЬ ===
    {"id": 96, "text": "Лень — мать всех пороков.", "category_id": 9},
    {"id": 97, "text": "Ленивому всё не успеть.", "category_id": 9},
    {"id": 98, "text": "У ленивого и крыша течёт, и печь не печёт.", "category_id": 9},
    {"id": 99, "text": "Пьяный проснится, а дурак никогда.", "category_id": 9},
    {"id": 100, "text": "Ленивый сидя спит, лежа работает.", "category_id": 9},
    {"id": 101, "text": "Спишь до обеда — пеняй на соседа.", "category_id": 9},
    {"id": 102, "text": "Лентяй до обеда здоров, а после обеда болен.", "category_id": 9},
    {"id": 103, "text": "Безделье — мать всех пороков.", "category_id": 9},
    {"id": 104, "text": "Ленивый и могилы не стоит.", "category_id": 9},
    {"id": 105, "text": "Лень не кормит, а только пучит.", "category_id": 9},

    # === ТЕРПЕНИЕ ===
    {"id": 106, "text": "Тише едешь, дальше будешь.", "category_id": 10},
    {"id": 107, "text": "Лучше поздно, чем никогда.", "category_id": 10},
    {"id": 108, "text": "Жди и дождёшься.", "category_id": 10},
    {"id": 109, "text": "Время — лучший лекарь.", "category_id": 10},
    {"id": 110, "text": "Поспешай медленно.", "category_id": 10},
    {"id": 111, "text": "Не всё сразу, а всё по порядку.", "category_id": 10},
    {"id": 112, "text": "Терпение — золото.", "category_id": 10},
    {"id": 113, "text": "Человек — не камень: терпит-терпит, да и треснет.", "category_id": 10},
    {"id": 114, "text": "Терпение и труд всё перетрут.", "category_id": 10},
    {"id": 115, "text": "Переделкино терпенье.", "category_id": 10},

    # === УМ ===
    {"id": 116, "text": "Ум за разум заходит.", "category_id": 11},
    {"id": 117, "text": "Умный не говорит всё, что знает.", "category_id": 11},
    {"id": 118, "text": "Умный молчит, когда дурак ворчит.", "category_id": 11},
    {"id": 119, "text": "Ум бороды не ждёт.", "category_id": 11},
    {"id": 120, "text": "Ум не в бороде, а в голове.", "category_id": 11},
    {"id": 121, "text": "С умом жить — беды избыть.", "category_id": 11},
    {"id": 122, "text": "Умная голова сто голов кормит.", "category_id": 11},
    {"id": 123, "text": "Глупый спорит с каждым, умный — с равным.", "category_id": 11},
    {"id": 124, "text": "Умного слушай, дурака учить не пытай.", "category_id": 11},
    {"id": 125, "text": "Умей вовремя сказать, вовремя смолчать.", "category_id": 11},

    # === ПРАВДА ===
    {"id": 126, "text": "Правда дороже золота.", "category_id": 12},
    {"id": 127, "text": "Правда светлее солнца.", "category_id": 12},
    {"id": 128, "text": "За правого Бог и добрые люди.", "category_id": 12},
    {"id": 129, "text": "Правда суда не боится.", "category_id": 12},
    {"id": 130, "text": "Не в силе Бог, а в правде.", "category_id": 12},
    {"id": 131, "text": "Ложью правды не выручишь.", "category_id": 12},
    {"id": 132, "text": "Правда как солнце: затмить нельзя.", "category_id": 12},
    {"id": 133, "text": "Кто правдой живёт, тот добро наживёт.", "category_id": 12},
    {"id": 134, "text": "Правда — свет разума.", "category_id": 12},
    {"id": 135, "text": "Без правды не проживёшь.", "category_id": 12},

    # === ТРУСОСТЬ ===
    {"id": 136, "text": "Смелость города берёт.", "category_id": 13},
    {"id": 137, "text": "Кто смел, тот и съел.", "category_id": 13},
    {"id": 138, "text": "Смелому Бог владеет.", "category_id": 13},
    {"id": 139, "text": "Глаза боятся, а руки делают.", "category_id": 13},
    {"id": 140, "text": "Не так страшен чёрт, как его малюют.", "category_id": 13},
    {"id": 141, "text": "У страха глаза велики.", "category_id": 13},
    {"id": 142, "text": "Трус и тени своей боится.", "category_id": 13},
    {"id": 143, "text": "После драки кулаками не машут.", "category_id": 13},
    {"id": 144, "text": "Смелый приступ — половина победы.", "category_id": 13},
    {"id": 145, "text": "Храбрый не тот, кто страха не знает, а кто узнал и навстречу идёт.", "category_id": 13},

    # === ЗАВИСТЬ ===
    {"id": 146, "text": "Завистью ничего не возьмешь.", "category_id": 14},
    {"id": 147, "text": "Завидливые глаза не знают стыда.", "category_id": 14},
    {"id": 148, "text": "Зависть — что ржа: съедает.", "category_id": 14},
    {"id": 149, "text": "Злой плачет от зависти, а добрый от радости.", "category_id": 14},
    {"id": 150, "text": "На чужую кучу нечего глаза пучить.", "category_id": 14},
    {"id": 151, "text": "Чужим здоровьем болен.", "category_id": 14},
    {"id": 152, "text": "Зависть — худой советчик.", "category_id": 14},
    {"id": 153, "text": "Кто чужого желает, скоро своё утратит.", "category_id": 14},
    {"id": 154, "text": "Зависть и клевета живут совместно.", "category_id": 14},
    {"id": 155, "text": "Лучше быть у других в зависти, чем самому в кручине.", "category_id": 14},

    # === УЧЁБА ===
    {"id": 156, "text": "Учение — свет, а неучение — тьма.", "category_id": 15},
    {"id": 157, "text": "Век живи — век учись.", "category_id": 15},
    {"id": 158, "text": "Учиться никогда не поздно.", "category_id": 15},
    {"id": 159, "text": "Корень учения горек, да плод его сладок.", "category_id": 15},
    {"id": 160, "text": "Повторение — мать учения.", "category_id": 15},
    {"id": 161, "text": "На ошибках учатся.", "category_id": 15},
    {"id": 162, "text": "Учись смолоду, пригодится на старость.", "category_id": 15},
    {"id": 163, "text": "Не стыдно не знать, стыдно не учиться.", "category_id": 15},
    {"id": 164, "text": "Книга — лучший друг.", "category_id": 15},
    {"id": 165, "text": "Чтение — лучшее учение.", "category_id": 15},

    # === ДОБРО ===
    {"id": 166, "text": "Делай добро и жди добра.", "category_id": 1},
    {"id": 167, "text": "За добро плати добром.", "category_id": 1},
    {"id": 168, "text": "Доброе дело два века живёт.", "category_id": 1},
    {"id": 169, "text": "Доброе дело лучше мягкого пирога.", "category_id": 1},
    {"id": 170, "text": "Доброта без разума пуста.", "category_id": 1},

    # === СЛОВО ===
    {"id": 171, "text": "Слово — серебро, молчание — золото.", "category_id": 11},
    {"id": 172, "text": "Слово не воробей: вылетит — не поймаешь.", "category_id": 11},
    {"id": 173, "text": "Доброе слово человеку — что дождь в засуху.", "category_id": 11},
    {"id": 174, "text": "Ласковым словом и камень растопишь.", "category_id": 11},
    {"id": 175, "text": "Доброе слово железные ворота отопрёт.", "category_id": 11},
    {"id": 176, "text": "Не болтай наугад — клади слово в лад.", "category_id": 11},
    {"id": 177, "text": "Острое словечко колет сердечко.", "category_id": 11},
    {"id": 178, "text": "Держи язык за зубами.", "category_id": 11},
    {"id": 179, "text": "Не спеши языком, торопись делом.", "category_id": 11},
    {"id": 180, "text": "Язык мой — враг мой.", "category_id": 11},

    # === ДОБРО И ЗЛО ===
    {"id": 181, "text": "Добро худо переможет.", "category_id": 1},
    {"id": 182, "text": "За добро постоим, а на зло настоим.", "category_id": 1},
    {"id": 183, "text": "Добро не умрёт, а зло пропадёт.", "category_id": 1},
    {"id": 184, "text": "От добра до худа один шажок.", "category_id": 1},
    {"id": 185, "text": "Не рой другому яму — сам в неё попадешь.", "category_id": 1},

    # === СОВЕСТЬ ===
    {"id": 186, "text": "Нечистая совесть спать не даёт.", "category_id": 12},
    {"id": 187, "text": "Добрая совесть — глаз Божий.", "category_id": 12},
    {"id": 188, "text": "Совесть без зубов, а загрызет.", "category_id": 12},
    {"id": 189, "text": "К чистому поганое не пристанет.", "category_id": 12},
    {"id": 190, "text": "Лучше быть честным бедняком, чем богатым подлецом.", "category_id": 12},

    # === СМЕЛОСТЬ ===
    {"id": 191, "text": "Смелым Бог владеет, пьяным чёрт качает.", "category_id": 13},
    {"id": 192, "text": "От смелого и смерть бежит.", "category_id": 13},
    {"id": 193, "text": "Смелый там найдёт, где робкий потеряет.", "category_id": 13},
    {"id": 194, "text": "Риск — благородное дело.", "category_id": 13},
    {"id": 195, "text": "Кто дрожит — тот и бежит.", "category_id": 13},

    # === ЖИЗНЬ ===
    {"id": 196, "text": "Человек не грибок, в день не вырастет.", "category_id": 1},
    {"id": 197, "text": "Человек предполагает, а Бог располагает.", "category_id": 1},
    {"id": 198, "text": "Не всё коту масленица, есть и Великий пост.", "category_id": 1},
    {"id": 199, "text": "Жизнь прожить — не поле перейти.", "category_id": 1},
    {"id": 200, "text": "Не родись красивым, а родись счастливым.", "category_id": 1},
]


def load_proverbs(proverbs_path: str) -> dict:
    try:
        with open(proverbs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": CATEGORIES, "proverbs": PROVERBS}


@router.message(Command("proverb"))
async def cmd_random_proverb(message: Message, db: Database, config: Config):
    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]
    proverb = random.choice(proverbs)

    await message.answer(
        f"📜 {proverb['text']}\n\n⭐ Добавить в избранное",
        reply_markup={
            "inline_keyboard": [[
                {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"},
            ]]
        }
    )


@router.message(Command("daily"))
async def cmd_daily(message: Message, db: Database, config: Config):
    from datetime import date
    today = date.today().isoformat()

    daily_id = await db.get_daily_proverb_id(today)
    if daily_id:
        data = load_proverbs(config.PROVERBS_PATH)
        proverb = next((p for p in data["proverbs"] if p["id"] == daily_id), None)
        if proverb:
            await message.answer(f"📅 Пословица дня:\n\n📜 {proverb['text']}")
            return

    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]
    proverb = random.choice(proverbs)

    await db.set_daily_proverb(today, proverb["id"])

    await message.answer(
        f"📅 Пословица дня:\n\n📜 {proverb['text']}\n\n⭐ Добавить в избранное",
        reply_markup={
            "inline_keyboard": [[
                {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"}
            ]]
        }
    )


@router.callback_query(F.data.startswith("fav_add_"))
async def add_favorite(callback: CallbackQuery, db: Database):
    proverb_id = int(callback.data.split("_")[2])
    await db.add_favorite(callback.from_user.id, proverb_id)
    await callback.answer("✅ Добавлено в избранное!")
    await callback.message.edit_reply_markup()


@router.message(F.text & ~F.text.startswith("/"))
async def match_proverb(message: Message, db: Database, config: Config, ai_matcher: AIMatcher):
    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]

    matched_text = ai_matcher.match_proverb(message.text, proverbs)

    matched_proverb = next(
        (p for p in proverbs if p["text"].lower() in matched_text.lower() or matched_text.lower() in p["text"].lower()),
        None
    )

    if matched_proverb:
        await message.answer(
            f"📜 {matched_proverb['text']}\n\n⭐ Добавить в избранное",
            reply_markup={
                "inline_keyboard": [[
                    {"text": "⭐ В избранное", "callback_data": f"fav_add_{matched_proverb['id']}"}
                ]]
            }
        )
    else:
        await message.answer(f"📜 {matched_text}")
