"""
The SpectrogramExtractor crawls the base folder and all its sub folder for wav files that
correspond with the valid speakers and extracts the spectrogram's of those files.

Based on previous work of Gerber, Lukic and Vogt.
"""
import os
import re
from collections import defaultdict

import common.spectogram.spectrogram_converter as spectrogram_converter


class SpectrogramExtractor:
    def __init__(self, max_speakers, base_folder, valid_speakers, file_match_pattern, max_audio_length=None):
        self.max_speakers = max_speakers
        self.base_folder = base_folder
        self.valid_speakers = valid_speakers
        self.file_match_regex = re.compile(file_match_pattern)
        self.max_audio_length = float(max_audio_length) / 100.0  #convert to seconds for librosa

    def extract_speaker_data(self, X, y):

        """
        Extract spectrogram and speaker names from given folder.

        :param X: return Array that saves the mel spectrogram's
        :param y: return Array that saves the speaker numbers
        :return: the filled X, y and the speaker names
        """

        speaker_names = []
        global_idx = 0
        curr_speaker_num = -1
        old_speaker = ''

        # Crawl the base and all sub folders
        for root, directories, filenames in os.walk(self.base_folder):
            # Ignore crp and DOC folder
            if self.valid_speakers and os.path.split(root)[1] not in self.valid_speakers:
                continue

            # Check files
            for filename in [filename for filename in filenames if self.file_match_regex.search(filename)]:
                # Extract speaker
                speaker = os.path.split(root)[1]
                if speaker != old_speaker:
                    curr_speaker_num += 1
                    old_speaker = speaker
                    speaker_names.append(speaker)
                    print('Extraction progress: %d/%d' % (curr_speaker_num + 1, self.max_speakers))

                if curr_speaker_num < self.max_speakers:
                    full_path = os.path.join(root, filename)
                    global_idx += extract_mel_spectrogram(full_path, X, y, global_idx, curr_speaker_num)

        return X[0:global_idx], y[0:global_idx], speaker_names

    def extract_speaker_data_n(self, X, y, max_files_per_speaker):
        speaker_names = []
        global_idx = 0
        curr_speaker_num = -1
        old_speaker = ''

        gen_spectrogram_per_speaker = defaultdict(int)

        # Crawl the base and all sub folders
        for root, directories, filenames in os.walk(self.base_folder):

            # Ignore crp and DOC folder
            if self.valid_speakers and os.path.split(root)[1] not in self.valid_speakers:
                continue

            # Check files
            for filename in [filename for filename in filenames if self.file_match_regex.search(filename)]:

                # Extract speaker
                speaker = os.path.split(root)[1]
                if speaker != old_speaker:
                    curr_speaker_num += 1
                    old_speaker = speaker
                    speaker_names.append(speaker)
                    print('Extraction progress: %d/%d' % (curr_speaker_num + 1, self.max_speakers))

                if curr_speaker_num < self.max_speakers and gen_spectrogram_per_speaker[speaker] < max_files_per_speaker:
                    full_path = os.path.join(root, filename)
                    global_idx += extract_mel_spectrogram(full_path, X, y, global_idx, curr_speaker_num,
                                                          max_duration=self.max_audio_length)
                    gen_spectrogram_per_speaker[speaker] += 1

        return X[0:global_idx], y[0:global_idx], speaker_names


def extract_mel_spectrogram(wav_path, X, y, index, curr_speaker_num, max_duration=None):
    """
    Extracts the mel spectrogram into the X array and saves the speaker into y.

    :param wav_path: the path to the wav file
    :param X: return Array that saves the mel spectrogram
    :param y: return Array that saves the speaker numbers
    :param index: the index in X and y this is stored in
    :param curr_speaker_num: the speaker number of the current speaker
    :param max_duration: only load up to this much audio (in seconds)
    :return: a one (1) to increase the index
    """
    Sxx = spectrogram_converter.mel_spectrogram(wav_path, max_duration)
    for i in range(Sxx.shape[0]):
        for j in range(Sxx.shape[1]):
            X[index, 0, i, j] = Sxx[i, j]
    y[index] = curr_speaker_num
    return 1


# Extracts the spectrogram and discards all padded data
def extract_spectrogram(spectrogram, segment_size, frequency_elements):
    zeros = 0

    for x in spectrogram[0]:
        if x == 0.0:
            zeros += 1
        else:
            zeros = 0

    while spectrogram.shape[1] - zeros < segment_size:
        zeros -= 1

    return spectrogram[0:frequency_elements, 0:spectrogram.shape[1] - zeros]
