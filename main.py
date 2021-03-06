import aiohttp
from accessify import private
from BotsLongPoll import BotsLongPoll

class VkAPI:
    def __init__(self, access_token : str, version : str):
        self.access_token = access_token
        self.version = version

    @private
    async def build_request(self, command : str, params : dict) -> str:
        parameters = ''.join([f'&{k}={v}' for k, v in params.items()])
        req = f"https://api.vk.com/method/{command}?v={self.version}&access_token={self.access_token}{parameters}"
        return req

    @private
    @staticmethod
    async def send_request_get_dict(self, string_request : str):
        async with aiohttp.ClientSession() as session:
            async with session.get(string_request) as response:
                q = await response.json()

        return q['response']

    @private
    async def show_errors(self, fields : list, params : dict):
        errors = [i for i in fields if i not in params]
        if errors:
            raise AttributeError(f"{', '.join(errors)} is/are not in params")

    """
        USER COMMANDS
    """
    async def get_user(self, params : dict, user_id=None) -> dict:
        if user_id != None:
            str_req = await self.build_request("users.get", {'user_ids': user_id}.update(params))
        else: 
            str_req = await self.build_request("users.get", { })

        user = await self.send_request_get_dict(str_req)
        for lst in user:
            user = lst

        return user

    async def get_user_subscriptions(self, params : dict) -> list:
        str_req = await self.build_request("users.getSubscriptions", params)
        response = (await self.send_request_get_dict(str_req))['items']
        names = []
        for subscription in response:
            names.append(subscription['name'])
        return names

    async def user_report(self, params : dict) -> bool:
        await self.show_errors(['user_id', 'type'], params)
        str_req = await self.build_request("users.report", params)
        code = await self.send_request_get_dict(str_req)
        return bool(code)

    async def get_user_followers(self, params : dict) -> dict:
        str_req = await self.build_request("users.getFollowers", params)
        response = (await self.send_request_get_dict(str_req))['items']
        return response

    async def user_search(self, params : dict) -> dict:
        str_req = await self.build_request("users.search", params)
        response = (await self.send_request_get_dict(str_req))['items']
        return response

    """
            GROUP COMMANDS
    """
    async def get_user_groups(self, params : dict, get_names = False) -> list:
        str_req = await self.build_request("groups.get", params)
        response = await self.send_request_get_dict(str_req)
        groups = []

        if get_names == True:
            groups_response = response['items']
            for group in groups_response:
                groups.append(group['name'])
        else:
            groups = response['items']

        return groups 

    async def group_add_address(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'title', 'address', 'country_id', 'city_id', 'latitude', 'longitude'], params)
        str_req = await self.build_request("groups.addAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_add_callback(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'url', 'title'], params)
        str_req = await self.build_request("groups.addCallbackServer", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_add_link(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'link'], params)
        str_req = await self.build_request("groups.addLink", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_approve_request(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'user_id'], params)
        str_req = await self.build_request("groups.approveRequest", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_ban(self, params : dict) -> bool:
        await self.show_errors(['group_id'], params)
        str_req = await self.build_request("groups.ban", params)
        response = await self.send_request_get_dict(str_req)
        return bool(response)

    async def group_create(self, params : dict) -> dict:
        await self.show_errors(['title'], params)
        str_req = await self.build_request("groups.create", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_delete_address(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'address_id'], params)
        str_req = await self.build_request("groups.deleteAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_delete_callback(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'server_id'], params)
        str_req = await self.build_request("groups.deleteCallbackServer", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_delete_link(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'link_id'], params)
        str_req = await self.build_request("groups.deleteLink", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_disable_online(self, params : dict) -> bool:
        await self.show_errors(['group_id'], params)
        str_req = await self.build_request("groups.disableOnline", params)
        response = await self.send_request_get_dict(str_req)
        return bool(response)

    async def group_edit(self, params : dict) -> bool:
        await self.show_errors(['group_id'], params)
        str_req = await self.build_request("groups.edit", params)
        response = await self.send_request_get_dict(str_req)
        return bool(response)

    async def group_edit_address(self, params : dict) -> dict:
        await self.show_errors(['group_id', 'address_id'], params)
        str_req = await self.build_request("groups.editAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response

    @private
    async def group_get_longpoll(self, longpoll : BotsLongPoll, group_id : str) -> BotsLongPoll:
        request = await self.build_request("groups.getLongPollServer", { "group_id": group_id })
        async with aiohttp.ClientSession() as session:
            async with session.get(request) as response:
                q = await response.json()
                await longpoll.write_longpoll_attrs(q['response']['server'], q['response']['key'], q['response']['ts'])

        return longpoll

    async def create_bot_longpoll(self, group_id : str) -> BotsLongPoll:
        longpoll = BotsLongPoll()
        longpoll = await self.group_get_longpoll(longpoll, group_id)
        return longpoll