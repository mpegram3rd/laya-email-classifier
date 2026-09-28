# Email Classification Test
The original intent of this project was to see how well [Laya](https://laya.convaiinnovations.com/ ) does with email classification. The goal was to classify emails into different categories such as spam, promotions, social, and primary. 
It has evolved to test different permutations of which Laya model variants performed the best for the task
as well as what data representation worked the best.  

After some experimentation and refinement with Laya, I added the ability to run the same tests using 
[TypeSafe's Jev AI](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

## Environment Setup
1. Clone the repository
2. Copy `.env-example` to `.env` and fill in the required values. 

## Dataset Setup
This code, right now, is tightly tied to a specific dataset. Specifically the 
[jason23322/high-accuracy-email-classifier on Huggingface](https://huggingface.co/datasets/jason23322/high-accuracy-email-classifier)

Download the [Full Dataset CSV File](https://huggingface.co/datasets/jason23322/high-accuracy-email-classifier/resolve/main/email_classification_dataset.csv) and place it in the `data` folder.

## Running the App
1. Run `uv sync`
4. Look at `main.py` and decide which permutations you want to run. Comment out the ones you don't want.
5. Start the app by running `uv run main.py`

The results will be output to the console. 



