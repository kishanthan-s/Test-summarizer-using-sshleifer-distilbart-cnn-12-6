from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_dir = "model_local"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    return summarizer

def text_summarizer(summarizer, text):
    summary = summarizer(text, max_length=60, min_length=25, do_sample=False)
    return summary[0]['summary_text']
