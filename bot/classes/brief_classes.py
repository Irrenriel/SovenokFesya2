import re

from bin.main_var import db

from bot.content import BRIEF_LOCATIONS_PARSE, BRIEF_ALLIANCE_PARSE, STATUS_HEADQUARTERS_DICT, STATUS_LOCATIONS_DICT,\
    LOC_TYPES, FORBIDDEn_CLASSES


class Location:
    def __init__(self, req, lvl):
        self.req = req
        self.lvl = lvl

    def __repr__(self):
        return self.req


class HeadquartersBrief:
    def __init__(self, events: str, date: str, message_id: int):
        '''   Создание объекта с базовыми переменными.   '''
        # Start of Answers, Time Date, Message ID and Split Info
        self.answer_mode1, self.answer_mode2 = '<i>🤝Альянсы:</i>\n', '<i>🤝Альянсы:</i>\n'
        self.events = events.replace('🤝Headquarters news:\n', '').split('\n\n\n')
        self.date = date
        self.message_id = message_id

    def _give_events_list(self):
        return self.events

    def work(self, event: str):
        '''   Основной метод обработки каждого ивента.   '''
        self.event = event
        self.head_name, self.status, self.stock, self.glory, self.code = self.parse(event)
        self.atk_answer, self.def_answer = '', ''

        for line in event.split('\n'):
            if '🎖Attack:' in line:
                self.atk_in_event_line(line)
            elif '🎖Defense:' in line:
                self.def_in_event_line(line)

        head_name_url = f'<a href="https://t.me/share/url?url=/l_info%20{self.code}">🎪{self.head_name}</a>'
        own = '🔷' if self.head_name == 'Alert Eyes' else ''
        breach = f'➖🎁: -{self.stock}📦, -{self.glory}🎖\n' if 'breached. ' in self.event else ''

        self.answer_mode1 += f'<b>{own}{head_name_url} [{self.status}]</b>\n{breach}{self.atk_answer}{self.def_answer}\n'
        self.answer_mode2 += f'<b>{own}{head_name_url} [{self.status}]</b>\n'

    def parse(self, event: str):
        '''   Парсинг основных переменных.   '''
        parse = re.search(BRIEF_ALLIANCE_PARSE, event)

        head_name = parse.group('head_name')
        status = STATUS_HEADQUARTERS_DICT.get(parse.group('status'))
        stock = parse.group('stock') if parse.group('stock') is not None else '0'
        glory = parse.group('glory') if parse.group('glory') is not None else '0'
        code = db.check('SELECT code FROM loc WHERE name = ?', [head_name])[0]
        code = code if code != None else f'NoneCode({head_name})'
        return head_name, status, stock, glory, code

    def atk_in_event_line(self, line: str):
        '''   Детекшон топ-атакеров, рейдеров.   '''
        self.attackers = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
        self.atk_answer += '🎖⚔: {}\n'.format(','.join(['{}[{}]'.format(i[0], i[1]) for i in self.attackers]))
        if 'breached' in self.event:
            self._with_breached()

    def def_in_event_line(self, line: str):
        '''   Детекшон топ-деферов   '''
        self.defenders = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
        self.def_answer += '🎖🛡: {}\n'.format(','.join(['{}[{}]'.format(i[0], i[1]) for i in self.defenders]))

    def _with_breached(self):
        '''   Запись рейдерков в историю.   '''
        raiders = set()
        for tag in self.attackers:
            raid_head_name = db.check('SELECT name FROM al_guild_info WHERE guild_tag = ?', [tag[1]])
            if raid_head_name:
                raiders.add(raid_head_name[0])
            else:
                raiders.add(f'NoneQuart({tag[1]})')
        db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)', [self.code, self.date, self.message_id,
            f'<b>🎪{self.head_name}[{self.status}]\n⬆⚔ 🎪{",🎪".join(raiders)}</b>'])
        for raider in raiders:
            raider_code = raider if raider.startswith('NoneQuart') else \
                db.check('SELECT code FROM loc WHERE name = ?', [raider])[0]
            db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)',
                     [raider_code, self.date, self.message_id, f'<b>🎪{raider} ⚔➡ 🎪{self.head_name}</b>'])

    def _defenders_info(self):
        '''   Запись защитников и определение новых/переехавших гильдий.   '''
        tags = [l[0] for l in db.checkall('SELECT guild_tag FROM al_guild_info', [])]
        for tag in self.defenders:
            if tag[1] not in tags:
                # New guild in alliance
                db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)',
                         [self.code, self.date, self.message_id, f'<b>⚜{tag[0]}[{tag[1]}]⚜</b>'])
                db.query('INSERT INTO al_guild_info (guild_tag, guild_emoji, name, code) VALUES (?,?,?,?)',
                         [tag[1], tag[0], self.head_name, self.code])

            elif db.check('SELECT name FROM al_guild_info WHERE guild_tag = ?', [tag[1]])[0] != self.head_name:
                # Guild change alliance
                db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)',
                         [self.code, self.date, self.message_id, f'<b>⚜{tag[0]}[{tag[1]}]⚜</b>'])
                old_code = db.check('SELECT code FROM al_guild_info WHERE guild_tag = ?', [tag[1]])[0]
                db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)',
                         [old_code, self.date, self.message_id, f'<b>⚠{tag[0]}[{tag[1]}]⚠</b>'])
                db.query('UPDATE al_guild_info SET guild_emoji = ?, name = ? WHERE guild_tag = ?',
                         [tag[0], self.head_name, tag[1]])

            else:
                # Update guild_emoji
                db.query('UPDATE al_guild_info SET guild_emoji = ? WHERE guild_tag = ?', [tag[0], tag[1]])

    def ending(self):
        x = '[{}]'.format('<a href="https://t.me/ChatWarsDigest/{}">{}</a>'.format(self.message_id, self.date))
        self.answer_mode1 += x
        self.answer_mode2 += x
        return self.answer_mode1, self.answer_mode2


class LocationsBrief:
    def __init__(self, events: str, date: str, message_id: int):
        self.forts, self.mines, self.ruins = [], [], []
        self.answer_mode1, self.answer_mode2 = '<i>🗺Локации:</i>\n', '<i>🗺Локации:</i>\n'
        self.events = events.replace('🗺State of map:\n', '').split('\n\n')
        self.date = date
        self.message_id = message_id
        self.all_locs = db.checkall('SELECT name, lvl FROM loc WHERE lvl != 99', [])

    def _give_events_list(self):
        return self.events

    def work(self, event: str):
        '''   Основной метод обработки каждого ивента.   '''
        self.event = event
        self.loc_name, self.loc_lvl, self.status, self.enemy_head, self.code, self.conqueror = self.parse(event)
        self.atk_answer, self.def_answer = '', ''

        for line in event.split('\n'):
            if '🎖Attack:' in line:
                self.atk_in_event_line(line)
            elif '🎖Defense:' in line:
                self.def_in_event_line(line)

        if 'belongs to' in self.event:
            self._if_conquest()
        elif 'Forbidden' not in self.event:
            working_num = db.check('SELECT working FROM loc WHERE code = ?', [self.code])[0]
            db.query('UPDATE loc SET work_status = "⚡", working = ? WHERE code = ?', [working_num + 1, self.code])

        own = '🔷' if self.conqueror == 'Alert Eyes' else ''
        loc_type = LOC_TYPES.get(self.loc_name.split(' ')[-1])
        name_lvl = '{} lvl.{}'.format(self.loc_name, self.loc_lvl)
        new_owner = f'\n➕🚩[{self.enemy_head}]' if self.enemy_head else ''

        ans = Location('<b>{}{}{} [{}]</b>'.format(own, loc_type, name_lvl, self.status), self.loc_lvl)
        if loc_type == '🏷':
            self.ruins.append(ans)
        elif loc_type == '📦':
            self.mines.append(ans)
        elif loc_type == '🎖':
            self.forts.append(ans)

        self.answer_mode1 += '<b>{}{}{} [{}]{}</b>\n{}{}\n'.format(
            own, loc_type, name_lvl, self.status, new_owner, self.atk_answer, self.def_answer)

    def parse(self, event: str):
        '''   Парсинг основных переменных.   '''
        parse = re.search(BRIEF_LOCATIONS_PARSE, event)

        loc_name = parse.group('location_name')
        loc_lvl = parse.group('location_lvl')
        status = STATUS_LOCATIONS_DICT.get(parse.group('def_status'), STATUS_LOCATIONS_DICT.get(parse.group('atk_status')))
        enemy_head = parse.group('enemy_head') if parse.group('enemy_head') is not None else ''

        tmp = (loc_name, int(loc_lvl))
        if tmp in self.all_locs:
            self.all_locs.remove(tmp)

        is_location_in_db = db.check('SELECT code,conqueror FROM loc WHERE name = ? and lvl = ?',
                                     [loc_name, int(loc_lvl)])
        if is_location_in_db:
            code, conqueror = is_location_in_db[0], is_location_in_db[1]
        else:
            code, conqueror = f'NoneCode({loc_name} lvl.{loc_lvl})', 'Forbidden Clan'
            db.query('INSERT INTO loc (code,name,lvl) VALUES (?,?,?)', [code, loc_name, int(loc_lvl)])
        return loc_name, loc_lvl, status, enemy_head, code, conqueror

    def atk_in_event_line(self, line: str):
        '''   Детекшон топ-атакеров, рейдеров.   '''
        attackers = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
        self.atk_answer += '🎖⚔: {}\n'.format(','.join(['{}[{}]'.format(i[0], i[1]) for i in attackers]))

    def def_in_event_line(self, line: str):
        '''   Детекшон топ-деферов   '''
        if 'Forbidden' in line:
            defenders = set(re.findall(r'Forbidden (?P<mob_class>\w+) lvl(?P<mob_lvl>\d+)', line))
            self.def_answer += '🎖🛡: {}\n'.format(','.join([f'🏴‍☠[{FORBIDDEn_CLASSES.get(i[0], "error")}]' for i in defenders]))
        else:
            defenders = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
            self.def_answer += '🎖🛡: {}\n'.format(
                ','.join([f'{i[0]}[{i[1]}]' for i in defenders]))

        if self.conqueror != 'Forbidden Clan' and 'Forbidden' not in line:
            tags = [el[0] for el in db.checkall('SELECT guild_tag FROM al_guild_info', [])]
            for guild in defenders:
                if guild[1] not in tags:
                    db.query('INSERT INTO al_guild_info (guild_tag, guild_emoji, name, code) VALUES (?,?,?,?)',
                             [guild[1], guild[0], self.conqueror, self.code])
                else:
                    db.query('UPDATE al_guild_info SET guild_emoji = ? WHERE guild_tag = ?', [guild[0], guild[1]])

    def _if_conquest(self):
        '''   Захват-передача локации.   '''
        enemy_code = db.check('SELECT code FROM loc WHERE name = ?', [self.enemy_head])
        db.query('UPDATE loc SET work_status = "⏳", conqueror = ? WHERE name = ? and lvl = ?',
                 [self.enemy_head, self.loc_name, int(self.loc_lvl)])

        if enemy_code:
            db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)',
                     [enemy_code[0], self.date, self.message_id, '<b>{}{} lvl.{}[✅🚩]</b>'.format(
                         LOC_TYPES.get(self.loc_name.split(' ')[-1]), self.loc_name, self.loc_lvl)])

        if self.conqueror != 'Forbidden Clan':
            db.query('INSERT INTO loc_history (code,time,url,txt) VALUES (?,?,?,?)', [
                self.code, self.date, self.message_id, '<b>{}{} lvl.{}[🚫🚩]</b>'.format(
                    LOC_TYPES.get(self.loc_name.split(' ')[-1]), self.loc_name, self.loc_lvl)])

    def ending(self):
        self.answer_mode2 += '{}{}{}\n'.format(
            '\n'.join([loc.req for loc in sorted(self.ruins, key=lambda loc: loc.lvl)]) + '\n\n' if self.ruins else '',
            '\n'.join([loc.req for loc in sorted(self.mines, key=lambda loc: loc.lvl)]) + '\n\n' if self.mines else '',
            '\n'.join([loc.req for loc in sorted(self.forts, key=lambda loc: loc.lvl)]))

        if self.all_locs:
            for loc in self.all_locs:
                db.query('UPDATE loc SET working = working + 1 WHERE name = ? and lvl = ?', [loc[0], loc[1]])
        x = '[{}]'.format('<a href="https://t.me/ChatWarsDigest/{}">{}</a>'.format(self.message_id, self.date))
        self.answer_mode1 += x
        self.answer_mode2 += x
        return self.answer_mode1, self.answer_mode2