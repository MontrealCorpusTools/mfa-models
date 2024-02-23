import collections
import re
import argparse

from bs4 import BeautifulSoup as bs
from praatio import textgrid as tgio
from praatio.utilities.constants import Interval
import soundfile
from pathlib import Path


def parse_directory(
        original_directory: Path,
        benchmark_directory: Path,
        reference_directory: Path,
        training_directory: Path
):
    benchmark_directory.mkdir(parents=True, exist_ok=True)
    reference_directory.mkdir(parents=True, exist_ok=True)
    training_directory.mkdir(parents=True, exist_ok=True)
    talk_to_speaker = collections.defaultdict(set)

    with open(original_directory.joinpath('speaker_data.dat'), 'r', encoding='shift_jis') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.split()
            try:
                speaker_id = int(line[0])
            except:
                continue
            talk_ids = line[-1]
            for t_id in talk_ids.split(':'):
                talk_to_speaker[t_id].add(speaker_id)

    for k,v in talk_to_speaker.items():
        if len(v) > 1:
            print(k,v)

    for transcription_path in original_directory.iterdir():
        if transcription_path.suffix != '.xml':
            continue
        talk_name = transcription_path.stem
        duration = soundfile.info(transcription_path.with_suffix('.wav')).duration
        benchmark_path = benchmark_directory.joinpath(talk_name + '.TextGrid')
        reference_path = reference_directory.joinpath(talk_name + '.TextGrid')
        training_path = training_directory.joinpath(talk_name + '.TextGrid')
        if False and benchmark_path.exists():
            continue
        print(transcription_path.name)
        benchmark_tg = tgio.Textgrid(minTimestamp=0.0, maxTimestamp=duration)
        reference_tg = tgio.Textgrid(minTimestamp=0.0, maxTimestamp=duration)
        with (open(transcription_path, 'r', encoding='utf8') as f):
            content = bs(f.read(), 'xml')
            talks = content.findAll('Talk')
            for talk in talks:
                speaker_id = 'CSJ_' + talk.attrs['SpeakerID']
                benchmark_tier = tgio.IntervalTier(speaker_id,[], minT=0.0, maxT=duration)
                reference_word_tier = tgio.IntervalTier(f"{speaker_id} - words",[], minT=0.0, maxT=duration)
                reference_phone_tier = tgio.IntervalTier(f"{speaker_id} - phones",[], minT=0.0, maxT=duration)
                alternate_speaker = None
                if len(talk_to_speaker[talk_name]) > 1:
                    alternate_speaker = [x for x in talk_to_speaker[talk_name] if x != int(talk.attrs['SpeakerID'])][0]
                    alternate_speaker = f"CSJ_{alternate_speaker}"
                    alternate_benchmark_tier = tgio.IntervalTier(alternate_speaker,[], minT=0.0, maxT=duration)
                    alternate_reference_word_tier = tgio.IntervalTier(f"{alternate_speaker} - words",[], minT=0.0, maxT=duration)
                    alternate_reference_phone_tier = tgio.IntervalTier(f"{alternate_speaker} - phones",[], minT=0.0, maxT=duration)
                utterance_intervals = talk.findAll('IPU')
                has_reference = False
                for utterance in utterance_intervals:
                    transcription = ''
                    utt_begin = float(utterance.attrs['IPUStartTime'])
                    utt_end = float(utterance.attrs['IPUEndTime'])
                    channel = 0 if utterance.attrs['Channel'] == 'L' else 1
                    long_words = utterance.findAll('LUW')
                    skip = False
                    for long_word in long_words:
                        word = ''
                        short_words = long_word.findAll('SUW')
                        word_begin = None
                        word_end = None
                        if skip:
                            break
                        for short_word in short_words:
                            if '(R' in short_word.attrs['OrthographicTranscription'] or \
                                    '(?' in short_word.attrs['OrthographicTranscription'] or \
                                    short_word.attrs['OrthographicTranscription'] in {'<FV>'}:
                                skip = True
                                break
                            word += short_word.attrs['OrthographicTranscription']
                            moras = short_word.findAll('Mora')
                            for mora in moras:
                                phonemes = mora.findAll('Phoneme')
                                for phoneme in phonemes:
                                    phones = phoneme.findAll('Phone')
                                    phone_label = phoneme.attrs["PhonemeEntity"]
                                    begin = None
                                    end = None
                                    for p in phones:
                                        if p.attrs['PhoneEndTime'] is None:
                                            continue
                                        if begin is None:
                                            begin = float(p.attrs['PhoneStartTime'])
                                        if p.attrs['PhoneEndTime'] is not None:
                                            end = float(p.attrs['PhoneEndTime'])
                                        has_reference = True
                                        if word_begin is None:
                                            word_begin = begin
                                        word_end = end
                                    if not word.startswith('(D') and begin != end and phones:
                                        if channel == 0 and alternate_speaker is not None:
                                            alternate_reference_phone_tier.insertEntry(Interval(begin, end, phone_label))
                                        else:
                                            reference_phone_tier.insertEntry(Interval(begin, end, phone_label))
                        if skip:
                            continue
                        word = word.replace(')', '')
                        if word.startswith('(D'):
                            word = "<cutoff>"
                        elif word.startswith('(?'):
                            word = "<unk>"
                        elif word.startswith('(A'):
                            word = word.split(maxsplit=1)[-1].split(';')[0].replace('．', '点')
                        while any(word.startswith(x) for x in ['(F', '(M', '(O']):
                            word = word.split(maxsplit=1)[-1]
                        word = re.sub(r'\(D (\(\?.*?\))?.*?\)', '<unk>', word)
                        word = re.sub(r'\(A ([^;]+?)?;.*?\)', r'\1', word).replace('．', '点')
                        word = re.sub(r'\([FM] (.*?)\)', r'\1', word)
                        transcription += word
                        if word_begin is None:
                            continue
                        if word == "<cutoff>":
                            if channel == 0 and alternate_speaker is not None:
                                alternate_reference_phone_tier.insertEntry(Interval(word_begin, word_end, "spn"))
                            else:
                                reference_phone_tier.insertEntry(Interval(word_begin, word_end, "spn"))
                        if channel == 0 and alternate_speaker is not None:
                            alternate_reference_word_tier.insertEntry(Interval(word_begin, word_end, word))
                        else:
                            reference_word_tier.insertEntry(Interval(word_begin, word_end, word))
                    if not skip and transcription:
                        if channel == 1 and alternate_speaker is not None:
                            alternate_benchmark_tier.insertEntry(Interval(utt_begin, utt_end, transcription))
                        else:
                            benchmark_tier.insertEntry(Interval(utt_begin, utt_end, transcription))
                benchmark_tg.addTier(benchmark_tier)
                reference_tg.addTier(reference_word_tier)
                reference_tg.addTier(reference_phone_tier)
                if alternate_speaker is not None:
                    benchmark_tg.addTier(alternate_benchmark_tier)
                    reference_tg.addTier(alternate_reference_word_tier)
                    reference_tg.addTier(alternate_reference_phone_tier)
            if has_reference:
                reference_tg.save(
                    str(reference_path),
                    "long_textgrid",
                    includeBlankSpaces=True)
                benchmark_tg.save(
                    str(benchmark_path),
                    "long_textgrid",
                    includeBlankSpaces=True)
            benchmark_tg.save(
                str(training_path),
                "long_textgrid",
                includeBlankSpaces=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='create_seoul_benchmark',
        description='Creates two directories of TextGrid files for use with MFA, '
                    'one as input with utterances (benchmark) and one for use in reference alignments (reference)')
    parser.add_argument('original_directory')
    parser.add_argument('benchmark_directory')
    parser.add_argument('reference_directory')
    parser.add_argument('training_directory')

    args = parser.parse_args()
    parse_directory(
        Path(args.original_directory),
        Path(args.benchmark_directory),
        Path(args.reference_directory),
        Path(args.training_directory),
    )
