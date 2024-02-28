Testing analogical reasoning capability of GPT-4
==============================

The final project created for Optimization for Cognitive, Behavioral and Social Data course.

This project explores the application of GPT-4 to analogical reasoning problems. It builds upon a foundational article (https://aclanthology.org/S12-1047/) that evaluates semantic relational similarity by measuring the prototypicality of word pairs within specific semantic relation classes. The primary objective is to assess GPT-4's effectiveness in this domain and to compare its performance with the results presented in the original study \cite{ref1}.

## Contributors

Kokot Maksim, Mikhail Kolobov, Yelnur Shauketbek

UNIPD, 2024


## Usage

1. Download the archive and unzip it into `data/raw` directory

    ```
    !wget -O data/raw/files.zip "https://drive.usercontent.google.com/u/0/uc?id=0BzcZKTSeYL8VX3JvVGkyMGlBNXM&export=download&resourcekey=0-s590MqFTmRTS4RSNZSgtcg"
    !unzip data/raw/files.zip  -d data/raw/
    !rm data/raw/files.zip
    ```

2. Make sure you have an access to GPT-4
3. Get OpenAI API key
4. Put the key into enviromental variables by creating `.env` file in the main directory and writing `OPENAI_API_KEY=<Your Key>` in the file
5. Run the script `src/ask_gpt_4.py` for forming the questions and sending them to GPT-4.

    ```
    python ask_gpt_4.py
    ```

6. Run the script `src/evaluate_answers.py` for evaluating GPT-4 answers

    ```
    python evaluate_answers.py
    ```

Project Organization
------------

    ├── LICENSE
    ├── Makefile                        <- Makefile with commands like `make data` or `make train`
    ├── README.md                       <- The top-level README for developers using this project.
    ├── config                          <- Config folder
    ├── data
    │   ├── external                    <- Data for the report.
    │   ├── interim                     <- Answers obtained from GPT-4.
    │   ├── processed                   <- Prepared questions to GPT-4.
    │   └── raw                         <- Data provided by authors of original study.
    │
    ├── docs                            <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── notebooks                       <- Jupyter notebooks. Naming convention is a number (for ordering),
    │   │                                  the creator's initials, and a short `-` delimited description, e.g.
    │   │                                 `1.0-jqp-initial-data-exploration`.
    │   ├── Ask GPT-4.ipynb             <- Notebook for forming the questions and sending them to GPT-4.
    │   └── Evaluate Answers.ipynb      <- Notebook for evaluating GPT-4 answers
    │
    ├── reports                         <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── BCSD_project.pdf            <- The project's report file
    │
    ├── requirements.txt                <- The requirements file for reproducing the analysis environment, e.g.
    │                                      generated with `pip freeze > requirements.txt`
    │
    ├── setup.py                        <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                             <- Source code for use in this project.
    │   ├── __init__.py                 <- Makes src a Python module
    │   ├── ask_gpt_4.py                <- Script for forming the questions and sending them to GPT-4.
    │   ├── evaluate_answers.py         <- Script for for evaluating GPT-4 answers.
    │   │
    │   ├── data                        <- Functions to manipulate the question data
    │   │   └── data.py
    │   │
    │   └──evaluation                  <- Functions for evaluating the answers
    │       ├── maxdiff.py
    │       └── spearman.py
    │
    │
    └── tox.ini                         <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
