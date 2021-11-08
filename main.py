import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from midiutil.MidiFile import MIDIFile
import time as ttime
from scipy.signal import find_peaks


def plot_spectrogram(Y, sr, hop_length, y_axis="linear"):
    plt.figure(figsize=(25, 10))
    librosa.display.specshow(Y, sr=sr, hop_length=hop_length, x_axis="time", y_axis=y_axis)
    plt.colorbar(format="%+2.f")


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def fonctionmagique(array, value):
    for i in array:
        if i[0] == value: return i[1]
    return None
#
#
# def dico(p):
#     if p == 0: return "Silence"
#     l = ["Do", "Do#", "Ré", "Ré#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]
#     return l[p % 12]


def build_notes():
    notes = [0, 27.5]
    for i in range(1, 88):
        notes.append(notes[i] * pow(2, 1 / 12))
    for i in range(len(notes)):
        notes[i] = round(notes[i] * 100) / 100
    return notes


def main_function(fichier, frame, hop):
    notes = build_notes()

    def get_pitch(f):
        return notes.index(f) + 8 if f != 0 else 0

    file, sr = librosa.load(fichier)
    tempo = round(librosa.beat.tempo(file)[0] / 5) * 5
    FRAME_SIZE = frame
    HOP_SIZE = hop

    S_scale = librosa.stft(file, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)
    Y_scale = np.abs(S_scale) ** 2
    Y_log_scale = librosa.power_to_db(Y_scale)

    liste = np.arange(0, 1 + FRAME_SIZE / 2) * sr / FRAME_SIZE

    ########
    # MIDI #
    ########
    final = []
    mf = MIDIFile(1, removeDuplicates=True, adjust_origin=None)
    track = 0
    channel = 0
    volume = 100
    time = 0

    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, tempo)

    minimum = 30
    notes_en_cours = []

    # Associer à chaque note les fréquences dans le spectrogramme
    # qui en sont le plus proche
    ndef = []
    for a in notes:
        l = []
        for b_i, b in enumerate(liste):
            if find_nearest(notes, b) == a:
                l.append((b_i, b))
        ndef.append(l)

    NOTE_ROUND = 4
    start_t = ttime.time()

    #############
    # MAIN LOOP #
    #############
    for k in range(0, Y_log_scale.shape[1]):
        peaks = find_peaks(Y_log_scale[:, k], height=minimum)[0]
        greatest_notes = []

        for p in peaks:
            note = find_nearest(notes, liste[p])
            if note not in greatest_notes:
                greatest_notes.append(note)

        for n in greatest_notes:
            if fonctionmagique(notes_en_cours, n) is None:
                notes_en_cours.append([n, time])
                final.append([n, time])

        notes_terminees = []
        for p in notes_en_cours:
            if p[0] not in greatest_notes:
                notes_terminees.append(p)
        notes_en_cours = [n for n in notes_en_cours if n not in notes_terminees]
        for i in final:
            if i in notes_terminees:
                i.append(time-i[1])
        time += 1

    for i in final:
        if i in notes_en_cours:
            i.append(time-i[1])

    duration_t = ttime.time() - start_t
    print('Execution time: %s' % duration_t)

    def get_time(t):
        return round(NOTE_ROUND * t * tempo * hop / (sr * 60)) / NOTE_ROUND

    liste = []

    for i in final:
        if get_time(i[2]) != 0:
            liste.append([get_time(i[1]), get_time(i[2]), get_pitch(i[0])])
    return liste
