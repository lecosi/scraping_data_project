from fake_useragent import UserAgent


def generate_user_agent() -> str:
    ua = UserAgent()
    return ua.random
