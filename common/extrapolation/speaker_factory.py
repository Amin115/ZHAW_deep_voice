"""
The factory to create all used speaker pickles in the networks.

Based on previous work of Gerber, Lukic and Vogt, adapted by Heusser
"""
from common.extrapolation.speaker import Speaker


def create_all_speakers():
    """
    A generator that yields all Speakers that are needed for the Speaker Clustering Suite to function
    :return: yields Speakers
    """
    yield Speaker(False, 100, 'speakers_voxceleb_speaker_diarization_100', dataset='voxceleb',
                  max_audio_length=800, sentences=45)
    yield Speaker(False, 19, 'speakers_rt09_speaker_diarization', dataset="rt09", max_audio_length=881, sentences=15)
    yield Speaker(False, 40, 'speakers_40_clustering_vs_reynolds')
    yield Speaker(False, 100, 'speakers_100_50w_50m_not_reynolds')
    yield Speaker(True, 40, 'speakers_40_clustering_vs_reynolds')
    yield Speaker(True, 60, 'speakers_60_clustering')
    yield Speaker(True, 80, 'speakers_80_clustering')
    yield Speaker(True, 590, 'speakers_590_clustering_without_raynolds')
