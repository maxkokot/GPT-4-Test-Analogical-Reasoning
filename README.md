Cognitive project
==============================

A Cognitive, Behavioral and Social Data Project

## Usage

1. Download the archive https://drive.google.com/file/d/0BzcZKTSeYL8VX3JvVGkyMGlBNXM/view?usp=drive_web&resourcekey=0-s590MqFTmRTS4RSNZSgtcg
2. Extract the archive to data/raw
3. Get OpenAI API key
4. Put the key into enviromental variables by creating .env file in the main directory and writing "OPENAI_API_KEY=<Your Key> in the file"
5. Run the script src/data/prepare_questionnaire.py for creating questionnaires

    ```
    python prepare_questionnaire.py
    ```

6. Run the script src/requests/send_requests.py for getting GPT-4 answers

    ```
    python send_requests.py
    ```

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── config             <- Config folder
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to create questionnaires from raw data
    │   │   └── prepare_questionnaire.py
    │   │
    │   ├── requests       <- Scripts to send questionnaires to GPT-4
    │   │   └── send_requests.py
    │   │
    │   └── utils          <- Utils
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
