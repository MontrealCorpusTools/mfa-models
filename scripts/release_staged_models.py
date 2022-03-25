import collections
import json
import os
import random
import shutil
import re
import typing
from datetime import datetime
import requests
import numpy as np
import montreal_forced_aligner.utils
from montreal_forced_aligner.models import MODEL_TYPES, ModelManager, ModelRelease
from montreal_forced_aligner.dictionary.pronunciation import PronunciationDictionary
from montreal_forced_aligner.data import voiced_variants, voiceless_variants, PhoneSetType

mfa_model_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPDATE = False

with open(os.path.join(mfa_model_root, 'scripts', 'token'), 'r') as f:
    token = f.read()

tag_template = "{model_type}-{model_name}-v{version}"

manager = ModelManager()
manager.refresh_remote()
model_type_names ={
    'acoustic': 'Acoustic models',
    'dictionary': 'Pronunciation dictionaries',
    'g2p': 'G2P models',
    'language_model': 'Language models',
    'corpus': 'Corpora',
}

print(manager.remote_models)

base_dict_template = 'https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/{language}/{phone_set}/{version}/{model_name}.dict'

acoustic_mfas = set()

for model_type, model_class in MODEL_TYPES.items():
    if model_type == 'ivector':
        continue
    model_directory = os.path.join(mfa_model_root, model_type)
    staging_directory = os.path.join(model_directory, 'staging')
    languages = os.listdir(model_directory)
    for lang in languages:
        if lang == 'staging':
            continue
        lang_dir = os.path.join(model_directory, lang)
        if not os.path.isdir(lang_dir):
            continue
        for phone_set in os.listdir(lang_dir):
            phone_set_dir = os.path.join(lang_dir, phone_set)
            if not os.path.isdir(phone_set_dir):
                continue
            versions = os.listdir(phone_set_dir)
            for v in versions:
                version_dir = os.path.join(phone_set_dir, v)
                with open(os.path.join(version_dir, 'meta.json'), 'r', encoding='utf8') as f:
                    meta = json.load(f)
                    model_name = meta['name']
                    version = meta['version']
                with open(os.path.join(version_dir, 'README.md'), 'r', encoding='utf8') as f:
                    readme = f.read()
                tag = tag_template.format(model_type=model_type, model_name=model_name, version=version)
                if 'mfa' in tag and model_type == 'acoustic':
                    acoustic_mfas.add(lang)
                elif 'mfa' in tag and lang not in acoustic_mfas:
                    continue
                if ('mfa' in tag or 'arpa' in tag) and model_type == 'dictionary':
                    dict_url = base_dict_template.format(language=lang,phone_set=phone_set, version=v, model_name=model_name)
                    readme = readme.replace('\n\n## Installation', f'\n- The dictionary downloadable from this release has trained pronunciation and silence probabilities. The base dictionary is available [here]({dict_url})\n\n##Installation')
                existing_releases= manager.remote_models[model_type]
                if model_name in existing_releases:
                    existing = existing_releases[model_name]
                    if existing.version.replace('v', '') == version:
                        if UPDATE:
                            r = requests.patch(existing.release_link, json={'body': readme})
                        continue
                release = ModelRelease(model_name,tag, version, '','')
                if model_type == 'dictionary':
                    ext = '.dict'
                    content_type = 'text/tab-separated-values'
                else:
                    ext = '.zip'
                    content_type = 'application/zip'
                model_path = os.path.join(staging_directory, model_name + ext)
                print(tag, len(readme))
                print(tag)
                r = requests.post(manager.base_url, json={"tag_name": tag, "name": f"{model_name} v{version}",
                                                          'body': readme,
                                                          "target_commitish": "main",
                                                          "draft": False, "prerelease": False,
                                  "generate_release_notes": False},
                                  headers={'Accept': "application/vnd.github.v3+json",
                                                            'Authorization': f"token {token}"})
                d = r.json()
                print(d)
                with open(model_path, 'rb') as f:
                    data = f.read()
                    r2 = requests.post(d['upload_url'].replace('{?name,label}',''), data=data, params={'name':os.path.basename(model_path)}, headers={"Content-Type": "application/zip",
                                                                 'Accept': "application/vnd.github.v3+json",
                                                                'Authorization': f"token {token}"})
                    print(r2.json())
                print(meta)
                print(tag)
