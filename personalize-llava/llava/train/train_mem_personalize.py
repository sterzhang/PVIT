from llava.train.train_personalize import train

if __name__ == "__main__":
    train(attn_implementation="flash_attention_2")
# from llava.train.train_personalize import train

# if __name__ == "__main__":
#     train(attn_implementation="eager")  # 使用 PyTorch 默认注意力
