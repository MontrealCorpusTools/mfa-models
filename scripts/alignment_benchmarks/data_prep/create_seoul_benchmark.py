import collections
import os
import re
import shutil
import subprocess
import argparse
from pathlib import Path
from praatio.textgrid import openTextgrid, Textgrid, IntervalTier

korean_root = '/mnt/d/Data/speech/korean_corpora'

seoul_corpus = os.path.join(korean_root, 'seoul_corpus')
original_textgrids = os.path.join(seoul_corpus, 'original')
training_textgrids = os.path.join(seoul_corpus, 'seoul_corpus_benchmark')
reference_dir = os.path.join(seoul_corpus, 'seoul_reference_alignments')


speaker_info = {}

def fix_sample_rate(benchmark_directory: Path):

    for speaker in os.listdir(benchmark_directory):
        speaker_dir = os.path.join(benchmark_directory, speaker)
        if not os.path.isdir(speaker_dir):
            continue
        for file in os.listdir(speaker_dir):
            if 'resampled' in file:
                os.remove(file)
            if file.endswith('.flac') and 'resampled' not in file:
                path = os.path.join(speaker_dir, file)
                resampled_file = path.replace('.flac', '_resampled.flac')
                subprocess.check_call(['sox', path, '-r', '16000', resampled_file])
                os.remove(path)
                os.rename(resampled_file, path)


def fix_textgrids(original_directory: Path, benchmark_directory: Path, reference_directory: Path):

    for file in os.listdir(original_directory):
        if os.path.isdir(os.path.join(original_directory, file)):
            continue
        speaker = file[:3]
        speaker_gender = file[3]
        speaker_age = file[4:6]
        print(speaker, speaker_gender, speaker_age)
        speaker_info[speaker] = {'gender': speaker_gender, 'age':speaker_age}
        speaker_directory = os.path.join(benchmark_directory, speaker)
        reference_speaker_directory = os.path.join(reference_directory, speaker)
        os.makedirs(speaker_directory, exist_ok=True)
        os.makedirs(reference_speaker_directory, exist_ok=True)
        if not file.endswith('.TextGrid'):
            shutil.move(os.path.join(original_directory, file), os.path.join(speaker_directory, file))
            continue
        tg_path = os.path.join(original_directory, file)
        tg = openTextgrid(tg_path, includeEmptyIntervals=False, duplicateNamesMode='rename')
        orth = tg._tierDict['utt.prono.']
        new_intervals = []
        new_tg_path = os.path.join(speaker_directory, file)
        reference_tg_path = os.path.join(reference_speaker_directory, file)
        new_tg = Textgrid(minTimestamp=tg.minTimestamp, maxTimestamp=tg.maxTimestamp)
        word_intervals = []
        for interval in orth._entries:
            if re.match(r'^<[^>]+>$', interval.label):
                continue
            text = interval.label.replace('<VOCNOISE>', '')
            if not text:
                continue
            begin = max(interval.start - 0.2, 0)
            end = min(interval.end + 0.2, orth.maxTimestamp)
            if new_intervals and begin <= new_intervals[-1][1]:
                new_intervals[-1][1] = end
                new_intervals[-1][2] += ' ' + text
            else:
                new_intervals.append([begin, end, text])
            word_intervals.append((interval.start, interval.end, text))
        tier = IntervalTier(speaker, new_intervals,minT=tg.minTimestamp, maxT=tg.maxTimestamp)
        new_tg.addTier(tier)
        new_tg.save(new_tg_path,includeBlankSpaces=True, format='short_textgrid')
        reference_tg = Textgrid(minTimestamp=tg.minTimestamp, maxTimestamp=tg.maxTimestamp)
        phone_intervals = []
        for interval in tg._tierDict['phoneme']._entries:
            if interval.label in {'<IVER>', '<SIL>', '<VOCNOISE>', '<NOISE>'}:
                continue
            text = interval.label
            if text.startswith('<'):
                text = 'spn'
            phone_intervals.append((interval.start, interval.end, text))
        word_tier = IntervalTier('words', word_intervals, minT=tg.minTimestamp, maxT=tg.maxTimestamp)
        phone_tier = IntervalTier('phones', phone_intervals, minT=tg.minTimestamp, maxT=tg.maxTimestamp)
        reference_tg.addTier(word_tier)
        reference_tg.addTier(phone_tier)
        reference_tg.save(reference_tg_path, format='short_textgrid', includeBlankSpaces=True)


def parse_directory(original_directory: Path, benchmark_directory: Path, reference_directory: Path):
    # fix_sample_rate(benchmark_directory)
    fix_textgrids(original_directory, benchmark_directory, reference_directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='create_seoul_benchmark',
        description='Creates two directories of TextGrid files for use with MFA, '
                    'one as input with utterances (benchmark) and one for use in reference alignments (reference)')
    parser.add_argument('original_directory')
    parser.add_argument('benchmark_directory')
    parser.add_argument('reference_directory')

    args = parser.parse_args()
    parse_directory(
        Path(args.original_directory),
        Path(args.benchmark_directory),
        Path(args.reference_directory)
    )
