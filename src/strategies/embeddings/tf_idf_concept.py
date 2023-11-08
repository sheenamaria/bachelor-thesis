from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer

def _tf_idf_embedding_strategy(vectorizer, text):
    tf_idf_text_vector = vectorizer.transform([text]).toarray()[0]
    return tf_idf_text_vector

def _create_strategy(corpus_provider):
    vectorizer = None

    def create_embedding(text):
        nonlocal vectorizer
        if not vectorizer:
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(corpus_provider())
            shape = X.shape
            feature_names = vectorizer.get_feature_names_out()

        return _tf_idf_embedding_strategy(vectorizer, text)
    return create_embedding

def _calculate_cosine_similarity(embedding1, embedding2):
    similarity = dot(embedding1, embedding2)/(norm(embedding1)*norm(embedding2))
    return similarity


# corpus_providers: {java_corpus: ICorpusProvider, java_subword_corpus: ICorpusProvider}
def create_tf_idf_concept_2(corpus_providers):
    strategies = []
    strategies.append({
        "id" : "corpus_default",
        "create_embedding" : _create_strategy(corpus_providers["java_standard_corpus"])
    })
    strategies.append({
        "id" : "corpus_splitted_subwords",
        "create_embedding" : _create_strategy(corpus_providers["java_subword_corpus"])
    })
    return {
        "id" : "tf_idf",
        "strategies": strategies,
        "calculate_similarity" : _calculate_cosine_similarity
    }