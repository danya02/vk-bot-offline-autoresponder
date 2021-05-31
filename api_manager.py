import vk_api

class APIManager:
    def __init__(self):
        self.apis = dict()

    def __getitem__(self, token):
        if token in self.apis: return self.apis[token]
        api = vk_api.VkApi(token=token)
        self.apis[token] = api
        return api

