from setuptools import setup, find_namespace_packages
import os

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

# Read README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gpt-sovits',
    version="0.1.0",
    description='GPT-SoVITS text-to-speech synthesis system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='X-T-E-R',
    author_email='',  # Add if available
    url='https://github.com/X-T-E-R/GPT-SoVITS-Inference',
    packages=find_namespace_packages(include=['gpt_sovits*']),
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'gpt_sovits': [
            'src/common_config.json',
            'Synthesizers/gsv_fast/gsv_config.json',
            'GPT_SoVITS/configs/*.yaml',
            'GPT_SoVITS/configs/*.json',
            'GPT_SoVITS/pretrained_models/*',
            'GPT_SoVITS/text/*.rep',
            'GPT_SoVITS/text/*.pickle',
            'GPT_SoVITS/text/*.txt',
            'Synthesizers/gsv_fast/configs/*.json',
            'Synthesizers/gsv_fast/ui_config.json',  # Add the specific ui_config.json
            'Synthesizers/base/*.py',
            'Synthesizers/*/configs/*.json',  # Include all json files in any synthesizer's configs directory
            'Synthesizers/*/configs/i18n/locale/*.json'
        ],
    },
    entry_points={
        'console_scripts': [
            'gpt-sovits=app:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
    ],
    python_requires='>=3.8',
)