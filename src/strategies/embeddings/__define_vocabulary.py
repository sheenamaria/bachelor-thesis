import re

from src.github.defs import RepositoryIdentifier
from src.store.mdb_store import db
from src.tasks.pipeline_context import PipelineContext


def get_corpus_standard_with_numbers(context: PipelineContext):
    corpus = []
    change_text_resources = db.find_resources(
        context.create_resource_criteria(
            {
                "kind": "change",
            }
        )
    )
    pr_resources = get_pull_request_titles(context)
    for change_text_resource in change_text_resources:
        change_text = db.get_resource_content(change_text_resource)["code"]["text"]
        corpus.append(change_text)
    for pr_resource in pr_resources:
        corpus.append(pr_resource)
    return corpus


def get_corpus_standard_without_numbers(context: PipelineContext):
    corpus = []
    change_text_resources = db.find_resources(
        context.create_resource_criteria(
            {
                "kind": "change",
            }
        )
    )
    pr_resources = get_pull_request_titles(context)
    for change_text_resource in change_text_resources:
        change_text = db.get_resource_content(change_text_resource)["code"]["text"]
        corpus.append(change_text)
    for pr_resource in pr_resources:
        corpus.append(pr_resource)
    return remove_numbers(corpus)


def get_corpus_subword_with_numbers(context: PipelineContext):
    corpus = []
    change_text_resources = db.find_resources(
        context.create_resource_criteria(
            {
                "kind": "change",
            }
        )
    )
    pr_resources = get_pull_request_titles(context)
    for change_text_resource in change_text_resources:
        change_text = db.get_resource_content(change_text_resource)["code"]["text"]
        change_text_subword_split = subword_splitter(change_text)
        corpus.append(change_text_subword_split)
    for pr_resource in pr_resources:
        pr_subword_split = subword_splitter(pr_resource)
        corpus.append(pr_subword_split)
    return corpus


def get_corpus_subword_without_numbers(context: PipelineContext):
    corpus = []
    change_text_resources = db.find_resources(
        context.create_resource_criteria(
            {
                "kind": "change",
            }
        )
    )
    pr_resources = get_pull_request_titles()
    for change_text_resource in change_text_resources:
        change_text = db.get_resource_content(change_text_resource)["code"]["text"]
        change_text_subword_split = subword_splitter(change_text)
        corpus.append(change_text_subword_split)
    for pr_resource in pr_resources:
        pr_subword_split = subword_splitter(pr_resource)
        corpus.append(pr_subword_split)
    return remove_numbers(corpus)


def corpus_standard_with_numbers_provider(context: PipelineContext):
    corpus = None

    def create_corpus():
        nonlocal corpus
        if not corpus:
            corpus = get_corpus_standard_with_numbers(context)
        return corpus

    return create_corpus


def corpus_standard_without_numbers_provider(context: PipelineContext):
    corpus = None

    def create_corpus():
        nonlocal corpus
        if not corpus:
            corpus = get_corpus_standard_without_numbers(context)
        return corpus

    return create_corpus


def corpus_subword_with_numbers_provider(context: PipelineContext):
    corpus = None

    def create_corpus():
        nonlocal corpus
        if not corpus:
            corpus = get_corpus_subword_with_numbers(context)
        return corpus

    return create_corpus


def corpus_subword_without_numbers_provider(context: PipelineContext):
    corpus = None

    def create_corpus():
        nonlocal corpus
        if not corpus:
            corpus = get_corpus_subword_without_numbers(context)
        return corpus

    return create_corpus


# TODO move function
def get_pull_request_titles(context: PipelineContext):
    pull_request_titles = []
    commits = db.find_commits(context.create_commit_criteria())
    for commit in commits:
        pull_request_titles.append(commit["pull_request_title"])
        if commit.get("pull_request_text"):
            pull_request_titles.append(commit.get("pull_request_text"))

    return pull_request_titles


def subword_splitter(input_string):
    words = re.findall(r"[A-Za-z]+", input_string)
    transformed_words = []
    for word in words:
        separators = ["_", "-"]
        for separator in separators:
            if separator in word:
                subwords = word.split(separator)
                transformed_words.extend(subwords)
                break
        else:
            subwords = re.findall(r"[a-z]+|[A-Z][a-z]*", word)
            transformed_words.extend(subwords)
    output_string = " ".join(transformed_words)
    return output_string


def remove_numbers(documents):
    pattern = r"\d+"
    regex = re.compile(pattern)
    cleaned_documents = []
    for document in documents:
        cleaned_document = regex.sub("", document)
        cleaned_documents.append(cleaned_document)
    return cleaned_documents
