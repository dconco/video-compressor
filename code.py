import os
from google.colab import drive

# --- 1. SETTINGS & TOGGLES ---
CODEC_CHOICE = "H264"    # "H264" or "H265"
QUALITY_PRESET = "slow"  # 'fast' or 'slow'
TARGET_RES = 360         # Options: 240, 360, 480, 720

# Bitrate Mapping (Resolution: [Maxrate, Bufsize])
RES_SETTINGS = {
    240: ["400k", "800k"],
    360: ["650k", "1200k"],
    480: ["1200k", "2000k"],
    720: ["2500k", "5000k"]
}

# --- 2. MOUNT DRIVE ---
try:
    if not os.path.exists('/content/drive'):
        drive.mount('/content/drive', force_remount=True)
    print("✅ Drive mounted successfully.")
except Exception as e:
    print(f"⚠️ Drive mount failed: {e}")
    print(f"📁 Falling back to local storage")

# --- 3. QUEUE ---
save_path = "/content/drive/compressed_videos"
os.makedirs(save_path, exist_ok=True)

episodes = {
    "Miraculous_S05E05_Illusion": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E05-Illusion.mp4",
    "Miraculous_S05E06_Determination": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E06-Determination.mp4",
    "Miraculous_S05E07_Passion": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E07-Passion.mp4",
    "Miraculous_S05E08_Reunion": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E08-Reunion.mp4"
}

# --- 4. ENGINE ---
max_rate, buf_size = RES_SETTINGS.get(TARGET_RES, ["650k", "1200k"])

for name, url in episodes.items():
    INPUT_FILE = "temp_input.mp4"
    
    # Configure Codec-Specific Settings
    if CODEC_CHOICE == "H265":
        v_codec = "hevc_nvenc"
        v_bitrate = "400k" # High efficiency
        suffix = "HEVC"
    else:
        v_codec = "h264_nvenc"
        v_bitrate = "550k" # Needs more data to match H265 quality
        suffix = "AVC"
    
    OUTPUT_FILE = f"{save_path}/{name}_{TARGET_RES}p_{suffix}.mp4"

    if os.path.exists(OUTPUT_FILE):
        print(f"⏩ Skipping {name}, already exists.")
        continue
    
    print(f"\n🚀 Processing: {name} @ {TARGET_RES}p | Codec: {CODEC_CHOICE}")
    
    # Download
    !wget -q -O {INPUT_FILE} "{url}"
    
    # Transcode
    !ffmpeg -hwaccel cuda -i {INPUT_FILE} \
        -vf "scale=-2:{TARGET_RES}" \
        -c:v {v_codec} \
        -b:v {v_bitrate} \
        -maxrate {max_rate} \
        -bufsize {buf_size} \
        -preset {QUALITY_PRESET} \
        -c:a aac -b:a 48k \
        -y "{OUTPUT_FILE}"
    
    # Cleanup
    if os.path.exists(OUTPUT_FILE):
        print(f"✅ Success: {os.path.basename(OUTPUT_FILE)}")
    else:
        print(f"❌ Failed to process {name}")
    
    !rm {INPUT_FILE}

print("\n🎉 All tasks complete!")
