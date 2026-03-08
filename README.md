# 🚀 Colab Video Shrink (H.264/H.265)

An efficient, GPU-accelerated video transcoding script designed to run on **Google Colab**. This tool helps users with limited data plans (like 1GB monthly limits) convert large video files into highly optimized, mobile-friendly versions without losing clarity.

## ✨ Features
- **GPU Accelerated**: Uses NVIDIA NVENC for lightning-fast encoding.
- **Codec Toggle**: Switch between **H.264 (AVC)** for compatibility and **H.265 (HEVC)** for maximum data saving.
- **Google Drive Integration**: Automatically saves finished files to your Drive to prevent data loss.
- **Batch Processing**: Queue multiple episodes and walk away while the script handles the rest.
- **Smart Bitrate**: Automatically adjusts bitrates based on your codec choice to maintain a ~75MB target.

## 🛠️ Usage
1. Copy the `code.py` script contents and paste it in **Google Colab** code cell.
2. Change the Runtime type to **T4 GPU** (`Runtime > Change runtime type`).
3. Configure the settings at the top of the script:
   - `CODEC_CHOICE`: Set to `"H264"` or `"H265"`.
   - `TARGET_RES`: Set the desired height (video resolution) (e.g., `240`, `360`, `480`, or `720`).
4. Add your video URLs to the `episodes` dictionary.
5. Run the cells and check your Google Drive at `My Drive/compressed_videos` or the workspace folder at `/content/drive/compressed_videos`!

## 📊 Why H.265?
H.265 (HEVC) provides roughly 30-50% better compression than H.264. This allows you to watch the same content with better quality while using significantly less of your data plan.

---

By [@dconco](https://github.com/dconco)
