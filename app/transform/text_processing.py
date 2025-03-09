import spacy

SPACY_PRETRAINED_PIPELINE = 'en_core_web_md'

nlp = spacy.load(SPACY_PRETRAINED_PIPELINE)

def ner_analysis(texts: list):
    entities = [ 
        {
            'entityname': entity.text,
            'entitylabel': entity.label_,
            'startposition': entity.start_char,
            'endposition': entity.end_char,
            'pagenumber': txt['pagenumber'],
            'ordernumber': txt['ordernumber']
        } 
        for txt in texts 
        for entity in nlp(txt['textvalue']).ents 
    ]

    return entities

if __name__ == '__main__':
    import sys
    sys.path.append(r'D:\Personal\vidavox_test_de\app')
    print(sys.path)
    from extract import ocr

    pdf_path = r'D:\Personal\vidavox_test_de\AR for improved learnability.pdf'
    data, text = ocr.extract_text_from_pdf(pdf_path)
    
    for entity in ner_analysis(data):
        print(entity)