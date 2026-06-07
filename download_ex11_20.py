#!/usr/bin/env python3
"""Download all Exodus 11-20 illustrations from Pollinations.ai"""
import urllib.request
import os
import concurrent.futures
import time

BASE = "/var/www/bible-kids/images"
API = "https://image.pollinations.ai/prompt/{}?width=1024&height=768&nologo=true"

# Prompts for each chapter - 5 images each
PROMPTS = {
    # Chapter 11 - 最后一灾的预告
    "ex11": [
        "Moses standing before Pharaoh in the Egyptian palace, warning of the final plague, dramatic lighting, dark storm clouds outside, Pharaoh on throne looking angry, children's Bible illustration style, soft watercolor, gentle colors, no text",
        "Moses speaking to the Israelite elders, families gathered around listening intently, torches lighting the scene, anticipation and hope, children's picture book illustration, warm earth tones, no text",
        "Israelite families preparing in their homes at dusk, packing belongings, bread without yeast, sandals on feet, staff in hand, lamp light, tender family scene, watercolor style, no text",
        "Egyptian mother holding her child, dread and sorrow visible, dark night scene, moonlight through window, emotional but gentle for children, soft watercolor illustration, no text",
        "Moses leaving Pharaoh's palace in righteous anger, back turned, palace guards watching, dramatic sunset sky, children's Bible art, warm colors, no text"
    ],
    # Chapter 12 - 逾越节
    "ex12": [
        "Israelite family gathered around a table eating Passover meal, roasted lamb, unleavened bread, bitter herbs, lamp light, children attentive, warm family scene, children's book illustration watercolor style, no text",
        "Close-up of a wooden doorpost with lamb's blood painted on the lintel and side posts using hyssop branch, evening light, symbolic and meaningful, soft watercolor style, no text",
        "Angel of death passing over Israelite homes at night, glowing light above houses with blood-marked doors, peaceful houses below, dark sky, protective divine presence, children's Bible illustration, no text",
        "Egyptian families weeping at night, firstborn sons taken, moonlight, sorrow and tragedy depicted gently, ancient Egyptian homes, soft watercolor style suitable for children, no text",
        "Israelites leaving Egypt at dawn, families with donkeys carrying belongings, walking out of the city gates, morning light, hope and freedom, children's picture book illustration, warm colors, no text"
    ],
    # Chapter 13 - 除酵节，头生的归父，云柱火柱
    "ex13": [
        "Israelite family celebrating Feast of Unleavened Bread, flatbread on table, children learning traditions, warm home scene, teaching moment, watercolor children's illustration, no text",
        "Father presenting firstborn son to God, hands raised in dedication, family gathered, spiritual moment, gentle lighting, children's Bible picture book style, no text",
        "Pillar of cloud leading Israelites through wilderness by day, tall majestic cloud column against blue sky, people walking below with animals, desert landscape, children's illustration watercolor, no text",
        "Pillar of fire guiding Israelites at night, brilliant column of fire against dark desert sky, camp below with tents glowing warm, stars above, children's Bible art, no text",
        "Israelites journeying through desert wilderness, families walking together, donkeys and sheep, vast landscape, sense of journey and hope, soft watercolor style, no text"
    ],
    # Chapter 14 - 过红海
    "ex14": [
        "Israelites trapped between the Red Sea and Pharaoh's advancing army with chariots, dramatic moment, people looking back in fear, sea before them, dust cloud from army approaching, children's Bible illustration, no text",
        "Moses standing at the edge of the Red Sea stretching out his staff over the water, strong wind blowing his robe, divine power, dramatic scene, watercolor children's book style, no text",
        "Red Sea waters parting miraculously, walls of water on both sides, dry path through the middle, amazing miracle scene, fish visible in the water walls, children's picture book illustration, no text",
        "Israelites walking through the parted Red Sea on dry ground, families with children and animals, walls of water towering on both sides, awe and wonder, soft watercolor style, no text",
        "Egyptian army drowning as Red Sea waters crash back together, chariots and soldiers engulfed, powerful scene shown gently for children, watercolor Bible illustration, no text"
    ],
    # Chapter 15 - 摩西和米利暗的颂歌
    "ex15": [
        "Moses leading the Israelites in singing the Song of the Sea, people gathered on the shore, arms raised in praise, joyful celebration, Red Sea in background, children's Bible illustration watercolor, no text",
        "Miriam the prophetess dancing with a timbrel in her hand, joyful movement, colorful robe flowing, women following behind with tambourines, celebration by the sea, children's book style, no text",
        "Women dancing and playing tambourines in a circle, joyful celebration after crossing the Red Sea, colorful robes, movement and music, children's picture book illustration style, no text",
        "Israelites at Marah finding bitter undrinkable water, disappointed faces, desert oasis with palm trees, water that looks good but is bitter, children's Bible art watercolor, no text",
        "Moses throwing a tree branch into the bitter waters of Marah, waters turning sweet and clear, people drinking joyfully, miracle scene, oasis setting, soft watercolor style, no text"
    ],
    # Chapter 16 - 吗哪和鹌鹑
    "ex16": [
        "Israelites complaining in the wilderness, hungry families looking sad, desert camp setting, morning light, people gathered talking to Moses, children's Bible illustration watercolor, no text",
        "Manna from heaven covering the desert ground like white frost, coriander seed appearance, early morning dew, miraculous bread from God, soft golden light, children's picture book illustration, no text",
        "Israelite family gathering manna in baskets, children helping pick up the white flakes, morning scene in desert camp, wonder and provision, watercolor children's Bible style, no text",
        "Flocks of quails covering the Israelite camp at evening, birds everywhere, desert sunset colors, people catching quails, miraculous provision, children's book illustration, no text",
        "Family eating manna together, mother preparing bread from manna, jar of manna set aside as memorial, tent interior warm light, children's Bible art watercolor, no text"
    ],
    # Chapter 17 - 磐石出水，亚玛力人争战
    "ex17": [
        "Moses striking a large rock with his staff at Horeb, water gushing out miraculously, desert setting, thirsty people watching in amazement, miracle of water, children's Bible illustration watercolor, no text",
        "Israelite families drinking fresh water flowing from the struck rock, joy and relief, children cupping hands to drink, desert oasis scene, watercolor children's book style, no text",
        "Joshua leading Israelite army in battle against Amalekites in the valley, swords and shields, intense fighting scene, dust and action, children's Bible art style, no text",
        "Moses on top of the hill with hands raised holding the staff of God, Aaron on one side and Hur on the other holding up his arms, sunset sky, spiritual battle, watercolor illustration, no text",
        "Israelites victorious in battle, celebration scene, Joshua with raised sword, sunset victory, children's picture book Bible illustration, warm triumphant colors, no text"
    ],
    # Chapter 18 - 叶忒罗来访
    "ex18": [
        "Jethro arriving at the Israelite camp with Zipporah and Moses' two sons Gershom and Eliezer, desert camp setting, joyful reunion, tents in background, children's Bible illustration watercolor, no text",
        "Moses and Jethro embracing warmly, father-in-law and son-in-law reunion, desert camp, emotional family moment, tents and mountain background, watercolor children's book style, no text",
        "Moses sitting and judging the people from morning until evening, long line of Israelites waiting, everyone standing, tired Moses, desert setting, children's Bible art, no text",
        "Jethro giving wise counsel to Moses, two men sitting together in a tent, earnest conversation, wisdom being shared, warm light, watercolor children's Bible illustration, no text",
        "Moses appointing capable men as leaders of thousands hundreds fifties and tens, group of Israelite men being commissioned, orderly scene, delegation and organization, children's picture book style, no text"
    ],
    # Chapter 19 - 西奈山下
    "ex19": [
        "Israelites camped at the foot of Mount Sinai, vast desert camp with countless tents, majestic mountain towering above, morning light, holy anticipation, children's Bible illustration watercolor, no text",
        "Mount Sinai covered in thick smoke and fire, lightning flashing, dark clouds, God descending in fire, awe-inspiring scene, mountain trembling, dramatic children's Bible art, no text",
        "Loud trumpet blast sounding from the mountain, Israelites trembling at the foot, families huddled together in awe and fear, dramatic scene, children's picture book Bible illustration, no text",
        "Moses climbing up Mount Sinai into the thick darkness and smoke to meet God, solitary figure ascending, holy mountain, dramatic lighting, watercolor children's Bible style, no text",
        "Israelite families washing clothes and consecrating themselves at the foot of Sinai, preparing to meet God, washing at water basins, three days of preparation, reverent scene, children's book illustration, no text"
    ],
    # Chapter 20 - 十诫
    "ex20": [
        "God speaking the Ten Commandments from Mount Sinai, mountain covered in fire and smoke, divine voice, awe and majesty, voice of God booming, children's Bible illustration watercolor dramatic, no text",
        "Moses on Mount Sinai receiving two stone tablets with the Ten Commandments written by the finger of God, holy moment, divine light, awe, children's picture book Bible illustration, no text",
        "Israelites standing far off in fear at the foot of Mount Sinai, watching the mountain burning with fire, people afraid, dramatic holy scene, watercolor children's Bible art, no text",
        "Moses descending from Mount Sinai carrying the two stone tablets of testimony, face radiant, people waiting below, moment of revelation, children's book illustration watercolor, no text",
        "Israelite family in their tent talking about the Ten Commandments, parents teaching children, altar of earth nearby, warm family scene with the mountain visible, children's Bible illustration, no text"
    ],
}

def download_image(chapter, idx, prompt):
    """Download a single image"""
    url = API.format(urllib.request.quote(prompt))
    folder = os.path.join(BASE, chapter)
    filename = f"{chapter}_{idx:02d}.jpg"
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"  [SKIP] {filepath} exists ({os.path.getsize(filepath)} bytes)")
        return True

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BibleKids/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            if len(data) > 5000:
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"  [OK] {filepath} ({len(data)} bytes)")
                return True
            else:
                print(f"  [RETRY] {filepath} too small: {len(data)} bytes (attempt {attempt+1})")
        except Exception as e:
            print(f"  [ERR] {filepath}: {e} (attempt {attempt+1})")
        time.sleep(2)
    return False

def main():
    tasks = []
    for chapter, prompts in PROMPTS.items():
        for i, prompt in enumerate(prompts):
            tasks.append((chapter, i+1, prompt))

    print(f"Downloading {len(tasks)} images for Exodus 11-20...")
    failed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(download_image, ch, idx, prompt): (ch, idx)
                   for ch, idx, prompt in tasks}
        for future in concurrent.futures.as_completed(futures):
            ch, idx = futures[future]
            if not future.result():
                failed.append(f"{ch}_{idx:02d}")
                print(f"  [FAIL] {ch}_{idx:02d}")

    if failed:
        print(f"\nFAILED ({len(failed)}): {', '.join(failed)}")
    else:
        print(f"\nAll {len(tasks)} images downloaded successfully!")

if __name__ == "__main__":
    main()
