# -*- coding: utf-8 -*-
"""Creates representative API response for specification
"""
import json 

if __name__ == "__main__":
    with open('syria-2.json') as spec:
        data = json.load(spec)

     
    sample_data = data['result'][0]
    sample_data['sentences'] = [sample_data['sentences'][0]]
    sample_data['sentences'][0]['tweets'] = [sample_data['sentences'][0]['tweets'][0]]

    with open('syria-spec.json', 'w') as new_spec:
        str_rep = json.dumps(sample_data,
                             separators=(',', ': '),
                             indent=2)
        new_spec.write(str_rep)
