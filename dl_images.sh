#!/bin/bash
# Download Exodus 11-20 images from Pollinations.ai using curl
# Images are downloaded sequentially with waits between requests

BASE="/var/www/bible-kids/images"
POLLINATIONS="https://image.pollinations.ai/prompt"

TOTAL=0
COMPLETED=0
FAILED=""

download() {
  local chapter=$1 filename=$2 prompt=$3
  local filepath="${BASE}/${chapter}/${filename}.jpg"
  local encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''${prompt}'''))")
  local url="${POLLINATIONS}/${encoded}?width=1024&height=768&nologo=true"

  if [ -f "$filepath" ] && [ $(stat -c%s "$filepath" 2>/dev/null || echo 0) -gt 10000 ]; then
    echo "  [SKIP] ${filename} (exists, $(stat -c%s "$filepath") bytes)"
    return 0
  fi

  for attempt in 1 2 3 4 5; do
    local tmpfile="/tmp/polli_${chapter}_${filename}.jpg"
    local http_code=$(curl -s -w "%{http_code}" --max-time 180 \
      "${url}" -o "$tmpfile" 2>/dev/null)
    local size=$(stat -c%s "$tmpfile" 2>/dev/null || echo 0)

    if [ "$http_code" = "200" ] && [ "$size" -gt 5000 ]; then
      mv "$tmpfile" "$filepath"
      echo "  [OK] ${filename} (${size} bytes)"
      return 0
    elif [ "$http_code" = "402" ]; then
      echo "  [RATE] ${filename}: rate limited (attempt ${attempt}), waiting 30s..."
      sleep 30
    else
      echo "  [ERR] ${filename}: HTTP ${http_code} size=${size} (attempt ${attempt})"
      [ -f "$tmpfile" ] && rm -f "$tmpfile"
      sleep 10
    fi
  done
  echo "  [FAIL] ${filename}"
  FAILED="${FAILED} ${filename}"
  return 1
}

# Count total
for ch in ex11 ex12 ex13 ex14 ex15 ex16 ex17 ex18 ex19 ex20; do
  case $ch in
    ex11) extras="ex11_01 ex11_02 ex11_04 ex11_05";;
    ex12) extras="ex12_01 ex12_02 ex12_03 ex12_04 ex12_05";;
    ex13) extras="ex13_01 ex13_02 ex13_03 ex13_04 ex13_05";;
    ex14) extras="ex14_01 ex14_02 ex14_03 ex14_04 ex14_05";;
    ex15) extras="ex15_01 ex15_02 ex15_03 ex15_04 ex15_05";;
    ex16) extras="ex16_01 ex16_02 ex16_03 ex16_04 ex16_05";;
    ex17) extras="ex17_01 ex17_02 ex17_03 ex17_04 ex17_05";;
    ex18) extras="ex18_01 ex18_02 ex18_03 ex18_04 ex18_05";;
    ex19) extras="ex19_01 ex19_02 ex19_03 ex19_04 ex19_05";;
    ex20) extras="ex20_01 ex20_02 ex20_03 ex20_04 ex20_05";;
  esac
  for f in $extras; do
    TOTAL=$((TOTAL + 1))
  done
done

echo "Total images to download: ${TOTAL}"
echo "Starting downloads..."
echo ""

# ex11
download ex11 ex11_01 "Moses standing before Pharaoh in Egyptian palace warning final plague, dramatic lighting, dark storm clouds, Pharaoh angry on throne, children's Bible illustration watercolor gentle colors"
sleep 12
download ex11 ex11_02 "Moses speaking to Israelite elders, families gathered listening intently, torches light, anticipation hope, children's picture book warm earth tones"
sleep 12
download ex11 ex11_04 "Egyptian mother holding child gently, sorrow, dark night moonlight, ancient Egyptian home, soft watercolor children's illustration"
sleep 12
download ex11 ex11_05 "Moses leaving Pharaoh's palace in anger, back turned, palace guards watching, dramatic sunset sky, children's Bible art warm colors"
sleep 12

# ex12
download ex12 ex12_01 "Israelite family gathered eating Passover meal, roasted lamb unleavened bread, lamp light, children attentive, warm family scene, children's book watercolor"
sleep 15
download ex12 ex12_02 "Close-up wooden doorpost with lamb blood painted on lintel using hyssop branch, evening light, symbolic meaningful, soft watercolor"
sleep 15
download ex12 ex12_03 "Angel of death passing over Israelite homes at night, glowing light above houses with blood-marked doors, dark sky, protective presence, children's Bible"
sleep 15
download ex12 ex12_04 "Egyptian families weeping at night, moonlight sorrow, ancient Egyptian homes, soft watercolor for children, gentle depiction"
sleep 15
download ex12 ex12_05 "Israelites leaving Egypt at dawn, families with donkeys belongings, morning light hope freedom, children's picture book warm colors"
sleep 15

# ex13
download ex13 ex13_01 "Israelite family celebrating Feast of Unleavened Bread, flatbread table, children learning, warm home, watercolor children's illustration"
sleep 15
download ex13 ex13_02 "Father presenting firstborn son hands raised dedication, family gathered, spiritual moment, gentle light, children's Bible picture book"
sleep 15
download ex13 ex13_03 "Pillar of cloud leading Israelites through desert day, majestic cloud against blue sky, people walking below, desert landscape, watercolor"
sleep 15
download ex13 ex13_04 "Pillar of fire guiding Israelites at night, brilliant column fire, dark desert sky, camp tents glowing, stars, children's Bible art"
sleep 15
download ex13 ex13_05 "Israelites journeying through desert wilderness, families walking together donkeys sheep, vast landscape journey hope, soft watercolor"
sleep 15

# ex14
download ex14 ex14_01 "Israelites trapped between Red Sea and Pharaoh's chariot army, people looking back fear, sea before them, dust approaching, children's Bible"
sleep 15
download ex14 ex14_02 "Moses at edge of Red Sea stretching staff over water, wind blowing robe, divine power dramatic, watercolor children's book"
sleep 15
download ex14 ex14_03 "Red Sea waters parting miraculously, walls of water both sides, dry path through middle, fish visible in water walls, children's illustration"
sleep 15
download ex14 ex14_04 "Israelites walking through parted Red Sea dry ground, families children animals, towering water walls, awe wonder, watercolor"
sleep 15
download ex14 ex14_05 "Egyptian army drowning Red Sea waters crash back, chariots engulfed, gentle depiction for children, watercolor Bible illustration"
sleep 15

# ex15
download ex15 ex15_01 "Moses leading Israelites singing Song of the Sea, people shore arms raised praise, joyful celebration, Red Sea background, watercolor"
sleep 15
download ex15 ex15_02 "Miriam prophetess dancing with timbrel, joyful movement, colorful robe flowing, women following tambourines, celebration sea, children's book"
sleep 15
download ex15 ex15_03 "Women dancing playing tambourines in circle, joyful celebration Red Sea crossing, colorful robes, movement music, children's picture book"
sleep 15
download ex15 ex15_04 "Israelites at Marah finding bitter water undrinkable, disappointed faces, desert oasis palm trees, children's Bible art watercolor"
sleep 15
download ex15 ex15_05 "Moses throwing tree branch into bitter waters Marah, waters turning sweet clear, people drinking joyfully, oasis, soft watercolor"
sleep 15

# ex16
download ex16 ex16_01 "Israelites complaining wilderness, hungry families sad, desert camp morning light, people gathered around Moses, children's Bible watercolor"
sleep 15
download ex16 ex16_02 "Manna covering desert ground like white frost, coriander seed appearance, morning dew, miraculous bread, golden light, children's picture book"
sleep 15
download ex16 ex16_03 "Israelite family gathering manna in baskets, children picking white flakes, morning desert camp, wonder provision, watercolor children's Bible"
sleep 15
download ex16 ex16_04 "Flocks of quails covering Israelite camp evening, birds everywhere, desert sunset, people catching, miraculous provision, children's book"
sleep 15
download ex16 ex16_05 "Family eating manna together, mother preparing bread, jar manna as memorial, tent interior warm light, children's Bible art watercolor"
sleep 15

# ex17
download ex17 ex17_01 "Moses striking large rock with staff at Horeb, water gushing miraculously, desert thirsty people amazed, children's Bible illustration watercolor"
sleep 15
download ex17 ex17_02 "Israelite families drinking fresh water from struck rock, joy relief, children cupping hands drink, desert oasis, watercolor children's book"
sleep 15
download ex17 ex17_03 "Joshua leading Israelite army battle against Amalekites valley, swords shields, intense fighting dust action, children's Bible art"
sleep 15
download ex17 ex17_04 "Moses on hilltop hands raised holding staff, Aaron Hur holding up his arms each side, sunset sky, spiritual battle, watercolor illustration"
sleep 15
download ex17 ex17_05 "Israelites victorious battle celebration, Joshua raised sword, sunset victory, children's picture book Bible, warm triumphant colors"
sleep 15

# ex18
download ex18 ex18_01 "Jethro arriving Israelite camp with Zipporah and Moses two sons, desert camp setting, joyful reunion, tents background, children's Bible watercolor"
sleep 15
download ex18 ex18_02 "Moses and Jethro embracing warmly father-in-law son-in-law reunion, desert camp, emotional family moment, tents mountain, watercolor children's book"
sleep 15
download ex18 ex18_03 "Moses sitting judging people from morning until evening, long line Israelites waiting standing, tired Moses, desert, children's Bible art"
sleep 15
download ex18 ex18_04 "Jethro giving wise counsel to Moses, two men sitting tent, earnest conversation, wisdom shared, warm light, watercolor children's Bible"
sleep 15
download ex18 ex18_05 "Moses appointing capable men leaders of thousands hundreds fifties tens, group commissioned, orderly delegation, children's picture book"
sleep 15

# ex19
download ex19 ex19_01 "Israelites camped foot Mount Sinai, vast desert camp countless tents, majestic mountain towering, morning light anticipation, children's Bible watercolor"
sleep 15
download ex19 ex19_02 "Mount Sinai covered thick smoke fire, lightning flashing, dark clouds, divine presence, mountain trembling, dramatic children's Bible art"
sleep 15
download ex19 ex19_03 "Loud trumpet blast from mountain, Israelites trembling at foot, families huddled awe fear, dramatic holy scene, children's picture book Bible"
sleep 15
download ex19 ex19_04 "Moses climbing Mount Sinai into thick darkness smoke, solitary figure ascending, holy mountain, dramatic lighting, watercolor children's Bible"
sleep 15
download ex19 ex19_05 "Israelite families washing clothes foot Sinai, preparing to meet God, water basins, reverent preparation, children's book illustration"
sleep 15

# ex20
download ex20 ex20_01 "God speaking Ten Commandments from Mount Sinai, mountain fire smoke, divine voice awe majesty, children's Bible illustration dramatic watercolor"
sleep 15
download ex20 ex20_02 "Moses on Mount Sinai receiving two stone tablets Ten Commandments, holy moment divine light, awe, children's picture book Bible"
sleep 15
download ex20 ex20_03 "Israelites standing far off fear foot Mount Sinai, watching mountain burning fire, dramatic holy scene, watercolor children's Bible art"
sleep 15
download ex20 ex20_04 "Moses descending Mount Sinai carrying two stone tablets, face radiant, people waiting below, revelation, watercolor children's book"
sleep 15
download ex20 ex20_05 "Israelite family tent talking about Ten Commandments, parents teaching children, warm family scene, mountain visible, children's Bible watercolor"

echo ""
echo "=== DONE ==="
for d in ex11 ex12 ex13 ex14 ex15 ex16 ex17 ex18 ex19 ex20; do
  echo "$d: $(ls ${BASE}/${d}/*.jpg 2>/dev/null | wc -l) files"
done
if [ -n "$FAILED" ]; then
  echo "Failed: $FAILED"
fi
