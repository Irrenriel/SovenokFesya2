STATUS_HEADQUARTERS_DICT = {'easily defended': '👌🛡',
                            'easily breached': '😎⚔',
                            'breached': '⚔',
                            'defended successfully': '🛡',
                            'closely defended': '⚡🛡',
                            'closely breached': '⚡⚔'}

STATUS_LOCATIONS_DICT = {'. Easy win:': '😎⚔',
                         ':': '⚔',
                         '. Massacre:': '⚡⚔',
                         'easily protected': '👌🛡',
                         'protected': '🛡',
                         'closely protected': '⚡🛡'}

LOC_TYPES = {'Ruins': '🏷', 'Mine': '📦', 'Fort': '🎖', 'Tower': '🎖', 'Outpost': '🎖'}

FORBIDDEn_CLASSES = {'Sentinel': '🛡'}

CALL_DATA_LOC_TYPE_DICT = {'loc_type_ruins': {'text': '🏷Руины', 'type': '🏷 ', 'parse': '"%Ruins%"'},
                'loc_type_mines': {'text': '📦Шахты', 'type': '📦 ', 'parse': '"%Mine%"'},
                'loc_type_forts': {'text': '🎖Форты', 'type': '🎖 ', 'parse': "('Fort', 'Tower', 'Outpost')"},
                'loc_type_al': {'text': '🎪Альянсы', 'type': '🎪 ', 'parse': ''},
                'loc_type_cap': {'text': '🚩Карта'}}