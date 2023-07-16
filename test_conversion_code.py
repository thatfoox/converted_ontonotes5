import pytest
from conversion_code import convert_ontonotes_dataset

def test_convert_ontonotes_dataset():
    dataset = [
        {'tokens': ['In', 'the', 'seven', 'Supreme', 'Court', 'terms', 'from', 'the', 'fall', 'of', '1962', 'through',
                    'the', 'spring', 'of', '1967', ',', 'the', 'height', 'of', 'the', 'Warren', 'Court', "'s", 'power',
                    ',', 'Justice', 'Brennan', 'cast', 'only', '25', 'dissenting', 'votes', 'in', '555', 'cases',
                    'decided', 'by', 'the', 'court', '.'],
         'tags': [0, 0, 1, 11, 12, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 1, 22, 0, 0,
                  0, 1, 0, 0, 0, 0, 0, 0]}
    ]

    converted_dataset = convert_ontonotes_dataset(dataset)

    assert len(converted_dataset) == 1

    example = converted_dataset[0]

    assert example.sentence == "In the seven Supreme Court terms from the fall of 1962 through the spring of 1967," \
                               " the height of the Warren Court's power, Justice Brennan cast only 25 dissenting" \
                               " votes in 555 cases decided by the court."

    entities = example.entities
    assert len(entities) == 7

    entity1 = entities[0]
    assert entity1.text == example.sentence[7:12]
    assert entity1.type == 'CARDINAL'
    assert entity1.span_start == 7
    assert entity1.span_end == 12

    entity2 = entities[1]
    assert entity2.text == example.sentence[13:26]
    assert entity2.type == 'ORG'
    assert entity2.span_start == 13
    assert entity2.span_end == 26

    entity3 = entities[2]
    assert entity3.text == example.sentence[33:81]
    assert entity3.type == 'DATE'
    assert entity3.span_start == 33
    assert entity3.span_end == 81

    entity4 = entities[3]
    assert entity4.text == example.sentence[101:107]
    assert entity4.type == 'PERSON'
    assert entity4.span_start == 101
    assert entity4.span_end == 107

    entity5 = entities[4]
    assert entity5.text == example.sentence[131:138]
    assert entity5.type == 'PERSON'
    assert entity5.span_start == 131
    assert entity5.span_end == 138

    entity6 = entities[5]
    assert entity6.text == example.sentence[144:151]
    assert entity6.type == 'CARDINAL'
    assert entity6.span_start == 144
    assert entity6.span_end == 151

    entity7 = entities[6]
    assert entity7.text == example.sentence[172:175]
    assert entity7.type == 'CARDINAL'
    assert entity7.span_start == 172
    assert entity7.span_end == 175


if __name__ == '__main__':
    pytest.main()
