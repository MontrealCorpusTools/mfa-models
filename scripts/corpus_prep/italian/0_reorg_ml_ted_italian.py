import os

import soundfile
from praatio.textgrid import IntervalTier, Textgrid
from praatio.utilities.constants import Interval

root_dir = r"C:\Users\micha\Documents\Data\model_training_corpora\italian\mtedx_it\it-it\data"

if __name__ == "__main__":
    for p in ["test", "train", "valid"]:
        audio_dir = os.path.join(root_dir, p, "wav")
        segments_file = os.path.join(root_dir, p, "txt", "segments")
        transcript_file = os.path.join(root_dir, p, "txt", f"{p}.it")
        transcripts = []
        with open(transcript_file, "r", encoding="utf8") as f:
            for line in f:
                line = line.strip()
                transcripts.append(line)
        intervals = {}
        with open(segments_file, "r", encoding="utf8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                _, file, begin, end = line.split()
                begin = float(begin)
                end = float(end)
                if file not in intervals:
                    intervals[file] = []
                if intervals[file] and begin < intervals[file][-1].end:
                    intervals[file][-1] = Interval(
                        intervals[file][-1].start,
                        end,
                        intervals[file][-1].label + " " + transcripts[i],
                    )
                    continue
                if transcripts[i] in ["[Applausi]", "(Applausi)", "(Musica)"]:
                    continue
                elif transcripts[i].startswith("[") or transcripts[i].startswith("("):
                    print(transcripts[i])
                intervals[file].append(Interval(begin, end, transcripts[i]))
        for file, interval_list in intervals.items():
            wav_path = os.path.join(audio_dir, f"{file}.flac")
            tg_path = os.path.join(audio_dir, f"{file}.TextGrid")
            info = soundfile.info(wav_path)
            duration = info.duration
            tg = Textgrid(minTimestamp=0, maxTimestamp=duration)
            interval_tier = IntervalTier(file, sorted(interval_list), minT=0, maxT=duration)
            tg.addTier(interval_tier)
            tg.save(tg_path, "short_textgrid", True)
