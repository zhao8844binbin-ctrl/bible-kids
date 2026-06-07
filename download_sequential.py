#!/usr/bin/env python3
"""Download Exodus 11-20 images from Pollinations.ai - sequential with waits"""
import urllib.request
import urllib.parse
import os
import time
import sys

BASE = "/var/www/bible-kids/images"
POLLINATIONS = "https://image.pollinations.ai/prompt/{}?width=1024&height=768&nologo=true"

# All prompts, organized by chapter
PROMPTS = {
    "ex11": [
        ("ex11_01", "Moses standing before Pharaoh in the Egyptian palace, warning of the final plague, dramatic lighting, dark storm clouds outside, Pharaoh on throne looking angry, childrens Bible illustration, watercolor, no text"),
        ("ex11_02", "Moses speaking to Israelite elders, families gathered listening, torches lighting the scene, hope and anticipation, childrens book illustration, warm earth tones, no text"),
        ("ex11_04", "Egyptian mother holding her child gently, sorrow visible, dark night, moonlight through window, ancient Egyptian home, soft watercolor illustration for children, no text"),
        ("ex11_05", "Moses leaving Pharaohs palace in anger, back turned, palace guards watching, dramatic sunset sky, childrens Bible art, warm colors, no text"),
    ],
    "ex12": [
        ("ex12_01", "Israelite family gathered around table eating Passover meal, roasted lamb, unleavened bread, lamp light, children attentive, warm family scene, childrens book watercolor, no text"),
        ("ex12_02", "Close-up of wooden doorpost with lamb blood painted on lintel using hyssop branch, evening light, symbolic, soft watercolor, no text"),
        ("ex12_03", "Angel of death passing over Israelite homes at night, glowing light above houses with blood-marked doors, dark sky, protective presence, childrens Bible illustration, no text"),
        ("ex12_04", "Egyptian families weeping gently at night, moonlight, sorrow in ancient Egyptian homes, soft watercolor for children, no text"),
        ("ex12_05", "Israelites leaving Egypt at dawn, families with donkeys carrying belongings, morning light, hope and freedom, childrens picture book watercolor, no text"),
    ],
    "ex13": [
        ("ex13_01", "Israelite family celebrating Feast of Unleavened Bread, flatbread on table, children learning, warm home scene, watercolor childrens illustration, no text"),
        ("ex13_02", "Father presenting firstborn son with hands raised in dedication, family gathered, spiritual moment, gentle light, childrens Bible picture book, no text"),
        ("ex13_03", "Pillar of cloud leading Israelites through desert by day, majestic cloud against blue sky, people walking below, desert landscape, watercolor illustration, no text"),
        ("ex13_04", "Pillar of fire guiding Israelites at night, brilliant column of fire, dark desert sky, camp tents glowing warm, stars above, childrens Bible art, no text"),
        ("ex13_05", "Israelites journeying through desert wilderness, families walking together, donkeys and sheep, vast landscape, journey and hope, soft watercolor, no text"),
    ],
    "ex14": [
        ("ex14_01", "Israelites trapped between the Red Sea and Pharaohs chariot army, people looking back in fear, sea before them, dust from approaching army, childrens Bible illustration, no text"),
        ("ex14_02", "Moses at edge of Red Sea stretching staff over water, wind blowing his robe, divine power, dramatic scene, watercolor childrens book, no text"),
        ("ex14_03", "Red Sea waters parting miraculously, walls of water on both sides, dry path through middle, fish visible in water walls, childrens picture book illustration, no text"),
        ("ex14_04", "Israelites walking through parted Red Sea on dry ground, families with children and animals, towering water walls, awe and wonder, watercolor, no text"),
        ("ex14_05", "Egyptian army drowning as Red Sea waters crash back, chariots engulfed, powerful scene shown gently for children, watercolor Bible illustration, no text"),
    ],
    "ex15": [
        ("ex15_01", "Moses leading Israelites singing the Song of the Sea, people on shore arms raised in praise, joyful celebration, Red Sea background, childrens Bible watercolor, no text"),
        ("ex15_02", "Miriam prophetess dancing with timbrel, joyful movement, colorful robe flowing, women following with tambourines, celebration by sea, childrens book, no text"),
        ("ex15_03", "Women dancing and playing tambourines in circle, joyful celebration after Red Sea crossing, colorful robes, movement and music, childrens picture book, no text"),
        ("ex15_04", "Israelites at Marah finding bitter water, disappointed faces, desert oasis with palm trees, water looks good but bitter, childrens Bible art watercolor, no text"),
        ("ex15_05", "Moses throwing tree branch into bitter waters of Marah, waters turning sweet and clear, people drinking joyfully, oasis scene, soft watercolor, no text"),
    ],
    "ex16": [
        ("ex16_01", "Israelites complaining in wilderness, hungry families looking sad, desert camp, morning light, people gathered around Moses, childrens Bible watercolor, no text"),
        ("ex16_02", "Manna covering desert ground like white frost, coriander seed appearance, early morning dew, miraculous bread, soft golden light, childrens picture book, no text"),
        ("ex16_03", "Israelite family gathering manna in baskets, children helping pick up white flakes, morning scene in desert camp, wonder and provision, watercolor childrens Bible, no text"),
        ("ex16_04", "Flocks of quails covering Israelite camp at evening, birds everywhere, desert sunset colors, people catching quails, miraculous provision, childrens book, no text"),
        ("ex16_05", "Family eating manna together, mother preparing bread, jar of manna set aside as memorial, tent interior warm light, childrens Bible art watercolor, no text"),
    ],
    "ex17": [
        ("ex17_01", "Moses striking large rock with staff at Horeb, water gushing out miraculously, desert, thirsty people watching amazed, childrens Bible illustration watercolor, no text"),
        ("ex17_02", "Israelite families drinking fresh water flowing from struck rock, joy and relief, children cupping hands to drink, desert oasis, watercolor childrens book, no text"),
        ("ex17_03", "Joshua leading Israelite army in battle against Amalekites in valley, swords and shields, intense fighting, dust and action, childrens Bible art, no text"),
        ("ex17_04", "Moses on hilltop with hands raised holding staff, Aaron and Hur holding up his arms on each side, sunset sky, spiritual battle, watercolor illustration, no text"),
        ("ex17_05", "Israelites victorious in battle celebrating, Joshua with raised sword, sunset victory, childrens picture book Bible illustration, warm triumphant colors, no text"),
    ],
    "ex18": [
        ("ex18_01", "Jethro arriving at Israelite camp with Zipporah and Moses two sons, desert camp setting, joyful reunion, tents background, childrens Bible watercolor, no text"),
        ("ex18_02", "Moses and Jethro embracing warmly, father-in-law and son-in-law reunion, desert camp, emotional family moment, tents and mountain, watercolor childrens book, no text"),
        ("ex18_03", "Moses sitting judging people from morning until evening, long line of Israelites waiting, everyone standing, tired Moses, desert, childrens Bible art, no text"),
        ("ex18_04", "Jethro giving wise counsel to Moses, two men sitting together in tent, earnest conversation, wisdom shared, warm light, watercolor childrens Bible, no text"),
        ("ex18_05", "Moses appointing capable men as leaders of thousands hundreds fifties tens, group being commissioned, orderly scene, delegation, childrens picture book, no text"),
    ],
    "ex19": [
        ("ex19_01", "Israelites camped at foot of Mount Sinai, vast desert camp with countless tents, majestic mountain towering above, morning light, anticipation, childrens Bible watercolor, no text"),
        ("ex19_02", "Mount Sinai covered in thick smoke and fire, lightning flashing, dark clouds, divine presence, mountain trembling, dramatic childrens Bible art, no text"),
        ("ex19_03", "Loud trumpet blast from mountain, Israelites trembling at foot, families huddled in awe and fear, dramatic holy scene, childrens picture book Bible, no text"),
        ("ex19_04", "Moses climbing Mount Sinai into thick darkness and smoke, solitary figure ascending, holy mountain, dramatic lighting, watercolor childrens Bible, no text"),
        ("ex19_05", "Israelite families washing clothes at foot of Sinai, preparing to meet God, washing at water basins, reverent preparation scene, childrens book, no text"),
    ],
    "ex20": [
        ("ex20_01", "God speaking Ten Commandments from Mount Sinai, mountain covered in fire and smoke, divine voice, awe and majesty, childrens Bible illustration dramatic watercolor, no text"),
        ("ex20_02", "Moses on Mount Sinai receiving two stone tablets with Ten Commandments, holy moment, divine light, awe, childrens picture book Bible illustration, no text"),
        ("ex20_03", "Israelites standing far off in fear at foot of Mount Sinai, watching mountain burning with fire, dramatic holy scene, watercolor childrens Bible art, no text"),
        ("ex20_04", "Moses descending from Mount Sinai carrying two stone tablets, face radiant, people waiting below, moment of revelation, watercolor childrens book, no text"),
        ("ex20_05", "Israelite family in tent talking about Ten Commandments, parents teaching children, warm family scene, mountain visible, childrens Bible watercolor, no text"),
    ],
}

def download_image(chapter, filename, prompt):
    filepath = os.path.join(BASE, chapter, f"{filename}.jpg")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"  [SKIP] {filename} (exists, {os.path.getsize(filepath)} bytes)")
        return True

    url = POLLINATIONS.format(urllib.parse.quote(prompt, safe=''))

    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BibleKids/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()

            if len(data) > 5000:
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"  [OK] {filename} ({len(data)} bytes)")
                return True
            else:
                print(f"  [SMALL] {filename}: {len(data)} bytes (attempt {attempt+1})")
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='replace')[:200]
            if "402" in str(e) or "Queue full" in body:
                print(f"  [RATE] {filename}: rate limited (attempt {attempt+1}), waiting...")
                time.sleep(30)
            else:
                print(f"  [HTTP {e.code}] {filename}: {body} (attempt {attempt+1})")
                time.sleep(10)
        except Exception as e:
            print(f"  [ERR] {filename}: {e} (attempt {attempt+1})")
            time.sleep(10)

    return False

def main():
    all_tasks = []
    for chapter, prompts in PROMPTS.items():
        for filename, prompt in prompts:
            all_tasks.append((chapter, filename, prompt))

    total = len(all_tasks)
    print(f"Total images to download: {total}")
    completed = 0
    failed = []

    for chapter, filename, prompt in all_tasks:
        print(f"\n[{completed+1}/{total}] {filename}")
        ok = download_image(chapter, filename, prompt)
        if ok:
            completed += 1
        else:
            failed.append(filename)
        # Wait between requests to avoid rate limiting
        if completed < total:
            time.sleep(10)

    print(f"\n=== DONE ===")
    print(f"Completed: {completed}/{total}")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    else:
        print("All images downloaded!")

if __name__ == "__main__":
    main()
