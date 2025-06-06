from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path

import soundfile
from praatio import textgrid as tgio
from praatio.utilities.constants import Interval

speaker_pattern = re.compile(r"^(?P<speaker>s\d{2}).*$")
word_line_pattern = re.compile(r"^(?P<time>[0-9.]+)  ?12[123] (?P<label>[-'_\w<>}{ ?=]+);?.*$")
phone_line_pattern = re.compile(
    r"^(?P<time>[0-9.]+)  ?12[123] (?P<label>[-'_\w<>}{?=]+)(\+1n?)?( ?;.*)?$"
)


def load_file(path: Path, max_time):
    begin = 0
    data = []
    if path.suffix == ".words":
        line_pattern = word_line_pattern
        line_type = "words"
    else:
        line_pattern = phone_line_pattern
        line_type = "phones"
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            m = line_pattern.match(line)
            if not m:
                if ("122" in line or "123" in line) and "color" not in line:
                    print("NOMATCH", line)
                    print(line_type, repr(line))
                continue
            end = float(m.group("time"))
            if end > max_time:
                continue
            label = m.group("label")
            label = label.replace(" ", "_")
            if "<NOISE-" in label.upper() and "_" not in label:
                label = label.lower().replace("<noise-", "")[:-1]
            elif "<NOSIE-" in label.upper() and "_" not in label:
                label = label.replace("<NOSIE-", "")[:-1]
            elif "<LAUH-" in label.upper() and "_" not in label:
                label = "<LAUGH>"
            elif "<VOCNOISE-" in label.upper():
                label = label.lower().replace("<vocnoise-", "")[:-1]
            elif "<EXT-" in label.upper() and "_" not in label:
                label = label.lower().replace("<ext-", "")[:-1]
            elif label.upper().startswith("<CUTOFF"):
                m = re.match(r"<CUTOFF-\w+=([^?_]+)>", label)
                if m is not None:
                    label = f"<CUTOFF-{m.group(1)}>"
                else:
                    label = "<CUTOFF>"
            elif label.upper().startswith("<HES") and "_" not in label:
                label = label.lower().replace("<hes-", "")[:-1]
            elif label.upper().startswith("<IVER"):
                label = ""
            elif line_type == "phones" and "IVER" in label.upper():
                label = ""
            elif label.startswith("{"):
                label = ""
            elif label.upper().startswith("<LAUGH-"):
                label = "<LAUGH>"
            elif label.upper().startswith("<EXCLUDE-"):
                label = "<EXCLUDE>"
            elif label.upper().startswith("<EXCL-") and "_" not in label:
                label = label.lower().replace("<excl-", "")[:-1]
            elif label.upper().startswith("<UNKNOWN"):
                label = "<UNKNOWN>"
            elif label.upper().startswith("<ERROR"):
                label = "<ERROR>"
            elif label.upper() == "UNKNOWN":
                label = "spn"
            elif label.lower() == "<laughyet>":
                label = "yet"
            elif label.lower() == "<noisethere>":
                label = "there"
            elif label.lower() == "<thirty>":
                label = ""
            elif line_type == "words" and label.upper() in [
                "<VOCNOISE>",
                "<VOCNOISED>",
                "<SIL>",
                "<NOISE>",
                "<IVER>",
            ]:
                label = ""
            elif line_type == "phones" and label.upper() in [
                "VOCNOISE",
                "SIL",
                "NOISE",
                "IVER",
            ]:
                label = ""
            elif line_type == "phones" and label.upper() in [
                "LAUGH",
                "UNKNOWN",
            ]:
                label = "spn"
            if "=" in label:
                label = "<UNKNOWN>"
            elif "_" in label:
                label = "<UNKNOWN>"
            elif label.endswith("-"):
                label = "<UNKNOWN>"
            if label.endswith("s'"):
                label += "s"
            if begin == end:
                continue
            if label in {"<LAUGH>"} and data and data[-1].label == label:
                data[-1] = Interval(data[-1].start, end, label)
            elif (
                line_type == "words"
                and label.lower() == "right"
                and data
                and data[-1].label.lower() == "all"
            ):
                data[-1] = Interval(data[-1].start, end, "alright")
            else:
                data.append(Interval(begin, end, label))
            if data[-1].label == "<LAUGH>" and data[-1].end - data[-1].start > 1:
                _ = data.pop(-1)
            begin = end
    data = [x for x in data if x.label]
    return data


def mid_point(interval):
    return interval.start + ((interval.end - interval.start) / 2)


def correct_phones(word_intervals, phone_intervals):
    new_phone_intervals = []
    for w in word_intervals:
        if w.label in {
            "<UNKNOWN>",
            "<LAUGH>",
            "<HES>",
            "<CUTOFF>",
            "<EXCLUDE>",
            "<EXT>",
            "<ERROR>",
            "<VOCNOISE>",
        }:
            word_phone_intervals = []
            for x in phone_intervals:
                if w.start > mid_point(x):
                    continue
                if w.end < mid_point(x):
                    break
                word_phone_intervals.append(x)
            for x in word_phone_intervals:
                if x.label == "spn":
                    new_phone_intervals.append(x)
                    break
            else:
                new_start = w.start
                if new_phone_intervals and new_phone_intervals[-1].end > new_start:
                    new_start = new_phone_intervals[-1].end
                new_phone_interval = Interval(new_start, w.end, "spn")
                new_phone_intervals.append(new_phone_interval)
        else:
            for x in phone_intervals:
                if w.start > mid_point(x):
                    continue
                if w.end < mid_point(x):
                    break
                new_start = x.start
                new_end = x.end
                # disabling this section
                # if x.start < w.start:
                #    new_start = w.start
                # if x.end > w.end:
                #    new_end = w.end
                # if i == 0:
                #    new_start = w.start
                # if i == len(word_phone_intervals) - 1:
                #    new_end = w.end
                if new_phone_intervals and new_phone_intervals[-1].end > new_start:
                    new_phone_intervals[-1] = Interval(
                        new_phone_intervals[-1].start, new_start, new_phone_intervals[-1].label
                    )
                new_phone_intervals.append(Interval(new_start, new_end, x.label))

    return sorted(new_phone_intervals, key=lambda y: y.start)


def construct_phrases(word_intervals, max_time):
    data = []
    cur_utt = []
    silence_padding = 0.2
    for i, w in enumerate(word_intervals):
        if cur_utt and i != 0:
            if w.start - word_intervals[i - 1].end > silence_padding * 1.5 or (
                w.start - word_intervals[i - 1].end > silence_padding
                and cur_utt[-1].end - cur_utt[0].start > 10
            ):
                begin = cur_utt[0].start - silence_padding
                if begin < 0:
                    begin = 0
                end = cur_utt[-1].end + silence_padding
                if end > max_time:
                    end = max_time
                label = " ".join(x.label for x in cur_utt)

                if data and data[-1].end > begin:
                    begin = (data[-1].end + begin) / 2
                    data[-1] = Interval(data[-1].start, begin, data[-1].label)
                data.append(Interval(begin, end, label))
                cur_utt = []
        cur_utt.append(w)
    if cur_utt:
        begin = cur_utt[0].start - silence_padding
        if begin < 0:
            begin = 0
        end = cur_utt[-1].end + silence_padding
        if end > max_time:
            end = max_time
        label = " ".join(x.label for x in cur_utt)
        if data and data[-1].end > begin:
            begin = (data[-1].end + begin) / 2
            data[-1] = Interval(data[-1].start, begin, data[-1].label)
        data.append(Interval(begin, end, label))

    # Ignore backchannel utterances
    skip_labels = {
        "<exclude>",
        "<cutoff>",
        "<unknown>",
        "<laugh>",
        "oh",
        "uh",
        "ah",
        "um",
        "a",
        "uh-oh",
        "yeah",
        "no",
        "okay",
        "or",
        "eh",
        "hum",
        "aw",
        "wow",
        "um-hum",
        "uh-huh",
        "mm",
        "really",
        "huh",
        "hm",
        "right",
        "sure",
        "mm-hmm",
        "umhum",
    }
    data = [
        x
        for x in data
        if x.end - x.start > 0.5 + (silence_padding * 2)
        and not all(y in skip_labels for y in x.label.lower().split())
        and x.label
        not in {
            "oh",
            "uh",
            "ah",
            "um",
            "a",
            "uh-oh",
            "yeah",
            "no",
            "okay",
            "or",
            "eh",
            "hum",
            "aw",
            "wow",
            "it's",
            "people",
            "or",
            "i'm",
            "there",
            "and",
            "my",
            "i",
            "right",
            "duh",
            "fine",
            "oh yeah",
            "what",
            "so",
            "huh",
            "hm",
            "the",
            "mm",
            "really",
            "umhum",
            "and uh",
            "um hum",
            "um-hum",
            "um-hum um-hum",
            "uh-huh",
            "uh huh",
            "but",
            "my",
            "ima",
            "uh uh",
            "whoa",
            "this",
            "yeah um",
            "we",
            "you",
            "mm-hmm",
            "yknow",
            "sure",
            "now",
            "i uh",
        }
    ]

    return data


def check_speaker_directories(original_directory: Path):
    for f_name in original_directory.iterdir():
        if f_name.is_dir() and f_name.name == "s01":
            return True
    return False


def parse_files(
    sound_file: Path,
    words_file: Path,
    phones_file: Path,
    benchmark_directory: Path,
    reference_directory: Path,
):
    file_name = sound_file.stem
    duration = soundfile.info(sound_file).duration
    speaker = speaker_pattern.search(file_name).group("speaker")

    benchmark_speaker_directory = benchmark_directory.joinpath(speaker)
    benchmark_speaker_directory.mkdir(parents=True, exist_ok=True)
    benchmark_sound_file = benchmark_speaker_directory.joinpath(sound_file.name)
    if not benchmark_sound_file.exists():
        shutil.copyfile(sound_file, benchmark_sound_file)

    aligned_speaker_directory = reference_directory.joinpath(speaker)
    aligned_speaker_directory.mkdir(parents=True, exist_ok=True)

    word_intervals = load_file(words_file, duration)
    phone_intervals = load_file(phones_file, duration)
    utterances = construct_phrases(word_intervals, duration)
    utterance_path = os.path.join(benchmark_speaker_directory, f"{file_name}.TextGrid")
    tg = tgio.Textgrid(maxTimestamp=duration)
    tier = tgio.IntervalTier(speaker, utterances, minT=0, maxT=duration)

    tg.addTier(tier)
    tg.save(utterance_path, includeBlankSpaces=True, format="long_textgrid", reportingMode="error")

    aligned_path = os.path.join(aligned_speaker_directory, f"{file_name}.TextGrid")
    tg = tgio.Textgrid(maxTimestamp=duration)
    phone_intervals = correct_phones(word_intervals, phone_intervals)

    word_tier = tgio.IntervalTier("words", word_intervals, minT=0, maxT=duration)
    phone_tier = tgio.IntervalTier("phones", phone_intervals, minT=0, maxT=duration)
    tg.addTier(word_tier)
    tg.addTier(phone_tier)

    tg.save(aligned_path, includeBlankSpaces=True, format="long_textgrid", reportingMode="error")


def parse_directory(
    original_directory: Path, benchmark_directory: Path, reference_directory: Path
):
    file_tuples = []
    if check_speaker_directories(original_directory):
        for s_name in original_directory.iterdir():
            for f_name in s_name.iterdir():
                if f_name.suffix == ".wav":
                    file_tuples.append(
                        (f_name, f_name.with_suffix(".words"), f_name.with_suffix(".phones"))
                    )
    else:
        for f_name in original_directory.iterdir():
            if f_name.suffix == ".wav":
                file_tuples.append(
                    (f_name, f_name.with_suffix(".words"), f_name.with_suffix(".phones"))
                )
    print(f"Found {len(file_tuples)} files!")
    for sound_file, words_file, phones_file in file_tuples:
        print(sound_file.stem)
        parse_files(sound_file, words_file, phones_file, benchmark_directory, reference_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="create_buckeye_benchmark",
        description="Creates two directories of TextGrid files for use with MFA, "
        "one as input with utterances (benchmark) and one for use in reference alignments (reference)",
    )
    parser.add_argument("original_directory")
    parser.add_argument("benchmark_directory")
    parser.add_argument("reference_directory")

    args = parser.parse_args()
    parse_directory(
        Path(args.original_directory),
        Path(args.benchmark_directory),
        Path(args.reference_directory),
    )
