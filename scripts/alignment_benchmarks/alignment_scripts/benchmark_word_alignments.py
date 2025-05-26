"""Based on https://pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html"""
import csv
import os
import re
import sys
import typing

import sqlalchemy
import torch
import torchaudio
import torchaudio.functional as F
import tqdm
from kalpy.fstext.lexicon import CtmInterval as KalpyCtmInterval
from kalpy.fstext.lexicon import HierarchicalCtm, WordCtmInterval
from montreal_forced_aligner import config
from montreal_forced_aligner.command_line.mfa import mfa_cli
from montreal_forced_aligner.corpus.acoustic_corpus import AcousticCorpus
from montreal_forced_aligner.data import CtmInterval
from montreal_forced_aligner.db import File, Utterance, Word, WordInterval
from montreal_forced_aligner.exceptions import TextGridParseError
from montreal_forced_aligner.helper import mfa_open
from praatio import textgrid as tgio

root_dir = r"D:\Data\experiments\alignment_benchmarking"
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\2.0.0a_archived"
mfa21_dir = r"D:\Data\models\2.1_trained"
mfa22_dir = r"D:\Data\models\2.2_trained"
mfa30_dir = r"D:\Data\models\3.0_trained"
trained22_dir = r"D:\Data\models\2.2_trained\buckeye"
trained30_dir = r"D:\Data\models\3.0_trained\buckeye"
mapping_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mapping_files"
)
nemo_tools_path = r"C:\Users\micha\Documents\Dev\NeMo\tools"
config.CLEAN = True
config.USE_POSTGRES = True

root_dir = r"D:\Data\experiments\alignment_benchmarking"

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit",
    "buckeye": r"D:\Data\speech\Buckeye",
}

conditions = {
    "torchaudio_mms_fa": (None, None),
    "nemo_forced_aligner": (None, None),
    "whisperx": (None, None),
    "arpa_1.0": (
        os.path.join(mfa10_dir, "english.dict"),
        os.path.join(mfa10_dir, "english.zip"),
    ),
    "arpa_2.0": (
        os.path.join(mfa20_dir, "english_us_arpa.dict"),
        os.path.join(mfa20_dir, "english_us_arpa.zip"),
    ),
    "arpa_2.0a": (
        os.path.join(mfa20a_dir, "english_us_arpa.dict"),
        os.path.join(mfa20a_dir, "english_us_arpa.zip"),
    ),
    "mfa_2.0": (
        os.path.join(mfa20_dir, "english_us_mfa.dict"),
        os.path.join(mfa20_dir, "english_mfa.zip"),
    ),
    "mfa_2.0a": (
        os.path.join(mfa20a_dir, "english_us_mfa.dict"),
        os.path.join(mfa20a_dir, "english_mfa.zip"),
    ),
    "mfa_2.1": (
        os.path.join(mfa21_dir, "english_us_mfa.dict"),
        os.path.join(mfa21_dir, "english_mfa.zip"),
    ),
    "mfa_2.2": (
        os.path.join(mfa22_dir, "english_us_mfa.dict"),
        os.path.join(mfa22_dir, "english_mfa.zip"),
    ),
    "mfa_3.0": (
        os.path.join(mfa30_dir, "english_us_mfa.dict"),
        os.path.join(mfa30_dir, "english_mfa.zip"),
    ),
    "arpa_3.0": (
        os.path.join(mfa30_dir, "english_us_arpa.dict"),
        os.path.join(mfa30_dir, "english_us_arpa.zip"),
    ),
    "trained_2.2": (
        os.path.join(trained22_dir, "english_us_mfa.dict"),
        os.path.join(trained22_dir, "english_mfa.zip"),
    ),
    "trained_3.0": (
        os.path.join(trained30_dir, "english_us_mfa.dict"),
        os.path.join(trained30_dir, "english_mfa.zip"),
    ),
    "arpa_2.2": (
        os.path.join(mfa20a_dir, "english_us_arpa.dict"),
        os.path.join(mfa20a_dir, "english_us_arpa.zip"),
    ),
}


def align(emission, tokens):
    targets = torch.tensor([tokens], dtype=torch.int32, device=device)
    alignments, scores = F.forced_align(emission, targets, blank=0)

    alignments, scores = (
        alignments[0],
        scores[0],
    )  # remove batch dimension for simplicity
    scores = scores.exp()  # convert back to probability
    return alignments, scores


def unflatten(list_, lengths):
    assert len(list_) == sum(lengths)
    i = 0
    ret = []
    for l in lengths:
        ret.append(list_[i : i + l])
        i += l
    return ret


def generate_ctm(
    token_spans, transcript, ratio, sample_rate, utterance_begin, reference
) -> HierarchicalCtm:
    i = 0
    reference_index = 0
    word_intervals = []
    for word in transcript:
        character_intervals = []
        for j in range(len(word)):
            span = token_spans[i]
            begin = int(ratio * span.start) / sample_rate
            begin += utterance_begin
            end = int(ratio * span.end) / sample_rate
            end += utterance_begin
            character_intervals.append(
                KalpyCtmInterval(begin, end, LABELS[span.token], span.token)
            )
            i += 1
        if word == reference[reference_index].label:
            reference_index += 1
        elif (
            word_intervals
            and f"{word_intervals[-1].label}-{word}" in reference[reference_index].label
        ):
            word_intervals[-1].label = f"{word_intervals[-1].label}-{word}"
            word_intervals[-1].symbol = f"{word_intervals[-1].label}-{word}"
            word_intervals[-1].phones.extend(character_intervals)
            if reference[reference_index].label == word_intervals[-1].label:
                reference_index += 1
            continue
        word_intervals.append(WordCtmInterval(word, word, character_intervals))
    return HierarchicalCtm(word_intervals)


def align_words(
    ref: typing.List[CtmInterval],
    test: typing.List[CtmInterval],
):
    try:
        assert len(ref) == len(test)
    except AssertionError:
        print(ref)
        print(test)
        raise
    error_sum = 0.0
    boundary_count = 0
    for i, r in enumerate(ref):
        t = test[i]
        # assert r.label == t.label
        error_sum += abs(r.begin - t.begin)
        error_sum += abs(r.end - t.end)
        boundary_count += 2
    return error_sum / boundary_count


def parse_aligned_textgrid(path: str, exclude_unknowns=True) -> typing.List[CtmInterval]:
    """
    Load a TextGrid as a dictionary of speaker's phone tiers

    Parameters
    ----------
    path: :class:`~pathlib.Path`
        TextGrid file to parse

    Returns
    -------
    dict[str, list[:class:`~montreal_forced_aligner.data.CtmInterval`]]
        Parsed phone tier
    """
    tg = tgio.openTextgrid(path, includeEmptyIntervals=False, reportingMode="silence")
    num_tiers = len(tg.tiers)
    if num_tiers == 0:
        raise TextGridParseError(path, "Number of tiers parsed was zero")
    data = []
    for tier_name in tg.tierNames:
        ti = tg._tierDict[tier_name]
        if not isinstance(ti, tgio.IntervalTier):
            continue
        if "words" not in tier_name:
            continue
        for begin, end, text in ti.entries:
            text = text.lower().strip().replace("?", "")
            if exclude_unknowns and re.match(r"^[\[(<].*", text):
                continue
            if not text:
                continue
            begin, end = round(begin, 4), round(end, 4)
            # if end - begin < 0.01:
            #    continue
            interval = CtmInterval(begin, end, text)
            data.append(interval)
    return data


if __name__ == "__main__":
    csv_header = [
        "file",
        "begin",
        "end",
        "speaker",
        "duration",
        "normalized_text",
        "filtered_text",
        "alignment_score",
        "alignment_likelihood",
        "word_count",
        "frames_per_second",
        "words_per_second",
    ]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

    for condition, (dictionary_path, model_path) in conditions.items():
        if condition == "torchaudio_mms_fa":
            with torch.inference_mode():
                for corpus, root in corpus_directories.items():
                    output_directory = os.path.join(root_dir, "alignments", condition, corpus)
                    if os.path.exists(output_directory):
                        continue
                    try:
                        bundle = torchaudio.pipelines.MMS_FA
                    except AttributeError:
                        print("Incorrect version of torchaudio, skipping torchaudio_mms_fa")
                        continue

                    model = bundle.get_model(with_star=False).to(device)

                    LABELS = bundle.get_labels(star=None)
                    DICTIONARY = bundle.get_dict(star=None)
                    corpus = AcousticCorpus(corpus_directory=os.path.join(root, "benchmark"))
                    corpus.delete_database()
                    corpus._load_corpus()
                    os.makedirs(output_directory, exist_ok=True)
                    csv_path = os.path.join(output_directory, "word_alignment.csv")
                    with (
                        corpus.session() as session,
                        mfa_open(csv_path, "w") as f,
                        tqdm.tqdm(total=corpus.num_utterances) as progress_bar,
                    ):
                        writer = csv.DictWriter(f, fieldnames=csv_header)
                        writer.writeheader()
                        file_query = (
                            session.query(File)
                            .options(
                                sqlalchemy.orm.joinedload(File.sound_file, innerjoin=True),
                            )
                            .order_by(File.name)
                        )
                        for file in file_query:
                            file_ctm = HierarchicalCtm([])
                            if file.relative_path:
                                output_path = os.path.join(output_directory, file.relative_path)
                                os.makedirs(output_path, exist_ok=True)
                            else:
                                output_path = output_directory
                            output_path = os.path.join(output_path, file.name + ".TextGrid")
                            query = (
                                session.query(Utterance)
                                .filter(Utterance.file_id == file.id)
                                .options(
                                    sqlalchemy.orm.joinedload(
                                        Utterance.file, innerjoin=True
                                    ).joinedload(File.sound_file, innerjoin=True),
                                )
                                .order_by(Utterance.begin)
                            )
                            reference_path = os.path.join(root, "reference")
                            if file.relative_path:
                                reference_path = os.path.join(reference_path, file.relative_path)
                            reference_path = os.path.join(reference_path, file.name + ".TextGrid")
                            reference_word_intervals = parse_aligned_textgrid(reference_path)
                            reference_interval_index = 0
                            for utterance in query:
                                kalpy_utterance = utterance.to_kalpy()
                                waveform = torch.unsqueeze(
                                    torch.Tensor(kalpy_utterance.segment.load_audio()),
                                    0,
                                )
                                text = utterance.text.lower().replace("-", " ")
                                transcript = [
                                    re.sub(rf'[^{"".join(LABELS[1:])}]', "", x)
                                    for x in text.split()
                                    if not re.match(r"^[\[(<].*", x)
                                ]
                                transcript = [x for x in transcript if x]
                                tokenized_transcript = [
                                    DICTIONARY[c] for word in transcript for c in word
                                ]
                                emission, _ = model(waveform.to(device))
                                aligned_tokens, alignment_scores = align(
                                    emission, tokenized_transcript
                                )
                                token_spans = F.merge_tokens(aligned_tokens, alignment_scores)
                                alignment_likelihood = sum(alignment_scores) / len(
                                    alignment_scores
                                )
                                word_spans = unflatten(
                                    token_spans, [len(word) for word in transcript]
                                )
                                ratio = waveform.size(1) / emission.size(1)
                                frames_per_second = emission.size(1) / utterance.duration
                                reference = []
                                while True:
                                    try:
                                        interval = reference_word_intervals[
                                            reference_interval_index
                                        ]
                                    except IndexError:
                                        break
                                    if interval.begin >= utterance.end:
                                        break
                                    if interval.begin >= utterance.begin:
                                        reference.append(interval)
                                    reference_interval_index += 1
                                ctm = generate_ctm(
                                    token_spans,
                                    transcript,
                                    ratio,
                                    bundle.sample_rate,
                                    utterance.begin,
                                    reference,
                                )
                                file_ctm.word_intervals.extend(ctm.word_intervals)
                                try:
                                    alignment_score = align_words(reference, ctm.word_intervals)
                                except AssertionError:
                                    print(file.name)
                                    raise
                                    continue
                                words_per_second = len(reference) / utterance.duration

                                data = {
                                    "file": file.name,
                                    "begin": utterance.begin,
                                    "end": utterance.end,
                                    "duration": utterance.duration,
                                    "speaker": utterance.speaker_name,
                                    "normalized_text": text.replace(",", ""),
                                    "filtered_text": " ".join(transcript),
                                    "alignment_score": alignment_score,
                                    "alignment_likelihood": float(alignment_likelihood),
                                    "word_count": len(ctm.word_intervals),
                                    "frames_per_second": frames_per_second,
                                    "words_per_second": words_per_second,
                                }
                                writer.writerow(data)
                                progress_bar.update(1)
                            file_ctm.export_textgrid(
                                output_path,
                                file_duration=file.duration,
                                output_format="short_textgrid",
                            )
        elif condition == "nemo_forced_aligner":
            try:
                from dataclasses import dataclass, field, is_dataclass

                from nemo.collections.asr.models.ctc_models import EncDecCTCModel
                from nemo.collections.asr.models.hybrid_rnnt_ctc_models import (
                    EncDecHybridRNNTCTCModel,
                )
                from nemo.collections.asr.parts.utils.streaming_utils import FrameBatchASR
                from nemo.collections.asr.parts.utils.transcribe_utils import setup_model
                from nemo.core.config import hydra_runner
            except ImportError:
                raise
                continue
            sys.path.append(nemo_tools_path)
            sys.path.insert(0, os.path.join(nemo_tools_path, "nemo_forced_aligner"))
            import tempfile

            from nemo_forced_aligner.align import AlignmentConfig, ASSFileConfig, CTMFileConfig
            from nemo_forced_aligner.utils.data_prep import (
                V_NEGATIVE_NUM,
                Segment,
                Token,
                Word,
                add_t_start_end_to_utt_obj,
                get_utt_obj,
            )
            from nemo_forced_aligner.utils.viterbi_decoding import viterbi_decoding

            cfg = AlignmentConfig()
            cfg.pretrained_name = "stt_en_conformer_ctc_medium"
            if cfg.transcribe_device is None:
                transcribe_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            else:
                transcribe_device = torch.device(cfg.transcribe_device)
            if cfg.viterbi_device is None:
                viterbi_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            else:
                viterbi_device = torch.device(cfg.viterbi_device)
            model, _ = setup_model(cfg, transcribe_device)
            model.eval()
            if isinstance(model, EncDecHybridRNNTCTCModel):
                model.change_decoding_strategy(decoder_type="ctc")
            if cfg.use_local_attention:
                model.change_attention_model(
                    self_attention_model="rel_pos_local_attn", att_context_size=[64, 64]
                )

            with torch.inference_mode():
                for corpus, root in corpus_directories.items():
                    output_directory = os.path.join(root_dir, "alignments", condition, corpus)
                    if os.path.exists(output_directory):
                        continue
                    corpus = AcousticCorpus(corpus_directory=os.path.join(root, "benchmark"))
                    corpus.delete_database()
                    corpus._load_corpus()
                    os.makedirs(output_directory, exist_ok=True)
                    csv_path = os.path.join(output_directory, "word_alignment.csv")
                    with (
                        corpus.session() as session,
                        mfa_open(csv_path, "w") as f,
                        tempfile.TemporaryDirectory() as tmpdir,
                        tqdm.tqdm(total=corpus.num_utterances) as progress_bar,
                    ):
                        writer = csv.DictWriter(f, fieldnames=csv_header)
                        writer.writeheader()
                        file_query = (
                            session.query(File)
                            .options(
                                sqlalchemy.orm.joinedload(File.sound_file, innerjoin=True),
                            )
                            .order_by(File.name)
                        )
                        for file in file_query:
                            file_ctm = HierarchicalCtm([])
                            if file.relative_path:
                                output_path = os.path.join(output_directory, file.relative_path)
                                os.makedirs(output_path, exist_ok=True)
                            else:
                                output_path = output_directory
                            output_path = os.path.join(output_path, file.name + ".TextGrid")
                            query = (
                                session.query(Utterance)
                                .filter(Utterance.file_id == file.id)
                                .options(
                                    sqlalchemy.orm.joinedload(
                                        Utterance.file, innerjoin=True
                                    ).joinedload(File.sound_file, innerjoin=True),
                                )
                                .order_by(Utterance.begin)
                            )
                            reference_path = os.path.join(root, "reference")
                            if file.relative_path:
                                reference_path = os.path.join(reference_path, file.relative_path)
                            reference_path = os.path.join(reference_path, file.name + ".TextGrid")
                            reference_word_intervals = parse_aligned_textgrid(reference_path)
                            reference_interval_index = 0
                            for utterance in query:
                                kalpy_utterance = utterance.to_kalpy()
                                reference = []
                                while True:
                                    try:
                                        interval = reference_word_intervals[
                                            reference_interval_index
                                        ]
                                    except IndexError:
                                        break
                                    if interval.begin >= utterance.end:
                                        break
                                    if interval.begin >= utterance.begin:
                                        reference.append(interval)
                                    reference_interval_index += 1
                                text = " ".join(x.label for x in reference)
                                with torch.no_grad():
                                    output_timestep_duration = None
                                    path = os.path.join(tmpdir, f"sound_file.wav")
                                    torchaudio.save(
                                        path,
                                        torch.unsqueeze(
                                            torch.Tensor(kalpy_utterance.segment.load_audio()),
                                            0,
                                        ),
                                        16000,
                                    )
                                    hypotheses = model.transcribe(
                                        [path],
                                        return_hypotheses=True,
                                        verbose=False,
                                        batch_size=1,
                                    )
                                    # if hypotheses form a tuple (from Hybrid model), extract just "best" hypothesis
                                    if type(hypotheses) == tuple and len(hypotheses) == 2:
                                        hypotheses = hypotheses[0]

                                    for hypothesis in hypotheses:
                                        log_probs_list_batch = [hypothesis.y_sequence]
                                        T_list_batch = [hypothesis.y_sequence.shape[0]]
                                        pred_text_batch = [hypothesis.text]
                                        utt_obj = get_utt_obj(
                                            text,
                                            model,
                                            cfg.additional_segment_grouping_separator,
                                            T_list_batch[0],
                                            file.sound_file.sound_file_path,
                                            utterance.kaldi_id,
                                        )
                                    alignment_likelihood = float(hypothesis.score)
                                y_list_batch = [utt_obj.token_ids_with_blanks]
                                U_list_batch = [len(utt_obj.token_ids_with_blanks)]
                                utt_obj_batch = [utt_obj]
                                T_max = max(T_list_batch)
                                U_max = max(U_list_batch)
                                if hasattr(model, "tokenizer"):
                                    V = len(model.tokenizer.vocab) + 1
                                else:
                                    V = len(model.decoder.vocabulary) + 1
                                T_batch = torch.tensor(T_list_batch)
                                U_batch = torch.tensor(U_list_batch)
                                log_probs_batch = V_NEGATIVE_NUM * torch.ones((1, T_max, V))
                                for b, log_probs_utt in enumerate(log_probs_list_batch):
                                    t = log_probs_utt.shape[0]
                                    log_probs_batch[b, :t, :] = log_probs_utt
                                y_batch = V * torch.ones((1, U_max), dtype=torch.int64)
                                for b, y_utt in enumerate(y_list_batch):
                                    U_utt = U_batch[b]
                                    y_batch[b, :U_utt] = torch.tensor(y_utt)
                                # calculate output_timestep_duration if it is None
                                if output_timestep_duration is None:
                                    if not "window_stride" in model.cfg.preprocessor:
                                        raise ValueError(
                                            "Don't have attribute 'window_stride' in "
                                            "'model.cfg.preprocessor' => cannot calculate "
                                            " model_downsample_factor => stopping process"
                                        )

                                    if not "sample_rate" in model.cfg.preprocessor:
                                        raise ValueError(
                                            "Don't have attribute 'sample_rate' in "
                                            "'model.cfg.preprocessor' => cannot calculate start "
                                            " and end time of segments => stopping process"
                                        )

                                    audio_dur = utterance.duration
                                    n_input_frames = (
                                        audio_dur / model.cfg.preprocessor.window_stride
                                    )
                                    model_downsample_factor = round(
                                        n_input_frames / int(T_batch[0])
                                    )

                                    output_timestep_duration = (
                                        model.preprocessor.featurizer.hop_length
                                        * model_downsample_factor
                                        / model.cfg.preprocessor.sample_rate
                                    )
                                alignments_batch = viterbi_decoding(
                                    log_probs_batch,
                                    y_batch,
                                    T_batch,
                                    U_batch,
                                    viterbi_device,
                                )
                                utt_obj, alignment_utt = (
                                    utt_obj_batch[0],
                                    alignments_batch[0],
                                )

                                utt_obj = add_t_start_end_to_utt_obj(
                                    utt_obj, alignment_utt, output_timestep_duration
                                )
                                segment = [
                                    x
                                    for x in utt_obj.segments_and_tokens
                                    if isinstance(x, Segment)
                                ][0]
                                words = [
                                    x for x in segment.words_and_tokens if isinstance(x, Word)
                                ]
                                word_intervals = []
                                for word in words:
                                    character_intervals = []
                                    word_label = word.text
                                    for token in word.tokens:
                                        if token.text == "<b>":
                                            continue
                                        begin = token.t_start + utterance.begin
                                        end = token.t_end + utterance.begin
                                        if end > utterance.end:
                                            end = utterance.end
                                        label = token.text
                                        character_intervals.append(
                                            KalpyCtmInterval(begin, end, label, label)
                                        )
                                    word_intervals.append(
                                        WordCtmInterval(
                                            word_label, word_label, character_intervals
                                        )
                                    )
                                ctm = HierarchicalCtm(word_intervals)

                                frames_per_second = (
                                    log_probs_list_batch[0].size(0) / utterance.duration
                                )
                                file_ctm.word_intervals.extend(ctm.word_intervals)
                                try:
                                    alignment_score = align_words(reference, ctm.word_intervals)
                                except AssertionError:
                                    print(file.name)
                                    raise
                                    continue
                                words_per_second = len(reference) / utterance.duration

                                data = {
                                    "file": file.name,
                                    "begin": utterance.begin,
                                    "end": utterance.end,
                                    "duration": utterance.duration,
                                    "speaker": utterance.speaker_name,
                                    "normalized_text": utterance.normalized_text,
                                    "filtered_text": text,
                                    "alignment_score": alignment_score,
                                    "alignment_likelihood": float(alignment_likelihood),
                                    "word_count": len(ctm.word_intervals),
                                    "frames_per_second": frames_per_second,
                                    "words_per_second": words_per_second,
                                }
                                writer.writerow(data)
                                progress_bar.update(1)
                            file_ctm.export_textgrid(
                                output_path,
                                file_duration=file.duration,
                                output_format="short_textgrid",
                            )
        elif condition == "whisperx":
            try:
                import whisperx
            except ImportError:
                print("whisperx not installed, skipping")
                continue
            compute_type = "float16"
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = whisperx.load_model(
                "large-v2", device, compute_type=compute_type, language="en"
            )
            model_a, metadata = whisperx.load_align_model(language_code="en", device=device)

            with torch.inference_mode():
                for corpus, root in corpus_directories.items():
                    output_directory = os.path.join(root_dir, "alignments", condition, corpus)
                    if os.path.exists(output_directory):
                        continue
                    corpus = AcousticCorpus(corpus_directory=os.path.join(root, "benchmark"))
                    corpus.delete_database()
                    corpus._load_corpus()
                    os.makedirs(output_directory, exist_ok=True)
                    csv_path = os.path.join(output_directory, "word_alignment.csv")
                    with (
                        corpus.session() as session,
                        mfa_open(csv_path, "w") as f,
                        tqdm.tqdm(total=corpus.num_utterances) as progress_bar,
                    ):
                        writer = csv.DictWriter(f, fieldnames=csv_header)
                        writer.writeheader()
                        file_query = (
                            session.query(File)
                            .options(
                                sqlalchemy.orm.joinedload(File.sound_file, innerjoin=True),
                            )
                            .order_by(File.name)
                        )
                        for file in file_query:
                            file_ctm = HierarchicalCtm([])
                            if file.relative_path:
                                output_path = os.path.join(output_directory, file.relative_path)
                                os.makedirs(output_path, exist_ok=True)
                            else:
                                output_path = output_directory
                            output_path = os.path.join(output_path, file.name + ".TextGrid")
                            query = (
                                session.query(Utterance)
                                .filter(Utterance.file_id == file.id)
                                .options(
                                    sqlalchemy.orm.joinedload(
                                        Utterance.file, innerjoin=True
                                    ).joinedload(File.sound_file, innerjoin=True),
                                )
                                .order_by(Utterance.begin)
                            )
                            reference_path = os.path.join(root, "reference")
                            if file.relative_path:
                                reference_path = os.path.join(reference_path, file.relative_path)
                            reference_path = os.path.join(reference_path, file.name + ".TextGrid")
                            reference_word_intervals = parse_aligned_textgrid(reference_path)
                            reference_interval_index = 0
                            for utterance in query:
                                kalpy_utterance = utterance.to_kalpy()
                                reference = []
                                while True:
                                    try:
                                        interval = reference_word_intervals[
                                            reference_interval_index
                                        ]
                                    except IndexError:
                                        break
                                    if interval.begin >= utterance.end:
                                        break
                                    if interval.begin >= utterance.begin:
                                        reference.append(interval)
                                    reference_interval_index += 1
                                text = " ".join(x.label for x in reference)

                                audio = kalpy_utterance.segment.load_audio()

                                # transcribe_result = model.transcribe(audio, batch_size=1)
                                # print(result["segments"])
                                segments = [
                                    {
                                        "text": text,
                                        "start": 0.0,
                                        "end": utterance.duration,
                                    }
                                ]
                                result = whisperx.align(
                                    segments,
                                    model_a,
                                    metadata,
                                    audio,
                                    device,
                                    return_char_alignments=True,
                                )

                                word_intervals = []
                                words = result["segments"][0]["words"]
                                chars = result["segments"][0]["chars"]
                                character_index = 0
                                score_sum = 0
                                for word in words:
                                    character_intervals = []
                                    word_label = word["word"]
                                    while True:
                                        try:
                                            c = chars[character_index]
                                        except IndexError:
                                            break
                                        if c["char"] == " ":
                                            character_index += 1
                                            continue
                                        if c["start"] >= word["end"]:
                                            break
                                        begin = c["start"] + utterance.begin
                                        end = c["end"] + utterance.begin
                                        character_intervals.append(
                                            KalpyCtmInterval(begin, end, c["char"], c["char"])
                                        )
                                        character_index += 1
                                    word_intervals.append(
                                        WordCtmInterval(
                                            word_label, word_label, character_intervals
                                        )
                                    )
                                    score_sum += word["score"]
                                ctm = HierarchicalCtm(word_intervals)
                                alignment_likelihood = score_sum / len(words)
                                file_ctm.word_intervals.extend(ctm.word_intervals)
                                try:
                                    alignment_score = align_words(reference, ctm.word_intervals)
                                except AssertionError:
                                    print(file.name)
                                    raise
                                    continue
                                words_per_second = len(reference) / utterance.duration

                                data = {
                                    "file": file.name,
                                    "begin": utterance.begin,
                                    "end": utterance.end,
                                    "duration": utterance.duration,
                                    "speaker": utterance.speaker_name,
                                    "normalized_text": utterance.normalized_text,
                                    "filtered_text": text,
                                    "alignment_score": alignment_score,
                                    "alignment_likelihood": float(alignment_likelihood),
                                    "word_count": len(ctm.word_intervals),
                                    "frames_per_second": "NA",
                                    "words_per_second": words_per_second,
                                }
                                writer.writerow(data)
                                progress_bar.update(1)
                            file_ctm.export_textgrid(
                                output_path,
                                file_duration=file.duration,
                                output_format="short_textgrid",
                            )
        else:
            if not os.path.exists(model_path):
                continue
            for corpus, root in corpus_directories.items():
                output_directory = os.path.join(root_dir, "alignments", condition, corpus)
                csv_path = os.path.join(output_directory, "word_alignment.csv")
                if os.path.exists(csv_path):
                    continue
                command = [
                    "align",
                    os.path.join(root, "benchmark"),
                    dictionary_path,
                    model_path,
                    output_directory,
                    "-j",
                    "10",
                    "--clean",
                    "--debug",
                    "--use_mp",
                    "--use_cutoff_model",
                    "--use_postgres",
                    "--cleanup_textgrids",
                    "--beam",
                    "10",
                    "--retry_beam",
                    "40",
                ]
                print(command)
                mfa_cli(command, standalone_mode=False)
                corpus = AcousticCorpus(corpus_directory=os.path.join(root, "benchmark"))
                with (
                    corpus.session() as session,
                    mfa_open(csv_path, "w") as f,
                    tqdm.tqdm(total=corpus.num_utterances) as progress_bar,
                ):
                    writer = csv.DictWriter(f, fieldnames=csv_header)
                    writer.writeheader()
                    file_query = (
                        session.query(File)
                        .options(
                            sqlalchemy.orm.joinedload(File.sound_file, innerjoin=True),
                        )
                        .order_by(File.name)
                    )
                    for file in file_query:
                        query = (
                            session.query(Utterance)
                            .filter(Utterance.file_id == file.id)
                            .options(
                                sqlalchemy.orm.joinedload(
                                    Utterance.file, innerjoin=True
                                ).joinedload(File.sound_file, innerjoin=True),
                            )
                            .order_by(Utterance.begin)
                        )
                        reference_path = os.path.join(root, "reference")
                        if file.relative_path:
                            reference_path = os.path.join(reference_path, file.relative_path)
                        reference_path = os.path.join(reference_path, file.name + ".TextGrid")
                        reference_word_intervals = parse_aligned_textgrid(
                            reference_path, exclude_unknowns=True
                        )
                        reference_interval_index = 0
                        for utterance in query:
                            word_interval_query = (
                                session.query(WordInterval)
                                .join(WordInterval.word)
                                .filter(WordInterval.utterance_id == utterance.id)
                                .filter(Word.word.op("~")(r"^[^\[<{(]"))
                                .options(
                                    sqlalchemy.orm.joinedload(WordInterval.word, innerjoin=True),
                                )
                                .order_by(WordInterval.begin)
                            )
                            reference = []
                            while True:
                                try:
                                    interval = reference_word_intervals[reference_interval_index]
                                except IndexError:
                                    break
                                if interval.begin >= utterance.end:
                                    break
                                if interval.begin >= utterance.begin:
                                    reference.append(interval)
                                reference_interval_index += 1
                            word_intervals = []
                            reference_index = 0
                            for i, wi in enumerate(word_interval_query):
                                if reference[reference_index].label == wi.word.word:
                                    word_intervals.append(wi.as_ctm())
                                    reference_index += 1
                                elif (
                                    word_intervals
                                    and reference[reference_index].label
                                    == word_intervals[-1].label + wi.word.word
                                ):
                                    word_intervals[-1].label += wi.word.word
                                    word_intervals[-1].end = wi.end
                                    reference_index += 1
                                elif (
                                    word_intervals
                                    and word_intervals[-1].label + "-" + wi.word.word
                                    in reference[reference_index].label
                                ):
                                    word_intervals[-1].label += "-" + wi.word.word
                                    word_intervals[-1].end = wi.end
                                    if (
                                        word_intervals[-1].label
                                        == reference[reference_index].label
                                    ):
                                        reference_index += 1
                                else:
                                    word_intervals.append(wi.as_ctm())
                            if not word_intervals:
                                continue
                            word_index = 0
                            alignment_score = align_words(reference, word_intervals)
                            words_per_second = len(reference) / utterance.duration
                            data = {
                                "file": file.name,
                                "begin": utterance.begin,
                                "end": utterance.end,
                                "duration": utterance.duration,
                                "speaker": utterance.speaker_name,
                                "normalized_text": utterance.normalized_text,
                                "filtered_text": " ".join(x.label for x in word_intervals),
                                "alignment_score": alignment_score,
                                "alignment_likelihood": utterance.alignment_log_likelihood,
                                "word_count": len(word_intervals),
                                "frames_per_second": 100,
                                "words_per_second": words_per_second,
                            }
                            writer.writerow(data)
                            progress_bar.update(1)
