
from radiomics import featureextractor
import os
import pandas as pd
import collections
import csv

#what string to search for in files to identify image files and rtstruct folder
image_search_string = ['_PT_']
rtstruct_search_string = ['FH', 'Firas', 'Hikmat']

parent_path_benign = '/shares/onfnas01/Research/Bradshaw/Lymphoma_UW_Retrospective/Data/nifti_bone_marrow_cases_Firas_contours/benign'
parent_path_malignant = '/shares/onfnas01/Research/Bradshaw/Lymphoma_UW_Retrospective/Data/nifti_bone_marrow_cases_Firas_contours/malignant'
params_file_path = '/home/tjb129/PycharmProjects/radiomics/bone_lesions_params.yaml'

csv_name = 'radiomics_results.csv'

extractor = featureextractor.RadiomicsFeatureExtractor(params_file_path)



for parent_path in [parent_path_benign, parent_path_malignant]:
    headers = None
    for subject in os.listdir(parent_path):
        subject_path = os.path.join(parent_path, subject)
        print(subject)
        files = os.listdir(subject_path)
        for file_i in files:
            if image_search_string in file_i:
                image_file_name = file_i
                image_file_path = os.path.join(subject_path, image_file_name)

            if rtstruct_search_string[0] in file_i or rtstruct_search_string[1] in file_i or rtstruct_search_string[2] in file_i:
                rtstruct_path = os.path.join(subject_path, file_i)

        csv_path = os.path.join(parent_path, csv_name)
        for rtstruct_file in os.listdir(rtstruct_path):
            rtstruct_file_path = os.path.join(rtstruct_path, rtstruct_file)

            try:
                featureVector = collections.OrderedDict()
                featureVector['Subject'] = subject
                featureVector['Image'] = image_file_name
                featureVector['Mask'] = rtstruct_file
                featureVector.update(extractor.execute(image_file_path, rtstruct_file_path))

                with open(csv_path, 'a') as outputFile:
                    writer = csv.writer(outputFile, lineterminator='\n')
                    if headers is None:
                        headers = list(featureVector.keys())
                        writer.writerow(headers)

                    row = []
                    for h in headers:
                        row.append(featureVector.get(h, "N/A"))
                    writer.writerow(row)
            except Exception:
                print('Problem with '+ rtstruct_file_path)





