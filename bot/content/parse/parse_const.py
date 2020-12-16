HERO_PARSE = r'(?P<castle>.)(?:(?!\[)(?P<guilds_emoji>\W)|)\[(?P<guild_tag>.+)\](?P<nickname>.+)\n🏅Уровень: (?P<lvl>\d+).*\n.*\n.*\n.*\n.*\n(?:(?=💧).*\n|).*\n.*\n.*\n(?P<class>.)'

NEW_LOC_INPUT_PARSE = r'(?=You found hidden location)(?:You found hidden location (?P<loc_name>.*)) lvl.(?P<loc_lvl>\d+)\n((?=То remember)|.+\n).+ (?P<loc_code>.+)|(?:You found hidden headquarter (?P<head_name>.*))\n.+: (?P<head_code>.+)$'

BRIEF_LOCATIONS_PARSE = r'(?P<location_name>.+) lvl\.(?P<location_lvl>\d+) (?:(?=was)was (?P<def_status>.+)|belongs to (?P<enemy_head>\w+.\w+)(?P<atk_status>.+)\n)'

BRIEF_ALLIANCE_PARSE = r'(?P<head_name>.+) was (?P<status>.+)(?:\:|\. )\n(?:(?=Attackers).+ (?P<stock>\d+|)📦 and (?P<glory>\d+|)🎖|)'