from datasets import load_dataset
import pandas as pd
from dataclasses import dataclass, asdict
from typing import List


@dataclass(frozen=True)
class Entity:
    text: str
    type: str
    span_start: int
    span_end: int


@dataclass(frozen=True)
class ConvertedExample:
    sentence: str
    entities: List[Entity]


def convert_entities(tokens: List[str], ner_tags: List[int], sentence: str, entity_type_mapping: dict) -> List[Entity]:
    """
        Converts the entities in a sentence based format.

    Arguments:
        :param tokens: List of tokens in the sentence.
        :param ner_tags: List of entity tags corresponding to each token.
        :param sentence: The sentence text.
        :param entity_type_mapping : Mapping of entity tag IDs to entity types.

    Returns:
        :returns List[Entity]: List of converted entities in the sentence.

    """

    entities = []
    prev_entity = None
    token_start = 0

    for i in range(len(tokens)):
        token = tokens[i]
        ner_tag = ner_tags[i]
        if ner_tag != 'O' and ner_tag != 0:
            entity_type = entity_type_mapping[ner_tag]

            if prev_entity is not None and entity_type == prev_entity.type:
                prev_entity = Entity(
                    text=prev_entity.text + " " + token,
                    type=entity_type,
                    span_start=prev_entity.span_start,
                    span_end=sentence.index(token, prev_entity.span_start) + len(token)
                )
                entities[-1] = prev_entity
            else:
                entity = Entity(
                    text=token,
                    type=entity_type,
                    span_start=sentence.index(token, token_start),
                    span_end=sentence.index(token, token_start) + len(token)
                )
                entities.append(entity)
                prev_entity = entity
                token_start = entity.span_end + 1
        else:
            prev_entity = None
    return entities


def convert_ontonotes_dataset(dataset) -> List[ConvertedExample]:
    """
        Converting ontonotes dataset to our scheme format.
    Arguments:
        :param dataset: ontonotes dataset.
    Returns:
        :returns List[ConvertedExample]: List of converted examples.

    """
    entity_types = {
        0: 'O',
        1: 'CARDINAL',
        2: 'DATE',
        3: 'DATE',
        4: 'PERSON',
        5: 'PERSON',
        6: 'NORP',
        7: 'GPE',
        8: 'GPE',
        9: 'LAW',
        10: 'LAW',
        11: 'ORG',
        12: 'ORG',
        13: 'PERCENT',
        14: 'PERCENT',
        15: 'ORDINAL',
        16: 'MONEY',
        17: 'MONEY',
        18: 'WORK_OF_ART',
        19: 'WORK_OF_ART',
        20: 'FAC',
        21: 'TIME',
        22: 'CARDINAL',
        23: 'LOC',
        24: 'QUANTITY',
        25: 'QUANTITY',
        26: 'NORP',
        27: 'LOC',
        28: 'PRODUCT',
        29: 'TIME',
        30: 'EVENT',
        31: 'EVENT',
        32: 'FAC',
        33: 'LANGUAGE',
        34: 'PRODUCT',
        35: 'ORDINAL',
        36: 'LANGUAGE'
    }

    converted_dataset = []

    for example in dataset:
        tokens = example['tokens']
        tags = example['tags']
        sentence = ""
        for token in tokens:
            if sentence and not token.startswith(("'", ",", "!", ".", "?", "%")):
                sentence += " "
            sentence += token

        entities = convert_entities(tokens, tags, sentence, entity_types)
        converted_example = ConvertedExample(sentence=sentence, entities=entities)
        converted_dataset.append(converted_example)

    return converted_dataset


def main():
    # Load the ontonotes dataset (in this case, the test split)
    ontonotes_dataset = load_dataset("tner/ontonotes5", split="test")

    # Convert the dataset using the defined function
    converted_ontonotes_dataset = convert_ontonotes_dataset(ontonotes_dataset)
    output_path = "./converted_ontonotes_dataset.parquet"
    df = pd.DataFrame([asdict(example) for example in converted_ontonotes_dataset])
    df.to_parquet(output_path)

    print("Conversion completed and saved to:", output_path)


if __name__ == '__main__':
    main()
