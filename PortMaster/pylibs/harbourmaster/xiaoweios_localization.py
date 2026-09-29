"""Presentation-only XiaoweiOS PortMaster catalog localization."""
import copy
import json
import os
import re
from pathlib import Path

SCHEMA = 'xiaoweios.ports.localization.v1'
LOCALE = 'zh_CN'
ID_RE = re.compile(r'^portmaster:[A-Za-z0-9][A-Za-z0-9._-]{0,255}\.zip$')
ENTRY_KEYS = {'source_title', 'title', 'description', 'instructions', 'review', 'provenance'}


def _valid_text(value, limit, empty=False):
    return isinstance(value, str) and len(value.encode('utf-8')) <= limit and (empty or bool(value.strip()))


def validate_overlay(value):
    if not isinstance(value, dict) or set(value) != {'schema', 'locale', 'upstream', 'entries'}:
        raise ValueError('invalid XiaoweiOS localization fields')
    if value['schema'] != SCHEMA or value['locale'] != LOCALE or not isinstance(value['entries'], dict):
        raise ValueError('invalid XiaoweiOS localization identity')
    upstream = value['upstream']
    if (not isinstance(upstream, dict) or set(upstream) != {'url', 'sha256'}
            or upstream['url'] != 'https://github.com/PortsMaster/PortMaster-New/releases/latest/download/ports.json'
            or not re.fullmatch(r'[0-9a-f]{64}', upstream['sha256'])):
        raise ValueError('invalid XiaoweiOS localization upstream identity')
    if len(value['entries']) > 8192:
        raise ValueError('XiaoweiOS localization exceeds entry limit')
    for entry_id, entry in value['entries'].items():
        if not ID_RE.fullmatch(entry_id) or not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            raise ValueError('invalid XiaoweiOS localization entry')
        if not (_valid_text(entry['source_title'], 1024) and _valid_text(entry['title'], 1024)
                and _valid_text(entry['description'], 32768, True)
                and _valid_text(entry['instructions'], 32768, True)):
            raise ValueError('invalid XiaoweiOS localized text')
        if entry['review'] not in ('machine-assisted', 'reviewed'):
            raise ValueError('invalid XiaoweiOS localization review state')
        provenance = entry['provenance']
        if (not isinstance(provenance, dict) or set(provenance) != {'method', 'reference'}
                or not _valid_text(provenance['method'], 128)
                or not _valid_text(provenance['reference'], 512)):
            raise ValueError('invalid XiaoweiOS localization provenance')
    return value


def load_overlay(path=None, locale=None):
    locale = locale or os.environ.get('LANG', '')
    if locale.split('.', 1)[0] != LOCALE:
        return None
    path = path or os.environ.get('XIAOWEIOS_PORTS_LOCALIZATION', '')
    if not path:
        return None
    try:
        return validate_overlay(json.loads(Path(path).read_text(encoding='utf-8')))
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError):
        return None


def localize_port_info(port_name, port_info, overlay):
    result = copy.deepcopy(port_info)
    if overlay is None or result is None:
        return result
    entry = overlay['entries'].get('portmaster:' + port_name.casefold())
    attr = result.get('attr') if isinstance(result, dict) else None
    if entry is None or not isinstance(attr, dict) or attr.get('title') != entry['source_title']:
        return result
    source_title = attr['title']
    attr['title'] = entry['title'] or source_title
    attr['desc'] = entry['description'] or attr.get('desc', '')
    attr['inst'] = entry['instructions'] or attr.get('inst', '')
    attr['title_aliases'] = [source_title] if source_title.casefold() != attr['title'].casefold() else []
    result['xiaoweios_localization'] = {'locale': LOCALE, 'review': entry['review']}
    return result


__all__ = ('load_overlay', 'localize_port_info', 'validate_overlay')
