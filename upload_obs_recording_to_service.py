#!/usr/bin/env python3

"""
Uploads OBS video recordings to a video service.
"""

import argparse
from enum import Enum
import logging
from pathlib import Path
import sys
from typing import List
import ffmpeg

__author__ = "Vincent Kocks"
__version__ = "1.0.0"
__email__ = "engineering@vingenuity.net"


class VideoServiceMixin:
    """
    Mixes in a custom constructor for the VideoService class.
    A mixin is used here for pylint compatibility.
    """
    def __new__(cls,
                ffmpeg_output_kwargs: dict,
                output_file_suffix: str):
        service = object.__new__(cls)
        service.ffmpeg_output_kwargs = ffmpeg_output_kwargs
        service.output_file_suffix = output_file_suffix
        return service


class VideoService(VideoServiceMixin, Enum):
    """
    Enumerates settings used for each video service.
    """
    VIMEO = (
        dict(vcodec='libx264',
             preset='veryslow',
             crf=18,
             acodec='copy',
             pix_fmt='yuv420p'),
        '.mp4'
    )
    YOUTUBE = (
        dict(vcodec='libx264',
             preset='veryslow',
             crf=19,
             acodec='copy',
             pix_fmt='yuv420p'),
        '.mp4'
    )

    def __str__(self):
        return str(self.name).lower()

    @staticmethod
    def from_argument(arg_str: str):
        """
        Converts an argument string into a VideoService enum value.
        """
        try:
            return VideoService[arg_str.upper()]
        except KeyError:
            raise ValueError()


def main(input_file: Path,
         input_directory: Path,
         input_suffix: str,
         converted_directory: Path,
         ffmpeg_exe: Path,
         video_service: VideoService,
         convert_video: bool) -> int:
    """
    Contains the main functionality of this script.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('main')

    if convert_video:
        input_pattern = "**/*{}".format(input_suffix)
        input_files = (list(input_file) if input_file
                       else list(input_directory.glob(input_pattern)))
        output_suffix = video_service.output_file_suffix

        logger.info("Converting %d files from %s to %s...",
                    len(input_files),
                    input_suffix,
                    output_suffix)
        for input_file in input_files:
            output_filename = input_file.stem + output_suffix
            output_file = converted_directory / output_filename

            logger.info("Converting '%s' to '%s'...", input_file, output_file)
            video_stream = ffmpeg.input(str(input_file))
            video_stream = ffmpeg.output(video_stream,
                                         str(output_file),
                                         **video_service.ffmpeg_output_kwargs)
            ffmpeg.run(video_stream, cmd=str(ffmpeg_exe))

    return 0


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """
    Parses command-line arguments into namespace data.
    """
    parser = argparse.ArgumentParser(
        description='Uploads OBS video recordings to a video service.'
    )

    parser.add_argument('--video-service',
                        '-vs',
                        dest='video_service',
                        required=True,
                        type=VideoService.from_argument,
                        choices=list(VideoService),
                        help='Video service to which to upload the recording.')

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input-file',
                             '-if',
                             dest='input_file',
                             type=Path,
                             help='Video file to upload.')
    input_group.add_argument('--input-directory',
                             '-id',
                             dest='input_directory',
                             type=Path,
                             help='Directory containing video files to upload.')

    parser.add_argument('--input-suffix',
                        '-is',
                        dest='input_suffix',
                        required=False,
                        type=str,
                        default='.mkv',
                        help='Suffix for video files in the input directory.')

    parser.add_argument('--converted-directory',
                        '-cd',
                        dest='converted_directory',
                        required=False,
                        type=Path,
                        default=Path.cwd(),
                        help='Path where MP4-converted video files are saved.')

    parser.add_argument('--ffmpeg-exe',
                        '-fe',
                        dest='ffmpeg_exe',
                        required=False,
                        type=Path,
                        default=Path('./ffmpeg/bin/ffmpeg'),
                        help='Path where MP4-converted video files are saved.')

    parser.add_argument('--no-convert',
                        '-nc',
                        dest='convert_video',
                        required=False,
                        action='store_false',
                        help='if set, input videos will not be converted.')

    return parser.parse_args(arguments)


if __name__ == "__main__":
    exit(main(**vars(parse_arguments(sys.argv[1:]))))
