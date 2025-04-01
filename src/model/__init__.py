from src.model.llm import LLM
from src.model.pt_llm import PromptTuningLLM
from src.model.graph_llm import GraphLLM


load_model = {
    "llm": LLM,
    "inference_llm": LLM,
    "pt_llm": PromptTuningLLM,
    "graph_llm": GraphLLM,
}

# Replace the following with the model paths
llama_model_path = {
    "7b": "meta-llama/Llama-2-7b-hf",
    "7b_chat": "meta-llama/Llama-2-7b-chat-hf",
    "13b": "meta-llama/Llama-2-13b-hf",
    "13b_chat": "meta-llama/Llama-2-13b-chat-hf",
    "3.2_3b_inst": "meta-llama/Llama-3.2-3B-Instruct",
    "3.2_3b": "meta-llama/Llama-3.2-3B",
    "3.1_8b": "meta-llama/Llama-3.1-8B-Instruct",
}
