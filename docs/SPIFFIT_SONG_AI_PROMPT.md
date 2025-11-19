# 🎸 Spiffit Song AI Agent - Performance Prompt

**Purpose:** AI agent to repeatedly perform the Spiffit song lyrics for 2-minute video loop  
**Use Case:** Display in corner of hackathon demo video  
**Tempo:** Upbeat 80s new wave style (à la Devo)

---

## 🎤 AI Agent Prompt

```
You are a high-energy 80s new wave performer singing the "Spiffit" song - a parody of Devo's "Whip It" for a sales incentive competition app.

INSTRUCTIONS:
- Sing/recite the Spiffit song repeatedly for exactly 2 minutes
- Maintain the energetic, robotic Devo-style delivery
- Emphasize the word "SPIFFIT" with enthusiasm each time
- Keep the tempo consistent (~120 BPM, upbeat)
- Add occasional ad-libs like "Yeah!", "Do it!", "That's right!" between verses
- When you hit 2 minutes, fade out with "Spiff it good!" and stop

SONG STRUCTURE (repeat this cycle):

**Verse:**
When a problem comes along
You must Spiff It!
Before the cream sits out too long
You must Spiff It!
When something's going wrong
You must Spiff It!

**Chorus:**
Now Spiff It!
Into shape!
Shape it up!
Get straight!
Go forward!
Move ahead!
Try to detect it!
It's not too late!
To Spiff It!
Spiff It good!

**Bridge (occasional):**
When your sales are looking weak
You must Spiff It!
Hit those numbers that you seek
You must Spiff It!
Give your team the boost they need
You must Spiff It!

PERFORMANCE STYLE:
- Robotic yet enthusiastic
- Staccato delivery on "Spiff It!"
- Build energy on each chorus
- Quick, punchy lines
- 80s new wave vocal style

TIME: Perform for 2 minutes, then end with "Spiff it good!"

BEGIN NOW:
```

---

## 🎬 Video Integration Options

### Option 1: Text-to-Speech Loop
**Tool:** ElevenLabs, Play.ht, or Azure TTS  
**Settings:**
- Voice: Energetic male/female, medium pitch
- Speed: 1.2x (upbeat)
- Emphasis: High on "Spiffit"
- Loop: 2 minutes

### Option 2: AI Avatar Performance
**Tool:** HeyGen, Synthesia, or D-ID  
**Settings:**
- Avatar: 80s style character
- Animation: Energetic head bobbing
- Background: Retro geometric patterns
- Duration: 2 minutes loop

### Option 3: Live Text Display (Karaoke Style)
**Tool:** OBS Studio or Streamlit  
**Settings:**
- Animated text appearing in rhythm
- 80s retro font (e.g., "Press Start 2P")
- Neon colors: Hot pink, cyan, yellow
- Corner overlay: 320x180px (small corner)

---

## 🎨 Visual Styling Recommendations

### Corner Video Specs:
- **Size:** 320x180px (corner overlay)
- **Position:** Bottom-right or top-right
- **Border:** 2px neon cyan glow
- **Background:** Dark purple/black gradient
- **Opacity:** 90% (slightly transparent)

### Text Animation (if using text display):
```css
Font: "Press Start 2P" or "VCR OSD Mono"
Colors: Rotate between #FF00FF, #00FFFF, #FFFF00
Animation: Bounce on "SPIFFIT", pulse on beat
Size: 24px main, 36px on "SPIFFIT"
```

---

## ⚡ Quick Implementation (Python + Streamlit)

If you want to generate this live in the app:

```python
import streamlit as st
import time

def spiffit_song_loop():
    """Display Spiffit lyrics in a loop for 2 minutes"""
    
    lyrics = [
        "🎸 When a problem comes along",
        "🎯 You must SPIFF IT! 🎯",
        "⚡ Before the cream sits out too long",
        "🎯 You must SPIFF IT! 🎯",
        "💥 When something's going wrong",
        "🎯 You must SPIFF IT! 🎯",
        "",
        "🔥 Now SPIFF IT! 🔥",
        "Into shape! Shape it up!",
        "Get straight! Go forward!",
        "Move ahead! Try to detect it!",
        "It's not too late!",
        "🎯 To SPIFF IT! 🎯",
        "🎸 Spiff it good! 🎸",
        ""
    ]
    
    container = st.empty()
    start_time = time.time()
    
    while time.time() - start_time < 120:  # 2 minutes
        for line in lyrics:
            if time.time() - start_time >= 120:
                break
            container.markdown(f"### {line}")
            time.sleep(0.8)  # Adjust tempo here
    
    container.markdown("### 🎸 SPIFF IT GOOD! 🎸")

# Usage in sidebar or corner:
with st.sidebar:
    st.markdown("### 🎤 Live Performance")
    spiffit_song_loop()
```

---

## 🎵 Sample Output (First 20 seconds)

```
[00:00] 🎸 When a problem comes along
[00:02] 🎯 You must SPIFF IT! 🎯
[00:04] ⚡ Before the cream sits out too long  
[00:06] 🎯 You must SPIFF IT! 🎯
[00:08] 💥 When something's going wrong
[00:10] 🎯 You must SPIFF IT! 🎯
[00:12] 
[00:13] 🔥 Now SPIFF IT! 🔥
[00:14] Into shape! Shape it up!
[00:16] Get straight! Go forward!
[00:18] Move ahead! Try to detect it!
[00:20] It's not too late!

... [continues for 2 minutes] ...

[01:58] 🎸 Spiff it good! 🎸
[02:00] [END]
```

---

## 🚀 Recommended: OBS Studio Corner Overlay

**Best for demo video recording:**

1. **Create Text Source in OBS:**
   - Add new "Text (GDI+)" source
   - Name: "Spiffit Song"
   - Set to 320x180px corner
   
2. **Configure Animation:**
   - Use "Scroll" filter (vertical scroll)
   - Speed: 50px/second
   - Loop every 15 seconds
   
3. **Add Audio:**
   - Use the original "LogicMom Spiff It Repeat Final.m4a"
   - Loop for 2 minutes
   - Sync text to audio

---

## 📝 Notes

- Adjust tempo/speed based on your actual audio file timing
- For video corner, keep it small but readable
- Consider adding subtle bounce/pulse animation on "SPIFF IT"
- Test audio sync before recording full demo

---

**Ready to Spiff It! 🎸🎯**

