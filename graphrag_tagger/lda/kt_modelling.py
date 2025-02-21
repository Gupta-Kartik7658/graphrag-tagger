from typing import List

from ktrain.text import get_topic_model


class KtrainTopicExtractor:
    """
    Topic extractor using ktrain's topic modeling capabilities.

    This class leverages ktrain's `get_topic_model` to build and utilize
    Latent Dirichlet Allocation (LDA) models for topic extraction from text data.
    """

    def __init__(
        self,
        n_components: int = None,
        n_features: int = 512,
        min_df: int = 2,
        max_df: float = 0.95,
        threshold: float = 0.25,
    ):
        """
        Initialize the TopicExtractor with parameters for ktrain's topic model.

        Parameters:
            n_features (int): Maximum number of features (words) to consider in the vocabulary.
                Limits the vocabulary size based on term frequency. Defaults to 512.
            min_df (int): Minimum document frequency for a word to be included in the vocabulary.
                Words appearing in fewer than `min_df` documents are discarded. Defaults to 2.
            max_df (float): Maximum document frequency for a word to be included in the vocabulary.
                Words appearing in more than `max_df` proportion of documents are discarded. Defaults to 0.95.
            threshold (float): Threshold value for filtering words in the topic model building process.
                Words with a document frequency below this threshold are filtered out during model building in `ktrain`.
                Defaults to 0.25.
        """
        self.n_features = n_features
        self.min_df = min_df
        self.max_df = max_df
        self.threshold = threshold
        self.n_components = n_components
        self.topic_model = None  # To store the ktrain topic model instance

    def fit(self, texts: List[str]):
        """
        Build the topic model using the provided list of texts.

        This method initializes and builds the topic model using ktrain's `get_topic_model`
        and `build` methods. It preprocesses the texts and trains the LDA model.

        Parameters:
            texts (List[str]): A list of strings, where each string is a document.

        Returns:
            self: Returns the instance itself to allow for method chaining.

        Raises:
            ValueError: If the input `texts` list is empty.
        """
        if not texts:
            raise ValueError("Input 'texts' list cannot be empty.")

        self.topic_model = get_topic_model(
            texts,
            n_features=self.n_features,
            min_df=self.min_df,
            max_df=self.max_df,
            n_topics=self.n_components,
        )
        self.topic_model.build(texts, threshold=self.threshold)
        return self

    def get_topics(self) -> List[str]:
        """
        Retrieve the topics generated by the LDA model.

        This method extracts the learned topics from the fitted LDA model.
        Each topic is represented as a string of space-separated top words.

        Returns:
            List[str]: A list of topic strings.

        Raises:
            ValueError: If the topic model has not been built yet (i.e., `fit()` has not been called).
        """
        if self.topic_model is None:
            raise ValueError("Topic model not built. Call fit() first.")
        topics = self.topic_model.get_topics()
        return topics

    def filter_texts(self, texts: List[str]) -> List[str]:
        """
        Optionally filter texts using the topic model.

        This method allows for filtering input texts based on criteria defined within the ktrain topic model
        (although the specific filtering mechanism in `ktrain.TopicModel.filter` is not LDA-topic based but rather based on document frequency).
        For LDA topic-based filtering, you would typically use topic probabilities from `transform`.

        Parameters:
            texts (List[str]): A list of strings to be filtered.

        Returns:
            List[str]: A list of filtered text strings, as determined by ktrain's `filter` method.

        Raises:
            ValueError: If the topic model has not been built yet (i.e., `fit()` has not been called).
        """
        if self.topic_model is None:
            raise ValueError("Topic model not built. Call fit() first.")
        return self.topic_model.filter(texts)

    def transform(self, texts: List[str], threshold: float = 0.25) -> List[List[float]]:
        """
        Transform texts into the topic space, obtaining topic distributions for each text.

        This method predicts the topic distribution for each document in the input `texts`.
        Each document is represented as a list of probabilities, where each probability corresponds to a topic.

        Parameters:
            texts (List[str]): A list of document texts to transform.
            threshold (float, optional): Probability threshold.
                Topics with probabilities below this threshold in a document's distribution are effectively considered absent (set to 0 in ktrain's predict method).
                Defaults to 0.25.

        Returns:
            List[List[float]]: A list of topic distributions. Each inner list represents a document
                                and contains probabilities for each topic. Shape: (n_samples, n_topics).

        Raises:
            ValueError: If the topic model has not been built yet (i.e., `fit()` has not been called).
        """
        if self.topic_model is None:
            raise ValueError("Topic model not built. Call fit() first.")
        if not texts:
            raise ValueError("Input 'texts' list cannot be empty.")
        return self.topic_model.predict(texts, threshold=threshold)


# ----- Example usage -----
if __name__ == "__main__":
    from sklearn.datasets import fetch_20newsgroups

    # Sample texts from 20 newsgroups dataset
    remove_categories = ("headers", "footers", "quotes")
    newsgroups_test = fetch_20newsgroups(subset="test", remove=remove_categories)
    texts: List[str] = newsgroups_test.data

    # Initialize and fit the topic extractor.
    extractor = KtrainTopicExtractor()
    extractor.fit(texts)

    # Retrieve the extracted topics.
    extracted_topics = extractor.get_topics()
    print("Topics from LDA:")
    for topic in extracted_topics:
        print("-", topic)
