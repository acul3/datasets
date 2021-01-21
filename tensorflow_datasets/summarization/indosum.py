# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""SQUAD: The Stanford Question Answering Dataset."""

import json
import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """\
@article{2016arXiv160605250R,
       author = {{Rajpurkar}, Pranav and {Zhang}, Jian and {Lopyrev},
                 Konstantin and {Liang}, Percy},
        title = "{SQuAD: 100,000+ Questions for Machine Comprehension of Text}",
      journal = {arXiv e-prints},
         year = 2016,
          eid = {arXiv:1606.05250},
        pages = {arXiv:1606.05250},
archivePrefix = {arXiv},
       eprint = {1606.05250},
}
"""

_DESCRIPTION = """\
Stanford Question Answering Dataset (SQuAD) is a reading comprehension \
dataset, consisting of questions posed by crowdworkers on a set of Wikipedia \
articles, where the answer to every question is a segment of text, or span, \
from the corresponding reading passage, or the question might be unanswerable.
"""

_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/"
_HOMEPAGE_URL = "https://rajpurkar.github.io/SQuAD-explorer/"


_V2_FEATURES = tfds.features.FeaturesDict({
    "id":
        tf.string,
    "paragraph":
        tfds.features.Text(),
    "summary":
        tfds.features.Text(),
})


def _generate_v2_examples(filepath):
  """Returns v2 examples."""
  _id = 0
  with tf.io.gfile.GFile(filepath) as f:
    idsum = json.load(f)
    for article in idsum["data"]:
      yield _id,{
          "id":str(_id),
          "paragraph": article["paragraph"],
          "summary": article["summary"],
      }
      _id += 1


class IdSumConfig(tfds.core.BuilderConfig):
  """BuilderConfig for SQUAD."""

  def __init__(self, *, train_file, dev_file, **kwargs):

    super(IdSumConfig, self).__init__(version="2.0.0", **kwargs)
    self.train_file = train_file
    self.dev_file = dev_file


class IdSum(tfds.core.GeneratorBasedBuilder):
  """SQUAD: The Stanford Question Answering Dataset."""

  BUILDER_CONFIGS = [
      IdSumConfig(
          name="v2.0",
          description="Version 2.0.0 of SQUAD",
          train_file="train-sum.json",
          dev_file="train-sum-dev.json",
      ),
  ]

  def _info(self):

    if self.builder_config.name == "v2.0":
      features_dict = _V2_FEATURES
    else:
      raise AssertionError("Dataset version should be either 1.1 or 2.0")

    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=features_dict,
        # No default supervised_keys (as we have to pass both question
        # and context as input).
        supervised_keys=None,
        homepage=_HOMEPAGE_URL,
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    urls_to_download = {
        "train": "https://github.com/acul3/Indosum_dataset/raw/main/train-sum.json",
        "dev": "https://github.com/acul3/Indosum_dataset/raw/main/train-sum-dev.json"
    }
    downloaded_files = dl_manager.download_and_extract(urls_to_download)

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"filepath": downloaded_files["train"]}),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={"filepath": downloaded_files["dev"]}),
    ]

  def _generate_examples(self, filepath):

    return _generate_v2_examples(filepath)
