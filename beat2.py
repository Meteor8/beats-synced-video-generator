from __future__ import print_function

import argparse
import sys
import numpy as np
import librosa


def onset_detect(input_file, output_csv):
    '''Onset detection function

    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save onset timestamps as a CSV file
    '''

    # 1. load the wav file and resample to 22.050 KHz
    print('Loading ', input_file)
    y, sr = librosa.load(input_file, sr=22050)

    # Use a default hop size of 512 frames @ 22KHz ~= 23ms
    hop_length = 512

    # 2. run onset detection
    print('Detecting onsets...')
    onsets = librosa.onset.onset_detect(y=y,
                                        sr=sr,
                                        hop_length=hop_length)

    print("Found {:d} onsets.".format(onsets.shape[0]))

    # 3. save output
    # 'beats' will contain the frame numbers of beat events.

    onset_times = librosa.frames_to_time(onsets,
                                         sr=sr,
                                         hop_length=hop_length)

    print('Saving output to ', output_csv)
    np.savetxt(output_csv, onset_times, delimiter=',')
    print('done!')


def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(
        description='librosa onset detection example')

    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')

    parser.add_argument('output_file',
                        action='store',
                        help='path to the output file (csv of onset times)')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # Get the parameters
    parameters = process_arguments(sys.argv[1:])

    # Run the beat tracker
    onset_detect(parameters['input_file'], parameters['output_file'])