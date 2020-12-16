from bin.main_var import db
from bot.content import REQ

class UsersCash:
    temp_user = {
        'id': 0,
        'username': None,
        'nickname': None,
        'lvl': None,
        'class': None,
        'guild_tag': None,
        'castle': None,
        'role': 1,
        'trade': '',
        'hb_sub': 0,
        'hb_show': 0,
        'time': 0,
        'top_loc': 0
    }

    def __init__(self, db_of_users: list = None):
        self.loading(db_of_users)

    def loading(self, db_of_users: list = None):
        '''   Create main stores.   '''
        self.ids_store = {}
        self.guild_tags_store = {}
        # self.classes_store = {"⚒": [], "📦": [], "⚗": [], "🛡": [], "🏹": [], "⚔": [], "🏛": []}
        self.castles_store = {'O': [], 'A': [], 'F': [], 'M': [], 'S': [], 'R': [], 'T': [], 'ERROR': []}
        self.roles_store = {1: [], 2: [], 3: [], 4: [], 5: []}

        '''   Loading stores from database.   '''
        if db_of_users is None:
            db_of_users = db.checkall(REQ)

        # Full Raw Database Var
        self.db = db_of_users

        # Sorting in Dicts
        for user_data in self.db:
            # All datas by ID
            self.ids_store[user_data[0]] = dict(zip(self.temp_user.keys(), user_data))

            # ID by classes
            # self.classes_store[user_data[4]].append(user_data[0])

            # ID by castles
            self.castles_store.get(user_data[6]).append(user_data[0])

            # ID by guild tags
            self.guild_tags_store.setdefault(user_data[5], []).append(user_data[0])

            # ID by roles
            self.roles_store[user_data[7]].append(user_data[0])

    def select(self, **kwargs):
        # By @ogurchinskiy
        '''
        Selecting info from stores.
        Example UsersCash().select(**{'guild_tag':'AT', 'lvl': lambda i: 20<i<41}) -> List[Dicts{}}
        '''
        return self.sort(list(kwargs.items()), list(self.ids_store.values()))

    def sort(self, s_list: list, s_dict: list): # By @ogurchinskiy
        '''   Sorting info for selecting.   '''
        if not s_list or not s_dict:
            return s_dict
        key, value = s_list.pop()
        ret_list = []
        for i in s_dict:
            if type(value) is list:
                if i.get(key) in value:
                    ret_list.append(i)
            elif callable(value):
                if value(i.get(key)):
                    ret_list.append(i)
            else:
                if i.get(key) == value:
                    ret_list.append(i)
        return self.sort(s_list, ret_list)

    def select_id(self, id: [list, int]):
        # By @ogurchinskiy
        '''   Selecting info from stores by ID/list of IDs.   '''
        if type(id) is list:
            return [self.ids_store.get(_user) for _user in id]
        else:
            return self.ids_store.get(id)

    # def select_class(self, _class: [list, str]):
    #     '''   Selecting info from stores by class(es).   '''
    #     if type(_class) is list:
    #         id_list = [self.classes_store.get(x, []) for x in _class]
    #         return [self.ids_store.get(i) for i in [_id for id_list in id_list for _id in id_list]]
    #     else:
    #         return [self.ids_store.get(i) for i in self.classes_store.get(_class, [])]

    def select_castle(self, _castle: [list, str]):
        '''   Selecting info from stores by castle(s).   '''
        if type(_castle) is list:
            id_list = [self.castles_store.get(x, []) for x in _castle]
            return [self.ids_store.get(i) for i in [_id for id_list in id_list for _id in id_list]]
        else:
            return [self.ids_store.get(i) for i in self.castles_store.get(_castle, [])]

    def select_guild_tag(self, _tag: [list, str]):
        '''   Selecting info from stores by tag.   '''
        if type(_tag) is list:
            id_list = [self.guild_tags_store.get(x, []) for x in _tag]
            return [self.ids_store.get(i) for i in [_id for id_list in id_list for _id in id_list]]
        else:
            return [self.ids_store.get(i) for i in self.guild_tags_store.get(_tag, [])]

    def check_perm_role(self, id: int, roles: [int, list]):
        '''   Selecting role from stores by id.   '''
        user_data = self.select_id(id)
        if user_data:
            if type(roles) is list:
                if user_data.get('role') in roles:
                    return True
            else:
                if user_data.get('role') == roles:
                    return True

    def insert(self, **kwargs):
        # By @ogurchinskiy
        '''   Inserting info from stores.   '''
        if not "id" in kwargs.keys():
            raise Exception("Missing id")
        temp = self.temp_user.copy()
        temp.update(kwargs)
        self.ids_store[kwargs.get("id")] = temp

    def update(self, **kwargs):
        # By @ogurchinskiy
        '''   Updating info from stores.   '''
        if not "id" in kwargs.keys():
            raise Exception("Missing id")
        self.ids_store[kwargs.get("id")].update(kwargs)

    def dalete(self, id: int):
        # By @ogurchinskiy
        '''   Deleting info from stores.   '''
        self.ids_store.pop(id, None)