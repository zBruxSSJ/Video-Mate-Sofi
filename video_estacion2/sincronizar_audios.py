#!/usr/bin/env python3
"""
sincronizar_audios.py
======================
Toma los 8 videos mudos de las escenas (en output/scene_0N_*.mp4) y los 8
audios grabados por los integrantes (uno por escena), ajusta la duración
de cada escena a la duración de su audio, les pega el audio con ffmpeg,
y concatena todo en Video_Final.mp4.

Uso:
    python3 sincronizar_audios.py --audios carpeta_con_audios/

Los audios deben llamarse escena_01.mp3 (o .wav / .m4a) ... escena_08.mp3,
uno por cada una de las 8 escenas, en ese orden. También acepta los nombres
scene_01.mp3 ... scene_08.mp3, o simplemente 01.mp3 ... 08.mp3.

Qué hace con cada escena:
  1. Mide la duración del audio (ffprobe).
  2. Estira o acorta el video de la escena con el filtro `setpts` para que
     dure exactamente lo mismo que el audio (así cada escena respira al
     ritmo de quien está hablando).
  3. Le pega el audio (re-encode a H.264 + AAC).
  4. Concatena las 8 escenas ya sincronizadas con el demuxer concat de
     ffmpeg y exporta Video_Final.mp4.

Requisitos: ffmpeg y ffprobe instalados y en el PATH.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
FPS = 24

SCENE_FILES = [
    "scene_01_intro.mp4",
    "scene_02_condiciones.mp4",
    "scene_03_el_caso.mp4",
    "scene_04_condicion1.mp4",
    "scene_05_condicion2.mp4",
    "scene_06_condicion3.mp4",
    "scene_07_grafico.mp4",
    "scene_08_error_cierre.mp4",
]

AUDIO_EXTS = [".mp3", ".m4a", ".wav", ".aac", ".ogg"]


def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("ERROR ejecutando:", " ".join(cmd))
        print(result.stderr)
        sys.exit(1)
    return result.stdout


def ffprobe_duration(path):
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(path),
    ])
    data = json.loads(out)
    return float(data["format"]["duration"])


def find_audio_for_scene(audios_dir: Path, scene_index_1based: int):
    candidates = [
        f"escena_{scene_index_1based:02d}",
        f"scene_{scene_index_1based:02d}",
        f"{scene_index_1based:02d}",
        f"escena{scene_index_1based}",
        f"scene{scene_index_1based}",
    ]
    for stem in candidates:
        for ext in AUDIO_EXTS:
            p = audios_dir / f"{stem}{ext}"
            if p.exists():
                return p
    return None


def build_scene_clip(video_path: Path, audio_path: Path, out_path: Path):
    video_dur = ffprobe_duration(video_path)
    audio_dur = ffprobe_duration(audio_path)
    ratio = video_dur / audio_dur  # >1 si el video original era más largo que el audio

    print(f"  video={video_dur:.2f}s  audio={audio_dur:.2f}s  setpts ratio={ratio:.4f}")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-filter:v", f"setpts={ratio:.6f}*PTS,fps={FPS}",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_path),
    ]
    run(cmd)


def concat_clips(clip_paths, out_path: Path, tmp_dir: Path):
    list_file = tmp_dir / "concat_list.txt"
    with open(list_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(out_path),
    ]
    run(cmd)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--audios", required=True, help="Carpeta con los 8 audios grabados (uno por escena)")
    parser.add_argument("--output", default=str(HERE / "Video_Final.mp4"), help="Ruta del video final (default: Video_Final.mp4)")
    parser.add_argument("--scenes-dir", default=str(OUTPUT_DIR), help="Carpeta con los 8 MP4 mudos de las escenas")
    args = parser.parse_args()

    audios_dir = Path(args.audios)
    scenes_dir = Path(args.scenes_dir)
    out_final = Path(args.output)

    if not audios_dir.is_dir():
        print(f"No existe la carpeta de audios: {audios_dir}")
        sys.exit(1)

    with tempfile.TemporaryDirectory(prefix="sync_audios_") as tmp:
        tmp_dir = Path(tmp)
        synced_clips = []

        for i, scene_file in enumerate(SCENE_FILES, start=1):
            video_path = scenes_dir / scene_file
            if not video_path.exists():
                print(f"Falta el video de la escena {i}: {video_path}")
                sys.exit(1)

            audio_path = find_audio_for_scene(audios_dir, i)
            if audio_path is None:
                print(f"Falta el audio de la escena {i} en {audios_dir} "
                      f"(se espera algo como escena_{i:02d}.mp3)")
                sys.exit(1)

            print(f"[{i}/8] {scene_file}  <-  {audio_path.name}")
            out_clip = tmp_dir / f"synced_{i:02d}.mp4"
            build_scene_clip(video_path, audio_path, out_clip)
            synced_clips.append(out_clip)

        print("Concatenando las 8 escenas sincronizadas...")
        concat_clips(synced_clips, out_final, tmp_dir)

    total_dur = ffprobe_duration(out_final)
    mins, secs = divmod(int(round(total_dur)), 60)
    print(f"\nListo: {out_final}  (duración total: {mins}:{secs:02d})")


if __name__ == "__main__":
    main()
