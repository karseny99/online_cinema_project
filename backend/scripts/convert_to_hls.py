import os
import subprocess

def convert_to_hls(input_file: str, output_dir: str):
    """Конвертировать видеофайл в HLS-формат."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "index.m3u8")
    command = [
        "ffmpeg",
        "-i", input_file,
        "-codec:", "copy",
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-f", "hls",
        output_path
    ]

    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error during HLS conversion: {result.stderr.decode()}")
    print(f"Successfully converted {input_file} to HLS at {output_path}")

# Пример использования
# convert_to_hls("example_movie.mp4", "hls_output/example_movie")
