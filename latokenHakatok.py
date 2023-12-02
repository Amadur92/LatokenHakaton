import autogen



config_list = [
    {
        'model': 'gpt-4',
        'api_key': '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',
    }
]


price_assistant = autogen.AssistantAgent(
    name="Price",
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,
        "temperature": 0,
    },
)

news_assistant = autogen.AssistantAgent(
    name="News",
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,
        "temperature": 0,
    },
)

total_assistant = autogen.AssistantAgent(
    name="Summary",
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,
        "temperature": 0,
    },
)

user_proxy = autogen.UserProxyAgent(
    name="LatokenBitcoinNews",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith(""),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)

user_proxy.initiate_chat(
    price_assistant,
    message="""На сколько изменилась цена биткойна за 7 дней? """,
)

price = user_proxy.last_message()

user_proxy.initiate_chat(
    price_assistant,
    message="""Какие новости связанные с биткоином были за последнюю неделю
    Используй gnews api-key f54a3bc78c3049d216544a09d227e2e9""",
)
news = user_proxy.last_message()
user_proxy.initiate_chat(
    total_assistant,
    message=f""" {price}
Ты профессиональный криптоаналитик. 
Проанализируй новости {news} и сделай вывод, почему так произошло""",
)