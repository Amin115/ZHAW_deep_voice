"""
A Speaker contains all needed information and methods to create the pickle file used for training.

Based on previous work of Gerber, Lukic and Vogt, adapted by Heusser
"""
import pickle

import numpy as np

from common.spectogram.speaker_train_splitter import SpeakerTrainSplit
from common.spectogram.spectrogram_extractor import SpectrogramExtractor
from common.utils.paths import *


class Speaker:
    def __init__(self, split_train_test, max_speakers, speaker_list, output_name=None, sentences=10,
                 frequency_elements=128, max_audio_length=800, dataset="timit"):
        """
        Represents a fully defined speaker in the Speaker clustering suite.

        :param frequency_elements: How many frequency elements should be in a spectrogram
        :param split_train_test: Whether or not to split the test and training data
        :param max_speakers: The maximum amount of speakers to fetch from the dataset
        :param speaker_list: The speaker list used to generate the pickle
        :param output_train: File name in which the train output pickle gets stored in
        :param output_test: File name in which the test output pickle gets stored in
        :param sentences: How many sentences there are from this speaker.
        :param max_audio_length: How long the audio of the speaker can maximally be
        """
        self.sentences = sentences
        self.frequency_elements = frequency_elements
        self.split_train_test = split_train_test
        self.max_speakers = max_speakers
        self.speaker_list = speaker_list
        self.max_audio_length = max_audio_length
        self.dataset = dataset

        if output_name is None:
            self.output_name = speaker_list
        else:
            self.output_name = output_name

    def safe_to_pickle(self):
        """
        Fetches all data for this speaker from the TIMIT dataset and safes it inside of a pickle.
        """
        print("Extracting {}".format(self.speaker_list))

        # Extract the spectrogram's, speaker numbers and speaker names
        X, y, speaker_names = self.extract_data_from_speaker()

        # Safe Test-Data to disk
        if self.split_train_test:
            speaker_train_split = SpeakerTrainSplit(0.2, self.sentences)
            X_train_valid, X_test, y_train_valid, y_test = speaker_train_split(X, y, None)

            with open(get_speaker_pickle(self.output_name + '_train'), 'wb') as f:
                pickle.dump((X_train_valid, y_train_valid, speaker_names), f, -1)

            with open(get_speaker_pickle(self.output_name + '_test'), 'wb') as f:
                pickle.dump((X_test, y_test, speaker_names), f, -1)
        else:
            with open(get_speaker_pickle(self.output_name + '_cluster'), 'wb') as f:
                pickle.dump((X, y, speaker_names), f, -1)

        print("Done Extracting {}".format(self.speaker_list))
        print("Safed to pickle.\n")

    def extract_data_from_speaker(self):
        """
        Extracts the training and testing data from the speaker list
        :return:
        x: the filled training data in the 4D array [Speaker, Channel, Frequency, Time]
        y: the filled testing data in a list of speaker_numbers
        speaker_names: the names associated with the numbers
        """
        if self.dataset == "timit":
            x = np.zeros((self.max_speakers * 20, 1, self.frequency_elements, self.max_audio_length), dtype=np.float32)
            y = np.zeros(self.max_speakers * 20, dtype=np.int32)

            return self.extract_timit(x, y)
        elif self.dataset == "rt09":
            x = np.zeros((self.max_speakers * self.sentences, 1, self.frequency_elements, self.max_audio_length), dtype=np.float32)
            y = np.zeros(self.max_speakers * self.sentences, dtype=np.int32)

            return self.extract_rt09(x, y)
        elif self.dataset == "voxceleb":
            x = np.zeros((self.max_speakers * self.sentences, 1, self.frequency_elements, self.max_audio_length + 1),
                         dtype=np.float32)
            y = np.zeros(self.max_speakers * self.sentences, dtype=np.int32)

            return self.extract_voxceleb(x, y)
        else:
            raise ValueError("self.dataset can currently only be 'timit, 'rt09' or 'voxceleb', was " + self.dataset + ".")

    def extract_voxceleb(self, x, y):
        valid_speakers = []
        with open(get_speaker_list(self.speaker_list), 'r') as f:
            valid_speakers.extend(map(lambda line: line.rstrip(), f.readlines()))

        # Prepare SpectrogramExtractor
        extractor = SpectrogramExtractor(self.max_speakers, get_training("VoxCelebV1"), valid_speakers,
                                         "_\d{7}\.wav$", self.max_audio_length)

        # Extract the spectrogram's, speaker numbers and speaker names
        return extractor.extract_speaker_data_n(x, y, self.sentences)

    def extract_rt09(self, x, y):
        """
        Extracts the training data from the speaker list of the RT-09 dataset
        :return:
        x: the filled training data in the 4D array [Speaker, Channel, Frequency, Time]
        y: the filled testing data in a list of speaker_numbers
        speaker_names: the names associated with the numbers
        """
        valid_speakers = []
        with open(get_speaker_list(self.speaker_list), 'r') as f:
            valid_speakers.extend(map(lambda line: line.rstrip(), f.readlines()))

        # Prepare SpectrogramExtractor
        extractor = SpectrogramExtractor(self.max_speakers, get_training("RT09"), valid_speakers,
                                         "_RIFF\.WAV$", self.max_audio_length)

        # Extract the spectrogram's, speaker numbers and speaker names
        return extractor.extract_speaker_data_n(x, y, self.sentences)

    def extract_timit(self, x, y):
        """
        Extracts the training and testing data from the speaker list of the TIMIT Dataset
        :return:
        x: the filled training data in the 4D array [Speaker, Channel, Frequency, Time]
        y: the filled testing data in a list of speaker_numbers
        speaker_names: the names associated with the numbers
        """
        # Add all valid speakers
        valid_speakers = []
        with open(get_speaker_list(self.speaker_list), 'rb') as f:
            for line in f:
                # Added bytes.decode() because python 2.x ignored leading b' while python 3.x doesn't
                valid_speakers.append(bytes.decode(line.rstrip()))

        # Prepare SpectrogramExtractor
        extractor = SpectrogramExtractor(self.max_speakers, get_training("TIMIT"), valid_speakers, "_RIFF\.WAV$")

        # Extract the spectrogram's, speaker numbers and speaker names
        return extractor.extract_speaker_data(x, y)

    def is_pickle_saved(self):
        """
        Whether or not a corresponding pickle file already exist.
        :return: true if it exists, false otherwise
        """
        if self.split_train_test:
            return path.exists(get_speaker_pickle(self.output_name + '_train'))
        else:
            path.exists(get_speaker_pickle(self.output_name + '_cluster'))
