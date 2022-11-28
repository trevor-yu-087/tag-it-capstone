# TAG-IT
TAG-IT: Tags Automically Generated for Imaging report Text is our biomedical engineering capstone project completed from September 2021 to April 2022.
This project was completed as part of our requirements for BME 461 and BME 462 engineering design courses with 
[Cathleen Leone](https://github.com/cgleone),
[Rachel DiMaio](https://github.com/rmdim),
[Tigger Wong](https://github.com/tigswong),
[Thomas Fortin](https://github.com/ThomasFortin),
and [Trevor Yu](https://github.com/trevor-yu-087).

# Project Description
The problem this capstone project aimed to address was the documentation burden with the use of Electronic Medical Records (EMRs).
Specifically, we focussed on the task of searching for a particular radiology report from within an EMR system. 
This task can be time consuming due to lack of appropriate naming and labelling of documents in the software, especially if documents are scanned in.
Normally, a user will need to manually add "tags" to improve searchability, such as using a search bar or filtering system.
We identified 5 tags that would be important to extract based on conversations with physician stakeholders: Body part, Imaging modality, Clinic name, Date of procedure, and Doctor name.

Our solution, TAG-IT, aims to automatically generate these tags from scanned medical imaging reports and present a physician with a user-friendly interface
to search through the tags, thereby reducing the amount of time spent performing this searching task.
Our solution had 3 main components: a graphical interface for users to upload and search for documents, 
an optical character recognition (OCR) system to transform scanned reports into text, 
and a natural language processign (NLP) system to extract tags from report text.

# My Contributions
My main contributions to the project were working on the NLP model API design and developing the named entity recognition (NER) model.
The relevant code can be found in the [models folder](models).

For the model API design, we agreed upon specifications of what funtionality the model would need to perform such as preprocessing, prediction, and inference.
We also had a common data specification so the UI developers could work with dummy data while we worked on models independently. I creeated a skeleton class
to build our different models from.

For the [NER model](models/ner_model.py), I used pre-trained transformer models from HuggingFace, including [BioClinical BERT](https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT),
[BioELECTRA](https://huggingface.co/kamalkraj/bioelectra-base-discriminator-pubmed),
[BERT base](https://huggingface.co/bert-base-uncased),
and [BERT small](https://huggingface.co/prajjwal1/bert-small).
These models were fine-tuned on reports generated from the imaging reports in MIMIC-III, but structured as real, complete imaging reports based on examples.
As part of our analysis, we performed 5-fold leave-one-out cross-validation using 10 different report templates to perform model selection. We used AWS SageMaker to run the training in the cloud.
The NER model with BioELECTRA was found to have the highest classification accuracy for the Date taken and Clinic name tags and was competative with the other tags.

## Citations

Johnson, A., Pollard, T., & Mark, R. (2016). MIMIC-III Clinical Database (version 1.4). *PhysioNet*. [https://doi.org/10.13026/C2XW26](https://doi.org/10.13026/C2XW26).

Johnson, A. E. W., Pollard, T. J., Shen, L., Lehman, L. H., Feng, M., Ghassemi, M., Moody, B., Szolovits, P., Celi, L. A., & Mark, R. G. (2016). MIMIC-III, a freely accessible critical care database. Scientific Data, 3, 160035.

Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.

