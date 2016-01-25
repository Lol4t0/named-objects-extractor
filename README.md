# Named objects extractor

Extracts people names, organization titles and geo object names from text

## Features

* Extracts people names, organization titles and geo object names from text
* Constructs names from multiple adjucent name parts    
  So _Steve Jobs_ will be the one name (_Steve Jobs_) and not two names (_Steve_ and _Jobs_)
* Join simmilar names, that are found more than once in the text, into the single object using some smart approach
* Provide normalized name, original tokens and places in text where tokens were found

This project uses `pymorphy2` as NLP-processor.

## Try it
```
pip install git+https://github.com/Lol4t0/named-objects-extractor.git
python -um named_objects_extractor some_article.txt | jq .
```

## API referance

* `named_objects_extractor.extract_objects(text)`   
  Returns objects dict from the given text

* `named_objects_extractor.ObjectExtractor(score_threshold=0.51)`   
  Constrcuts reusable object extractor. Loads model on constrcution

* `named_objects_extractor.ObjectExtractor.extract(text)`   
  Returns objects dict from the given text

## Extraction data format

```
{
    <object-type> :: person | organization | place : [
        {
            "name": ["normzalized", "name"],
            "original": [
                {
                    "token": "Token #1",
                    "positions": [
                        (start1, end1), (start2, end2), ...
                    ]
                },
                ...
            ],
            "count": <number of times the given name found in the text>
        },
        ...
    ]
}
```
