#!/bin/bash
# Une las 8 escenas MP4 (mudas) en Video_Estacion2_CasoDeEstudio.mp4
# usando el demuxer concat de ffmpeg (sin recodificar).
set -e
cd "$(dirname "$0")"

LIST=output/concat_list.txt
> "$LIST"
for f in scene_01_intro scene_02_condiciones scene_03_el_caso scene_04_condicion1 \
         scene_05_condicion2 scene_06_condicion3 scene_07_grafico scene_08_error_cierre; do
  echo "file '$(pwd)/output/${f}.mp4'" >> "$LIST"
done

ffmpeg -y -f concat -safe 0 -i "$LIST" -c copy Video_Estacion2_CasoDeEstudio.mp4
echo "OK -> Video_Estacion2_CasoDeEstudio.mp4"
