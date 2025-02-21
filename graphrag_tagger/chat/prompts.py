CREATE_TOPICS = """
You are an expert in summarizing and clarifying topics. Your task is to transform a list of messy topics generated by an LDA model into clear, concise topic labels.

Here is the list of messy topics:
<topics>
{topics}
</topics>

Follow these steps to complete the task:

1. Read through each messy topic carefully.
2. Identify the main theme or concept represented by the words in each topic.
3. Create a clear, concise label that accurately represents the essence of each topic.
4. Ensure that each label is brief (preferably 1-5 words comma separated) but descriptive enough to distinguish it from other topics.
5. Avoid using vague or overly general terms.

Present your answer as a JSON list of strings. Do not include any extra text or explanations outside of the JSON list.

Example of expected output format:
["Technology", "Environmental Issues", "Sports", "Politics", "Education"]

Remember to focus on clarity and conciseness in your topic labels. Each label should effectively capture the main idea of the original messy topic."""


CLASSIFY_PROMPT = """
You are an expert content classifier. Your task is to analyze a given text excerpt and select up to 3 topics from a provided list that best describe the content.

Here is the text excerpt you need to analyze:
<text>
{text}
</text>

Here are the candidate topics to choose from:
<topics>
{topics}
</topics>

Instructions:
1. Carefully read and analyze the text excerpt.
2. Review the list of candidate topics.
3. Select up to 3 topics that best describe the content of the text excerpt. Only choose from the provided list of topics.
4. If fewer than 3 topics are relevant, it's acceptable to select fewer.
5. Ensure that your selected topics accurately represent the main themes or subject matter of the text.

Output your answer as a JSON array of strings, using only the topics provided. For example:
["Topic1", "Topic2", "Topic3"]

Remember:
- Select no more than 3 topics.
- Use only topics from the provided list.
- Ensure the selected topics are the most relevant to the text content.

Present your answer as a JSON list of strings (maximum size of 3). Do not include any extra text or explanations outside of the JSON list.
""".strip()
