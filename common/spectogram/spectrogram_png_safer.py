import numpy as np
from matplotlib import pyplot as plot

from common.spectogram.spectrogram_converter import mel_spectrogram
from common.utils.paths import *


def save_spectrogramm_png(path):
    # Load the mel spectrogram
    spectrogram = mel_spectrogram(path)

    # Begin the plot
    figure = plot.figure(1)
    plot.imshow(spectrogram[:, 20:160])

    # Add the color bar
    color_bar = plot.colorbar()
    n = np.linspace(0, 35, num=11)
    labels = []
    for l in n:
        labels.append(str(l) + ' dB')
    color_bar.ax.set_yticklabels(labels)

    # Add x and y labels
    plot.xlabel('Spektra (in Zeit)')
    plot.ylabel('Frequenz-Datenpunkte')

    # Save the figure to disc
    figure.savefig(get_result_png(str.join("_", path.split("/")[-2:]) + "_spectrogram.png"))
    figure.clear()


if __name__ == '__main__':
    save_spectrogramm_png('/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/RT09/TRAIN/EDI/EDI_spkr1/0_RIFF.WAV')
    save_spectrogramm_png(
        '/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/RT09/TRAIN/EDI/EDI_spkr1/0_RIFF_normalized.WAV')
    save_spectrogramm_png('/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/RT09/TRAIN/IDI/IDI_spkr1/0_RIFF.WAV')
    save_spectrogramm_png(
        '/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/RT09/TRAIN/IDI/IDI_spkr1/0_RIFF_normalized.WAV')
    save_spectrogramm_png('/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/RT09/TRAIN/NIST/NIST_253/0_RIFF.WAV')
    save_spectrogramm_png('/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/TIMIT/TRAIN/DR1/FCJF0/SA1_RIFF.WAV')
    save_spectrogramm_png('/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/TIMIT/TRAIN/DR5/MDWH0/SI1925_RIFF.WAV')
    save_spectrogramm_png('/home/amin/studium_zhaw/Bachelor_Thesis/code/SPDR/ZHAW_deep_voice/common/data/training/RT09/TRAIN/NIST/NIST_253/0_RIFF_normalized.WAV')
