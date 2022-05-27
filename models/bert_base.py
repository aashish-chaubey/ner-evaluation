from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class NERModel:
    """
    Using Transformer based BERT model for NER
    """
    def __init__(self, text) -> None:
        self.text = text
        self.entities_per_loc = self.__get_entities()
    
    def __extract_entities(self) -> dict:
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        nlp = pipeline("ner", model=model, tokenizer=tokenizer)
        ner_results = nlp(self.text)
        return ner_results
    
    def __get_entities(self) -> dict:
        this_name = []
        this_loc = []
        all_names_list_tmp = []
        all_loc_list_tmp = []
        ner_results = self.__extract_entities()
        for ner_dict in ner_results:
            if ner_dict['entity'] == 'B-PER':
                if len(this_name) == 0:
                    this_name.append(ner_dict['word'])
                else:
                    all_names_list_tmp.append([this_name])
                    this_name = []
                    this_name.append(ner_dict['word'])
            elif ner_dict['entity'] == 'I-PER':
                this_name.append(ner_dict['word'])

            elif ner_dict['entity'] == 'B-LOC':
                if len(this_loc) == 0:
                    this_loc.append(ner_dict['word'])
                else:
                    all_loc_list_tmp.append([this_loc])
                    this_loc = []
                    this_loc.append(ner_dict['word'])
            elif ner_dict['entity'] == 'I-PER':
                this_loc.append(ner_dict['word'])

        all_names_list_tmp.append([this_name])
        all_loc_list_tmp.append([this_loc])

        final_name_list = []
        final_loc_list = []
        for name_list in all_names_list_tmp:
            full_name = ' '.join(name_list[0]).replace(' ##', '').replace(' .', '.')
            final_name_list.append([full_name])
        for loc_list in all_loc_list_tmp:
            full_loc = ' '.join(loc_list[0]).replace(' ##', '').replace(' .', '.')
            final_loc_list.append([full_loc])

        return {
            'person': final_name_list,
            'location': final_loc_list
        }
