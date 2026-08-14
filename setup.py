# Copyright 2025 Pixagan Technologies
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

from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="doqlets",
    version="0.1.0", 
    author="Anil Variyar",
    author_email="pixagan@gmail.com",
    description="Doqlets is an LLM powered Agentic Knowledge Base",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/pixagan/doqlets",
    packages=find_packages(),
    install_requires=[
        "laeyerz",
        "chromadb",
        "python-dotenv",
        'uuid',
        "pymongo",
        "bson",
        "datetime",
        "openai",
        "fitz"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="ai agents workflow rag llm graph",
    license="Apache License 2.0",
    python_requires=">=3.8",  # Minimum Python version required
    project_urls={
    "Source": "https://github.com/pixagan/doqlets",
    "Documentation": "https://pixagan.ai/doqlets",
}
)
