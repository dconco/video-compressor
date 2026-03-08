import os
from google.colab import drive

# --- 1. SETTINGS & TOGGLES ---
CODEC_CHOICE = "H264"  # Options: "H264" or "H265"
QUALITY_PRESET = "slow" # 'fast' for speed, 'slow' for better quality per MB

# --- 2. MOUNT DRIVE ---
if not os.path.exists('/content/drive'):
    drive.mount('/content/drive')

# --- 3. QUEUE ---
save_path = "/content/drive/compressed_videos"
os.makedirs(save_path, exist_ok=True)

# --- 4. The key is the name to save the compressed video, and the value is the video URL to compress ---
episodes = {
    "Miraculous_S05E05_Illusion": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E05-Illusion.mp4",
    "Miraculous_S05E06_Determination": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E06-Determination.mp4",
    "Miraculous_S05E07_Passion": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E07-Passion.mp4",
    "Miraculous_S05E08_Reunion": "https://xcrop.onlyfairuse.xyz/wp-content/uploads/2025/11/M-S5-E08-Reunion.mp4"
}

# --- 5. ENGINE ---
for name, url in episodes.items():
    INPUT_FILE = "temp_input.mp4"
    
    # Configure Codec-Specific Settings
    if CODEC_CHOICE == "H265":
        v_codec = "hevc_nvenc"
        v_bitrate = "400k"  # High efficiency
        suffix = "HEVC"
    else:
        v_codec = "h264_nvenc"
        v_bitrate = "550k"  # Needs more data to match H265 quality
        suffix = "AVC"

    OUTPUT_FILE = f"{save_path}/{name}_360p_{suffix}.mp4"

    if os.path.exists(OUTPUT_FILE):
        print(f"⏩ Skipping {name}, already exists.")
        continue

    print(f"\n🚀 Processing: {name} | Codec: {CODEC_CHOICE} | Target: {v_bitrate}")
    
    # Download
    !wget -q -O {INPUT_FILE} "{url}"
    
    # Transcode
    !ffmpeg -hwaccel cuda -i {INPUT_FILE} \
        -vf "scale=-2:360" \
        -c:v {v_codec} \
        -b:v {v_bitrate} \
        -maxrate 650k \
        -bufsize 1200k \
        -preset {QUALITY_PRESET} \
        -c:a aac -b:a 48k \
        -y "{OUTPUT_FILE}"
    
    # Cleanup
    if os.path.exists(OUTPUT_FILE):
        !rm {INPUT_FILE}
        print(f"✅ Success: {os.path.basename(OUTPUT_FILE)}")
    else:
        print(f"❌ Failed to process {name}")

print("\n🎉 All tasks complete!")
